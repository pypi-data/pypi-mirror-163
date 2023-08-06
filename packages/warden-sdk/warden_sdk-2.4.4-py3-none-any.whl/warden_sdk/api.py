import inspect

from warden_sdk.hub import Hub
from warden_sdk.scope import Scope

__all__ = [
    "debug",
    "set_test_user",
    "capture_event",
    "capture_message",
    "capture_exception",
    "add_breadcrumb",
    "configure_scope",
    "push_scope",
    "flush",
    "last_event_id",
    "start_span",
    "start_transaction",
    "set_tag",
    "set_context",
    "set_extra",
    "set_user",
    "set_level",
]

from typing import (Optional, Union, List)


def hubmethod(f):
  f.__doc__ = "%s\n\n%s" % (
      "Alias for :py:meth:`warden_sdk.Hub.%s`" % f.__name__,
      inspect.getdoc(getattr(Hub, f.__name__)),
  )
  return f


@hubmethod
def set_test_user(user_fid: Optional[str] = None,
                  user_scope: Optional[Union[str, List[str]]] = None):
  """
    Set the test user for testing APIs, at the same time setting options.debug
    to true for comprehensive debugging.

    To turn off debug, use the `debug()` function.
    """
  return Hub.current.set_test_user(user_fid, user_scope)


@hubmethod
def debug(val: Optional[bool] = None) -> bool:
  """
    Returns the value of options.debug and if `val` is a boolean, it sets the 
    property of options.debug.
    """
  return Hub.current.debug(val)


@hubmethod
def env(env: Optional[str] = None) -> str:
  """
    Returns the value of options.debug and if `val` is a boolean, it sets the 
    property of options.debug.
    """
  return Hub.current.env(env)


def scopemethod(f):
  f.__doc__ = "%s\n\n%s" % (
      "Alias for :py:meth:`warden_sdk.Scope.%s`" % f.__name__,
      inspect.getdoc(getattr(Scope, f.__name__)),
  )
  return f


@hubmethod
def capture_event(
    event,
    hint=None,
    scope=None,
    **scope_args,
):
  return Hub.current.capture_event(event, hint, scope=scope, **scope_args)


@hubmethod
def capture_message(
    message,
    level=None,
    scope=None,
    **scope_args,
):
  return Hub.current.capture_message(message, level, scope=scope, **scope_args)


@hubmethod
def capture_exception(
    error=None,
    scope=None,
    **scope_args,
):
  return Hub.current.capture_exception(error, scope=scope, **scope_args)


@hubmethod
def last_event_id():
  return Hub.current.last_event_id()


@hubmethod
def flush(
    timeout=None,
    callback=None,
):
  return Hub.current.flush(timeout=timeout, callback=callback)


@hubmethod
def push_scope(callback=None,):
  return Hub.current.push_scope(callback)


@hubmethod
def configure_scope(callback=None,):
  return Hub.current.configure_scope(callback)


@hubmethod
def start_transaction(
    transaction=None,
    **kwargs,
):
  return Hub.current.start_transaction(transaction, **kwargs)


@hubmethod
def add_breadcrumb(
    crumb=None,
    hint=None,
    **kwargs,
):
  return Hub.current.add_breadcrumb(crumb, hint, **kwargs)


@scopemethod    # noqa
def set_tag(key, value):
  return Hub.current.scope.set_tag(key, value)


@scopemethod    # noqa
def set_context(key, value):
  return Hub.current.scope.set_context(key, value)


@scopemethod    # noqa
def set_extra(key, value):
  return Hub.current.scope.set_extra(key, value)


@scopemethod    # noqa
def set_user(value):
  return Hub.current.scope.set_user(value)


@scopemethod    # noqa
def set_level(value):
  return Hub.current.scope.set_level(value)


@hubmethod
def start_span(
    span=None,
    **kwargs,
):
  return Hub.current.start_span(span=span, **kwargs)
