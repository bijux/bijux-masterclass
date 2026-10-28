# Core 9: OS Scheduling, Affinity, and Process Start Methods

> **Core question:**  
> How does the operating system schedule your threads and processes, how do you pin them to specific cores with affinity, and how do you choose the right process start method (`spawn`, `fork`, `forkserver`) to avoid crashes, memory bloat, or security holes?

In **Core 1** you learned *when* to choose threads vs processes.  
In **Core 2** you learned *why* the GIL limits threads.  
In **Core 3** you mastered safe threading.  
In **Core 4** you learned multiprocessing basics.  
In **Core 5** you learned synchronization primitives.  
In **Core 6** you learned cost models.  
In **Core 7** you learned ownership and topologies.  
In **Core 8** you learned determinism and reproducibility.  
Here in **Core 9** you learn **OS-level control**: scheduling behavior, CPU affinity for performance, and process start methods for safety and compatibility.

**Audience:** Developers whose parallel code “works on my machine” but hangs, crashes, or slows down in production — especially across Linux vs Windows/macOS or on heavily loaded servers.

**Outcome:** After this file, you should:
1. Explain in one sentence why `fork` is fast but dangerous with threads.
2. Choose the right start method (`spawn` / `fork` / `forkserver`) for any platform in < 10 seconds.
3. Pin **processes** to cores with affinity when contention or cache locality matters.
4. Spot and fix three classic OS-level bugs in code review:
   - Using `fork` after creating threads → deadlock
   - Default `spawn` on Linux when pure-Python CPU could use `fork`
   - No affinity on NUMA/multi-socket → cache thrash

---

## 1. Historical & Conceptual Backbone

### 1.1 History in 5 Lines

- 1960s–1980s: Unix `fork()` is the classic process creation primitive — fast, copy-on-write, inherits everything.
- 1990s: Windows uses `CreateProcess` (spawn semantics) — safer isolation, more overhead.
- Python 2.6 (2008): `multiprocessing` introduced — defaults to `fork` on Unix, `spawn` on Windows.
- Python 3.4: `forkserver` added: start a clean server process, then `fork()` from there.
- Python 3.8+: macOS switches default to `spawn` (because `fork` + threads is cursed there); Linux still defaults to `fork`.

**This entire core focuses on OS-level behavior.**  
Python gives you knobs — turn them *on purpose*.

### 1.2 Scheduling, Affinity, and Start Methods in One Precise Sentence

> The OS schedules threads and processes onto cores, affinity restricts which cores they may run on, and start methods (`fork` / `spawn` / `forkserver`) control how new processes inherit state from the parent.

### 1.3 The One-Sentence Rule

> **Let the OS schedule unless you measure contention. Use `spawn` for safety, `fork` on Linux for speed (if you understand the risks), `forkserver` as a safe middle ground; use affinity only when profiling says you need it.**

Everything else in this core is a justification and elaboration of that rule.

### 1.4 Positioning of `concurrent.futures`

Executors sit on top of `multiprocessing`:
- `ThreadPoolExecutor`: uses OS threads within a single process; scheduling completely handled by the OS.
- `ProcessPoolExecutor`: uses the platform’s `multiprocessing` defaults:
  - Windows: `spawn`
  - macOS: `spawn`
  - Linux/other Unix: usually `fork` (unless overridden)
- No built-in API for affinity; you set it manually in worker code.

For this core: **understand what the OS and start method are doing under the covers** so executors don’t surprise you.

---

## 2. Mental Model: Scheduling, Affinity, Start Methods

### 2.1 One Picture

```text
CPU Cores (with caches)
+-----------------------------------------------------------+
| Core 0     Core 1     Core 2     Core 3     ...           |
|  L1$ L2$    L1$ L2$    L1$ L2$    L1$ L2$                 |
|                                                           |
| OS Scheduler:                                             |
|   - Runs runnable threads/processes on any available core |
|   - Can migrate them between cores over time              |
|                                                           |
| Affinity:                                                 |
|   - Restricts which cores a process/thread may run on     |
|   - Used for cache locality / NUMA control                |
|                                                           |
| Process start methods (multiprocessing):                  |
|   - fork:       Clone current process via copy-on-write   |
|   - spawn:      Start a fresh interpreter, import target  |
|   - forkserver: Pre-start clean server, fork from there   |
+-----------------------------------------------------------+

Default: scheduler can move work around freely.
Affinity: you constrain where things can run.
Start method: controls what state children inherit.
```

### 2.2 Contract Table

**Defaults (Python 3.8+):**

* **Linux / most Unix:** `fork`
* **macOS:** `spawn`
* **Windows:** `spawn`

**Summary table:**

| Aspect                | `fork` (Unix)                          | `spawn` (all)                          | `forkserver` (Unix)                      |
| --------------------- | -------------------------------------- | -------------------------------------- | ---------------------------------------- |
| Startup speed         | Fastest (CoW)                          | Slow (new interpreter + imports)       | Medium (one-time server + fast forks)    |
| Memory behavior       | Copy-on-write from parent              | Fresh process; data via pickle         | Copy-on-write from *clean* server        |
| Inherits parent state | Yes: FDs, env, globals, threads’ locks | Minimal (only arguments via pickle)    | From server only (not your main process) |
| Safe with threads?    | **No** (fork-after-threads is risky)   | Yes                                    | Yes                                      |
| Available on Windows? | No                                     | Yes                                    | No                                       |
| Good for              | Pure-Python CPU, few/no threads        | Cross-platform, libraries with threads | Mixed workloads, wants fork speed safely |

**Affinity:**

| API                           | Platform                 | What it controls              |
| ----------------------------- | ------------------------ | ----------------------------- |
| `os.sched_setaffinity`        | Linux only               | Process-level allowed CPU set |
| `psutil.Process.cpu_affinity` | Linux, Windows (limited) | Process-level allowed CPU set |
| `taskset` (CLI)               | Linux only               | Affinity at process start     |
| `numactl` (CLI)               | Linux only               | NUMA node & memory binding    |

macOS basically shrugs at you for CPU affinity; you get almost no control there.

---

## 3. Anti-Pattern First: “The OS is smart, it’ll schedule this fine (until NUMA + contention say hi).”

### Example 1 – Heavy CPU Pool, No Affinity (Baseline)

```python
# Example 1: CPU-heavy Pool with default scheduling
import time
from multiprocessing import Pool

def cpu_intensive(_):
    total = 0
    for i in range(10**7):
        total += i
    return total

if __name__ == "__main__":
    start = time.perf_counter()
    with Pool() as pool:
        list(pool.map(cpu_intensive, range(8)))
    print(f"No explicit affinity: {time.perf_counter() - start:.3f} s")
```

On a **single-socket, small machine**, this is often fine. On **multi-socket / NUMA** with other workloads, you may see noisy, unstable timings.

---

## 4. Correct Pattern: Pin with Affinity *When Profiling Justifies It*

### Example 2 – Pin the Parent (and Thus Children) on Linux

```python
# Example 2: Pin current process to CPUs 0–3 (Linux only)
import os
import time
from multiprocessing import Pool

def cpu_intensive(_):
    total = 0
    for i in range(10**7):
        total += i
    return total

if __name__ == "__main__":
    if hasattr(os, "sched_setaffinity"):
        os.sched_setaffinity(0, {0, 1, 2, 3})
        print("Pinned main process (and children) to CPUs 0–3")
    else:
        print("os.sched_setaffinity not available; skipping pinning")

    start = time.perf_counter()
    with Pool() as pool:
        list(pool.map(cpu_intensive, range(8)))
    print(f"With affinity: {time.perf_counter() - start:.3f} s")
```

**What to do in real life:**

* Use `htop` / `top` / perf tools to see if your processes bounce between sockets or cores.
* Add affinity *only* if you see gains (cache locality, fewer migrations).

---

## 5. Correct Pattern: Choose Start Method On Purpose

### Example 3 – Measuring `spawn` vs `fork` vs `forkserver`

```python
# Example 3: Compare start methods (Unix-only for fork/forkserver)
import multiprocessing as mp
import os
import time

def work(_):
    total = 0
    for i in range(10**6):
        total += i
    return total

def run_with_method(method: str):
    ctx = mp.get_context(method)
    start = time.perf_counter()
    with ctx.Pool(4) as pool:
        list(pool.map(work, range(8)))
    return time.perf_counter() - start

if __name__ == "__main__":
    methods = ["spawn"]
    if os.name != "nt":
        methods += ["fork", "forkserver"]

    for method in methods:
        elapsed = run_with_method(method)
        print(f"{method:9}: {elapsed:.3f} s")
```

**Typical pattern on Linux:**

* `fork` fastest to start.
* `forkserver` slightly slower startup, but safer with complex code.
* `spawn` clearly slower, but clean and portable.

---

## 6. Consequence: Wrong Start Method = Hangs, Crashes, or Massive Overhead

This is where people get bit.

### Example 4 – `fork` After Threads (DO NOT DO THIS)

```python
# Example 4: fork after starting threads → undefined behavior (Unix)
import multiprocessing as mp
import threading
import time
import os

def thread_work():
    # Hold the GIL for a bit doing "work"
    t_end = time.time() + 2
    while time.time() < t_end:
        pass

def child():
    print("Child PID:", os.getpid())

if __name__ == "__main__":
    if os.name == "nt":
        print("fork is not available on Windows; skipping demo.")
    else:
        mp.set_start_method("fork", force=True)

        t = threading.Thread(target=thread_work)
        t.start()

        # While thread is running, we fork
        p = mp.Process(target=child)
        p.start()
        p.join()

        t.join()
        print("Program finished (but this pattern is unsafe).")
```

On many systems this *appears* to work. The problem: the child inherits **only the forking thread**, with copied locks and inconsistent internal state. In more complex programs this manifests as “random” deadlocks and crashes. The docs literally say: **don’t fork a multi-threaded process without exec**.

### Example 5 – Safe Alternative: Use `spawn` or `forkserver`

```python
# Example 5: Safe start methods with threads
import multiprocessing as mp
import threading
import time

def thread_work():
    time.sleep(1)

def child():
    print("Child ran safely under spawn/forkserver")

if __name__ == "__main__":
    # Use a safe method *before* creating threads
    try:
        mp.set_start_method("forkserver")
    except ValueError:
        mp.set_start_method("spawn")

    t = threading.Thread(target=thread_work)
    t.start()

    ctx = mp.get_context()
    p = ctx.Process(target=child)
    p.start()
    p.join()
    t.join()
```

---

## 7. OS Scheduling, Affinity, and Start Methods in One Sentence

> The OS scheduler moves things around freely; you constrain it with affinity only when you have evidence, and you choose `spawn`/`fork`/`forkserver` to trade off startup speed against safety and inherited state.

### Example 6 – Inspecting the Default Start Method

```python
# Example 6: See what your platform uses by default
import multiprocessing as mp

if __name__ == "__main__":
    print("Default start method:", mp.get_start_method())
```

Typical outputs:

* Linux: `fork`
* macOS: `spawn`
* Windows: `spawn`

---

## 8. Cost Model: Control Has a Price

* **Affinity**

  * Small overhead to set.
  * May improve cache locality and reduce migrations.
  * May hurt if you restrict CPUs too much or fight the OS.

* **fork**

  * Very fast startup via copy-on-write.
  * Risky with threads, bindings that keep internal state, open FDs, etc.

* **spawn**

  * Startup cost = new interpreter + imports + unpickling.
  * Safe: no weird inherited locks; great default for long-lived workers.

* **forkserver**

  * One-time cost to start a “clean” server process.
  * Fast subsequent forks from that clean state; safer with libraries.

### Example 7 – Start Method Overhead (Simple)

```python
# Example 7: Start method overhead for empty work
import multiprocessing as mp
import os
import time

def noop(_):
    return 0

def measure(method: str):
    ctx = mp.get_context(method)
    start = time.perf_counter()
    with ctx.Pool(4) as pool:
        list(pool.map(noop, range(50)))
    return time.perf_counter() - start

if __name__ == "__main__":
    methods = ["spawn"]
    if os.name != "nt":
        methods += ["fork", "forkserver"]

    for m in methods:
        print(f"{m:9}: {measure(m):.3f} s")
```

---

## 9. Practical Design Recipe

> **“Let the OS do its thing until you see real contention. Then tune start method, then affinity — in that order.”**

```text
1. First: pick a safe start method

   - Cross-platform, threads, complex libs?
       → set_start_method("spawn") explicitly.
   - Linux, pure-Python CPU, no threads?
       → use default ("fork"), or explicitly "fork" via context.
   - Linux + threads + performance-sensitive?
       → try "forkserver": safer than "fork", faster than "spawn".

2. Structure your workers

   - Use ctx = mp.get_context(method) and ctx.Pool/ctx.Process
   - Avoid global mutable state that behaves differently under fork vs spawn.

3. Only then think about affinity

   - On Linux:
       - For quick experiments: run `taskset -c 0-3 python script.py`
       - In code: os.sched_setaffinity(0, {0,1,2,3})
       - Or psutil.Process().cpu_affinity([...])
   - On Windows: psutil’s cpu_affinity is your main in-Python option.
   - On macOS: shrug; the OS largely owns scheduling.

4. Measure everything

   - Compare methods with a small micro-benchmark (like Example 7 or 30).
   - Watch CPU usage and migrations with htop / perf.
   - Don’t keep “optimizations” that don’t move the needle.

5. Avoid the landmines

   - Don’t call fork in a process that already started threads.
   - Don’t mix start methods haphazardly; set it once at startup.
   - Don’t hard-pin to a single core on a busy machine unless you understand the trade-offs.
```

---

## 10. API & Tool Survey

| API / Tool                         | Role                                             | Platform          | Notes                                          |
| ---------------------------------- | ------------------------------------------------ | ----------------- | ---------------------------------------------- |
| `multiprocessing.get_start_method` | Inspect current default                          | All               | Call at runtime                                |
| `multiprocessing.set_start_method` | Set global default (`spawn`/`fork`/`forkserver`) | All               | Call once, inside `if __name__ == "__main__":` |
| `multiprocessing.get_context`      | Create a context with specific start method      | All               | Use `ctx.Pool`, `ctx.Process`                  |
| `os.sched_setaffinity`             | Set allowed CPUs for a process                   | Linux only        | Requires root or CAP_SYS_NICE                  |
| `psutil.Process.cpu_affinity`      | Cross-platform-ish wrapper (Linux/Windows)       | Linux, Windows    | Needs `psutil`                                 |
| `taskset` CLI                      | Start a process with affinity                    | Linux             | `taskset -c 0-3 python script.py`              |
| `numactl` CLI                      | Bind to NUMA node and memory                     | Linux             | Advanced server tuning                         |

---

## 11. Worked Examples (1–30)

All runnable, platform-aware, and avoid unpicklable traps (no lambdas as process targets).

### Example 8 – Inspect Default Start Method

```python
# Example 8: What does this platform default to?
import multiprocessing as mp

if __name__ == "__main__":
    print("Default start method:", mp.get_start_method())
```

### Example 9 – Force `spawn` (Safe Cross-Platform Default)

```python
# Example 9: Explicit spawn (safe on all platforms)
import multiprocessing as mp

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    print("Start method is now:", mp.get_start_method())
```

### Example 10 – `fork` Pool on Linux/Unix

```python
# Example 10: Use fork on a pure-Python CPU workload (Unix only)
import multiprocessing as mp
import os

def work(x):
    total = 0
    for i in range(10**6):
        total += i * x
    return total

if __name__ == "__main__":
    if os.name == "nt":
        print("fork is not available on Windows.")
    else:
        ctx = mp.get_context("fork")
        with ctx.Pool(4) as pool:
            results = pool.map(work, range(4))
        print("Results:", results)
```

### Example 11 – `forkserver` Context

```python
# Example 11: forkserver context (Unix)
import multiprocessing as mp
import os

def work(x):
    return x * x

if __name__ == "__main__":
    if os.name == "nt":
        print("forkserver is not available on Windows.")
    else:
        ctx = mp.get_context("forkserver")
        with ctx.Pool(4) as pool:
            print(list(pool.map(work, range(8))))
```

### Example 12 – Pin Current Process with `os.sched_setaffinity` (Linux)

```python
# Example 12: Pin this process to CPUs 0–1 (Linux only)
import os

if __name__ == "__main__":
    if hasattr(os, "sched_setaffinity"):
        os.sched_setaffinity(0, {0, 1})
        print("Pinned to CPUs 0–1")
    else:
        print("os.sched_setaffinity not supported here")
```

### Example 13 – psutil Affinity (Linux/Windows)

```python
# Example 13: psutil affinity wrapper
import psutil

if __name__ == "__main__":
    p = psutil.Process()
    print("Current affinity:", p.cpu_affinity())
    p.cpu_affinity([0, 1])
    print("New affinity:", p.cpu_affinity())
```

### Example 14 – `taskset` (Conceptual, CLI)

```bash
# Example 14: Run your script pinned to CPUs 0–3 (Linux)
taskset -c 0-3 python your_script.py
```

### Example 15 – `numactl` (Conceptual, CLI)

```bash
# Example 15: Bind to NUMA node 0 (Linux)
numactl --cpunodebind=0 --membind=0 python your_script.py
```

### Example 16 – Lower Process Priority with `os.nice`

```python
# Example 16: Lower this process's priority (Unix)
import os

if __name__ == "__main__":
    try:
        os.nice(10)
        print("New nice value:", os.nice(0))
    except AttributeError:
        print("os.nice not available on this platform.")
```

### Example 17 – Context-Specific Pool

```python
# Example 17: Use a context explicitly instead of global start_method
import multiprocessing as mp
import os

def work(x):
    return x * x

if __name__ == "__main__":
    methods = ["spawn"]
    if os.name != "nt":
        methods += ["fork", "forkserver"]

    for method in methods:
        ctx = mp.get_context(method)
        with ctx.Pool(2) as pool:
            res = list(pool.map(work, range(4)))
        print(method, "→", res)
```

### Example 18 – Threaded Program Using `spawn` Safely

```python
# Example 18: Threaded program using spawn for workers
import multiprocessing as mp
import threading
import time

def thread_task():
    time.sleep(0.5)

def worker(x):
    return x * x

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)

    t = threading.Thread(target=thread_task)
    t.start()

    ctx = mp.get_context()
    with ctx.Pool(4) as pool:
        print(list(pool.map(worker, range(8))))

    t.join()
```

### Example 19 – Fork-After-Threads (Bad Pattern) vs Spawn (Good Pattern)

```python
# Example 19: Good pattern – start method set before threads
import multiprocessing as mp
import threading
import time

def background():
    time.sleep(1)

def child():
    print("Hello from child process")

if __name__ == "__main__":
    # Set safe method up front
    try:
        mp.set_start_method("forkserver")
    except ValueError:
        mp.set_start_method("spawn")

    t = threading.Thread(target=background)
    t.start()

    ctx = mp.get_context()
    p = ctx.Process(target=child)
    p.start()
    p.join()
    t.join()
```

### Example 20 – Simple Affinity in Worker (Linux)

```python
# Example 20: Each worker pins itself (Linux only)
import multiprocessing as mp
import os

def worker(idx):
    if hasattr(os, "sched_setaffinity"):
        # Simple stripe: worker 0 on CPU0, worker 1 on CPU1, etc.
        cpu = idx % os.cpu_count()
        os.sched_setaffinity(0, {cpu})
        print(f"Worker {idx} pinned to CPU {cpu}")
    return idx

if __name__ == "__main__":
    with mp.Pool(4) as pool:
        print(list(pool.map(worker, range(4))))
```

### Example 21 – Watching Scheduler Behavior (Print PIDs & CPUs)

```python
# Example 21: Observe where workers run (Linux)
import multiprocessing as mp
import os
import time

def worker(_):
    pid = os.getpid()
    cpu = "unknown"
    if hasattr(os, "sched_getaffinity"):
        cpu_set = os.sched_getaffinity(0)
        cpu = sorted(cpu_set)
    print(f"PID {pid}, allowed CPUs {cpu}")
    time.sleep(0.2)

if __name__ == "__main__":
    with mp.Pool(4) as pool:
        pool.map(worker, range(8))
```

### Example 22 – Mixing Global & Context (DON’T)

```python
# Example 22: Demonstration of what NOT to do
# (Mixing global set_start_method and contexts randomly)
import multiprocessing as mp

def work(x):
    return x

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    # Don’t do weird combinations like this:
    # ctx = mp.get_context("fork")  # Confusing and error-prone
    ctx = mp.get_context()  # just use the global choice
    with ctx.Pool(2) as pool:
        print(list(pool.map(work, range(4))))
```

### Example 23 – Measuring Effect of Affinity on CPU-Bound Work

```python
# Example 23: Quick affinity vs no-affinity comparison (Linux)
import multiprocessing as mp
import os
import time

def cpu_work(_):
    total = 0
    for i in range(10**7):
        total += i
    return total

def run(label, pin: bool):
    if pin and hasattr(os, "sched_setaffinity"):
        os.sched_setaffinity(0, {0, 1})
    start = time.perf_counter()
    with mp.Pool(2) as pool:
        pool.map(cpu_work, range(2))
    print(f"{label}: {time.perf_counter() - start:.3f} s")

if __name__ == "__main__":
    run("No affinity", pin=False)
    run("Pinned to 0–1", pin=True)
```

### Example 24 – CPU-Bound vs I/O-Bound and Scheduling

```python
# Example 24: OS scheduling impact – CPU-bound vs I/O-bound
import multiprocessing as mp
import time

def cpu_bound(_):
    total = 0
    for i in range(10**7):
        total += i
    return total

def io_bound(_):
    time.sleep(0.5)
    return 1

if __name__ == "__main__":
    with mp.Pool(4) as pool:
        start = time.perf_counter()
        pool.map(cpu_bound, range(4))
        print("CPU-bound pool:", time.perf_counter() - start)

        start = time.perf_counter()
        pool.map(io_bound, range(4))
        print("I/O-bound pool:", time.perf_counter() - start)
```

### Example 25 – Priority Tuning with `psutil` (Nice / Windows priority)

```python
# Example 25: Adjust process priority with psutil
import psutil
import os

if __name__ == "__main__":
    p = psutil.Process()
    print("Current nice/priority:", p.nice())
    try:
        p.nice(10)  # On Unix, increase niceness (lower priority)
        print("New nice:", p.nice())
    except psutil.AccessDenied:
        print("Access denied when changing priority.")
```

### Example 26 – Using a Dedicated Worker Script (Spawn-Friendly)

```python
# Example 26: Spawn-friendly design with a separate module
# main.py
import multiprocessing as mp
from worker_mod import work

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    with mp.Pool(4) as pool:
        print(pool.map(work, range(8)))
```

```python
# worker_mod.py
def work(x):
    return x * x
```

### Example 27 – Observing Memory Behavior: `fork` vs `spawn` (Conceptual)

```python
# Example 27: Large global + fork vs spawn
import multiprocessing as mp
import os

big = bytearray(100_000_000)  # ~100 MB

def worker(_):
    return os.getpid()

def run(method):
    ctx = mp.get_context(method)
    with ctx.Pool(2) as pool:
        print(method, "PIDs:", pool.map(worker, range(2)))

if __name__ == "__main__":
    if os.name != "nt":
        run("fork")       # CoW: children share pages until modified
        run("spawn")      # Each child allocates its own copy when needed
    else:
        run("spawn")      # Only method available
```

### Example 28 – Don’t Fork Inside a Worker (Anti-Pattern)

```python
# Example 28: Do not fork inside pool workers
import multiprocessing as mp
import os

def inner():
    print("Inner PID:", os.getpid())

def bad_worker(_):
    # Spawning processes inside worker processes → complexity/max PIDs
    p = mp.Process(target=inner)
    p.start()
    p.join()

if __name__ == "__main__":
    with mp.Pool(2) as pool:
        pool.map(bad_worker, range(4))
```

### Example 29 – Safer Topology: Supervising Process + Pool

```python
# Example 29: Supervised topology instead of recursive forks
import multiprocessing as mp

def worker(x):
    return x * x

def supervisor():
    with mp.Pool(4) as pool:
        return pool.map(worker, range(8))

def run_supervisor():
    print("Results:", supervisor())

if __name__ == "__main__":
    # One extra process supervises; no recursive forking
    ctx = mp.get_context("spawn")
    p = ctx.Process(target=run_supervisor)
    p.start()
    p.join()
```

### Example 30 – Universal Start-Method Benchmark Template

```python
# Example 30: Benchmark start methods for your workload
import multiprocessing as mp
import os
import time

def cpu_work(_):
    total = 0
    for i in range(10**7):
        total += i
    return total

def benchmark(method: str):
    ctx = mp.get_context(method)
    start = time.perf_counter()
    with ctx.Pool(4) as pool:
        pool.map(cpu_work, range(4))
    elapsed = time.perf_counter() - start
    print(f"{method:9}: {elapsed:.3f} s")

if __name__ == "__main__":
    methods = ["spawn"]
    if os.name != "nt":
        methods += ["fork", "forkserver"]

    for m in methods:
        benchmark(m)
```

---

## 12. Pre-Core Quiz

1. `fork` safe after creating threads? → No  
2. `spawn` default on Windows? → Yes  
3. Affinity reduces cache misses? → Yes  
4. `forkserver` preloads interpreter? → Yes  
5. OS migrates threads freely by default? → Yes  

## 13. Post-Core Reflection

Open your parallel code.

Check start method and affinity.

Force `spawn` or `forkserver`.

Pin workers if cache-bound.

Measure.

Did you avoid a deadlock or gain 20% speed?

You now own **OS-level parallel performance** in Python.

**Next:** Core 10 – Debugging Crashes, Hangs, and Zombie Processes.
