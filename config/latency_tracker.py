import asyncio
import atexit
import json
import queue
import threading
import time
from datetime import datetime
from functools import wraps
from pathlib import Path

_QUEUE: queue.Queue = queue.Queue(maxsize=10_000)
_STOP = object()
_thread = None
dropped = 0


def _worker(path: Path):
    with open(path, "a", encoding="utf-8") as f:       # open once
        while True:
            event = _QUEUE.get()
            if event is _STOP:
                break
            try:
                f.write(json.dumps(event, default=str) + "\n")
                f.flush()
            except Exception:
                pass                                   # never let one bad event kill the thread


def start_telemetry(path: str = "logs/node_times.jsonl"):
    """Call once at app start."""
    global _thread
    if _thread is not None:
        return
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    _thread = threading.Thread(target=_worker, args=(p,), daemon=True)
    _thread.start()
    atexit.register(stop_telemetry)


def stop_telemetry():
    global _thread
    if _thread is None:
        return
    _QUEUE.put(_STOP)
    _thread.join(timeout=5)                            # drain remaining events
    _thread = None


def _emit(name: str, start: float, status: str, error: str | None):
    global dropped
    event = {
        "ts": datetime.now().isoformat(),
        "node": name,
        "duration_s": round(time.perf_counter() - start, 4),
        "status": status,
        "error": error,
    }
    try:
        _QUEUE.put_nowait(event)                       # never blocks the node
    except queue.Full:
        dropped += 1


def track_time(func):
    name = func.__name__

    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start, status, error = time.perf_counter(), "ok", None
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                status, error = "error", type(e).__name__
                raise
            finally:
                _emit(name, start, status, error)
        return async_wrapper

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start, status, error = time.perf_counter(), "ok", None
        try:
            return func(*args, **kwargs)
        except Exception as e:
            status, error = "error", type(e).__name__
            raise
        finally:
            _emit(name, start, status, error)
    return sync_wrapper