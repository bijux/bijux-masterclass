# Core 6: Cost Models and Overheads for Threads and Processes

> **Core question:**  
> How much do threads and processes really cost in startup time, memory, context switches, and serialization — and how do you *measure* them before your “parallel” code mysteriously slows down?

In **Core 1** you learned *when* to choose threads vs processes.  
In **Core 2** you learned *why* the GIL limits threads for CPU.  
In **Core 3** you mastered safe threading.  
In **Core 4** you learned multiprocessing for CPU parallelism.  
In **Core 5** you learned synchronization primitives.  
Here in **Core 6** you learn the **real costs** of parallelism: time, memory, and hidden overheads — and how to benchmark them in every new project.

**Audience:** Developers who have working parallel code but wonder “why isn’t it faster?” or “why does it use so much memory?”

**Outcome:** After this file, you should:
1. Estimate overhead for any workload in < 10 seconds.
2. Explain in one sentence why 10,000 threads or processes is usually a bad idea.
3. Write a 20-line benchmark that reveals if parallelism helps or hurts.
4. Spot and fix the three most common overhead bugs in code review:
   - Spawning too many workers for tiny tasks
   - Pickling large objects on every task
   - Memory explosion from copy-on-write or shared memory misuse

---

## 1. Historical & Conceptual Backbone

### 1.1 History in 5 Lines

- 1990s: Python inherits OS-level costs for threads and processes; no magic.
- 2008: `multiprocessing` adds pools to amortize process startup.
- 2010s: `concurrent.futures` hides raw overhead; developers forget it still exists.
- Python 3.8+: `multiprocessing.shared_memory` reduces IPC overhead for large data.
- November 2025: Overhead bugs remain the #1 reason parallel Python fails to scale.

**This entire core focuses on measurable costs.**  
Always benchmark — never assume “more workers = faster”.

### 1.2 Cost Models in One Precise Sentence

> Threads are cheap to start but contend on the GIL; processes are expensive to start but truly parallel — both waste resources if tasks are too small or data too large.

### 1.3 The One-Sentence Rule

> **Measure first, parallelize second. Never spawn more workers than your task size justifies.**

Everything else in this core is a justification and elaboration of that rule.

### 1.4 Positioning of `concurrent.futures`

Executors hide overhead but don’t eliminate it:
- `ThreadPoolExecutor`: hides thread creation (~10–100 µs each).
- `ProcessPoolExecutor`: hides process startup (~10–50 ms each) and pickling.
- Use them for convenience — but understand the costs underneath.

For this core: **benchmark raw primitives** so you know what executors are hiding.

---

## 2. Mental Model: Costs of Parallelism

### 2.1 One Picture

```text
Cost Timeline for One Task
+-----------------------------------------------------------+
|  Sequential:  [ Task Work ]                               |
|                                                           |
|  Thread:      [ Thread Startup (~50 µs) ]                 |
|               [ Context Switch ] [ Task Work ]            |
|               [ GIL Contention ]                          |
|                                                           |
|  Process:     [ Process Startup (~20 ms) ]                |
|               [ Pickle Args/Results ]                     |
|               [ Task Work on separate core ]              |
|               [ Unpickle Results ]                        |
|                                                           |
|  Shared Memory: [ Setup Shared Buffer ]                    |
|                 [ Zero-copy access ]                       |
+-----------------------------------------------------------+

Startup + serialization often dominate for small tasks.
Work must be >> overhead for parallelism to win.
```

### 2.2 Contract Table

| Cost Type              | Threads                                  | Processes                                  | Mitigation                          |
|------------------------|------------------------------------------|--------------------------------------------|-------------------------------------|
| Startup time           | ~10–100 µs                               | ~5–50 ms                                   | Reuse with pools / executors        |
| Memory per worker      | ~1–8 MB (stack)                          | ~10–100 MB (full interpreter)              | Limit workers to CPU count          |
| Context switch         | ~1–10 µs                                 | ~100 µs + scheduler                        | Minimize contention                 |
| GIL contention         | High for CPU-bound                       | None (per-process GIL)                     | Use processes for CPU               |
| Serialization          | None (shared memory)                     | Pickle args/results (slow for big data)    | Use shared_memory / chunksize       |
| Copy-on-write (fork)   | N/A                                      | Duplicates large globals on write          | Avoid big globals; use spawn        |

---

## 3. Anti-Pattern First: “More workers = faster (until it isn’t).”

### Example 1 – Too Many Tiny Tasks (Anti-Pattern)

```python
# Example 1: 10,000 tiny processes → overhead dominates
import time
from multiprocessing import Process

def tiny():
    pass  # 0 work

if __name__ == "__main__":
    N = 200  # keep this small; 10_000 will hurt your machine
    start = time.perf_counter()
    procs = [Process(target=tiny) for _ in range(N)]
    for p in procs: p.start()
    for p in procs: p.join()
    print(f"{N} tiny processes: {time.perf_counter() - start:.3f} s")
```

**What to observe:**  
Even a few hundred processes can take noticeable time just to start and stop.

---

## 4. Correct Pattern: Reuse Workers with Pools

### Example 2 – Same Tiny Tasks with Pool (Correct)

```python
# Example 2: Pool reuses workers → fast even for many tasks
import time
from multiprocessing import Pool

def tiny(_):
    pass

if __name__ == "__main__":
    N = 10_000
    start = time.perf_counter()
    with Pool() as pool:
        list(pool.map(tiny, range(N)))
    print(f"Pool {N} tiny tasks: {time.perf_counter() - start:.3f} s")
```

**What to observe:**  
One pool startup + many tasks → much cheaper than 1 process per task.

---

## 5. Correct Pattern: Measure Before You Scale

### Example 3 – Universal Overhead Benchmark

```python
# Example 3: Measure your own overhead
import time
import timeit
from threading import Thread
from multiprocessing import Process

def noop():
    pass

if __name__ == "__main__":
    # Thread startup
    thread_time = timeit.timeit(
        "t = Thread(target=noop); t.start(); t.join()",
        setup="from threading import Thread; from __main__ import noop",
        number=500,
    )
    print(f"Thread startup avg: {thread_time / 500 * 1e6:.1f} µs")

    # Process startup
    start = time.perf_counter()
    for _ in range(50):
        p = Process(target=noop)
        p.start()
        p.join()
    process_time = (time.perf_counter() - start) / 50
    print(f"Process startup avg: {process_time * 1000:.1f} ms")
```

**What to observe:**  
Threads ~10–100 µs, processes ~5–50 ms. Your task must be larger than this.

---

## 6. Consequence: Serialization & Memory Kill Performance Fast

### Example 4 – Pickling Large Data Is Brutal

```python
# Example 4: Pickling a large object per task is expensive
import time
from multiprocessing import Pool

# ~50 MB string (adjust if needed)
big = "x" * 50_000_000

def identity(x):
    return x

if __name__ == "__main__":
    start = time.perf_counter()
    with Pool(2) as pool:
        # big is pickled once per task
        list(pool.map(identity, [big] * 4))
    print(f"4 tasks with 50 MB payload: {time.perf_counter() - start:.1f} s")
```

**What to observe:**  
You can easily spend seconds *just* serializing and deserializing.

---

### Example 5 – `shared_memory` Avoids Pickling

```python
# Example 5: shared_memory → zero-copy for large arrays (Python 3.8+)
from multiprocessing import Process, shared_memory
import numpy as np
import time

def modify(shm_name):
    shm = shared_memory.SharedMemory(name=shm_name)
    arr = np.ndarray((5_000, 5_000), dtype=np.float32, buffer=shm.buf)
    arr += 1.0
    shm.close()

if __name__ == "__main__":
    size_bytes = 5_000 * 5_000 * 4  # float32
    shm = shared_memory.SharedMemory(create=True, size=size_bytes)
    arr = np.ndarray((5_000, 5_000), dtype=np.float32, buffer=shm.buf)
    arr.fill(0.0)

    start = time.perf_counter()
    p = Process(target=modify, args=(shm.name,))
    p.start()
    p.join()
    print(f"Shared-memory modify: {time.perf_counter() - start:.3f} s")
    print("arr[0, 0] =", arr[0, 0])  # → 1.0

    shm.close()
    shm.unlink()
```

**Takeaway:**  
For big arrays, **don’t pickle** them per task → share them.

---

## 7. Cost Models in One Sentence

> Threads cost microseconds and stacks; processes cost milliseconds, pickling, and full interpreters — both can still lose to sequential if tasks are tiny or data is huge.

### Example 6 – Memory Blow-Up with Many Processes

```python
# Example 6: Large global + many processes = memory pressure
# Requires: pip install psutil
import time
import psutil
from multiprocessing import Process

big_global = "x" * 10_000_000  # ~10 MB

def worker():
    time.sleep(2)

if __name__ == "__main__":
    proc = psutil.Process()
    print(f"Parent RSS before: {proc.memory_info().rss / 1e6:.1f} MB")

    N = 10  # Do NOT make this huge; it's just a demo
    procs = [Process(target=worker) for _ in range(N)]
    for p in procs:
        p.start()
    time.sleep(1.0)  # let them start

    print(f"Parent RSS during ({N} processes): {proc.memory_info().rss / 1e6:.1f} MB")

    for p in procs:
        p.terminate()
    for p in procs:
        p.join()
```

On fork platforms, writes to big globals can cause **copy-on-write** duplication.
On spawn platforms, each process starts fresh and may allocate its own copy.

---

## 8. Break-Even: When Do Processes Beat Threads?

### Example 7 – Find Break-Even for Your Workload

```python
# Example 7: Where do processes beat threads?
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def work(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

def measure(executor_cls, workers, tasks, task_size):
    with executor_cls(max_workers=workers) as exe:
        start = time.perf_counter()
        list(exe.map(work, [task_size] * tasks))
        return time.perf_counter() - start

if __name__ == "__main__":
    for size in [10_4, 10_5, 10_6, 10_7]:
        threads_time = measure(ThreadPoolExecutor, 8, 8, size)
        procs_time   = measure(ProcessPoolExecutor, 8, 8, size)
        print(f"Task size {size:>7}: threads {threads_time:.3f}s, procs {procs_time:.3f}s")
```

> Rule of thumb: processes only win once each task is **tens of milliseconds or more** of CPU work.

---

## 9. Practical Design Recipe: “Measure first. Pool second. Share wisely.”

```text
1. Profile sequential baseline

2. Estimate overhead:
   - Thread startup ~50 µs
   - Process startup ~20 ms
   - Pickling 100 MB ~1–5 seconds

3. For threads:
   - Use ThreadPoolExecutor
   - Workers ≤ CPU count + 4 (I/O bound)

4. For processes:
   - Use ProcessPoolExecutor or Pool
   - Workers ≤ CPU count
   - chunksize for many small tasks

5. Share memory only when:
   - Data > 100 MB
   - Use shared_memory (zero-copy)

6. Always:
   - Use `if __name__ == "__main__":` for multiprocessing.
   - Keep worker functions at module top level (picklable).
   - Benchmark with templates (e.g. Example 30) on your machine.
```

---

## 10. API & Technique Cost Survey

| API / Technique                 | Overhead Profile                        | When to Use                                |
| ------------------------------- | --------------------------------------- | ------------------------------------------ |
| `threading.Thread`              | Low startup, GIL contention             | Custom I/O workers                         |
| `ThreadPoolExecutor`            | Low, reused threads                     | Simple I/O-bound `map`                     |
| `multiprocessing.Process`       | High startup, full isolation            | A few long-running CPU workers             |
| `multiprocessing.Pool`          | Medium startup, reused workers          | CPU `map` / `starmap`                      |
| `ProcessPoolExecutor`           | Like `Pool`, nicer API                  | Modern CPU-parallel code                   |
| `multiprocessing.shared_memory` | Low incremental cost, zero-copy         | Large arrays (NumPy, ML tensors)           |
| `multiprocessing.Manager`       | High IPC per access                     | Avoid — slow                               |

---

## 11. Worked Examples (1–30)

All runnable, multiprocessing guarded, and no unpicklable process targets.

We already saw Examples 1–7. Continuing from 8.

### Example 8 – Thread Creation vs Thread Pool Reuse

```python
# Example 8: Raw threads vs executor
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

def tiny():
    pass

if __name__ == "__main__":
    # Raw
    start = time.perf_counter()
    threads = [Thread(target=tiny) for _ in range(1000)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"1000 raw threads:      {time.perf_counter() - start:.3f} s")

    # Executor reuse
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=8) as exe:
        list(exe.map(lambda _: tiny(), range(1000)))
    print(f"ThreadPool 1000 tasks: {time.perf_counter() - start:.3f} s")
```

### Example 9 – Process Creation vs Pool Reuse

```python
# Example 9: Raw processes vs pool
import time
from multiprocessing import Process, Pool

def tiny():
    pass

def tiny_arg(_):
    tiny()

if __name__ == "__main__":
    # Raw
    start = time.perf_counter()
    procs = [Process(target=tiny) for _ in range(50)]
    for p in procs: p.start()
    for p in procs: p.join()
    print(f"50 raw processes: {time.perf_counter() - start:.3f} s")

    # Pool
    start = time.perf_counter()
    with Pool(8) as pool:
        list(pool.map(tiny_arg, range(200)))
    print(f"Pool 200 tasks:   {time.perf_counter() - start:.3f} s")
```

### Example 10 – Memory Per 100 Threads

```python
# Example 10: Memory growth with threads (requires psutil)
import time
import psutil
from threading import Thread

def sleeper():
    time.sleep(5)

if __name__ == "__main__":
    proc = psutil.Process()
    print(f"RSS before: {proc.memory_info().rss / 1e6:.1f} MB")
    threads = [Thread(target=sleeper) for _ in range(100)]
    for t in threads: t.start()
    time.sleep(1)
    print(f"RSS with 100 threads: {proc.memory_info().rss / 1e6:.1f} MB")
    for t in threads: t.join()
```

### Example 11 – Memory Per 10 Processes

```python
# Example 11: Memory growth with processes (requires psutil)
import time
import psutil
from multiprocessing import Process

def sleeper():
    time.sleep(5)

if __name__ == "__main__":
    proc = psutil.Process()
    print(f"RSS before: {proc.memory_info().rss / 1e6:.1f} MB")
    procs = [Process(target=sleeper) for _ in range(10)]
    for p in procs: p.start()
    time.sleep(1)
    print(f"RSS with 10 processes: {proc.memory_info().rss / 1e6:.1f} MB")
    for p in procs:
        p.terminate()
    for p in procs:
        p.join()
```

### Example 12 – Pickling Cost for Large Objects

```python
# Example 12: Pickling overhead benchmark
import time
from multiprocessing import Pool

big = list(range(1_000_000))  # a few MB pickled

def identity(x):
    return x

if __name__ == "__main__":
    start = time.perf_counter()
    with Pool(2) as pool:
        pool.map(identity, [big] * 4)
    print(f"4x pickle/unpickle big list: {time.perf_counter() - start:.2f} s")
```

### Example 13 – `shared_memory` vs Pickle (Conceptual)

```python
# Example 13: shared_memory avoids repeated pickle of arrays
from multiprocessing import Process, shared_memory
import numpy as np
import time

def worker(shm_name):
    shm = shared_memory.SharedMemory(name=shm_name)
    arr = np.ndarray((1000, 1000), dtype=np.float64, buffer=shm.buf)
    arr += 1
    shm.close()

if __name__ == "__main__":
    shm = shared_memory.SharedMemory(create=True, size=8_000_000)
    arr = np.ndarray((1000, 1000), dtype=np.float64, buffer=shm.buf)
    arr.fill(0)

    start = time.perf_counter()
    p = Process(target=worker, args=(shm.name,))
    p.start(); p.join()
    print(f"Shared memory 8 MB: {time.perf_counter() - start:.3f} s")
    shm.close(); shm.unlink()
```

### Example 14 – GIL Contention for CPU Threads

```python
# Example 14: GIL contention with CPU-bound threads
import time
from threading import Thread

def cpu():
    total = 0
    for i in range(10**7):
        total += i
    return total

if __name__ == "__main__":
    start = time.perf_counter()
    threads = [Thread(target=cpu) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"8 CPU-bound threads: {time.perf_counter() - start:.3f} s")
```

### Example 15 – Lock Contention and Context Switches

```python
# Example 15: Many context switches via contended Lock
import time
from threading import Thread, Lock

lock = Lock()
counter = 0

def inc():
    global counter
    for _ in range(200_000):
        with lock:
            counter += 1

if __name__ == "__main__":
    start = time.perf_counter()
    threads = [Thread(target=inc) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"4 threads, contended lock: {time.perf_counter() - start:.3f} s")
    print("Final counter:", counter)
```

### Example 16 – Fork Copy-on-Write Surprise (POSIX Only)

```python
# Example 16: Large global + write in child (fork CoW)
import os
import sys
from multiprocessing import Process
import numpy as np

big = np.zeros((2000, 2000), dtype=np.float64)  # ~32 MB

def modify():
    big[0, 0] = 42.0  # may trigger CoW on fork

if __name__ == "__main__":
    if sys.platform.startswith("linux"):
        print("On fork platforms, writing in child may duplicate pages.")
    p = Process(target=modify)
    p.start()
    p.join()
    print("Parent still has big[0, 0] =", big[0, 0])  # usually 0.0
```

### Example 17 – Using `spawn` to Avoid CoW

```python
# Example 17: spawn start method (no CoW, fresh interpreter)
import multiprocessing as mp

def worker():
    print("Worker running under", mp.get_start_method())

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    p = mp.Process(target=worker)
    p.start()
    p.join()
```

### Example 18 – `Manager` Overhead

```python
# Example 18: Manager is slow for frequent updates
import time
from multiprocessing import Process, Manager

def update(d):
    for i in range(50_000):
        d["key"] = i  # round-trip via manager server

if __name__ == "__main__":
    with Manager() as m:
        d = m.dict()
        start = time.perf_counter()
        p = Process(target=update, args=(d,))
        p.start(); p.join()
        print(f"Manager 50k updates: {time.perf_counter() - start:.3f} s")
```

### Example 19 – `Value` for Cheap Primitive Sharing

```python
# Example 19: Value is cheaper than Manager for primitives
import time
from multiprocessing import Process, Value

def update(v: Value):
    for i in range(50_000):
        with v.get_lock():
            v.value = i

if __name__ == "__main__":
    v = Value('i', 0)
    start = time.perf_counter()
    p = Process(target=update, args=(v,))
    p.start(); p.join()
    print(f"Value 50k updates: {time.perf_counter() - start:.3f} s")
```

### Example 20 – `chunksize` Impact in `Pool.map`

```python
# Example 20: chunksize reduces overhead in Pool.map
import time
from multiprocessing import Pool

def work(x: int) -> int:
    return x

if __name__ == "__main__":
    data = list(range(100_000))

    start = time.perf_counter()
    with Pool() as pool:
        pool.map(work, data, chunksize=1)
    print(f"chunksize=1:    {time.perf_counter() - start:.3f} s")

    start = time.perf_counter()
    with Pool() as pool:
        pool.map(work, data, chunksize=1000)
    print(f"chunksize=1000: {time.perf_counter() - start:.3f} s")
```

### Example 21 – Thread Stack Size (Memory Tuning)

```python
# Example 21: Custom thread stack size (advanced)
import threading

if __name__ == "__main__":
    print("Default stack size:", threading.stack_size())
    threading.stack_size(1024 * 1024)  # 1 MB for future threads
    print("New default stack size:", threading.stack_size())
```

### Example 22 – Empty Process Memory Baseline (Requires psutil)

```python
# Example 22: Memory used by an empty child process
from multiprocessing import Process
import psutil

def empty():
    pass

if __name__ == "__main__":
    p = Process(target=empty)
    p.start()
    child = psutil.Process(p.pid)
    print(f"Empty child RSS: {child.memory_info().rss / 1e6:.1f} MB")
    p.join()
```

### Example 23 – Threads: CPU-Bound vs I/O-Bound

```python
# Example 23: GIL hurt CPU-bound, but I/O-bound scales
import time
from threading import Thread

def cpu():
    total = 0
    for i in range(5_000_000):
        total += i

def io():
    time.sleep(0.5)

if __name__ == "__main__":
    start = time.perf_counter()
    threads = [Thread(target=cpu) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"8 CPU threads: {time.perf_counter() - start:.3f} s")

    start = time.perf_counter()
    threads = [Thread(target=io) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"8 I/O threads:  {time.perf_counter() - start:.3f} s")
```

### Example 24 – Process Limits (POSIX Only, Conceptual)

```python
# Example 24: Process limit (POSIX only, advanced)
try:
    import resource
except ImportError:
    resource = None

if __name__ == "__main__":
    if resource is not None:
        soft, hard = resource.getrlimit(resource.RLIMIT_NPROC)
        print(f"Process limit: soft={soft}, hard={hard}")
    else:
        print("resource module not available on this platform.")
```

### Example 25 – CPU Affinity (POSIX Only, Advanced)

```python
# Example 25: CPU affinity can affect scheduling
import os
import sys

if __name__ == "__main__":
    print("Available CPUs:", os.cpu_count())
    if hasattr(os, "sched_setaffinity") and sys.platform.startswith("linux"):
        # os.sched_setaffinity(0, {0, 1})  # Uncomment to pin to cores 0 and 1
        print("On Linux, you can pin processes to specific CPUs.")
```

### Example 26 – Pickle vs Shared Memory (High-Level Comparison)

```python
# Example 26: Compare pickle vs shared_memory for a medium array
from multiprocessing import Pool, shared_memory
import numpy as np
import pickle
import time

arr = np.random.rand(1000, 1000)  # ~8 MB

def pickle_roundtrip(_):
    blob = pickle.dumps(arr)
    return pickle.loads(blob)

def shm_worker(name_shape_dtype):
    name, shape, dtype_str = name_shape_dtype
    dtype = np.dtype(dtype_str)
    shm = shared_memory.SharedMemory(name=name)
    arr2 = np.ndarray(shape, dtype=dtype, buffer=shm.buf)
    # read some data
    _ = float(arr2[0, 0])
    shm.close()

if __name__ == "__main__":
    # Pickle
    start = time.perf_counter()
    with Pool(1) as pool:
        pool.map(pickle_roundtrip, range(3))
    print(f"Pickle roundtrips: {time.perf_counter() - start:.3f} s")

    # Shared memory
    shm = shared_memory.SharedMemory(create=True, size=arr.nbytes)
    shm_arr = np.ndarray(arr.shape, dtype=arr.dtype, buffer=shm.buf)
    shm_arr[:] = arr

    start = time.perf_counter()
    with Pool(1) as pool:
        pool.map(shm_worker, [(shm.name, arr.shape, arr.dtype.str)] * 3)
    print(f"Shared memory access: {time.perf_counter() - start:.3f} s")

    shm.close()
    shm.unlink()
```

### Example 27 – Too Many Threads (Memory Footprint)

```python
# Example 27: Many threads consume memory (requires psutil)
import time
from threading import Thread
import psutil

def sleeper():
    time.sleep(5)

if __name__ == "__main__":
    N = 1000  # Not 10_000: be kind to your machine
    threads = [Thread(target=sleeper) for _ in range(N)]
    for t in threads: t.start()
    time.sleep(1)
    rss = psutil.Process().memory_info().rss / 1e6
    print(f"RSS with {N} sleeping threads: {rss:.1f} MB")
    for t in threads: t.join()
```

### Example 28 – Batch Startup: Threads vs Processes

```python
# Example 28: Startup cost scaling with number of workers
import time
from threading import Thread
from multiprocessing import Process

def noop():
    pass

def measure_threads(n: int) -> float:
    start = time.perf_counter()
    threads = [Thread(target=noop) for _ in range(n)]
    for t in threads: t.start()
    for t in threads: t.join()
    return time.perf_counter() - start

def process_target():
    noop()

def measure_processes(n: int) -> float:
    start = time.perf_counter()
    procs = [Process(target=process_target) for _ in range(n)]
    for p in procs: p.start()
    for p in procs: p.join()
    return time.perf_counter() - start

if __name__ == "__main__":
    for n in [10, 50, 100]:
        print(f"{n:3} threads:   {measure_threads(n):.3f} s")
        print(f"{n:3} processes: {measure_processes(n):.3f} s")
```

### Example 29 – Large Global List & CoW (Conceptual)

```python
# Example 29: Large global + modify in child (fork CoW)
from multiprocessing import Process
import psutil

big_list = list(range(2_000_000))  # a few tens of MB

def modify():
    big_list[0] = 42  # may trigger CoW on fork

if __name__ == "__main__":
    proc = psutil.Process()
    print(f"Before child RSS: {proc.memory_info().rss / 1e6:.1f} MB")
    p = Process(target=modify)
    p.start()
    p.join()
    print(f"After child RSS:  {proc.memory_info().rss / 1e6:.1f} MB")
```

### Example 30 – Universal Overhead Benchmark Template

```python
# Example 30: Copy-paste to measure overhead vs work size
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def benchmark(name: str, executor_cls, workers: int, tasks: int, task_work: int) -> None:
    def work(_idx: int) -> int:
        total = 0
        for i in range(task_work):
            total += i * i
        return total

    start = time.perf_counter()
    with executor_cls(max_workers=workers) as exe:
        list(exe.map(work, range(tasks)))
    elapsed = time.perf_counter() - start
    print(f"{name}: workers={workers}, tasks={tasks}, work={task_work} → {elapsed:.3f} s")

if __name__ == "__main__":
    for work in [10_4, 10_5, 10_6, 10_7]:
        benchmark("Threads  ", ThreadPoolExecutor, 8, 8, work)
        benchmark("Processes", ProcessPoolExecutor, 8, 8, work)
```

---

## 12. Pre-Core Quiz

1. Thread startup time ballpark? → **Tens of microseconds**
2. Process startup time ballpark? → **Single–tens of milliseconds**
3. Does a pool reuse workers? → **Yes** (threads and processes)
4. Can large globals be duplicated on fork when written from children? → **Yes** (CoW)
5. Is pickling 50–100 MB per task “cheap”? → **No**, it is *very* expensive

---

## 13. Post-Core Reflection

Open your parallel code.

1. Implement a small benchmark like **Example 30** that mimics your workload:

   * Same operation
   * Similar task size
   * Similar worker count
2. Vary:

   * Work per task (1e4 → 1e7 iterations)
   * Number of tasks
   * Threads vs processes
3. Look for:

   * Where processes start to beat threads.
   * Where both are slower than sequential.

Did you discover that:

* Your tasks are too small for processes?
* You’re pickling way too much data?
* You’re using more workers than your hardware can handle?

If yes: congratulations. You now own the **cost model** of parallelism in Python, not just the syntax.

**Next:** Core 7 – Process and Thread Ownership and Topologies.
