# Core 3: Threading Fundamentals – Threads, Locks, Queues

> **Core question:**  
> How do you safely spawn threads, protect shared state from races, and communicate between threads without deadlocks or corruption?

In **Core 1** you learned *when* to choose threads vs processes.  
In **Core 2** you learned *why* threads can’t use multiple cores for pure Python CPU (the GIL).  
Here in **Core 3** you learn *how* to use threads correctly: spawning, locking, and message-passing with queues.

**Audience:** Developers who already know “threads → I/O, processes → CPU”  
but are not yet confident writing thread-safe code.

**Outcome:** After this file, you should:
1. Spawn and join threads correctly in < 10 lines.
2. Explain why a lock prevents data races in one sentence.
3. Use `queue.Queue` for producer-consumer patterns without thinking.
4. Spot and fix the three most common threading bugs in code review:
   - Unsynchronized shared state
   - Manual lock misuse / deadlocks
   - Home-rolled queues instead of `Queue`

---

## 1. Historical & Conceptual Backbone

### 1.1 History in 5 Lines

- Early Python: `_thread` module exposes raw threads.
- Python 2.0: `threading` module adds object-oriented `Thread`, `Lock`, `RLock`, `Condition`, `Event`, `Semaphore`.
- Python 2.3/2.4: `Queue` module becomes the standard thread-safe FIFO.
- Python 3.2: `concurrent.futures` introduces `ThreadPoolExecutor` on top of `threading`.
- 2020s: `threading` + `queue` remain the stable foundation; executors are preferred for simple cases.

**This entire core focuses on low-level `threading` + `queue`.**  
Executors, async, and frameworks all build on these primitives.

### 1.2 Threading Primitives in One Precise Sentence

> The `threading` module lets you run functions concurrently in OS threads and gives you primitives (locks, conditions, events, semaphores) to keep shared memory consistent.

### 1.3 The One-Sentence Rule

> **Share nothing if you can. If you must share memory, lock it. If you must communicate, use a queue.**

Everything else in this core is a justification and elaboration of that rule.

### 1.4 Positioning of `concurrent.futures`

`concurrent.futures.ThreadPoolExecutor` is a **higher-level wrapper**:
- It **uses** `threading.Thread` under the hood.
- It hides:
  - thread creation / joining
  - error propagation
  - pool sizing
- Use it when:
  - your pattern is “map function over many independent tasks”.
  - you don’t need fine-grained control over locks or custom queues.
- Drop to raw `threading` when:
  - you’re building pipelines (multiple stages),
  - long-lived worker threads,
  - or custom synchronization (events, semaphores, conditions).

For this core: **master `threading` + `queue` first**. Executors will then be obvious.

---

## 2. Mental Model: Threads, Locks, Queues

### 2.1 One Picture

```text
Single Process with Multiple Threads
+-----------------------------------------------------------+
|        Shared Objects in One Address Space                |
|  (lists, dicts, DB connections, caches, global state)     |
|                                                           |
|   [ Thread A ]   [ Thread B ]   [ Thread C ]   [ Thread D ]
|        |              |              |              |
|        v              v              v              v
|      +----------------- Critical Sections ----------------+
|      |   read/modify shared objects under a Lock         |
|      +---------------------------------------------------+
|                                                           |
|               Thread-safe Queues (queue.Queue)           |
|   Producer ---- put() -->  [   Queue   ]  --> get() ---- Consumer
|                                                           |
+-----------------------------------------------------------+

Lock:   acquire → do critical work → release
Queue:  put(item) from producers, get() from consumers, safe & blocking
```

### 2.2 Contract Table

| Primitive   | Purpose                                     | Thread-Safe? | Can Block? | Typical Use                          |
| ----------- | ------------------------------------------- | ------------ | ---------- | ------------------------------------ |
| `Thread`    | Run a function concurrently                 | Yes          | No         | I/O workers, background tasks        |
| `Lock`      | Mutual exclusion (non-reentrant)            | Yes          | Yes        | Protect simple critical sections     |
| `RLock`     | Reentrant lock (same thread can re-acquire) | Yes          | Yes        | Object methods that call each other  |
| `Queue`     | Thread-safe FIFO / producer-consumer        | Yes          | Yes        | Pipelines, work queues               |
| `Condition` | Wait/notify on shared state                 | Yes          | Yes        | Advanced coordination                |
| `Event`     | One-bit flag, wait until set                | Yes          | Yes        | Stop signals, ready flags            |
| `Semaphore` | Limit concurrent access to a resource       | Yes          | Yes        | Connection pools, “N at a time”      |
| `Barrier`   | Make threads rendezvous at a point          | Yes          | Yes        | Advanced phase synchronization       |

---

## 3. Anti-Pattern First: “Sharing memory is easy. Sharing it correctly is not.”

### Example 1 – Shared Mutable Without Lock (Race Condition)

```python
# Example 1: Race condition on shared counter
from threading import Thread

counter = 0

def inc():
    global counter
    # Not atomic: read, add, write can interleave
    counter += 1

if __name__ == "__main__":
    threads = [Thread(target=inc) for _ in range(1000)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Expected 1000, got {counter}")  # Often < 1000
```

**What to observe:**
You often get a number less than 1000 → classic lost updates.

---

## 4. Correct Pattern: Protect Shared State with Locks

### Example 2 – Same Counter with `Lock`

```python
# Example 2: Thread-safe counter with Lock
from threading import Thread, Lock

counter = 0
lock = Lock()

def inc():
    global counter
    with lock:          # acquire → critical section → release
        counter += 1

if __name__ == "__main__":
    threads = [Thread(target=inc) for _ in range(1000)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Counter = {counter}")  # → 1000
```

**What to observe:**
Always 1000. Lock makes the read-modify-write sequence appear atomic.

---

## 5. Correct Pattern: Communicate with Queues, Not Shared Buffers

### Example 3 – Producer–Consumer with `Queue`

```python
# Example 3: Queue for safe communication
from threading import Thread
from queue import Queue
import time

q = Queue()

def producer():
    for i in range(5):
        time.sleep(0.1)  # Simulate I/O
        q.put(i)
    q.put(None)  # Sentinel to signal completion

def consumer():
    while True:
        item = q.get()  # Blocks when queue empty
        if item is None:
            break
        print(f"Consumed {item}")
        q.task_done()

if __name__ == "__main__":
    Thread(target=producer, daemon=True).start()
    worker = Thread(target=consumer)
    worker.start()

    q.join()  # Wait until consumer calls task_done() for all real items
    worker.join()
    print("Done")
```

**What to observe:**
No shared list, no manual locking, no races. All coordination via the queue.

---

## 6. Consequence: Locks Prevent Races, Queues Prevent Locks

**This section is about what each primitive buys you once you’ve chosen it.**

### Example 4 – Reentrant Lock (`RLock`) for Nested Calls

```python
# Example 4: RLock allows nested acquire
from threading import RLock

lock = RLock()

def inner():
    with lock:
        print("Inner critical section")

def outer():
    with lock:
        print("Outer critical section")
        inner()  # Re-acquires the same lock in the same thread

if __name__ == "__main__":
    outer()
```

If you used `Lock` instead of `RLock`, `inner()` would deadlock by trying to re-acquire the same lock.

### Example 5 – Why a Plain `Lock` Can Deadlock Recursively

```python
# Example 5: Lock does NOT allow nested acquire
from threading import Lock

lock = Lock()

def outer():
    with lock:
        print("Outer entered")
        # inner() tries to re-acquire lock → deadlock
        # inner()

def inner():
    with lock:
        print("Inner entered")

if __name__ == "__main__":
    outer()
    print("OK (because we didn't call inner)")
    # Uncomment inner() call inside outer() to see the deadlock
```

**Takeaway:**
Use `Lock` for non-recursive code. Use `RLock` when methods that acquire the lock may call each other.

---

## 7. Threading Fundamentals in One Sentence

> Use `Lock` to guard shared writes, `RLock` for recursive code, and `Queue` to move data instead of sharing state.

### Example 6 – `Queue.get()` Blocks Safely

```python
# Example 6: Queue.get() blocks until item available
from threading import Thread
from queue import Queue
import time

q = Queue()

def producer():
    time.sleep(1.0)
    q.put("data")

def consumer():
    print("Waiting for item...")
    item = q.get()      # Blocks ~1 second
    print(f"Got {item}")
    q.task_done()

if __name__ == "__main__":
    Thread(target=producer, daemon=True).start()
    Thread(target=consumer).start()
    q.join()
```

---

## 8. Cost Model: Threads Are Lighter Than Processes, but Not Free

Threads are **cheaper** than processes:

* No new interpreter, smaller memory overhead, faster startup.

But they still cost:

* Each thread has a stack (1–8 MB default).
* Too many threads → context switch overhead, scheduler thrash.

### Example 7 – Creating 1,000 Threads

```python
# Example 7: 1,000 threads – measurable but reasonable for I/O
import time
from threading import Thread

def tiny():
    pass

if __name__ == "__main__":
    start = time.perf_counter()
    threads = [Thread(target=tiny) for _ in range(1_000)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"1,000 threads took {time.perf_counter() - start:.3f} s")
```

**Key point:**
Threads are cheap *enough* for hundreds of concurrent I/O tasks. Use **pools** instead of spawning thousands on the fly.

---

## 9. Practical Design Recipe: “Share nothing. Lock what you must. Queue the rest.”

```text
1. Start from Core 1:
   - Is this I/O-bound? → threads
   - Is this CPU-bound? → processes (Core 4)

2. Within threads:
   - Prefer message passing:
     - Producers push work/items into a Queue
     - Consumers pull from the Queue

3. If you must share mutable state:
   - Wrap every read-modify-write in `with lock:`
   - Use one lock per logically related chunk of data

4. Avoid:
   - Global mutable state without locks
   - Nested locks in multiple orders (deadlocks)
   - Hand-rolled queues using lists + locks

5. Use advanced primitives only when needed:
   - `Event` for simple “start/stop” signals
   - `Condition` for wait/notify on complex predicates
   - `Semaphore` to cap concurrency (N-at-a-time)

6. Benchmark:
   - Use Example 30 to check if your locking/queues dominate runtime.
```

---

## 10. API Survey

These are the core primitives you’ll use most.

| API                   | Purpose                             | Typical Use                                  |
| --------------------- | ----------------------------------- | -------------------------------------------- |
| `threading.Thread`    | Run function in a new thread        | I/O workers, background tasks                |
| `threading.Lock`      | Mutual exclusion                    | Protect shared counters, lists, dicts        |
| `threading.RLock`     | Reentrant mutex                     | Object with methods that call each other     |
| `queue.Queue`         | Thread-safe FIFO                    | Work queues, pipelines                       |
| `threading.Event`     | One-bit flag (wait/set/clear)       | Stop signals, ready flags                    |
| `threading.Condition` | Wait/notify on arbitrary conditions | Advanced coordination on shared state        |
| `threading.Semaphore` | Bounded concurrent access           | Limit “N concurrent tasks”                   |
| `threading.Barrier`   | Phase synchronization               | All threads must reach a point before moving |

---

## 11. Worked Examples (1–30)

All runnable, guarded, and free of implementation-detail hacks.

### Example 8 – Minimal Thread Spawn & Join

```python
# Example 8: Hello from thread
from threading import Thread

def hello():
    print("Hello from thread")

if __name__ == "__main__":
    t = Thread(target=hello)
    t.start()
    t.join()
```

### Example 9 – Join with Timeout

```python
# Example 9: Thread join with timeout
from threading import Thread
import time

def sleep_forever():
    time.sleep(100)

if __name__ == "__main__":
    t = Thread(target=sleep_forever, daemon=True)
    t.start()
    t.join(timeout=0.5)
    print("Join timed out, main continues")
```

### Example 10 – Daemon vs Non-Daemon

```python
# Example 10: Daemon thread dies with main
from threading import Thread
import time

def background():
    while True:
        time.sleep(1)

if __name__ == "__main__":
    Thread(target=background, daemon=True).start()
    time.sleep(2)
    print("Main exits → daemon stopped automatically")
```

### Example 11 – Lock vs RLock Recap

```python
# Example 11: RLock allows recursion
from threading import RLock

lock = RLock()

def recursive(n):
    with lock:
        if n > 0:
            recursive(n - 1)

if __name__ == "__main__":
    recursive(10)
    print("Completed recursive locking")
```

### Example 12 – `Condition` Wait/Notify (advanced)

```python
# Example 12: Condition for producer-consumer (advanced)
from threading import Condition, Thread
import time

cond = Condition()
items = []

def producer():
    time.sleep(0.2)
    with cond:
        items.append("data")
        cond.notify()  # Wake up one waiter

def consumer():
    with cond:
        while not items:
            cond.wait()  # Release lock, sleep, re-acquire on wake
        item = items.pop()
    print(f"Got {item}")

if __name__ == "__main__":
    Thread(target=consumer).start()
    Thread(target=producer).start()
    time.sleep(1)
```

### Example 13 – `Event` Signal

```python
# Example 13: Event for simple signaling
from threading import Event, Thread
import time

event = Event()

def waiter():
    print("Waiting for event...")
    event.wait()
    print("Event received!")

if __name__ == "__main__":
    Thread(target=waiter, daemon=True).start()
    time.sleep(1)
    event.set()
    time.sleep(0.5)
```

### Example 14 – `Semaphore` to Limit Concurrency (advanced)

```python
# Example 14: Semaphore for resource pool (advanced)
from threading import Semaphore, Thread
import time

sem = Semaphore(3)  # Max 3 concurrent workers

def worker(i):
    with sem:
        print(f"Worker {i} acquired")
        time.sleep(0.5)
        print(f"Worker {i} released")

if __name__ == "__main__":
    for i in range(8):
        Thread(target=worker, args=(i,), daemon=True).start()
    time.sleep(3)
```

### Example 15 – Bounded Queue Blocks Producer

```python
# Example 15: Bounded queue back-pressures producer
from queue import Queue
from threading import Thread
import time

q = Queue(maxsize=2)

def producer():
    for i in range(5):
        q.put(i)  # Blocks when full until consumer takes items
        print(f"Produced {i}")

def consumer():
    time.sleep(1)
    while True:
        item = q.get()
        print(f"Consumed {item}")
        q.task_done()
        if item == 4:
            break

if __name__ == "__main__":
    Thread(target=producer, daemon=True).start()
    Thread(target=consumer).start()
    q.join()
```

### Example 16 – Thread-Local Storage

```python
# Example 16: Thread-local variables
from threading import Thread, local
import time

tls = local()

def worker(i):
    tls.id = i
    time.sleep(0.01)
    print(f"Thread {i} sees tls.id = {tls.id}")

if __name__ == "__main__":
    for i in range(5):
        Thread(target=worker, args=(i,)).start()
    time.sleep(1)
```

### Example 17 – Barrier Synchronization (advanced)

```python
# Example 17: Barrier for rendezvous
from threading import Barrier, Thread
import time

bar = Barrier(3)

def worker(i):
    print(f"Thread {i} before barrier")
    bar.wait()
    print(f"Thread {i} after barrier")

if __name__ == "__main__":
    for i in range(3):
        Thread(target=worker, args=(i,)).start()
    time.sleep(1)
```

### Example 18 – Timer Thread

```python
# Example 18: Timer for delayed execution
from threading import Timer

def delayed():
    print("Timer fired")

if __name__ == "__main__":
    t = Timer(1.0, delayed)
    t.start()
    t.join()
```

### Example 19 – Active Thread Count

```python
# Example 19: Monitor active threads
import threading
import time

def worker():
    time.sleep(0.2)

if __name__ == "__main__":
    print("Active before:", threading.active_count())
    t = threading.Thread(target=worker)
    t.start()
    print("Active during:", threading.active_count())
    t.join()
    print("Active after:", threading.active_count())
```

### Example 20 – Thread Name and Ident

```python
# Example 20: Thread identification
from threading import Thread, current_thread

def worker():
    cur = current_thread()
    print(f"Name: {cur.name}, ID: {cur.ident}")

if __name__ == "__main__":
    t = Thread(target=worker, name="WorkerThread")
    t.start()
    t.join()
```

### Example 21 – Exceptions in Threads Don’t Propagate Automatically

```python
# Example 21: Exceptions don't propagate to main thread
from threading import Thread

def buggy():
    raise ValueError("Oops inside thread")

if __name__ == "__main__":
    t = Thread(target=buggy)
    t.start()
    t.join()
    print("Main didn't see the exception (check stderr)")
```

### Example 22 – Queue `task_done` / `join`

```python
# Example 22: Queue join for completion
from queue import Queue
from threading import Thread

q = Queue()

def worker():
    while True:
        item = q.get()
        if item is None:
            q.task_done()
            break
        # process item ...
        q.task_done()

if __name__ == "__main__":
    for _ in range(4):
        Thread(target=worker, daemon=True).start()

    for i in range(10):
        q.put(i)

    # Send sentinel to each worker
    for _ in range(4):
        q.put(None)

    q.join()
    print("All tasks done")
```

### Example 23 – Two-Stage I/O Pipeline with Queues

```python
# Example 23: Threads + queues for I/O pipeline (ParaPipe style)
from threading import Thread
from queue import Queue
import time

in_q = Queue()
out_q = Queue()

def stage1():
    for i in range(5):
        time.sleep(0.1)  # Simulate I/O
        in_q.put(i)
    in_q.put(None)

def stage2():
    while True:
        item = in_q.get()
        if item is None:
            out_q.put(None)
            in_q.task_done()
            break
        out_q.put(item * 2)
        in_q.task_done()

def consumer():
    while True:
        item = out_q.get()
        if item is None:
            out_q.task_done()
            break
        print(f"Result {item}")
        out_q.task_done()

if __name__ == "__main__":
    Thread(target=stage1, daemon=True).start()
    Thread(target=stage2, daemon=True).start()
    Thread(target=consumer).start()

    in_q.join()
    out_q.join()
```

### Example 24 – `Event` for Stop Signals

```python
# Example 24: Graceful shutdown with Event
from threading import Thread, Event
import time

stop = Event()

def worker():
    while not stop.is_set():
        print("Working...")
        time.sleep(0.2)
    print("Worker stopping")

if __name__ == "__main__":
    t = Thread(target=worker)
    t.start()
    time.sleep(1)
    stop.set()
    t.join()
```

### Example 25 – `Semaphore` as Mutex

```python
# Example 25: Semaphore(1) = mutex
from threading import Semaphore, Thread
import time

mutex = Semaphore(1)

def critical(i):
    with mutex:
        print(f"{i} in critical section")
        time.sleep(0.1)

if __name__ == "__main__":
    for i in range(3):
        Thread(target=critical, args=(i,), daemon=True).start()
    time.sleep(1)
```

### Example 26 – `Condition` with Timeout (advanced)

```python
# Example 26: Condition wait with timeout (advanced)
from threading import Condition, Thread
import time

cond = Condition()
ready = False

def waiter():
    global ready
    with cond:
        while not ready:
            if not cond.wait(timeout=1.0):
                print("Timed out waiting")
                return
        print("Condition satisfied")

def setter():
    time.sleep(0.5)
    global ready
    with cond:
        ready = True
        cond.notify_all()

if __name__ == "__main__":
    Thread(target=waiter).start()
    Thread(target=setter).start()
    time.sleep(2)
```

### Example 27 – Non-Blocking Queue Access with `Empty`

```python
# Example 27: Queue.get_nowait raises Empty
from queue import Queue, Empty

q = Queue()

try:
    q.get_nowait()
except Empty:
    print("Queue was empty")
```

### Example 28 – Simple Thread Pool with `ThreadPoolExecutor`

```python
# Example 28: ThreadPoolExecutor recap (high-level)
from concurrent.futures import ThreadPoolExecutor

def task(i):
    return i * i

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as exe:
        results = list(exe.map(task, range(10)))
    print("Squares:", results)
```

### Example 29 – Capturing Exceptions from Threads (advanced pattern)

```python
# Example 29: Capture exceptions from threads
from threading import Thread
import traceback

def run_with_capture(fn, *args, **kwargs):
    result = {"exc": None}

    def wrapper():
        try:
            fn(*args, **kwargs)
        except Exception:
            result["exc"] = traceback.format_exc()

    t = Thread(target=wrapper)
    t.start()
    t.join()
    if result["exc"]:
        raise RuntimeError(f"Thread failed:\n{result['exc']}")

def buggy():
    raise ValueError("Broken in thread")

if __name__ == "__main__":
    try:
        run_with_capture(buggy)
    except RuntimeError as e:
        print("Caught thread error in main:")
        print(e)
```

### Example 30 – Universal Threading Benchmark Template

```python
# Example 30: Copy-paste to benchmark locking vs queues
import time
from threading import Thread, Lock
from queue import Queue

def benchmark(name, fn):
    start = time.perf_counter()
    fn()
    print(f"{name}: {time.perf_counter() - start:.3f} s")

if __name__ == "__main__":
    N = 100_000

    def race():
        counter = 0
        def inc():
            nonlocal counter
            for _ in range(N):
                counter += 1  # UNSAFE
        threads = [Thread(target=inc) for _ in range(4)]
        for t in threads: t.start()
        for t in threads: t.join()
        print("Final counter (race):", counter)

    def locked():
        counter = 0
        lock = Lock()
        def inc():
            nonlocal counter
            for _ in range(N):
                with lock:
                    counter += 1
        threads = [Thread(target=inc) for _ in range(4)]
        for t in threads: t.start()
        for t in threads: t.join()
        print("Final counter (locked):", counter)

    def queued():
        q = Queue()
        def producer():
            for _ in range(4 * N):
                q.put(1)
            for _ in range(4):
                q.put(None)  # Sentinels
        def consumer():
            total = 0
            while True:
                item = q.get()
                if item is None:
                    break
                total += item
            print("Total from queue:", total)
        t_prod = Thread(target=producer)
        consumers = [Thread(target=consumer) for _ in range(4)]
        t_prod.start()
        for t in consumers: t.start()
        t_prod.join()
        for t in consumers: t.join()

    benchmark("Race (unsafe)", race)
    benchmark("Lock (safe)", locked)
    benchmark("Queue (message passing)", queued)
```

---

## 12. Pre-Core Quiz

1. A `Lock` prevents races if you wrap **every** read-modify-write? → Yes  
2. `queue.Queue` is thread-safe? → Yes  
3. `RLock` allows the same thread to re-acquire the lock? → Yes  
4. Daemon threads keep your process alive? → No  
5. Use threads for CPU-bound parallelism in CPython? → No (GIL; use processes)  

## 13. Post-Core Reflection

Open your codebase.  
Find **one** place where multiple threads touch the same list or counter.

* Option A: Remove the shared state and use a `Queue` instead.  
* Option B: Wrap the shared state access in a `Lock`.

Run your tests. Did you eliminate a potential race?

You now own the fundamental tools for **safe threaded concurrency** in Python.

**Next:** Core 4 – Multiprocessing Basics (Processes, Pools, Shared Memory). 
