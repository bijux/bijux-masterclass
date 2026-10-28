# Core 10: Debugging Crashes, Hangs, and Zombie Processes

> **Core question:**  
> How do you diagnose and fix crashes, infinite hangs, zombie processes, and resource leaks in parallel Python code — before they take down production?

In **Core 1** you learned *when* to choose threads vs processes.  
In **Core 2** you learned *why* the GIL limits threads.  
In **Core 3** you mastered safe threading.  
In **Core 4** you learned multiprocessing basics.  
In **Core 5** you learned synchronization primitives.  
In **Core 6** you learned cost models.  
In **Core 7** you learned ownership and topologies.  
In **Core 8** you learned determinism.  
In **Core 9** you learned OS scheduling and start methods.  
Here in **Core 10** you learn **debugging**: the tools, signals, and patterns to find crashes, hangs, zombies, and leaks in parallel code.

**Audience:** Developers whose parallel code “works locally” but crashes, hangs, or leaves zombies in CI/production.

**Outcome:** After this file, you should:
1. Diagnose a hang or crash in < 5 minutes with the right tool.
2. Explain in one sentence why `p.join(timeout=...) + p.terminate()` is the safe way to reap children.
3. Kill zombie processes and prevent orphans without rebooting.
4. Spot and fix three classic debugging bugs in code review:
   - Unjoined children → zombies
   - Deadlock from lock ordering
   - Resource leak from daemon workers

---

## 1. Historical & Conceptual Backbone

### 1.1 History in 5 Lines

- 1970s: Unix introduces signals, zombies, and `wait()` for reaping.
- 1990s: Threads add new hang causes (deadlocks); `strace`/`gdb` become essential.
- Python 2.6 (2008): `multiprocessing` inherits OS zombies; no built-in debugging.
- 2010s: `py-spy`, `psutil`, `faulthandler` added for Python-specific insight.
- November 2025: Parallel debugging remains “black magic” — but the tools are mature.

**This entire core focuses on diagnosis and cleanup.**  
Parallel bugs are intermittent — measure, log, and signal.

### 1.2 Debugging Parallel Python in One Precise Sentence

> Parallel crashes/hangs/zombies stem from unsynchronized state, unjoined children, or mishandled signals — diagnose with process trees, signals, and runtime probes.

### 1.3 The One-Sentence Rule

> **Log everything. Join or terminate every child. Handle signals. Measure twice, code once.**

Everything else in this core is a justification and elaboration of that rule.

### 1.4 Positioning of `concurrent.futures`

Executors help debugging:
- Auto-joins on shutdown → fewer zombies.
- Propagates exceptions from workers.
- But hides raw PIDs/signals — drop to `multiprocessing` for deep diagnosis.

For this core: **use raw tools** to see what’s really happening.

---

## 2. Mental Model: Crashes, Hangs, Zombies

### 2.1 One Picture

```text
Main Process
+-----------------------------------------------------------+
|                                                           |
|  [ Thread A ]  [ Thread B ]  ← deadlock / crash           |
|                                                           |
|  [ Child Process 1 ]  ← zombie if not joined              |
|        |                                                  |
|        +-- [ Grandchild ]  ← orphan if parent dies        |
|                                                           |
|  Signals: SIGTERM → graceful, SIGKILL → abrupt            |
|                                                           |
|  Tools:                                                   |
|   ps/tree → process tree                                  |
|   py-spy → stack traces                                   |
|   strace/ltrace → syscalls                                |
|   faulthandler → dump all thread stacks on crash/hang     |
+-----------------------------------------------------------+

Crash: exception / segfault
Hang: deadlock / livelock / blocked on I/O
Zombie: dead child not reaped
Orphan: child survives parent
```

### 2.2 Contract Table

| Symptom              | Likely Cause                             | Diagnostic Tool                    | Fix Pattern                          |
|----------------------|------------------------------------------|------------------------------------|--------------------------------------|
| Process never exits  | Non-daemon threads / unjoined children   | `ps -T` / `htop` / `py-spy top`    | Join or daemon + signal shutdown     |
| Zombie processes     | Child exited, parent didn’t `join()`     | `ps aux | grep Z`                   | `p.join()` or `p.terminate()+join()` |
| High CPU, no progress| Deadlock / busy-wait                     | `py-spy dump` / `gdb`              | Locks with timeout / Condition       |
| Crash in child       | Exception not propagated                 | `faulthandler` / stderr            | `pool.map` or manual exception catch |
| Memory leak          | Daemon holding resources                 | `psutil` / `top`                   | Cooperative shutdown with Event      |
| Orphan processes     | Parent died early                        | `ps -o ppid`                       | Join before exit / supervise         |

---

## 3. Anti-Pattern First: “It works on my machine — ship it (until production zombies eat your server).”

### Example 1 – Unjoined Children → Zombies (Anti-Pattern)

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
    # No join → zombies until main process fully exits
```

**What to observe:**  
`ps aux | grep Z` shows defunct (zombie) processes.

---

## 4. Correct Pattern: Join or Terminate + Join

### Example 2 – Safe Cleanup with Timeout + Terminate

```python
# Example 2: Timeout + terminate → no zombies
from multiprocessing import Process
import time

def hanging():
    time.sleep(100)

if __name__ == "__main__":
    p = Process(target=hanging)
    p.start()
    p.join(timeout=2.0)
    if p.is_alive():
        print("Terminating hanging child...")
        p.terminate()
        p.join()  # Reap zombie
    print("Clean exit")
```

**What to observe:**  
No zombies, even if child hangs.

---

## 5. Correct Pattern: Signal Handling for Graceful Shutdown

### Example 3 – Catch SIGTERM in Workers

```python
# Example 3: Graceful shutdown on SIGTERM
import signal
import time
from multiprocessing import Process

stop = False

def handler(signum, frame):
    global stop
    stop = True
    print("Received SIGTERM")

def worker():
    signal.signal(signal.SIGTERM, handler)
    while not stop:
        time.sleep(0.1)
    print("Worker exiting cleanly")

if __name__ == "__main__":
    p = Process(target=worker)
    p.start()
    time.sleep(1)
    p.terminate()  # Sends SIGTERM
    p.join()
```

**What to observe:**  
Worker exits cleanly on terminate.

---

## 6. Consequence: Bad Cleanup = Production Nightmares

**This section is not about *which* tool to use, but about what happens when you ignore cleanup.**

### Example 4 – Daemon Thread Leak on Abrupt Exit

```python
# Example 4: Daemon holding file → no cooperative cleanup (data may not be flushed)
from threading import Thread
import time

def leaky():
    f = open("/tmp/leak", "w")
    while True:
        time.sleep(1)  # File stays open

if __name__ == "__main__":
    Thread(target=leaky, daemon=True).start()
    time.sleep(2)
    print("Main exits — daemon never flushes/closes explicitly")
```

### Example 5 – Zombie Storm from Many Unjoined

```python
# Example 5: Many unjoined → zombie apocalypse
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
    print("Check `ps aux | grep Z`")
```

---

## 7. Debugging Parallel Python in One Sentence

> Use process trees, signals, and runtime probes to find hangs/crashes; always join or terminate children and handle SIGTERM for graceful shutdown.

### Example 6 – faulthandler for Hangs and Stack Dumps

```python
# Example 6: Use faulthandler to dump stacks if the process hangs
import faulthandler
import time

# If the process is still running after 10 seconds, dump all thread stacks
faulthandler.dump_traceback_later(10, repeat=False)

# Simulate long-running or stuck parallel code
time.sleep(60)  # During debugging, this would cause a traceback dump
```

---

## 8. Cost Model: Debugging Adds Overhead (But Prevents Outages)

* Logging/signals: negligible.
* py-spy sampling: <1% CPU.
* strace: high overhead — use sparingly.
* Manual join/terminate: tiny cost, huge reliability gain.

### Example 7 – py-spy for Live Stack Traces

```python
# Example 7: Install py-spy, run:
# py-spy top --pid <pid>
# or py-spy dump --pid <pid>
print("See live stacks without stopping the process")
```

---

## 9. Practical Design Recipe: “Log everything. Join or terminate every child. Handle signals. Measure twice, code once.”

```text
1. Always:
   - `if __name__ == "__main__":` for multiprocessing
   - Join or (timeout + terminate + join) for every child

2. For threads:
   - Non-daemon → join or use executor
   - Daemon → Event for cooperative shutdown

3. For processes:
   - Use Pool/Executor → auto-cleanup
   - Raw Process → explicit join/terminate

4. Signals:
   - Catch SIGTERM in long-running workers
   - Use Event/Queue for cross-process shutdown

5. Debugging toolkit:
   - ps/tree/htop → process tree
   - py-spy → stack traces
   - faulthandler → dump all thread stacks on crash/hang
   - strace (Linux) → syscalls

6. Benchmark cleanup impact with Example 30
```

---

## 10. API & Tool Survey

| API / Tool                   | Purpose                                  | Platform          |
|------------------------------|------------------------------------------|-------------------|
| `p.join(timeout=)`           | Wait with timeout                        | All               |
| `p.terminate()` / `p.kill()` | Request / forcefully stop child (SIGTERM / SIGKILL on Unix; TerminateProcess on Windows) | All (kill ≥ 3.7) |
| `signal` module              | Handle SIGTERM/SIGINT                    | Unix              |
| `faulthandler`               | Dump tracebacks for all threads on demand or on fatal signals | All               |
| `py-spy`                     | Live sampling profiler                   | All               |
| `psutil`                     | Process tree, memory, CPU                | All               |
| `strace` / `ltrace`          | Syscall tracing                          | Linux             |
| `gdb` / `lldb`               | Attach to hanging process                | Unix/macOS        |

---

## 11. Worked Examples (1–30)

All examples are runnable on their stated platforms (Unix-only ones are marked).

### Example 8 – Basic Join with Timeout + Terminate

```python
# Example 8: Safe join with timeout
from multiprocessing import Process
import time

def hanging():
    time.sleep(100)

if __name__ == "__main__":
    p = Process(target=hanging)
    p.start()
    p.join(timeout=2.0)
    if p.is_alive():
        p.terminate()
        p.join()
    print("Clean exit")
```

### Example 9 – Daemon Process with SIGTERM Handler

```python
# Example 9: Graceful daemon shutdown
import signal
from multiprocessing import Process
import time

def handler(signum, frame):
    print("Received SIGTERM")
    raise SystemExit()

def worker():
    signal.signal(signal.SIGTERM, handler)
    while True:
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=worker, daemon=True)
    p.start()
    time.sleep(1)
    p.terminate()  # Sends SIGTERM
    p.join()
```

### Example 10 – Thread Exceptions Already Print Tracebacks

```python
# Example 10: Thread exceptions already print tracebacks.
# faulthandler is more useful for hangs / low-level crashes.
import threading
import time

def crash():
    raise ValueError("Thread crash")

if __name__ == "__main__":
    threading.Thread(target=crash).start()
    time.sleep(1)
    # Traceback printed to stderr
```

### Example 11 – py-spy Conceptual Usage

```python
# Example 11: py-spy for hangs
print("pip install py-spy")
print("py-spy top --pid <pid>  # live view")
print("py-spy dump --pid <pid> # stack traces")
```

### Example 12 – psutil Process Tree

```python
# Example 12: psutil for process tree (requires psutil)
import psutil
from multiprocessing import Process
import time

def child():
    time.sleep(10)

if __name__ == "__main__":
    p = Process(target=child)
    p.start()
    proc = psutil.Process()
    print("Children:", [c.pid for c in proc.children(recursive=True)])
    p.join()
```

### Example 13 – strace Conceptual

```python
# Example 13: strace for syscalls (Linux)
print("strace -p <pid>  # attach to running process")
print("strace -f -e trace=network python script.py")
```

### Example 14 – Send Custom Signal (Unix only)

```python
# Example 14: Send custom signal (Unix only)
import os
from multiprocessing import Process
import signal
import time

def child():
    def handler(signum, frame):
        print("Custom signal received:", signum)
    signal.signal(signal.SIGUSR1, handler)
    while True:
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=child)
    p.start()
    time.sleep(1)
    os.kill(p.pid, signal.SIGUSR1)
    p.terminate()
    p.join()
```

### Example 15 – Zombie Detection Script

```python
# Example 15: Find zombies (Unix)
import subprocess

def zombies():
    output = subprocess.check_output(["ps", "aux"]).decode()
    zombies = [line for line in output.splitlines() if " Z " in line]
    print(f"Found {len(zombies)} zombies")
    for z in zombies[:5]:
        print(z)

if __name__ == "__main__":
    zombies()
```

### Example 16 – Pool + Timeout Using AsyncResult.get()

```python
# Example 16: Pool + timeout using AsyncResult.get()
from multiprocessing import Pool, TimeoutError
import time

def work(_):
    time.sleep(100)

if __name__ == "__main__":
    with Pool(4) as pool:
        async_result = pool.map_async(work, range(4))
        try:
            async_result.get(timeout=2.0)
        except TimeoutError:
            print("Pool hung; terminating workers")
            pool.terminate()
        # Context manager will join() here
```

### Example 17 – Thread Hang Detection with py-spy

```python
# Example 17: Conceptual py-spy usage
print("py-spy dump --pid <pid> > dump.txt")
print("Look for threads stuck in acquire()")
```

### Example 18 – Decoupled Supervisor Keeps Child Alive After Main Exits (Intentional Orphan)

```python
# Example 18: Decoupled supervisor keeps child alive after main exits (intentional orphan)
from multiprocessing import Process
import time

def child():
    time.sleep(10)

def supervisor():
    p = Process(target=child)
    p.start()
    p.join()  # Supervisor waits
    print("Child finished")

if __name__ == "__main__":
    Process(target=supervisor).start()
    time.sleep(2)
    print("Main exits; supervisor keeps child alive")
```

### Example 19 – Clean Daemon Thread with Event

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

### Example 20 – Process Tree Visualization with psutil

```python
# Example 20: psutil process tree (requires psutil)
import psutil
from multiprocessing import Process
import time

def child():
    time.sleep(10)

if __name__ == "__main__":
    p = Process(target=child)
    p.start()
    proc = psutil.Process()
    print("Children:", [c.pid for c in proc.children(recursive=True)])
    p.join()
```

### Example 21 – SIGINT Handler for Clean Exit

```python
# Example 21: Catch Ctrl+C in multiprocessing
import signal
import multiprocessing as mp
import time

def handler(signum, frame):
    print("SIGINT received")
    raise SystemExit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    with mp.Pool(4) as pool:
        pool.map(time.sleep, [10] * 4)
```

### Example 22 – Zombie Reaper Function

```python
# Example 22 (Unix only): Reap all children
import os
from multiprocessing import Process

def reap_children():
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
            print(f"Reaped zombie PID {pid}")
        except ChildProcessError:
            break

if __name__ == "__main__":
    reap_children()
```

### Example 23 – Hang from Lock in Child

```python
# Example 23: Deadlock in child process
from multiprocessing import Process, Lock

lock = Lock()

def deadlocked():
    with lock:
        with lock:  # Deadlock
            pass

if __name__ == "__main__":
    p = Process(target=deadlocked)
    p.start()
    p.join()  # Hangs forever
```

### Example 24 – Timeout + Terminate for Hanging Child

```python
# Example 24: Safe handling of hanging child
from multiprocessing import Process
import time

def hanging():
    time.sleep(100)

if __name__ == "__main__":
    p = Process(target=hanging)
    p.start()
    p.join(timeout=2.0)
    if p.is_alive():
        p.terminate()
        p.join()
    print("Clean exit")
```

### Example 25 – psutil for Zombie Detection

```python
# Example 25: Detect zombies with psutil
import psutil

def zombies():
    zombies = [p for p in psutil.process_iter(['status']) if p.info['status'] == 'zombie']
    print(f"Found {len(zombies)} zombies")
    for z in zombies[:5]:
        print(z.pid)

if __name__ == "__main__":
    zombies()
```

### Example 26 – terminate() Requests Child Shutdown (Unix: SIGTERM)

```python
# Example 26: terminate() requests child shutdown (Unix: SIGTERM)
from multiprocessing import Process
import time

def child():
    time.sleep(10)

if __name__ == "__main__":
    p = Process(target=child)
    p.start()
    time.sleep(1)
    p.terminate()  # On Unix: sends SIGTERM; on Windows: TerminateProcess
    p.join()
```

### Example 27 – Custom Signal Handler in Child

```python
# Example 27: Child handles SIGTERM
import signal
from multiprocessing import Process
import time

def handler(signum, frame):
    print("Child received SIGTERM")
    raise SystemExit()

def child():
    signal.signal(signal.SIGTERM, handler)
    while True:
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=child)
    p.start()
    time.sleep(1)
    p.terminate()
    p.join()
```

### Example 28 – Debugging with gdb (Conceptual)

```python
# Example 28: Attach gdb to hanging process
print("gdb -p <pid>")
print("thread apply all bt  # backtrace all threads")
```

### Example 29 – faulthandler in Child

```python
# Example 29: faulthandler in child
import faulthandler
from multiprocessing import Process

def crash():
    faulthandler.enable()
    raise ValueError("Child crash")

if __name__ == "__main__":
    p = Process(target=crash)
    p.start()
    p.join()
    # Traceback in stderr
```

### Example 30 – Universal Debugging Template

```python
# Example 30: Template for debugging parallel code
import multiprocessing as mp
import psutil
import faulthandler
import signal
import time
import os

faulthandler.enable()

def handler(signum, frame):
    print("SIGTERM received")
    raise SystemExit()

signal.signal(signal.SIGTERM, handler)

def debug_worker():
    print("Worker PID:", os.getpid())
    time.sleep(10)  # Simulate work

if __name__ == "__main__":
    print("Parent PID:", os.getpid())
    p = mp.Process(target=debug_worker)
    p.start()
    time.sleep(2)
    print("Killing worker...")
    p.terminate()
    p.join()
    print("Clean exit")
```

---

## 12. Pre-Core Quiz

1. Unjoined child → zombie on Unix? → Yes  
2. Daemon thread blocks exit? → No  
3. `p.terminate()` sends SIGTERM? → Yes (Unix); TerminateProcess (Windows)  
4. `faulthandler` can dump tracebacks for all threads on demand or on fatal signals? → Yes  
5. `py-spy` needs process stop? → No  

## 13. Post-Core Reflection

Open your parallel code.

Find **one** unjoined process or daemon worker.

Add join/terminate or Event shutdown.

Run under load.

Did you eliminate a hang or zombie?

You now own **debugging parallel Python** — no more mystery crashes.

**Congratulations: You completed all 10 Cores.**  
You have now mastered the basics of threads and processes in Python.
