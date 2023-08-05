from datetime import datetime
import io
import json
import mimetypes

from warden_sdk._compat import text_type
from warden_sdk.session import Session
from warden_sdk.utils import json_dumps, capture_internal_exceptions

from typing import (Any, Optional, Union, Dict, List, Iterator)


def parse_json(data):
  # print(f'{datetime.now()} \t {data}')
  return json.loads(data)


class Envelope(object):

  def __init__(
      self,
      headers=None,
      items=None,
  ):
    if headers is not None:
      headers = dict(headers)
    self.headers = headers or {}
    if items is None:
      items = []
    else:
      items = list(items)
    self.items = items

  @property
  def description(self):
    return "envelope with %s items (%s)" % (
        len(self.items),
        ", ".join(x.data_category for x in self.items),
    )

  def add_event(self, event):
    self.add_item(Item(payload=PayloadRef(json=event), type="event"))

  def add_transaction(self, transaction):
    self.add_item(Item(payload=PayloadRef(json=transaction),
                       type="transaction"))

  def add_profile(
      self,
      profile    # type: Any
  ):
    # type: (...) -> None
    self.add_item(Item(payload=PayloadRef(json=profile), type="profile"))

  def add_session(self, session):
    if isinstance(session, Session):
      session = session.to_json()
    self.add_item(Item(payload=PayloadRef(json=session), type="session"))

  def add_sessions(self, sessions):
    self.add_item(Item(payload=PayloadRef(json=sessions), type="sessions"))

  def add_item(self, item):
    self.items.append(item)

  def get_event(self):
    for items in self.items:
      event = items.get_event()
      if event is not None:
        return event
    return None

  def get_transaction_event(self):
    for item in self.items:
      event = item.get_transaction_event()
      if event is not None:
        return event
    return None

  def __iter__(self):
    return iter(self.items)

  def serialize_into(
      self,
      f,
  ):
    f.write(json_dumps(self.headers))
    f.write(b"\n")
    for item in self.items:
      item.serialize_into(f)

  def serialize(self):
    out = io.BytesIO()
    self.serialize_into(out)
    return out.getvalue()

  @classmethod
  def deserialize_from(
      cls,
      f,
  ):
    headers = json.loads(f.readline())
    items = []
    while 1:
      item = Item.deserialize_from(f)
      if item is None:
        break
      items.append(item)
    return cls(headers=headers, items=items)

  @classmethod
  def deserialize(
      cls,
      bytes,
  ):
    return cls.deserialize_from(io.BytesIO(bytes))

  def __repr__(self):
    return "<Envelope headers=%r items=%r>" % (self.headers, self.items)


class PayloadRef(object):

  def __init__(
      self,
      bytes=None,    # type: Optional[bytes]
      path=None,    # type: Optional[Union[bytes, text_type]]
      json=None,    # type: Optional[Any]
  ):
    # type: (...) -> None
    self.json = json
    self.bytes = bytes
    self.path = path

  def get_bytes(self):
    # type: (...) -> bytes
    if self.bytes is None:
      if self.path is not None:
        with capture_internal_exceptions():
          with open(self.path, "rb") as f:
            self.bytes = f.read()
      elif self.json is not None:
        self.bytes = json_dumps(self.json)
      else:
        self.bytes = b""
    return self.bytes

  @property
  def inferred_content_type(self):
    # type: (...) -> str
    if self.json is not None:
      return "application/json"
    elif self.path is not None:
      path = self.path
      if isinstance(path, bytes):
        path = path.decode("utf-8", "replace")
      ty = mimetypes.guess_type(path)[0]
      if ty:
        return ty
    return "application/octet-stream"

  def __repr__(self):
    # type: (...) -> str
    return "<Payload %r>" % (self.inferred_content_type,)


class Item(object):

  def __init__(
      self,
      payload,    # type: Union[bytes, text_type, PayloadRef]
      headers=None,    # type: Optional[Dict[str, Any]]
      type=None,    # type: Optional[str]
      content_type=None,    # type: Optional[str]
      filename=None,    # type: Optional[str]
  ):
    if headers is not None:
      headers = dict(headers)
    elif headers is None:
      headers = {}
    self.headers = headers
    if isinstance(payload, bytes):
      payload = PayloadRef(bytes=payload)
    elif isinstance(payload, text_type):
      payload = PayloadRef(bytes=payload.encode("utf-8"))
    else:
      payload = payload

    if filename is not None:
      headers["filename"] = filename
    if type is not None:
      headers["type"] = type
    if content_type is not None:
      headers["content_type"] = content_type
    elif "content_type" not in headers:
      headers["content_type"] = payload.inferred_content_type

    self.payload = payload

  def __repr__(self):
    return "<Item headers=%r payload=%r data_category=%r>" % (
        self.headers,
        self.payload,
        self.data_category,
    )

  @property
  def type(self):
    return self.headers.get("type")

  @property
  def data_category(self) -> str:
    ty = self.headers.get("type")
    if ty == "session":
      return "session"
    elif ty == "attachment":
      return "attachment"
    elif ty == "transaction":
      return "transaction"
    elif ty == "event":
      return "error"
    elif ty == "client_report":
      return "internal"
    else:
      return "default"

  def get_bytes(self):
    return self.payload.get_bytes()

  def get_event(self):
    """
    Returns an error event if there is one.
    """
    if self.type == "event" and self.payload.json is not None:
      return self.payload.json
    return None

  def get_transaction_event(self):
    if self.type == "transaction" and self.payload.json is not None:
      return self.payload.json
    return None

  def serialize_into(
      self,
      f: Any,
  ):
    headers = dict(self.headers)
    bytes = self.get_bytes()
    headers["length"] = len(bytes)
    f.write(json_dumps(headers))
    f.write(b"\n")
    f.write(bytes)
    f.write(b"\n")

  def serialize(self):
    out = io.BytesIO()
    self.serialize_into(out)
    return out.getvalue()

  @classmethod
  def deserialize_from(
      cls,
      f: Any,
  ):
    # type: (...) -> Optional[Item]
    line = f.readline().rstrip()
    if not line:
      return None
    headers = parse_json(line)
    length = headers.get("length")
    if length is not None:
      payload = f.read(length)
      f.readline()
    else:
      # if no length was specified we need to read up to the end of line
      # and remove it (if it is present, i.e. not the very last char in an eof terminated envelope)
      payload = f.readline().rstrip(b"\n")
    if headers.get("type") in ("event", "transaction", "metric_buckets"):
      rv = cls(headers=headers, payload=PayloadRef(json=parse_json(payload)))
    else:
      rv = cls(headers=headers, payload=payload)
    return rv

  @classmethod
  def deserialize(
      cls,
      bytes    # type: bytes
  ):
    return cls.deserialize_from(io.BytesIO(bytes))
