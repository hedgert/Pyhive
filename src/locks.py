import asyncio
import threading


class AsyncLock(asyncio.Lock):
    """Alias for the asyncio implementation."""
    pass


class SyncLock:
    """Thread-safe synchronous lock."""

    def __init__(self):
        self._lock = threading.RLock()

    def acquire(self):
        self._lock.acquire()
        return True

    def release(self):
        self._lock.release()

    def locked(self):
        return self._lock._recursion_count() > 0

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.release()
        return False

