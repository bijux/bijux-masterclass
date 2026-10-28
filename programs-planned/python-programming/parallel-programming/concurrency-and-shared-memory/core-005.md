# Core 5: Synchronization Fundamentals – Locks, RLocks, Conditions

> **Core question:**  
> How do you protect shared mutable state from races, allow reentrant locking, and coordinate threads with wait/notify — without deadlocks or busy-waiting?

In **Core 1** you learned *when* to choose threads vs processes.  
In **Core 2** you learned *why* shared-state threads need synchronization (GIL + shared memory).  
In **Core 3** you mastered basic threading, `Thread`, and `Queue`.  
In **Core 4** you learned multiprocessing for CPU parallelism.  
Here in **Core 5** you learn the **synchronization primitives** that make shared-state threading safe: `Lock`, `RLock`, and `Condition`.

**Audience:** Developers who can spawn threads and use `Queue`, but still hit races, deadlocks, or “why won’t my threads coordinate?” bugs.

**Outcome:** After this file, you should:
1. Choose `Lock` vs `RLock` vs `Condition` in < 10 seconds.
2. Explain in one sentence why `with lock:` is safer than manual `acquire()/release()`.
3. Implement a `Condition`-based wait/notify instead of a busy-wait loop.
4. Spot and fix three classic sync bugs in code review:
   - Unsynchronized access to shared state
   - Deadlocks from inconsistent lock ordering / reentrancy mistakes
   - Busy-waiting instead of `Condition.wait()`

---

## 1. Historical & Conceptual Backbone

### 1.1 History in 5 Lines

- Early Python: `_thread` module exposes primitive locks.
- Python 2.0: `threading` adds higher-level `Lock`, `RLock`, `Condition`, `Event`, `Semaphore`.
- Python 2.x: `Condition` and `Lock` gain more ergonomic features (timeouts, etc.).
- Python 3.x: Context managers (`with lock:`) become idiomatic and ubiquitous.
- November 2025: These primitives are stable; `queue.Queue`, executors, and frameworks build directly on them.

**This core focuses on `Lock`, `RLock`, and `Condition`.**  
`queue.Queue` (Core 3) is implemented *on top* of `Condition`.

### 1.2 Synchronization Primitives in One Precise Sentence

> `Lock` provides mutual exclusion, `RLock` provides mutual exclusion that can be re-acquired by the same thread, and `Condition` lets threads wait and be notified when shared state changes.

### 1.3 The One-Sentence Rule

> **Lock every critical section; use `RLock` only when the same thread must re-acquire; use `Condition` to wait efficiently instead of spinning.**

Everything else in this core is a justification and elaboration of that rule.

### 1.4 Positioning of `queue.Queue`

`queue.Queue` is a **higher-level abstraction** built on `Condition`:
- It hides:
  - The lock
  - The wait/notify protocol
  - Bookkeeping for “items in progress”
- Use it for:
  - Producer–consumer patterns
  - I/O pipelines (Core 3)
- Drop down to raw `Condition` when:
  - You need a custom predicate (`while not <complex_state>`)  
  - You have *multiple* shared objects but one wait condition
  - You need more control than `Queue` offers

For this core: **master the primitives** so that queues and higher-level APIs are no longer magic.

---

## 2. Mental Model: Locks and Conditions

### 2.1 One Picture

```text
Shared Mutable State (counters, caches, queues)
+-------------------------------------------------------------+
|                                                             |
|   [ Thread A ]     [ Thread B ]     [ Thread C ]            |
|        |                |                |                  |
|        v                v                v                  |
|   +-------------------- Critical Section -----------------+ |
|   |  with lock:                                         | | |
|   |      read / modify / write shared state             | | |
|   +-----------------------------------------------------+ | |
|                                                             |
|         Condition Variable (cond = Condition(lock))         |
|   Waiter:                                                  |
|       with cond:                                           |
|           while not predicate(shared_state):               |
|               cond.wait()   # releases lock + sleeps       |
|   Notifier:                                                |
|       with cond:                                           |
|           modify shared_state                               |
|           cond.notify() or cond.notify_all()               |
+-------------------------------------------------------------+

Lock:   only ONE thread in critical section at a time.
RLock:  same, but the SAME thread can enter multiple times.
Condition: lock + wait-queue → efficient wait/notify on predicates.
```

### 2.2 Contract Table

| Primitive   | Purpose                                       | Reentrant? | Blocks? | Needs Associated Lock?  | Typical Use                          |
| ----------- | --------------------------------------------- | ---------- | ------- | ----------------------- | ------------------------------------ |
| `Lock`      | Mutual exclusion for critical sections        | No         | Yes     | No                      | Simple shared counters, lists, dicts |
| `RLock`     | Reentrant mutual exclusion                    | Yes        | Yes     | No                      | Object methods that re-enter locking |
| `Condition` | Wait/notify on arbitrary predicate over state | N/A        | Yes     | Yes (`Lock` or `RLock`) | Producer–consumer, bounded buffers   |

---

## 3. Anti-Pattern First: “Sharing memory is easy. Sharing it correctly is not.”

### Example 1 – Race Without Lock (Anti-Pattern)

```python
# Example 1: Race on shared counter (DO NOT COPY)
from threading import Thread

counter = 0

def inc():
    global counter
    counter += 1  # Not atomic: read, add, write

if __name__ == "__main__":
    threads = [Thread(target=inc) for _ in range(1000)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Expected 1000, got {counter}")  # Often < 1000
```

**What to observe:**
You often get a value < 1000 — classic lost updates.

---

## 4. Correct Pattern: Simple Mutual Exclusion with `Lock`

### Example 2 – Protected Counter with `Lock`

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

> **Why `with lock:` is better:**
> It guarantees the lock is released even if an exception happens inside the block.

---

## 5. Correct Pattern: Reentrant Locking with `RLock`

### Example 3 – Recursive Calls with `RLock`

```python
# Example 3: RLock allows nested acquire
from threading import RLock, Thread
import time

lock = RLock()

def inner():
    with lock:
        print("Inner acquired")

def outer():
    with lock:
        print("Outer acquired")
        inner()  # Same thread re-enters lock

if __name__ == "__main__":
    t = Thread(target=outer)
    t.start()
    t.join()
```

**What to observe:**
No deadlock — same thread acquires the lock twice (and must release twice).

---

## 6. Consequence: Locks Prevent Races, Conditions Prevent Spinning

**This section is about what each primitive buys you once you’ve chosen it.**

### Example 4 – Deadlock with Plain `Lock` in Recursive Code

```python
# Example 4: Lock deadlocks on re-acquire (DO NOT RUN)
from threading import Lock

lock = Lock()

def inner():
    with lock:
        print("Inner acquired")

def outer():
    with lock:
        print("Outer acquired")
        inner()  # Deadlock: tries to re-acquire same Lock

# outer()  # Uncomment to see deadlock
```

Use `RLock` if your locked methods can call each other.

### Example 5 – Busy-Wait Anti-Pattern vs `Condition`

#### 5a. Busy-Wait (Anti-Pattern)

```python
# Example 5a: Busy-waiting (DO NOT COPY)
import time
from threading import Thread

ready = False

def waiter():
    while not ready:
        # burns CPU doing nothing
        pass
    print("Waiter proceeds")

def notifier():
    global ready
    time.sleep(1)
    ready = True

if __name__ == "__main__":
    Thread(target=waiter, daemon=True).start()
    Thread(target=notifier).start()
    time.sleep(2)
```

#### 5b. Same Logic With `Condition` (Correct)

```python
# Example 5b: Condition avoids busy-waiting
from threading import Condition, Thread
import time

cond = Condition()
ready = False

def waiter():
    with cond:
        while not ready:
            print("Waiting...")
            cond.wait()  # Releases lock, sleeps
        print("Waiter proceeds")

def notifier():
    global ready
    time.sleep(1)
    with cond:
        ready = True
        cond.notify_all()  # Wake all waiters

if __name__ == "__main__":
    Thread(target=waiter, daemon=True).start()
    Thread(target=notifier).start()
    time.sleep(2)
```

**What to observe:**
No CPU spin. Waiter blocks inside `wait()` until notified.

---

## 7. Synchronization Fundamentals in One Sentence

> Use `Lock` for simple critical sections, `RLock` when locked code can re-enter itself, and `Condition` to put threads to sleep until a predicate over shared state becomes true.

### Example 6 – `Condition.wait()` Releases the Lock

```python
# Example 6: Condition.wait() releases associated lock
from threading import Condition

cond = Condition()

def demo():
    with cond:
        print("Holding lock, calling wait()...")
        cond.wait(timeout=0.1)  # Releases lock while waiting
        print("Re-acquired lock after wait() returns")

if __name__ == "__main__":
    demo()
```

---

## 8. Cost Model: Synchronization Is Cheap (When Uncontended)

* Uncontended `Lock` acquire/release: **very fast** (tens of nanoseconds).
* Contended `Lock`: threads may block and context-switch → microseconds.
* `Condition.wait()`: parks thread efficiently, no userspace spin.

### Example 7 – Contended vs Uncontended Lock

```python
# Example 7: Lock contention overhead
import time
from threading import Thread, Lock

lock = Lock()

def contended():
    for _ in range(50_000):
        with lock:
            pass

def uncontended():
    local = 0
    for _ in range(50_000):
        local += 1

if __name__ == "__main__":
    start = time.perf_counter()
    threads = [Thread(target=contended) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"Contended lock:   {time.perf_counter() - start:.3f} s")

    start = time.perf_counter()
    threads = [Thread(target=uncontended) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"Uncontended work: {time.perf_counter() - start:.3f} s")
```

**Key point:**
Don’t serialize your entire program on one global lock; design your state to minimize contention.

---

## 9. Practical Design Recipe: “Lock early, release soon. Wait with Condition, never spin.”

```text
1. Prefer message passing (Queue from Core 3) over shared state.

2. If you must share mutable state:
   - Create a Lock per logical resource (cache, connection pool, etc.).
   - Wrap every read-modify-write in `with lock:`.
   - Keep critical sections as small as possible.

3. Use RLock only when:
   - Methods that acquire the lock may call each other.
   - You understand that each acquire must be matched by a release.

4. For waiting on state changes:
   - Decide on a clear predicate, e.g. "buffer not empty", "count < N".
   - Use `Condition` + a `while not predicate: cond.wait()`.
   - Notify with `cond.notify()` (one thread) or `cond.notify_all()`.

5. Avoid:
   - Busy-wait loops.
   - Multiple locks acquired in inconsistent orders (deadlock).
   - One giant global lock protecting everything.

6. Benchmark:
   - Use Example 30 to see where locking or Conditions dominate runtime.
```

---

## 10. API Survey

Core primitives you’ll use 99% of the time:

| API                   | Purpose                               | Notes                                     |
| --------------------- | ------------------------------------- | ----------------------------------------- |
| `threading.Lock`      | Non-reentrant mutual exclusion        | Use `with lock:`                          |
| `threading.RLock`     | Reentrant mutual exclusion            | Only when locked code can re-enter itself |
| `threading.Condition` | Wait/notify on shared state predicate | Built on top of a `Lock` or `RLock`       |

---

## 11. Worked Examples (1–30)

All runnable, no hidden gotchas. (Anti-patterns are clearly marked.)

We already saw Examples 1–7 above. Continuing from 8:

### Example 8 – Minimal Lock Usage

```python
# Example 8: Basic lock usage
from threading import Lock, Thread
import time

lock = Lock()
shared = 0

def inc():
    global shared
    with lock:
        shared += 1

if __name__ == "__main__":
    threads = [Thread(target=inc) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(shared)  # → 10
```

### Example 9 – Lock Acquire with Bounded Timeout

```python
# Example 9: Lock acquire with bounded timeout
from threading import Lock
import time

lock = Lock()

# Pretend some other part of code holds the lock
lock.acquire()

acquired = lock.acquire(timeout=0.1)
if acquired:
    print("Unexpected: acquired lock")
    lock.release()
else:
    print("Timeout: could not acquire lock within 0.1s")

lock.release()
```

### Example 10 – `with lock:` Is Exception-Safe

```python
# Example 10: with lock: auto-releases on exception
from threading import Lock

lock = Lock()

try:
    with lock:
        print("In critical section")
        raise ValueError("Oops")
except ValueError:
    pass

# Lock is released here; no deadlock
if lock.acquire(blocking=False):
    print("Lock was released correctly")
    lock.release()
```

### Example 11 – Condition with Predicate Loop

```python
# Example 11: Proper Condition usage with predicate loop
from threading import Condition, Thread
import time

cond = Condition()
data = None

def producer():
    global data
    time.sleep(0.5)
    with cond:
        data = "ready"
        cond.notify_all()

def consumer():
    with cond:
        while data is None:
            cond.wait()
        print("Data ready:", data)

if __name__ == "__main__":
    Thread(target=consumer).start()
    Thread(target=producer).start()
    time.sleep(1)
```

### Example 12 – `notify` vs `notify_all`

```python
# Example 12: notify vs notify_all
from threading import Condition, Thread
import time

cond = Condition()
ready = False

def waiter(name):
    with cond:
        while not ready:
            cond.wait()
        print(f"{name} proceeded")

def notifier():
    global ready
    time.sleep(0.5)
    with cond:
        ready = True
        cond.notify_all()  # try cond.notify() to wake only one

if __name__ == "__main__":
    for name in "ABC":
        Thread(target=waiter, args=(name,)).start()
    Thread(target=notifier).start()
    time.sleep(1)
```

### Example 13 – Condition Wait with Timeout

```python
# Example 13: Condition wait with timeout
from threading import Condition
import time

cond = Condition()

def demo():
    with cond:
        print("Waiting up to 0.5s...")
        notified = cond.wait(timeout=0.5)
        if notified:
            print("Notified")
        else:
            print("Timed out")

if __name__ == "__main__":
    demo()
```

### Example 14 – Non-Blocking Try-Lock

```python
# Example 14: Non-blocking try-lock
from threading import Lock

lock = Lock()

if lock.acquire(blocking=False):
    try:
        print("Got lock immediately")
    finally:
        lock.release()
else:
    print("Lock contended; do something else")
```

### Example 15 – Consistent Lock Ordering to Avoid Deadlocks

```python
# Example 15: Consistent lock ordering prevents deadlock
from threading import Lock, Thread
import time

lock_a = Lock()
lock_b = Lock()

def thread1():
    with lock_a:
        time.sleep(0.1)
        with lock_b:
            print("Thread 1 done")

def thread2():
    with lock_a:  # Same order: lock_a, then lock_b
        with lock_b:
            print("Thread 2 done")

if __name__ == "__main__":
    t1 = Thread(target=thread1)
    t2 = Thread(target=thread2)
    t1.start(); t2.start()
    t1.join(); t2.join()
```

### Example 16 – Inconsistent Ordering (Deadlock Anti-Pattern)

```python
# Example 16: Inconsistent lock ordering (DO NOT RUN)
from threading import Lock

lock_a = Lock()
lock_b = Lock()

def thread1():
    with lock_a:
        with lock_b:
            pass

def thread2():
    with lock_b:       # Opposite order
        with lock_a:
            pass

# Starting both threads can deadlock if they interleave badly.
```

### Example 17 – Condition with Multiple Consumers

```python
# Example 17: Multiple consumers with Condition
from threading import Condition, Thread
import time

cond = Condition()
buffer = []

def producer():
    time.sleep(0.5)
    with cond:
        buffer.append("item")
        cond.notify_all()

def consumer(name):
    with cond:
        while not buffer:
            cond.wait()
        item = buffer.pop(0)
    print(f"{name} consumed {item}")

if __name__ == "__main__":
    for name in "ABC":
        Thread(target=consumer, args=(name,)).start()
    Thread(target=producer).start()
    time.sleep(1)
```

### Example 18 – `RLock` in Class Methods

```python
# Example 18: RLock for object methods that call each other
from threading import RLock, Thread

class Counter:
    def __init__(self):
        self._lock = RLock()
        self._value = 0

    def inc(self):
        with self._lock:
            self._value += 1

    def double_inc(self):
        with self._lock:
            # Safe: inner acquires same RLock
            self.inc()
            self.inc()

    @property
    def value(self):
        return self._value

if __name__ == "__main__":
    c = Counter()
    threads = [Thread(target=c.double_inc) for _ in range(100)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(c.value)  # → 200
```

### Example 19 – Bounded Buffer with `Condition` (DIY Queue)

```python
# Example 19: Bounded buffer with Condition (Queue-like)
from threading import Condition, Thread
import time

cond = Condition()
buffer = []
MAX = 3

def producer():
    for i in range(10):
        with cond:
            while len(buffer) == MAX:
                cond.wait()
            buffer.append(i)
            cond.notify_all()
        time.sleep(0.05)

def consumer():
    for _ in range(10):
        with cond:
            while not buffer:
                cond.wait()
            item = buffer.pop(0)
            cond.notify_all()
        print("Consumed", item)

if __name__ == "__main__":
    Thread(target=producer, daemon=True).start()
    Thread(target=consumer).start()
    time.sleep(2)
```

### Example 20 – Lock Contention Benchmark

```python
# Example 20: Contended lock overhead
import time
from threading import Thread, Lock

lock = Lock()
counter = 0

def worker():
    global counter
    for _ in range(100_000):
        with lock:
            counter += 1

if __name__ == "__main__":
    start = time.perf_counter()
    threads = [Thread(target=worker) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"8 threads, contended lock: {time.perf_counter() - start:.3f} s")
    print("Final counter:", counter)
```

### Example 21 – Condition + Timeout to Avoid Hanging Forever

```python
# Example 21: Condition with timeout to avoid indefinite wait
from threading import Condition, Thread
import time

cond = Condition()
ready = False

def waiter():
    global ready
    with cond:
        end = time.time() + 1.0
        while not ready:
            remaining = end - time.time()
            if remaining <= 0 or not cond.wait(timeout=remaining):
                print("Gave up waiting")
                return
        print("Condition satisfied")

if __name__ == "__main__":
    Thread(target=waiter).start()
    # No notifier → will time out
    time.sleep(2)
```

### Example 22 – Lock Used as Simple Once-Initializer

```python
# Example 22: Use Lock to guard one-time initialization
from threading import Lock, Thread
import time

init_lock = Lock()
initialized = False

def maybe_init():
    global initialized
    with init_lock:
        if not initialized:
            print("Doing expensive initialization...")
            time.sleep(0.2)
            initialized = True
        else:
            print("Already initialized")

if __name__ == "__main__":
    threads = [Thread(target=maybe_init) for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
```

### Example 23 – Turn a Busy-Wait Loop into Condition Wait

```python
# Example 23: Refactor busy-wait into Condition
from threading import Condition, Thread
import time

cond = Condition()
flag = False

def waiter():
    with cond:
        while not flag:
            cond.wait()
        print("Flag is now True")

def notifier():
    global flag
    time.sleep(0.5)
    with cond:
        flag = True
        cond.notify_all()

if __name__ == "__main__":
    Thread(target=waiter).start()
    Thread(target=notifier).start()
    time.sleep(1)
```

### Example 24 – Using Condition for “Batch Ready” Signal

```python
# Example 24: Condition to signal batch readiness
from threading import Condition, Thread
import time

cond = Condition()
batch = []

def producer():
    for i in range(5):
        time.sleep(0.1)
        with cond:
            batch.append(i)
            if len(batch) == 5:
                cond.notify_all()

def consumer():
    with cond:
        while len(batch) < 5:
            cond.wait()
        print("Full batch:", list(batch))

if __name__ == "__main__":
    Thread(target=consumer).start()
    Thread(target=producer).start()
    time.sleep(1)
```

### Example 25 – `Condition` with Custom Underlying Lock

```python
# Example 25: Condition using a separate lock
from threading import Condition, Lock, Thread
import time

lock = Lock()
cond = Condition(lock)
ready = False

def waiter():
    with cond:
        while not ready:
            cond.wait()
        print("Waiter sees ready = True")

def notifier():
    global ready
    time.sleep(0.3)
    with cond:
        ready = True
        cond.notify_all()

if __name__ == "__main__":
    Thread(target=waiter).start()
    Thread(target=notifier).start()
    time.sleep(1)
```

### Example 26 – Using `Lock` to Protect a Cache

```python
# Example 26: Lock-protected cache
from threading import Lock, Thread
import time

cache_lock = Lock()
cache = {}

def get_or_compute(key):
    with cache_lock:
        if key in cache:
            return cache[key]
    # Compute outside lock
    time.sleep(0.1)
    value = key * 2
    with cache_lock:
        cache[key] = value
    return value

if __name__ == "__main__":
    threads = [Thread(target=get_or_compute, args=(i,)) for i in [1, 1, 2, 2, 3]]
    for t in threads: t.start()
    for t in threads: t.join()
    print(cache)
```

### Example 27 – Try-Lock Fallback Path

```python
# Example 27: Try-lock with graceful fallback
from threading import Lock

lock = Lock()

def maybe_critical():
    if lock.acquire(blocking=False):
        try:
            print("Doing critical work")
        finally:
            lock.release()
    else:
        print("Lock busy; doing degraded work")

if __name__ == "__main__":
    lock.acquire()  # Simulate someone else holding it
    maybe_critical()
    lock.release()
```

### Example 28 – Condition as “Barrier Lite”

```python
# Example 28: Condition as a simple barrier
from threading import Condition, Thread
import time

cond = Condition()
arrived = 0
TARGET = 3

def worker(i):
    global arrived
    time.sleep(0.1 * i)
    with cond:
        arrived += 1
        if arrived == TARGET:
            cond.notify_all()
        else:
            while arrived < TARGET:
                cond.wait()
    print(f"Worker {i} passed barrier")

if __name__ == "__main__":
    for i in range(TARGET):
        Thread(target=worker, args=(i,)).start()
    time.sleep(1)
```

### Example 29 – Debugging Lock Contention

```python
# Example 29: Quick and dirty lock contention probe
from threading import Lock, Thread
import time

lock = Lock()
counter = 0

def worker():
    global counter
    for _ in range(50_000):
        acquired = lock.acquire(timeout=0.001)
        if not acquired:
            # Contention very high
            continue
        try:
            counter += 1
        finally:
            lock.release()

if __name__ == "__main__":
    start = time.perf_counter()
    threads = [Thread(target=worker) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    print("Counter:", counter)
    print("Elapsed:", time.perf_counter() - start)
```

### Example 30 – Universal Sync Benchmark Template

```python
# Example 30: Benchmark lock vs Condition vs Queue
import time
from threading import Thread, Lock, Condition
from queue import Queue

def benchmark(name, fn):
    start = time.perf_counter()
    fn()
    print(f"{name}: {time.perf_counter() - start:.3f} s")

if __name__ == "__main__":
    N = 50_000

    def locked_counter():
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
        print("Locked counter:", counter)

    def condition_producer_consumer():
        cond = Condition()
        items = []
        done = False

        def producer():
            nonlocal done
            for i in range(N):
                with cond:
                    items.append(i)
                    cond.notify()
            with cond:
                done = True
                cond.notify_all()

        def consumer():
            consumed = 0
            while True:
                with cond:
                    while not items and not done:
                        cond.wait()
                    if not items and done:
                        print("Condition consumed:", consumed)
                        return
                    items.pop(0)
                    consumed += 1

        t_prod = Thread(target=producer)
        t_cons = Thread(target=consumer)
        t_prod.start()
        t_cons.start()
        t_prod.join()
        t_cons.join()

    def queue_producer_consumer():
        q = Queue()
        def producer():
            for i in range(N):
                q.put(i)
            for _ in range(4):
                q.put(None)
        def consumer():
            consumed = 0
            while True:
                item = q.get()
                if item is None:
                    break
                consumed += 1
            print("Queue consumed:", consumed)

        prod = Thread(target=producer)
        consumers = [Thread(target=consumer) for _ in range(4)]
        prod.start()
        for t in consumers: t.start()
        prod.join()
        for t in consumers: t.join()

    benchmark("Locked counter", 
locked_counter)
    benchmark("Condition PC", condition_producer_consumer)
    benchmark("Queue PC", queue_producer_consumer)
```

---

## 12. Pre-Core Quiz

1. Does `with lock:` ensure the lock is released even on exceptions? → **Yes**
2. Should you use `RLock` whenever you can? → **No**, only when reentrancy is required.
3. Does `Condition.wait()` release the underlying lock while waiting? → **Yes**
4. Is busy-waiting (`while not flag: pass`) acceptable in production code? → **No**
5. Is one global lock for everything usually a good design? → **No** — it becomes a bottleneck.

---

## 13. Post-Core Reflection

Open your codebase:

* Find one place with manual `lock.acquire()` / `lock.release()` and replace it with `with lock:`.
* Find one busy-wait loop (`while not flag: ...`). Replace it with a `Condition` + `wait()` / `notify_all()`.

Run your tests.

Did you:

* Remove a potential deadlock or forgotten-release bug?
* Eliminate unnecessary CPU burn from spinning?

You now own the core **synchronization primitives** for safe shared-state threading in Python.

**Next:** Core 6 – Cost Models and Overheads for Threads and Processes.
