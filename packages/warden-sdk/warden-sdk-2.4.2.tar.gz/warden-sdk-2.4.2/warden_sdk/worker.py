import os
import threading

from time import sleep, time
from warden_sdk._compat import check_thread_support
from warden_sdk._queue import Queue, FullError
from warden_sdk.utils import logger
from warden_sdk.consts import DEFAULT_QUEUE_SIZE

_TERMINATOR = object()


class BackgroundWorker(object):

  def __init__(self, queue_size=DEFAULT_QUEUE_SIZE):
    check_thread_support()
    self._queue = Queue(queue_size)
    self._lock = threading.Lock()
    self._thread = None
    self._thread_for_pid = None

  @property
  def is_alive(self):
    if self._thread_for_pid != os.getpid():
      return False
    if not self._thread:
      return False
    return self._thread.is_alive()

  def _ensure_thread(self):
    if not self.is_alive:
      self.start()

  def _timed_queue_join(self, timeout):
    deadline = time() + timeout
    queue = self._queue

    queue.all_tasks_done.acquire()

    try:
      while queue.unfinished_tasks:
        delay = deadline - time()
        if delay <= 0:
          return False
        queue.all_tasks_done.wait(timeout=delay)

      return True
    finally:
      queue.all_tasks_done.release()

  def start(self):
    with self._lock:
      if not self.is_alive:
        self._thread = threading.Thread(target=self._target,
                                        name="raven-warden.BackgroundWorker")
        self._thread.daemon = True
        self._thread.start()
        self._thread_for_pid = os.getpid()

  def kill(self):
    """
        Kill worker thread. Returns immediately. Not useful for
        waiting on shutdown for events, use `flush` for that.
        """
    logger.debug("background worker got kill request")
    with self._lock:
      if self._thread:
        try:
          self._queue.put_nowait(_TERMINATOR)
        except FullError:
          logger.debug("background worker queue full, kill failed")

        self._thread = None
        self._thread_for_pid = None

  def flush(self, timeout, callback=None):
    logger.debug("background worker got flush request")
    with self._lock:
      if self.is_alive and timeout > 0.0:
        self._wait_flush(timeout, callback)
    logger.debug("background worker flushed")

  def _wait_flush(self, timeout, callback):
    initial_timeout = min(0.1, timeout)
    if not self._timed_queue_join(initial_timeout):
      pending = self._queue.qsize() + 1
      logger.debug("%d event(s) pending on flush", pending)
      if callback is not None:
        callback(pending, timeout)

      if not self._timed_queue_join(timeout - initial_timeout):
        pending = self._queue.qsize() + 1
        logger.error("flush timed out, dropped %s events", pending)

  def submit(self, callback):
    self._ensure_thread()
    try:
      self._queue.put_nowait(callback)
      return True
    except FullError:
      return False

  def _target(self):
    while True:
      callback = self._queue.get()
      try:
        if callback is _TERMINATOR:
          break
        try:
          callback()
        except Exception:
          logger.error("Failed processing job", exc_info=True)
      finally:
        self._queue.task_done()
      sleep(0)
