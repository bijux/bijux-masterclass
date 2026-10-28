# Core 4: Multiprocessing Fundamentals – Processes, Pools, Shared Memory

> **Core question:**  
> How do you spawn isolated processes, distribute CPU-bound tasks across cores with pools, and share data safely without pickling everything to death?

In **Core 1** you learned *when* to choose processes for CPU-bound work.  
In **Core 2** you learned *why* the GIL forces that choice.  
In **Core 3** you mastered safe threading for I/O.  
Here in **Core 4** you learn *how* to use multiprocessing correctly: spawning processes, using pools efficiently, and sharing memory without falling into the classic pitfalls.

**Audience:** Developers who know “processes → CPU” but have never written multiprocessing code that:
- works reliably on Windows/macOS (spawn),
- scales on Linux (fork),
- and doesn’t randomly hang or explode with pickling errors.

**Outcome:** After this file, you should:
1. Spawn processes and pools correctly in < 10 lines, with proper `if __name__ == "__main__":` guards.
2. Explain in one sentence why the import guard prevents infinite child-process recursion.
3. Use `Pool` for map-style CPU tasks and `shared_memory` for large arrays without thinking.
4. Spot and fix the three most common multiprocessing bugs in code review:
   - Missing import guard (infinite spawn on Windows/macOS)
   - Unpicklable targets / lambdas / closures
   - Assuming globals are shared (copy-on-write + isolation surprises)

---

## 1. Historical & Conceptual Backbone

### 1.1 History in 5 Lines

- Python 2.6 (2008): `multiprocessing` module added to bypass the GIL using real OS processes.
- 2009+: `multiprocessing.Pool` becomes the standard for parallel `map`.
- 2010s: `Manager`, `Value`, `Array` added for shared state; `concurrent.futures.ProcessPoolExecutor` wraps it.
- Python 3.8 (2019): `multiprocessing.shared_memory` introduces zero-copy shared buffers.
- November 2025: `multiprocessing` remains the **gold standard** for CPU parallelism; executors are preferred for simple patterns.

**This entire core focuses on low-level `multiprocessing`.**  
Executors and frameworks (joblib, dask, Ray, etc.) build on these primitives.

### 1.2 Multiprocessing in One Precise Sentence

> The `multiprocessing` module spawns separate Python interpreters as OS processes, distributes work via pools, and shares data only through explicit IPC or shared memory.

### 1.3 The One-Sentence Rule

> **If it computes, fork it (or spawn it) with multiprocessing. Guard your imports. Put worker functions at top level. Share only what you must.**

Everything else in this core is a justification and elaboration of that rule.

### 1.4 Positioning of `concurrent.futures`

`concurrent.futures.ProcessPoolExecutor` is a **higher-level wrapper**:
- Uses `multiprocessing` under the hood.
- Hides:
  - process creation / joining
  - chunking for `map`
  - error propagation and shutdown
- Use it when:
  - your pattern is “map function over many inputs”,
  - you don’t need `shared_memory`, custom queues, or start-method tricks.
- Drop to raw `multiprocessing` when:
  - you need zero-copy shared arrays,
  - custom start methods (`spawn`, `forkserver`),
  - or complex pipelines with `Queue` / `Pipe`.

For this core: **master `multiprocessing` first**. Executors will then feel like a thin convenience layer.

---

## 2. Mental Model: Processes, Pools, Shared Memory

### 2.1 One Picture

```text
Main Process (Python Interpreter #1)
+------------------------------------------------------------+
|  Its own memory, its own GIL, its own globals              |
|                                                            |
|   [ Process 1 ]   [ Process 2 ]   [ Process 3 ]   [ Process 4 ]
|    (Python #2)     (Python #3)     (Python #4)     (Python #5)
|       |                |                |                |
|       v                v                v                v
|   Separate address spaces: no implicit shared objects     |
|                                                            |
|                 Pool: task distribution                    |
|    main → submit work → [ Pool of workers ] → collect results
|                                                            |
|         Shared Memory (Value / Array / SharedMemory)       |
|    main <------ explicit shared region ------> workers     |
+------------------------------------------------------------+

- Threads share memory by default.
- Processes are isolated by default.
- Sharing in multiprocessing is explicit and usually more expensive.
```

### 2.2 Contract Table

| Primitive                                  | Purpose                                  | Isolated? | Overhead                     | Typical Use                           |
| ------------------------------------------ | ---------------------------------------- | --------- | ---------------------------- | ------------------------------------- |
| `Process`                                  | Spawn a single OS process                | Yes       | High (startup)               | Fire-and-forget tasks, custom workers |
| `Pool` / `ProcessPool`                     | Fixed worker pool + automatic map        | Yes       | Medium (reused)              | Parallel map/reduce                   |
| `Value` / `Array`                          | Shared primitive / fixed-size buffer     | Shared    | Low                          | Counters, small arrays                |
| `Manager`                                  | Shared Python objects via proxy          | Shared    | High (IPC per op)            | Complex shared dict/list (rare)       |
| `shared_memory`                            | Zero-copy large buffers (NumPy-friendly) | Shared    | Low                          | Large arrays, ML tensors              |
| `Queue` / `Pipe`                           | Message passing between processes        | IPC       | Medium                       | Producer–consumer pipelines           |
| Start method (`spawn`/`fork`/`forkserver`) | How processes are created                | N/A       | N/A                          | Platform behavior + safety trade-offs |

---

## 3. Anti-Pattern First: “If it computes, fork it — but without guards, it will fork itself to death.”

### Example 1 – No Import Guard (Anti-Pattern)

```python
# Example 1: Missing guard → infinite recursion on spawn platforms
from multiprocessing import Process

def worker():
    print("Worker running")

# BAD: this runs at import time in both parent and child
p = Process(target=worker)
p.start()
p.join()
```

**What happens:**

* On **spawn** platforms (Windows/macOS, default Python 3.8+ even on some Linuxes with explicit spawn):

  * Child imports your module.
  * Top-level code runs again.
  * New `Process` is created.
  * Repeat → infinite chain of processes until your machine melts.

---

## 4. Correct Pattern: Always Guard with `if __name__ == "__main__":`

### Example 2 – Proper Process Spawn with Guard

```python
# Example 2: Safe process spawn (works on all platforms)
from multiprocessing import Process

def worker():
    print("Worker running")

if __name__ == "__main__":
    p = Process(target=worker)
    p.start()
    p.join()
    print("Done")
```

**Why this works (one sentence):** child processes import the module but do **not** run the guarded main block, so you don’t respawn processes recursively.

---

## 5. Correct Pattern: Use `Pool` for CPU Map-Style Tasks

### Example 3 – Parallel Map with `Pool`

```python
# Example 3: Pool for CPU-bound map
from multiprocessing import Pool

def square(x: int) -> int:
    total = 0
    for i in range(200_000):
        total += i * x
    return total

if __name__ == "__main__":
    with Pool() as pool:  # pool size = #cores by default
        results = pool.map(square, range(8))
    print("Got", len(results), "results")
```

**What to observe:**

* One `Pool` instance → many tasks → workers reused.
* Near-linear speedup on a multi-core machine for CPU-heavy work.

---

## 6. Consequence: Isolation Is Safety; Sharing Is Explicit and Costs You

**This section is about what you get once you choose processes: strong isolation, and explicit sharing.**

### Example 4 – Globals Are Not Shared

```python
# Example 4: Child modifies global; parent does NOT see it
from multiprocessing import Process

counter = 0

def child():
    global counter
    counter += 1
    print("Child sees counter =", counter)

if __name__ == "__main__":
    print("Parent before:", counter)
    p = Process(target=child)
    p.start()
    p.join()
    print("Parent after :", counter)  # Still 0
```

**Takeaway:**

* Each process has its **own copy** of globals.
* It doesn’t matter whether the OS used fork or spawn – parent never sees child writes.

### Example 5 – Use `shared_memory` for True Zero-Copy (NumPy)

```python
# Example 5: Zero-copy with shared_memory (Python 3.8+)
from multiprocessing import Process, shared_memory
import numpy as np

def worker(shm_name: str) -> None:
    shm = shared_memory.SharedMemory(name=shm_name)
    arr = np.ndarray((1000, 1000), dtype=np.float64, buffer=shm.buf)
    arr[0, 0] = 42.0
    shm.close()

if __name__ == "__main__":
    # 1000 * 1000 * 8 bytes = 8 MB
    shm = shared_memory.SharedMemory(create=True, size=8_000_000)
    arr = np.ndarray((1000, 1000), dtype=np.float64, buffer=shm.buf)
    arr.fill(0.0)

    p = Process(target=worker, args=(shm.name,))
    p.start()
    p.join()

    print(arr[0, 0])  # → 42.0 (child wrote into shared buffer)
    shm.close()
    shm.unlink()
```

**Takeaway:**

* SharedMemory lets **multiple processes** read/write the same bytes.
* No pickling of the array, no per-process copies.

---

## 7. Multiprocessing Fundamentals in One Sentence

> Use `Process` for custom workers, `Pool` for map-style CPU parallelism, and explicit shared memory (Value/Array/shared_memory) when you truly need processes to see the same data.

### Example 6 – Lambdas / Closures Are Not Picklable Workers

```python
# Example 6: Lambda not picklable on spawn platforms
from multiprocessing import Pool

if __name__ == "__main__":
    try:
        with Pool() as pool:
            pool.map(lambda x: x * x, range(10))  # BAD
    except Exception as e:
        print("Expected pickling error on spawn platforms:")
        print(e)
```

**Takeaway:**
Worker functions and Pool targets must be **top-level** (`def` at module level), not lambdas, not nested defs, not closures capturing outer variables.

---

## 8. Cost Model: Processes Are Powerful but Expensive

True parallelism costs you:

* Process startup (milliseconds).
* Pickling arguments/results.
* Memory overhead per process (stacks, heaps).
* Potential CoW duplication of big globals.

### Example 7 – Raw Processes vs `Pool` Reuse

```python
# Example 7: Pool reuses workers → faster for many tasks
import time
from multiprocessing import Process, Pool

def tiny(_):
    # tiny CPU task
    return 42

if __name__ == "__main__":
    # Raw processes: one process per task
    start = time.perf_counter()
    procs = [Process(target=tiny, args=(i,)) for i in range(200)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(f"200 raw processes: {time.perf_counter() - start:.3f} s")

    # Pool: reuse 8 workers
    start = time.perf_counter()
    with Pool(8) as pool:
        list(pool.map(tiny, range(200)))
    print(f"Pool 200 tasks: {time.perf_counter() - start:.3f} s")
```

**Key point:**
Raw processes are fine for a few big tasks. For many small tasks → **always use a pool**.

---

## 9. Practical Design Recipe: “If it computes, fork it. Guard, top-level, then pool.”

```text
1. Start from Core 1:
   - I/O-bound? → threads (Core 3)
   - CPU-bound? → multiprocessing (this core)

2. Always:
   - Put process-spawning code under:
       if __name__ == "__main__":
           ...
   - Define worker functions at module top level.

3. Prefer pools over raw processes:
   - Pool.map / starmap for simple fan-out/fan-in CPU tasks.
   - Adjust chunksize for many small tasks.

4. Share memory only when it measurably pays off:
   - Use Value / Array for simple numeric state.
   - Use shared_memory for large contiguous arrays (NumPy).
   - Avoid Manager unless you truly need shared Python objects.

5. Avoid:
   - Lambdas / nested functions / closures as worker targets.
   - Very large globals that each worker copies (measure!).
   - Nested multiprocessing (pool inside a worker).

6. Benchmark:
   - Use Example 30 to compare sequential vs Pool vs shared memory.
```

---

## 10. API Survey

Core primitives:

| API                               | Purpose                           | Modern Alternative             |
| --------------------------------- | --------------------------------- | ------------------------------ |
| `multiprocessing.Process`         | Single process spawn              | —                              |
| `multiprocessing.Pool`            | Fixed worker pool + map           | `ProcessPoolExecutor`          |
| `multiprocessing.Value` / `Array` | Shared C-style primitives/buffers | `shared_memory` for big arrays |
| `multiprocessing.Manager`         | Shared Python objects via proxies | Avoid if performance-critical  |
| `multiprocessing.shared_memory`   | Zero-copy byte buffers (3.8+)     | —                              |
| `multiprocessing.Queue` / `Pipe`  | Inter-process message passing     | —                              |

---

## 11. Worked Examples (1–30)

All runnable, guarded, no unpicklable worker functions.

### Example 8 – Minimal Process Spawn

```python
# Example 8: Hello from process
from multiprocessing import Process

def hello() -> None:
    print("Hello from process")

if __name__ == "__main__":
    p = Process(target=hello)
    p.start()
    p.join()
```

### Example 9 – Process Join with Timeout

```python
# Example 9: Process join with timeout
from multiprocessing import Process
import time

def sleep_forever() -> None:
    time.sleep(100)

if __name__ == "__main__":
    p = Process(target=sleep_forever)
    p.start()
    p.join(timeout=1.0)
    if p.is_alive():
        p.terminate()
        p.join()
        print("Process timed out and was terminated")
```

### Example 10 – Daemon Processes (Use Sparingly)

```python
# Example 10: Daemon processes die with main
from multiprocessing import Process
import time

def background() -> None:
    while True:
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=background, daemon=True)
    p.start()
    time.sleep(2)
    print("Main exits → daemon killed")
```

### Example 11 – Pool with `chunksize`

```python
# Example 11: Pool chunksize to reduce overhead
from multiprocessing import Pool

def square(x: int) -> int:
    return x * x

if __name__ == "__main__":
    with Pool() as pool:
        results = pool.map(square, range(1000), chunksize=50)
    print(results[:5])
```

### Example 12 – `starmap` for Multiple Args

```python
# Example 12: starmap for (x, y) tuples
from multiprocessing import Pool

def add(x: int, y: int) -> int:
    return x + y

if __name__ == "__main__":
    pairs = [(i, i * 2) for i in range(10)]
    with Pool() as pool:
        results = pool.starmap(add, pairs)
    print(results[:5])
```

### Example 13 – Shared `Value` Counter

```python
# Example 13: Shared Value with lock
from multiprocessing import Process, Value

def inc(counter: Value) -> None:
    with counter.get_lock():
        counter.value += 1

if __name__ == "__main__":
    v = Value('i', 0)
    procs = [Process(target=inc, args=(v,)) for _ in range(100)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(v.value)  # → 100
```

### Example 14 – Shared `Array` Buffer

```python
# Example 14: Shared Array across processes
from multiprocessing import Process, Array

def double(arr: Array) -> None:
    for i in range(len(arr)):
        arr[i] *= 2

if __name__ == "__main__":
    arr = Array('i', range(10))  # [0,1,2,...,9]
    p = Process(target=double, args=(arr,))
    p.start()
    p.join()
    print(list(arr))  # [0,2,4,...,18]
```

### Example 15 – Manager for Python Objects (Slow but Easy)

```python
# Example 15: Manager dict (correct but slow)
from multiprocessing import Process, Manager

def update(d) -> None:
    d["count"] += 1

if __name__ == "__main__":
    with Manager() as m:
        d = m.dict(count=0)
        procs = [Process(target=update, args=(d,)) for _ in range(100)]
        for p in procs:
            p.start()
        for p in procs:
            p.join()
        print(d["count"])  # → 100
```

### Example 16 – `multiprocessing.Queue`

```python
# Example 16: multiprocessing.Queue for IPC
from multiprocessing import Process, Queue

def producer(q: Queue) -> None:
    q.put("data")

def consumer(q: Queue) -> None:
    item = q.get()
    print("Got:", item)

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
```

### Example 17 – `Pipe` for Simple Two-Way Communication

```python
# Example 17: Pipe (two endpoints)
from multiprocessing import Process, Pipe

def child(conn) -> None:
    conn.send("hello from child")
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p = Process(target=child, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()
```

### Example 18 – Start Methods (spawn / fork / forkserver)

```python
# Example 18: Explicit start method (advanced)
import multiprocessing as mp

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    print("Start method:", mp.get_start_method())
```

### Example 19 – Pool `initializer` for Per-Worker Setup

```python
# Example 19: Pool initializer for setup
from multiprocessing import Pool

def init_worker():
    print("Worker initialized")

def work(x: int) -> int:
    return x * 2

if __name__ == "__main__":
    with Pool(initializer=init_worker) as pool:
        results = pool.map(work, range(4))
    print(results)
```

### Example 20 – `shared_memory` with Small NumPy Array

```python
# Example 20: Zero-copy NumPy array
from multiprocessing import Process, shared_memory
import numpy as np

def worker(shm_name: str) -> None:
    shm = shared_memory.SharedMemory(name=shm_name)
    arr = np.ndarray((10,), dtype=np.int64, buffer=shm.buf)
    arr[:] *= 2
    shm.close()

if __name__ == "__main__":
    shm = shared_memory.SharedMemory(create=True, size=10 * 8)
    arr = np.ndarray((10,), dtype=np.int64, buffer=shm.buf)
    arr.fill(1)

    p = Process(target=worker, args=(shm.name,))
    p.start()
    p.join()

    print(arr)  # [2 2 ... 2]
    shm.close()
    shm.unlink()
```

### Example 21 – Process Name and PID

```python
# Example 21: Process identification
from multiprocessing import Process, current_process

def worker() -> None:
    proc = current_process()
    print(f"Name: {proc.name}, PID: {proc.pid}")

if __name__ == "__main__":
    p = Process(target=worker, name="WorkerProc")
    p.start()
    p.join()
```

### Example 22 – Exceptions Propagate Out of `Pool`

```python
# Example 22: Pool propagates exceptions
from multiprocessing import Pool

def buggy(_) -> int:
    raise ValueError("Oops in worker")

if __name__ == "__main__":
    try:
        with Pool() as pool:
            pool.map(buggy, range(1))
    except ValueError as e:
        print("Caught worker exception:", e)
```

### Example 23 – Two-Stage CPU Pipeline with Queues

```python
# Example 23: Processes + queues for CPU pipeline
from multiprocessing import Process, Queue

def stage1(out_q: Queue) -> None:
    for i in range(5):
        out_q.put(i)
    out_q.put(None)  # Sentinel

def stage2(in_q: Queue, out_q: Queue) -> None:
    while True:
        item = in_q.get()
        if item is None:
            out_q.put(None)
            break
        out_q.put(item * item)

def consumer(in_q: Queue) -> None:
    while True:
        item = in_q.get()
        if item is None:
            break
        print("Result", item)

if __name__ == "__main__":
    q1 = Queue()
    q2 = Queue()

    p1 = Process(target=stage1, args=(q1,))
    p2 = Process(target=stage2, args=(q1, q2))
    p3 = Process(target=consumer, args=(q2,))

    p1.start(); p2.start(); p3.start()
    p1.join(); p2.join(); p3.join()
```

### Example 24 – `maxtasksperchild` to Refresh Workers

```python
# Example 24: Refresh workers to avoid leaks
from multiprocessing import Pool

def work(x: int) -> int:
    return x * 2

if __name__ == "__main__":
    with Pool(maxtasksperchild=10) as pool:
        results = pool.map(work, range(50))
    print(len(results))
```

### Example 25 – Measuring Too Many Processes (Be Careful)

```python
# Example 25: Many processes → resource limits
from multiprocessing import Process

def work() -> None:
    pass

if __name__ == "__main__":
    N = 100
    procs = [Process(target=work) for _ in range(N)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print("Started and joined", N, "processes")
```

### Example 26 – `ProcessPoolExecutor` (Modern Wrapper)

```python
# Example 26: concurrent.futures.ProcessPoolExecutor
from concurrent.futures import ProcessPoolExecutor

def square(x: int) -> int:
    return x * x

if __name__ == "__main__":
    with ProcessPoolExecutor() as exe:
        results = list(exe.map(square, range(20)))
    print(results[:10])
```

### Example 27 – Simple Shared Counter with `Value` and Pool

```python
# Example 27: Shared Value with pool (advanced)
from multiprocessing import Pool, Value

_counter = None  # will be set in initializer

def init_counter(shared_counter):
    global _counter
    _counter = shared_counter

def increment(_):
    with _counter.get_lock():
        _counter.value += 1

if __name__ == "__main__":
    counter = Value('i', 0)
    with Pool(initializer=init_counter, initargs=(counter,)) as pool:
        pool.map(increment, range(100))
    print("Counter:", counter.value)  # → 100
```

### Example 28 – Shared ctypes Structure

```python
# Example 28: Custom shared struct
from multiprocessing import Process, RawArray
import ctypes

class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]

def modify(buf) -> None:
    pt = Point.from_buffer(buf)
    pt.x = 42.0

if __name__ == "__main__":
    buf = RawArray(ctypes.c_double, 2)
    pt = Point.from_buffer(buf)
    pt.x = 0.0
    pt.y = 0.0

    p = Process(target=modify, args=(buf,))
    p.start()
    p.join()

    print("Point.x =", pt.x)  # → 42.0
```

### Example 29 – Avoid Lambdas: Top-Level Worker with Pool

```python
# Example 29: Correct worker definition for Pool
from multiprocessing import Pool

def cube(x: int) -> int:
    return x * x * x

if __name__ == "__main__":
    with Pool() as pool:
        results = pool.map(cube, range(10))
    print(results)
```

### Example 30 – Universal Multiprocessing Benchmark Template

```python
# Example 30: Copy-paste to benchmark multiprocessing patterns
import time
from multiprocessing import Process, Pool
import math

def benchmark(name: str, fn) -> None:
    start = time.perf_counter()
    fn()
    print(f"{name}: {time.perf_counter() - start:.3f} s")

# Worker functions MUST be top-level:

def cpu_task(_) -> float:
    total = 0.0
    for i in range(200_000):
        total += math.sqrt(i)
    return total

def sequential() -> None:
    for _ in range(8):
        cpu_task(None)

def raw_processes() -> None:
    procs = [Process(target=cpu_task, args=(None,)) for _ in range(8)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

def pooled() -> None:
    with Pool(8) as pool:
        list(pool.map(cpu_task, range(8)))

if __name__ == "__main__":
    benchmark("Sequential", sequential)
    benchmark("Raw processes", raw_processes)
    benchmark("Pool", pooled)
```

---

## 12. Pre-Core Quiz

1. Need `if __name__ == "__main__":` guard when using `multiprocessing`? → Yes
2. Does `Pool` reuse worker processes? → Yes
3. Are lambdas / nested functions safe as Pool targets on Windows? → No
4. Does `shared_memory` give zero-copy access to the same bytes? → Yes
5. Should you use multiprocessing for tiny I/O-bound tasks? → No (use threads)

## 13. Post-Core Reflection

Open your codebase.

Find **one** CPU-bound loop currently running in threads or sequentially.

* Wrap the worker body in a **top-level** function.
* Add an `if __name__ == "__main__":` guard.
* Replace your loop with `ProcessPoolExecutor` or `multiprocessing.Pool.map`.

Measure. Did you get a >2× speedup on a 4+ core machine?

You now own **true CPU parallelism** in Python, safely, on all major platforms.

**Next:** Core 5 – Advanced Synchronization Primitives.
