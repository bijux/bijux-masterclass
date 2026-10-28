# Core 7: Process and Thread Ownership and Topologies

> **Core question:**  
> Who owns what in a hierarchy of threads and processes — and how do parent-child relationships, daemons, and topologies affect cleanup, signals, and resource leaks?

In **Core 1** you learned *when* to choose threads vs processes.  
In **Core 2** you learned *why* the GIL limits threads.  
In **Core 3** you mastered safe threading.  
In **Core 4** you learned multiprocessing basics.  
In **Core 5** you learned synchronization primitives.  
In **Core 6** you learned cost models.  
Here in **Core 7** you learn **ownership and topologies**: how threads and processes relate as parents/children, daemons, zombies, and structured groups — and why getting this wrong causes hangs, leaks, or crashes.

**Audience:** Developers who spawn threads/processes but have seen “zombie processes”, “daemon didn’t die”, or “child inherited open files and broke everything”.

**Outcome:** After this file, you should:
1. Draw the ownership topology of any parallel code in < 10 seconds.
2. Explain in one sentence why daemon threads/processes don’t block exit but can leak resources.
3. Structure pools, pipelines, and worker groups without orphans or zombies.
4. Spot and fix three classic topology bugs in code review:
   - Forgetting to join children → zombies
   - Daemon workers that outlive their purpose
   - Parent dying while children hold resources

---

## 1. Historical & Conceptual Backbone

### 1.1 History in 5 Lines

- Early Unix: `fork()` creates process trees; zombies appear if parents don’t `wait()`.
- Python 1.x: Threads inherit OS topology; no built-in process trees.
- Python 2.6: `multiprocessing` adds explicit parent-child relationships and `join()`.
- Python 3.0+: Daemon threads/processes formalized; `concurrent.futures` hides topology.
- November 2025: Topology bugs remain a top cause of “Python process won’t exit” reports.

**This entire core focuses on ownership and structure.**  
Bad topology = leaks, hangs, or security holes.

### 1.2 Ownership and Topology in One Precise Sentence

> Threads share their process as parent; processes form explicit trees with parents that must join children — daemons opt out of blocking exit but risk abrupt termination.

### 1.3 The One-Sentence Rule

> **Join your children or make them daemons. Never leave orphans. Structure as trees or pools, not flat chaos.**

Everything else in this core is a justification and elaboration of that rule.

### 1.4 Positioning of `concurrent.futures`

Executors hide topology but don’t eliminate it:
- `ThreadPoolExecutor`: flat pool of non-daemon threads; auto-joins on shutdown.
- `ProcessPoolExecutor`: flat pool of child processes; auto-joins workers.
- Use them for simple cases — but understand the hidden parent-child tree underneath.

For this core: **master raw ownership** so executors don’t surprise you.

---

## 2. Mental Model: Ownership and Topologies

### 2.1 One Picture

```text
Main Process (Python Interpreter)
+------------------- Parent -------------------+
|                                                |
|  Owns: files, signals, memory, child processes |
|                                                |
|   [ Thread A ]  [ Thread B ]  [ Thread C ]     |
|    (non-daemon by default)                     |
|                                                |
|   [ Child Process 1 ]                          |
|        |                                       |
|        +-- [ Grandchild Process ]              |
|                                                |
|   [ Pool of 8 Worker Processes ]               |
|        |        |        |                     |
|      Worker1  Worker2  Worker3 ...            |
+------------------------------------------------+

Daemons: don't block parent exit, but may be killed.
Zombies: dead children not joined → resource leak until parent dies.
Orphans: children whose parent died → adopted by init (PID 1).
```

### 2.2 Contract Table

| Entity               | Owned By                | Blocks Parent Exit? | Killed on Parent Exit? | Cleanup Required                  |
|----------------------|-------------------------|---------------------|------------------------|-----------------------------------|
| Non-daemon Thread    | Process                 | Yes                 | N/A (process waits)    | Threads must finish               |
| Daemon Thread        | Process                 | No                  | Yes (abrupt)           | None (may leak)                   |
| Child Process        | Parent Process          | No                  | No                     | `join()` or `terminate()+join()`  |
| Daemon Process       | Parent Process          | No                  | Yes (SIGTERM)          | None (may leak)                   |
| Pool Worker          | Pool (in parent)        | No                  | Yes                    | Pool `close()` + `join()`         |
| Zombie (Unix)        | Parent (until reaped)   | No                  | No                     | `join()` / `wait()`               |
| Orphan (Unix)        | init / PID 1            | No                  | No                     | Child must exit cleanly           |

---

## 3. Anti-Pattern First: “Spawn and forget — they’ll clean up themselves (they won’t).”

### Example 1 – Non-Joined Child Processes → Zombies (Anti-Pattern)

```python
# Example 1: Forgetting to join children → zombies (Unix)
from multiprocessing import Process
import time

def child():
    time.sleep(1)

if __name__ == "__main__":
    procs = [Process(target=child) for _ in range(5)]
    for p in procs: p.start()
    print("Main exiting without join...")
    # No join → exited children can linger as zombies while the parent is still alive
```

**What to observe:**  
`ps aux | grep Z` shows defunct (zombie) processes.

---

## 4. Correct Pattern: Join Your Children

### Example 2 – Proper Join to Avoid Zombies

```python
# Example 2: Join children → clean exit
from multiprocessing import Process
import time

def child():
    time.sleep(1)

if __name__ == "__main__":
    procs = [Process(target=child) for _ in range(5)]
    for p in procs: p.start()
    for p in procs: p.join()  # Wait for completion
    print("All children joined — no zombies")
```

**What to observe:**  
Clean exit, no zombies.

---

## 5. Correct Pattern: Daemon Processes for Fire-and-Forget

### Example 3 – Daemon Child Doesn’t Block Exit

```python
# Example 3: Daemon process dies with parent
from multiprocessing import Process
import time

def background():
    while True:
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=background, daemon=True)
    p.start()
    time.sleep(2)
    print("Main exits → daemon killed automatically")
```

**What to observe:**  
Parent exits immediately; daemon terminated.

---

## 6. Consequence of the Decision: Topology Determines Lifetime and Cleanup

**This section is not about *which* topology to choose, but about what you get once you’ve chosen: how ownership affects exit, signals, and resources.**

### Example 4 – Non-Daemon Thread Blocks Exit

```python
# Example 4: Non-daemon thread prevents exit
from threading import Thread
import time

def sleeper():
    time.sleep(10)

if __name__ == "__main__":
    Thread(target=sleeper).start()  # Non-daemon by default
    print("Main tries to exit...")
    # Hangs for 10 seconds
```

### Example 5 – Daemon Thread Allows Immediate Exit

```python
# Example 5: Daemon thread dies with main
from threading import Thread
import time

def sleeper():
    time.sleep(10)

if __name__ == "__main__":
    Thread(target=sleeper, daemon=True).start()
    print("Main exits immediately")
    # Exits without waiting
```

---

## 7. Ownership and Topology in One Sentence

> Threads belong to their process; processes belong to their parent — join non-daemons or mark as daemon, and structure as trees or pools to avoid orphans and zombies.

### Example 6 – Orphan Process Adopted by Init

```python
# Example 6: Child outlives parent → orphan
from multiprocessing import Process
import time
import os

def child():
    print("Child PPID before:", os.getppid())
    time.sleep(5)
    print("Child PPID after parent death:", os.getppid())  # → 1

if __name__ == "__main__":
    p = Process(target=child)
    p.start()
    print("Parent exiting...")
    # Child becomes orphan
```

**What to observe:**  
Child PPID changes to 1 (init) after parent exits.

---

## 8. Cost Model: Bad Topology = Leaks and Hangs

Bad topology costs:
- Zombies: leak process table slots.
- Orphans: may run forever.
- Daemons: abrupt kill → lost work or corrupted state.

### Example 7 – Zombie Process Leak

```python
# Example 7: Many unjoined children → zombie apocalypse
from multiprocessing import Process
import time

def child():
    pass

if __name__ == "__main__":
    for _ in range(1000):
        p = Process(target=child)
        p.start()
        # No join → 1000 zombies
    time.sleep(5)
    print("Check `ps aux | grep Z` — many zombies")
```

**Key point:**  
Always join or use pools.

---

## 9. Practical Design Recipe: “Join your children or make them daemons. Structure as trees or pools, not flat chaos.”

```text
1. Threads
   - Non-daemon by default → must join or use executor
   - Daemon for background (logging, monitoring)

2. Processes
   - Always under `if __name__ == "__main__":`
   - Non-daemon → must join
   - Daemon → fire-and-forget (careful with cleanup)

3. Structure:
   - Flat: raw spawn + join (simple scripts)
   - Tree: parent spawns children that spawn grandchildren
   - Pool: fixed workers (preferred for CPU)

4. Avoid:
   - Unjoined children → zombies
   - Daemons that hold resources (files, sockets)
   - Orphans that run forever

5. When in doubt:
   - Draw the tree: who spawns whom? who joins whom?
   - Make sure every non-daemon worker has a clear join/shutdown path.
```

---

## 10. API Survey

| API                          | Ownership Role                      | Cleanup Behavior                    |
| ---------------------------- | ----------------------------------- | ----------------------------------- |
| `threading.Thread`           | Owned by process                    | Non-daemon blocks exit              |
| `multiprocessing.Process`    | Child of parent process             | Must join or daemon                 |
| `concurrent.futures` pools   | Hidden children, auto-joined        | Clean on close                      |
| `daemon=True`                | Opt-out of blocking exit            | Killed on parent exit               |
| `p.join()` / `p.terminate()` | Explicit cleanup                    | Required for non-daemon             |

---

## 11. Worked Examples (1–30)

All runnable, guarded, no bad patterns.

### Example 8 – Thread Ownership (Non-Daemon Blocks)

```python
# Example 8: Non-daemon thread blocks process exit
from threading import Thread
import time

def sleeper():
    time.sleep(5)

if __name__ == "__main__":
    Thread(target=sleeper).start()
    print("Main tries to exit...")
    # Hangs for 5 seconds
```

### Example 9 – Daemon Thread Allows Exit

```python
# Example 9: Daemon thread doesn't block
from threading import Thread
import time

def sleeper():
    time.sleep(5)

if __name__ == "__main__":
    Thread(target=sleeper, daemon=True).start()
    print("Main exits immediately")
```

### Example 10 – Process Tree with Grandchildren

```python
# Example 10: Multi-level process tree
from multiprocessing import Process
import os

def grandchild():
    print("Grandchild PID:", os.getpid())

def child():
    print("Child PID:", os.getpid())
    gc = Process(target=grandchild)
    gc.start()
    gc.join()

if __name__ == "__main__":
    p = Process(target=child)
    p.start()
    p.join()
```

### Example 11 – Zombie Process Creation

```python
# Example 11: Unjoined child → zombie
from multiprocessing import Process
import time

def child():
    pass

if __name__ == "__main__":
    p = Process(target=child)
    p.start()
    time.sleep(2)  # Child exits, parent doesn't join
    print("Check ps: zombie process exists")
    p.join()  # Cleans zombie
```

### Example 12 – Daemon Process Lifecycle

```python
# Example 12: Daemon process killed on parent exit
from multiprocessing import Process
import time

def background():
    while True:
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=background, daemon=True)
    p.start()
    time.sleep(2)
    print("Main exits → daemon killed automatically")
```

### Example 13 – Pool Auto-Joins Workers

```python
# Example 13: Pool cleans up workers
from multiprocessing import Pool

def work(_):
    pass

if __name__ == "__main__":
    with Pool(4) as pool:
        pool.map(work, range(100))
    print("Pool closed — workers joined automatically")
```

### Example 14 – Orphan Process (Parent Dies First)

```python
# Example 14: Parent exits before child → orphan
from multiprocessing import Process
import time
import os

def child():
    print("Child PPID before:", os.getppid())
    time.sleep(5)
    print("Child PPID after parent death:", os.getppid())  # → 1

if __name__ == "__main__":
    p = Process(target=child)
    p.start()
    print("Parent exiting...")
    # Child becomes orphan
```

### Example 15 – ThreadPoolExecutor Auto-Cleanup

```python
# Example 15: Executor auto-joins threads
from concurrent.futures import ThreadPoolExecutor
import time

def sleep():
    time.sleep(1)

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as exe:
        exe.map(sleep, range(4))
    print("Executor closed — threads joined")
```

### Example 16 – ProcessPoolExecutor Auto-Cleanup

```python
# Example 16: Executor auto-joins processes
from concurrent.futures import ProcessPoolExecutor

def work(x):
    return x * x

if __name__ == "__main__":
    with ProcessPoolExecutor() as exe:
        results = list(exe.map(work, range(8)))
    print("Process pool shut down cleanly. Results:", results)
```

### Example 17 – Custom Process Tree

```python
# Example 17: Manual process tree
from multiprocessing import Process
import os

def leaf():
    print("Leaf PID:", os.getpid())

def branch():
    print("Branch PID:", os.getpid())
    leaf_proc = Process(target=leaf)
    leaf_proc.start()
    leaf_proc.join()

def root():
    print("Root PID:", os.getpid())
    branch_proc = Process(target=branch)
    branch_proc.start()
    branch_proc.join()

if __name__ == "__main__":
    root()
```

### Example 18 – Daemon Thread Leak (Conceptual)

```python
# Example 18: Daemon holding resource → leak on exit
from threading import Thread
import time

def holder():
    f = open("/tmp/leak", "w")
    while True:
        time.sleep(1)  # File stays open

if __name__ == "__main__":
    Thread(target=holder, daemon=True).start()
    time.sleep(2)
    print("Main exits — file may remain open")
```

### Example 19 – Proper Daemon Cleanup

```python
# Example 19: Daemon with cleanup
from threading import Thread, Event
import time

stop = Event()

def worker():
    f = open("/tmp/data", "w")
    try:
        while not stop.is_set():
            time.sleep(0.1)
    finally:
        f.close()
        print("Daemon cleaned up")

if __name__ == "__main__":
    t = Thread(target=worker, daemon=True)
    t.start()
    time.sleep(2)
    stop.set()
    t.join(timeout=1.0)
```

### Example 20 – Manual Join to Avoid Zombies

```python
# Example 20: join() is your "wait()" to reap child processes
from multiprocessing import Process

def child():
    # Do some quick work
    return

if __name__ == "__main__":
    p = Process(target=child)
    p.start()
    # When child exits, it's briefly a zombie on Unix until we join.
    p.join()  # Reaps the child process
    print("Child joined; no zombie remains.")
```

### Example 21 – Pool with maxtasksperchild

```python
# Example 21: Refresh workers to avoid leaks
from multiprocessing import Pool

def work(x):
    return x * 2

if __name__ == "__main__":
    with Pool(maxtasksperchild=10) as pool:
        results = pool.map(work, range(50))
    print(len(results))
```

### Example 22 – Process Identification

```python
# Example 22: Process name and PID
from multiprocessing import Process, current_process

def worker():
    proc = current_process()
    print(f"Name: {proc.name}, PID: {proc.pid}")

if __name__ == "__main__":
    p = Process(target=worker, name="WorkerProc")
    p.start()
    p.join()
```

### Example 23 – Exceptions in Child Processes

```python
# Example 23: Exceptions in child don't crash parent
from multiprocessing import Process

def buggy():
    raise ValueError("Child error")

if __name__ == "__main__":
    p = Process(target=buggy)
    p.start()
    p.join()
    print("Parent continues; check stderr for child exception")
```

### Example 24 – Two-Stage CPU Pipeline with Queues

```python
# Example 24: Processes + queues for CPU pipeline
from multiprocessing import Process, Queue

def stage1(out_q):
    for i in range(5):
        out_q.put(i)
    out_q.put(None)

def stage2(in_q, out_q):
    while True:
        item = in_q.get()
        if item is None:
            out_q.put(None)
            break
        out_q.put(item * item)

def consumer(in_q):
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

### Example 25 – Measuring Too Many Processes (Be Careful)

```python
# Example 25: Many processes → resource limits
from multiprocessing import Process

def work():
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

### Example 26 – ProcessPoolExecutor (Modern Wrapper)

```python
# Example 26: concurrent.futures.ProcessPoolExecutor
from concurrent.futures import ProcessPoolExecutor

def square(x):
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

_counter = None

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

def modify(buf):
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

def cube(x):
    return x * x * x

if __name__ == "__main__":
    with Pool() as pool:
        results = pool.map(cube, range(10))
    print(results)
```

### Example 30 – Universal Topology Benchmark Template

```python
# Example 30: Benchmark topology impact on exit time
import time
from multiprocessing import Process, Pool

def benchmark(name, fn):
    start = time.perf_counter()
    fn()
    print(f"{name}: {time.perf_counter() - start:.3f} s")

def sleep_brief(_):
    time.sleep(0.01)

if __name__ == "__main__":
    def flat_spawn():
        procs = [Process(target=time.sleep, args=(0.01,)) for _ in range(50)]
        for p in procs: p.start()
        for p in procs: p.join()

    def pooled():
        with Pool(8) as pool:
            pool.map(sleep_brief, range(50))

    benchmark("Flat spawn + join (50 children)", flat_spawn)
    benchmark("Pooled (8 workers, 50 tasks)", pooled)
```

---

## 12. Pre-Core Quiz

1. Non-daemon thread blocks process exit? → Yes  
2. Daemon process needs join? → No  
3. Unjoined dead child → zombie? → Yes  
4. Orphan adopted by PID 1? → Yes  
5. Pool auto-joins workers? → Yes  

## 13. Post-Core Reflection

Open your codebase.

Find **one** place spawning threads or processes.

Draw the topology: parent → children → daemons?

Add missing joins or convert to daemons/pools.

Did you eliminate zombies or exit hangs?

You now own **process and thread lifetimes** in Python.

**Next:** Core 8 – Determinism, Ordering, and Reproducibility in Parallel Execution.
