# Core 1: Threads vs Processes – When to Use Each

> **Core question:**  
> Do you need *concurrency* (lots of waiting, overlapping I/O) or *true parallelism* (lots of CPU work on multiple cores)?  
> In CPython, this is equivalent to: **threads vs processes**.

If you get *this* choice right, most other parallelism decisions become straightforward:
- Locks, pools, queues, async, pipelines – all hang off this decision.
- Get it wrong → “no speedup”, random hangs, or noisy code that does nothing faster.

**Audience:** Intermediate Python developers who can write functions and loops but have never seen reliable >1× speedup.

**Outcome:** After this file, you should:
1. Decide between threads and processes in < 10 seconds for any given task.
2. Explain the GIL in one precise sentence.
3. Write short benchmarks to validate your choice.
4. Recognize misuses in code review immediately.

---

## 1. Historical & Conceptual Backbone

### 1.1 History in 5 Lines

- Python had a **Global Interpreter Lock (GIL)** from the early days of CPython.
- The GIL makes **only one thread run Python bytecode at a time** per process.
- Threads stayed, but **CPU-bound scaling across cores never worked with threads**.
- The `multiprocessing` module was added to get **true multi-core parallelism** by using multiple processes.
- Experiments like PEP 703 (“no-GIL”) exist, but **99 % of production Python you will see in 2025 still has a GIL**.

**This entire core assumes standard CPython with a GIL.** If no-GIL ever becomes the default, the mental model shifts: threads become viable for CPU parallelism, and processes remain mainly for isolation, robustness, and distribution.

### 1.2 Concurrency vs Parallelism

Rob Pike’s distilled view:

> Concurrency is about *dealing with* lots of things at once.  
> Parallelism is about *doing* lots of things at once.

In CPython:

- **Threads** → concurrency: great for overlapping waits (network, disk, sleep).
- **Processes** → parallelism: great for using multiple cores on CPU-heavy work.

### 1.3 The One-Sentence Rule

> **If it waits, thread it (or async it). If it computes, fork it. When unsure — measure it.**

Everything else in this core is a justification and elaboration of that rule.

### 1.4 Positioning of `asyncio`

`asyncio` is **not** a third primitive — it is an alternative to threads for pure I/O-bound concurrency:
- Cooperative (single-threaded) → no thread overhead, no GIL contention during awaits.
- Still **GIL-bound** for any CPU work.
- Use it when you want thousands of concurrent connections with minimal memory.

For the low-level decision this core teaches: **threads vs processes**, `asyncio` sits on the “thread” side of the fence.

---

## 2. Mental Model: Threads vs Processes

### 2.1 One Picture

```text
+--------------------- Single Python Process ----------------------+
|                    One GIL (one thread runs Python at a time)    |
|                                                                  |
|  [ Thread 1 ]  [ Thread 2 ]  [ Thread 3 ]  [ Thread 4 ]          |
|    Shared memory, cheap to start, great for I/O,                 |
|    BUT all Python bytecode serialized by the GIL                 |
+------------------------------------------------------------------+

+----------------------- Multiple Processes -----------------------+
|  Process A   |  Process B   |  Process C   |  Process D          |
|  Own memory  |  Own memory  |  Own memory  |  Own memory         |
|  Own GIL     |  Own GIL     |  Own GIL     |  Own GIL            |
|  More costly to start, harder to share data,                     |
|  BUT can run truly in parallel on separate cores                 |
+------------------------------------------------------------------+
```

### 2.2 Contract Table

| Property              | Threads (within one process)                                      | Processes (multiple processes)                                  |
|-----------------------|-------------------------------------------------------------------|-----------------------------------------------------------------|
| Memory                | Shared (same address space)                                       | Isolated (separate address spaces, copy-on-write)               |
| GIL                   | One per process → **at most one thread runs Python bytecode**     | One per process → fully independent interpreters                |
| CPU parallelism       | No for Python bytecode; **yes if C extensions release the GIL**   | Yes across processes (each process has its own GIL and can run on a different core) |
| Startup cost          | Microseconds                                                      | Milliseconds                                                    |
| Data sharing          | Direct (globals, objects) – fast but risky                        | Explicit (queues, pipes, shared memory)                         |
| Crash isolation       | Whole process dies                                                | One process dies → others survive                               |
| Best for              | I/O-bound, waiting, overlapping tasks                             | CPU-bound, heavy computation                                    |

---

## 3. Anti-Pattern First: “If your threads are busy thinking, you are probably wrong.”

### Example 1 – Threads Doing CPU Work (Anti-Pattern)

```python
# Example 1: CPU-bound work on threads → usually no speedup
from threading import Thread
import time

def cpu_task(n: int) -> None:
    total = 0
    for i in range(n):
        total += i * i

def run_with_threads(worker_count: int, n: int) -> float:
    threads = [Thread(target=cpu_task, args=(n,)) for _ in range(worker_count)]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start

if __name__ == "__main__":
    duration = run_with_threads(worker_count=4, n=10**7)
    print(f"4 threads (CPU-bound) took {duration:.2f} s")
```

**What to observe:**  
Typically 2–4× the single-thread time (or worse). The GIL serializes everything.

---

## 4. Correct Pattern: Processes on CPU-Bound Work

### Example 2 – Processes Doing CPU Work (Correct)

```python
# Example 2: CPU-bound work on processes → real multi-core scaling
from multiprocessing import Process
import time

def cpu_task(n: int) -> None:
    total = 0
    for i in range(n):
        total += i * i

def run_with_processes(worker_count: int, n: int) -> float:
    processes = [Process(target=cpu_task, args=(n,)) for _ in range(worker_count)]
    start = time.perf_counter()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    return time.perf_counter() - start

if __name__ == "__main__":
    duration = run_with_processes(worker_count=4, n=10**7)
    print(f"4 processes (CPU-bound) took {duration:.2f} s")
```

**What to observe:**  
Typically 3–4× faster than a single process on a 4+ core machine.

---

## 5. Correct Pattern: Threads on I/O-Bound Work

### Example 3 – Sequential I/O vs Threads

```python
# Example 3: I/O-bound work – sequential vs threads
from threading import Thread
import time

def io_task(delay: float) -> None:
    time.sleep(delay)  # Simulate slow I/O

def run_sequential(count: int, delay: float) -> float:
    start = time.perf_counter()
    for _ in range(count):
        io_task(delay)
    return time.perf_counter() - start

def run_threads(count: int, delay: float) -> float:
    threads = [Thread(target=io_task, args=(delay,)) for _ in range(count)]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start

if __name__ == "__main__":
    seq = run_sequential(count=5, delay=0.5)
    thr = run_threads(count=5, delay=0.5)
    print(f"Sequential: {seq:.2f} s, threads: {thr:.2f} s")
```

**What to observe:**  
Sequential ≈ count × delay. Threads ≈ delay. I/O releases the GIL → true overlap.

---

## 6. Consequence of the Decision: Sharing Memory is Easy, Sharing it Correctly is Not

**This section is not about *which* you should choose, but about what you get once you’ve chosen: what “shared memory vs isolated memory” actually looks like.**

### Example 4 – Threads Share Globals

```python
# Example 4: Threads see the same global variable
from threading import Thread

counter = 0

def increment():
    global counter
    counter += 1

if __name__ == "__main__":
    threads = [Thread(target=increment) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(counter)  # → 3
```

### Example 5 – Processes Do Not Share Globals

```python
# Example 5: Processes do NOT share globals
from multiprocessing import Process

counter = 0

def set_counter():
    global counter
    counter = 42

if __name__ == "__main__":
    p = Process(target=set_counter)
    p.start()
    p.join()
    print(counter)  # → 0
```

---

## 7. GIL in One Sentence

> In CPython, the GIL ensures that **at most one thread executes Python bytecode at a time per process**.

### Example 6 – GIL Hog

```python
# Example 6: One thread hogs the GIL, starving others
# WARNING: This will peg one CPU core at 100% — run only briefly!
from threading import Thread
import time

def hog():
    while True:
        pass  # Never releases GIL

def reporter():
    while True:
        print("Still alive...")
        time.sleep(1)

if __name__ == "__main__":
    Thread(target=hog, daemon=True).start()
    Thread(target=reporter, daemon=True).start()
    time.sleep(5)
```

**What to observe:**  
Reporter may print rarely or never.

---

## 8. Cost Model: Parallelism is Not Free

### Example 7 – Tiny Tasks (Overhead Dominates)

```python
# Example 7: Overhead dominates trivial work
import time
from multiprocessing import Process

def tiny():
    sum(range(1000))

if __name__ == "__main__":
    processes = [Process(target=tiny) for _ in range(50)]
    start = time.perf_counter()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    duration = time.perf_counter() - start
    print(f"50 tiny tasks took {duration:.3f} s")
```

**Key point:** Processes are expensive. Only use them when work >> startup cost.

---

## 9. Practical Design Recipe: “If it waits, thread it. If it sweats, fork it. If you’re not sure, measure.”

```text
1. Classify workload
   - Waiting a lot? → I/O-bound → threads / asyncio
   - Crunching numbers? → CPU-bound → processes

2. Pick primitive
   - threads → ThreadPoolExecutor
   - processes → ProcessPoolExecutor

3. Granularity check
   - Task < few ms? → stay sequential

4. Benchmark (Example 30 template)

5. Robustness
   - Need crash isolation? → processes

6. Refine with queues / shared memory only if truly needed
```

---

## 10. API Survey

Raw `threading.Thread` and `multiprocessing.Process` are useful for demos and special cases,  
but in real code **prefer the executor APIs**; they handle pools, shutdown, and error propagation.

| API                               | Use Case                              | Modern? |
|-----------------------------------|---------------------------------------|---------|
| `concurrent.futures.ThreadPoolExecutor` | I/O-bound, map-style                | Yes     |
| `concurrent.futures.ProcessPoolExecutor` | CPU-bound, map-style               | Yes     |

---

## 11. Worked Examples (1–30)

### Example 8 – Minimal Hello

```python
# Example 8: Hello from thread vs process
from threading import Thread
from multiprocessing import Process

def say_hello(label: str) -> None:
    print(f"Hello from {label}")

if __name__ == "__main__":
    t = Thread(target=say_hello, args=("thread",))
    t.start()
    t.join()

    p = Process(target=say_hello, args=("process",))
    p.start()
    p.join()
```

### Example 9 – Thread Race

```python
# Example 9: Race condition (shared counter)
from threading import Thread

counter = 0
def inc(n: int):
    global counter
    for _ in range(n):
        counter += 1

if __name__ == "__main__":
    threads = [Thread(target=inc, args=(100_000,)) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"Expected 400000, got {counter}")  # Often <400000
```

### Example 10 – Fixed with Lock

```python
# Example 10: Thread-safe counter
from threading import Thread, Lock

counter = 0
lock = Lock()

def inc(n: int):
    global counter
    for _ in range(n):
        with lock:
            counter += 1

if __name__ == "__main__":
    threads = [Thread(target=inc, args=(100_000,)) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(counter)  # → 400000
```

### Example 11 – Shared Counter with Processes via Value

```python
# Example 11: Shared counter for processes
from multiprocessing import Process, Value

def inc(shared: Value, n: int):
    for _ in range(n):
        with shared.get_lock():
            shared.value += 1

if __name__ == "__main__":
    counter = Value('i', 0)
    procs = [Process(target=inc, args=(counter, 100_000)) for _ in range(4)]
    for p in procs: p.start()
    for p in procs: p.join()
    print(counter.value)  # → 400000
```

### Example 12 – Process Queue

```python
# Example 12: Producer-consumer with Queue
from multiprocessing import Process, Queue

def producer(q: Queue):
    for i in range(5):
        q.put(f"item-{i}")
    q.put(None)

def consumer(q: Queue):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Consumed {item}")

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))
    p1.start(); p2.start()
    p1.join(); p2.join()
```

### Example 13 – ThreadPoolExecutor I/O

```python
# Example 13: ThreadPoolExecutor for I/O
import time
from concurrent.futures import ThreadPoolExecutor

def io_task(i: int) -> str:
    time.sleep(0.2)
    return f"done-{i}"

if __name__ == "__main__":
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=10) as exe:
        results = list(exe.map(io_task, range(20)))
    print(f"20 tasks in {time.perf_counter() - start:.2f} s")
```

### Example 14 – ProcessPoolExecutor CPU

```python
# Example 14: ProcessPoolExecutor for CPU
from concurrent.futures import ProcessPoolExecutor

def cpu_task(i: int) -> int:
    total = 0
    for n in range(2_000_000):
        total += n * n
    return total

if __name__ == "__main__":
    with ProcessPoolExecutor() as exe:
        results = list(exe.map(cpu_task, range(8)))
    print(f"8 tasks finished")
```

### Example 15 – Pickle Error (Local Function)

```python
# Example 15: Local function → pickle error on spawn
from multiprocessing import Process

def make_process():
    def inner():
        print("Hello")
    p = Process(target=inner)
    p.start()
    p.join()

if __name__ == "__main__":
    try:
        make_process()
    except Exception as e:
        print("Error:", e)
```

### Example 16 – Fixed Top-Level

```python
# Example 16: Top-level function → works everywhere
from multiprocessing import Process

def inner():
    print("Hello from top-level")

if __name__ == "__main__":
    p = Process(target=inner)
    p.start()
    p.join()
```

### Example 17 – Thread-Local Storage

```python
# Example 17: Thread-local data
from threading import Thread, local

tls = local()

def worker(i: int):
    tls.value = i
    print(f"Thread {i} stored {tls.value}")

if __name__ == "__main__":
    threads = [Thread(target=worker, args=(i,)) for i in range(3)]
    for t in threads: t.start()
    for t in threads: t.join()
```

### Example 18 – Manager Shared Dict (advanced, correctness over performance)

```python
# Example 18: Shared dict via Manager
from multiprocessing import Process, Manager

def worker(d, k, v):
    d[k] = v

if __name__ == "__main__":
    with Manager() as m:
        d = m.dict()
        procs = [Process(target=worker, args=(d, i, i*i)) for i in range(5)]
        for p in procs: p.start()
        for p in procs: p.join()
        print(d)
```

### Example 19 – Startup Cost (Platform-Safe)

```python
# Example 19: Startup cost comparison (safe, script-oriented)
import time
import timeit
from threading import Thread
from multiprocessing import Process

def noop():
    pass

if __name__ == "__main__":
    # NOTE: This assumes the file is executed as __main__ (script, not imported).
    # Thread startup: use timeit
    thread_time = timeit.timeit(
        "t = Thread(target=noop); t.start(); t.join()",
        setup="from threading import Thread; from __main__ import noop",
        number=1000,
    )

    # Process startup: manual loop
    start = time.perf_counter()
    for _ in range(100):
        p = Process(target=noop)
        p.start()
        p.join()
    process_time = (time.perf_counter() - start) / 100

    print(f"Thread avg:  {thread_time / 1000:.6f} s")
    print(f"Process avg: {process_time:.6f} s")
```

### Example 20 – Sequential Wins Tiny Tasks

```python
# Example 20: Sequential faster for tiny work
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def tiny(_):
    total = 0
    for i in range(1000):
        total += i
    return total

def bench(label, fn):
    start = time.perf_counter()
    fn()
    print(f"{label}: {time.perf_counter() - start:.4f} s")

if __name__ == "__main__":
    n = 100

    bench("Sequential", lambda: [tiny(i) for i in range(n)])

    def threads_run():
        with ThreadPoolExecutor() as exe:
            list(exe.map(tiny, range(n)))

    def processes_run():
        with ProcessPoolExecutor() as exe:
            list(exe.map(tiny, range(n)))

    bench("Threads", threads_run)
    bench("Processes", processes_run)
```

### Example 21 – Daemon Threads

```python
# Example 21: Daemon thread dies with main
from threading import Thread
import time

def bg():
    while True:
        print("Background...")
        time.sleep(1)

if __name__ == "__main__":
    Thread(target=bg, daemon=True).start()
    time.sleep(2)
    print("Main exits → daemon killed")
```

### Example 22 – Start Methods (advanced, platform behaviour)

```python
# Example 22: Explicit start method
import multiprocessing as mp

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    print("Start method:", mp.get_start_method())
```

### Example 23 – Two-Stage Pipeline

```python
# Example 23: Threads → I/O, Processes → CPU
from threading import Thread
from multiprocessing import Process, Queue
import time

def producer(q: Queue, count: int):
    for i in range(count):
        time.sleep(0.1)
        q.put(i)
    q.put(None)

def cpu_worker(q: Queue):
    while True:
        item = q.get()
        if item is None:
            break
        total = sum(j*j for j in range(200_000))
        print(f"Processed {item}")

if __name__ == "__main__":
    q = Queue()
    t = Thread(target=producer, args=(q, 5))
    p = Process(target=cpu_worker, args=(q,))
    t.start(); p.start()
    t.join()   # producer finished → sentinel definitely queued
    p.join()   # worker will exit after consuming sentinel
    # NOTE: For multiple CPU workers you would need one sentinel per worker.
```

### Example 24 – Affinity (Linux-only, advanced tuning)

```python
# Example 24: Pin to cores (Linux-only)
import os

if hasattr(os, "sched_setaffinity"):
    os.sched_setaffinity(0, {0, 1})
    print("Pinned to cores 0-1")
else:
    print("Affinity not available")
```

### Example 25 – Many I/O Tasks

```python
# Example 25: 100 concurrent sleeps
from concurrent.futures import ThreadPoolExecutor
import time

def io_task(i: int):
    time.sleep(0.05)
    return i

if __name__ == "__main__":
    with ThreadPoolExecutor(50) as exe:
        results = list(exe.map(io_task, range(100)))
    print("100 tasks done")
```

### Example 26 – Many CPU Tasks

```python
# Example 26: 8 heavy CPU tasks
from concurrent.futures import ProcessPoolExecutor

def cpu_task(i: int):
    total = 0
    for n in range(300_000):
        total += n * n
    return total

if __name__ == "__main__":
    with ProcessPoolExecutor() as exe:
        results = list(exe.map(cpu_task, range(8)))
    print("8 tasks done")
```

### Example 27 – NumPy Releases GIL

```python
# Example 27: Threads scale with NumPy
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time

def heavy(_):
    a = np.random.rand(2000, 2000)
    return (a @ a)[0, 0]

if __name__ == "__main__":
    start = time.perf_counter()
    with ThreadPoolExecutor() as exe:
        list(exe.map(heavy, range(4)))
    print(f"NumPy threads took {time.perf_counter() - start:.2f} s")
```

### Example 28 – Too Many Processes

```python
# Example 28: Resource exhaustion demo (keep N small)
from multiprocessing import Process

def work():
    sum(range(100_000))

if __name__ == "__main__":
    N = 100
    # WARNING: Increasing N too far can exhaust OS resources (fd limit, process limit).
    procs = [Process(target=work) for _ in range(N)]
    for p in procs: p.start()
    for p in procs: p.join()
```

### Example 29 – SharedMemory (advanced, zero-copy, Python 3.8+)

```python
# Example 29: Zero-copy large array sharing
from multiprocessing import Process, shared_memory
import numpy as np

def worker(shm_name: str) -> None:
    shm = shared_memory.SharedMemory(name=shm_name)
    arr = np.ndarray((1000, 1000), dtype=np.float64, buffer=shm.buf)
    arr[:] = 42.0
    shm.close()

if __name__ == "__main__":
    shm = shared_memory.SharedMemory(create=True, size=8_000_000)  # 1000*1000*8 bytes
    arr = np.ndarray((1000, 1000), dtype=np.float64, buffer=shm.buf)
    arr.fill(0.0)

    p = Process(target=worker, args=(shm.name,))
    p.start(); p.join()

    print(arr[0, 0])  # → 42.0
    shm.close(); shm.unlink()
```

### Example 30 – Universal Benchmark Template

```python
# Example 30: Copy-paste this for every new project
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def benchmark(fn, label: str, workers: int, tasks: int, executor_cls):
    start = time.perf_counter()
    with executor_cls(max_workers=workers) as exe:
        list(exe.map(fn, range(tasks)))
    print(f"{label}: {time.perf_counter() - start:.2f} s")

if __name__ == "__main__":
    def cpu(_):
        total = 0
        for i in range(500_000):
            total += i * i
        return total

    def io(_):
        time.sleep(0.05)

    print("CPU-bound")
    benchmark(cpu, "Threads   ", 4, 8, ThreadPoolExecutor)
    benchmark(cpu, "Processes ", 4, 8, ProcessPoolExecutor)

    print("\nI/O-bound")
    benchmark(io, "Threads   ", 20, 40, ThreadPoolExecutor)
    benchmark(io, "Processes ", 20, 40, ProcessPoolExecutor)
```

---

## 12. Pre-Core Quiz

1. Threads share globals? → Yes  
2. Threads run Python bytecode in parallel? → No (unless C extensions release GIL)  
3. Processes bypass each other’s GIL? → Yes  
4. Pure Python CPU task first choice? → Processes  
5. Thousands of HTTP requests? → Threads or asyncio  

## 13. Post-Core Reflection

Open your codebase. Find one I/O loop, one CPU loop. Replace with correct primitive. Run Example 30. Did you beat sequential?

You now own the single most important decision in Python parallelism.

**Next:** Core 2 – GIL Deep Dive & Real-World Workarounds.
