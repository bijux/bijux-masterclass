# Core 8: Determinism, Ordering, and Reproducibility in Parallel Execution

> **Core question:**  
> Why does the same parallel code give different results on every run — and how do you make it deterministic, ordered, and reproducible without sacrificing performance?

In **Core 1** you learned *when* to choose threads vs processes.  
In **Core 2** you learned *why* the GIL limits threads.  
In **Core 3** you mastered safe threading.  
In **Core 4** you learned multiprocessing basics.  
In **Core 5** you learned synchronization primitives.  
In **Core 6** you learned cost models.  
In **Core 7** you learned ownership and topologies.  
Here in **Core 8** you learn **determinism**: why parallel execution is inherently nondeterministic, how ordering affects results, and techniques to achieve reproducibility without turning parallel code sequential.

**Audience:** Developers whose parallel code “works most of the time” but fails nondeterministically in production or CI.

**Outcome:** After this file, you should:
1. Explain in one sentence why `pool.map` order is preserved but raw threads/processes are not.
2. Make any parallel workload deterministic and reproducible in < 10 lines.
3. Force ordered output or sorted results without blocking parallelism.
4. Spot and fix three classic determinism bugs in code review:
   - Unseeded randomness in workers
   - Race-dependent algorithm logic
   - Assuming execution order matches submission order

---

## 1. Historical & Conceptual Backbone

### 1.1 History in 5 Lines

- 1960s: Early parallel systems show nondeterminism as a core challenge.
- 1990s: Java/Pthreads expose ordering races; “happens-before” formalized.
- 2008: Python `multiprocessing` inherits OS nondeterminism; no built-in ordering guarantees.
- 2010s: `concurrent.futures` adds ordered `map`; scientific Python adopts seeding patterns.
- November 2025: Reproducibility crises in ML/research drive explicit determinism tools.

**This entire core focuses on making chaos predictable.**  
Parallelism is nondeterministic by nature — embrace it or control it.

### 1.2 Determinism in One Precise Sentence

> Parallel execution is nondeterministic because task scheduling, OS preemption, and hardware variability can change interleaving and order on every run.

### 1.3 The One-Sentence Rule

> **Never assume order or timing in parallel code. Seed randomness, sort results, and use deterministic algorithms — or accept nondeterminism.**

Everything else in this core is a justification and elaboration of that rule.

### 1.4 Positioning of `concurrent.futures`

Executors provide partial ordering:
- `ThreadPoolExecutor.map`: preserves iteration order of results.
- `ProcessPoolExecutor.map`: same (since Python 3.7+).
- Raw threads/processes + manual collection: **no order guarantee**.

For this core: **master raw nondeterminism** so executors’ conveniences don’t hide bugs.

---

## 2. Mental Model: Determinism and Ordering

### 2.1 One Picture

```text
Sequential (Deterministic)
task1 → task2 → task3 → task4 → [ Ordered Results ]

Parallel (Nondeterministic)
          task1
task2                task3
               task4
          ↓     ↓        ↓        ↓
      [ Results in arbitrary order ]

Solutions:
1. Pool.map → ordered collection
2. Sort results by input index/key
3. Seed per-worker RNG with worker ID + global seed
4. Use deterministic algorithms (no randomness, no timing assumptions)
```

### 2.2 Contract Table

| Aspect                | Threads / Raw Processes                  | Pool / Executor `.map`                    | Deterministic Techniques                  |
|-----------------------|------------------------------------------|-------------------------------------------|-------------------------------------------|
| Task execution order  | Arbitrary (scheduler-dependent)          | Arbitrary                                 | N/A — cannot control                      |
| Result collection order | Whatever order threads finish            | Preserves input iteration order           | Sort by key/index                         |
| Randomness            | Global RNG shared → races                | Workers inherit RNG state → different     | Seed per-worker with global + worker ID   |
| Timing dependencies   | Dangerous (sleeps, I/O)                  | Still dangerous                           | Avoid; use barriers/conditions            |
| Reproducibility       | Low (hardware, load)                     | Medium (ordered results)                  | High with seeding + sorting               |

---

## 3. Anti-Pattern First: “Parallel code will run in the same order every time (it won’t).”

### Example 1 – Unordered Results from Raw Threads (Anti-Pattern)

```python
# Example 1: Raw threads → nondeterministic order
from threading import Thread
import time
import random

results = []

def task(i):
    time.sleep(random.random() * 0.1)
    results.append(i)

if __name__ == "__main__":
    threads = [Thread(target=task, args=(i,)) for i in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    print("Results:", results)  # Not guaranteed to be [0,1,2,3,4]
```

**What to observe:**  
Order changes every run.

---

## 4. Correct Pattern: Preserve Order with `Pool.map`

### Example 2 – Ordered Results with `Pool.map`

```python
# Example 2: Pool.map preserves input order
from multiprocessing import Pool
import time
import random

def task(i):
    time.sleep(random.random() * 0.1)
    return i

if __name__ == "__main__":
    with Pool() as pool:
        results = pool.map(task, range(10))
    print(results)  # Always [0, 1, 2, ..., 9] — ordered
```

**What to observe:**  
Results match input order, even though workers ran in parallel.

---

## 5. Correct Pattern: Make Randomness Reproducible

### Example 3 – Unseeded Randomness → Nondeterministic

```python
# Example 3: Global random → different every run
import random
from multiprocessing import Pool

def random_task(_):
    return random.randint(0, 100)

if __name__ == "__main__":
    with Pool(4) as pool:
        print(pool.map(random_task, range(8)))  # Different every run
```

### Example 4 – Per-Worker Seeding for Reproducibility

```python
# Example 4: Deterministic randomness based on input index
import random
from multiprocessing import Pool

GLOBAL_SEED = 42

def seeded_random(i):
    random.seed(GLOBAL_SEED + i)
    return random.randint(0, 100)

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(seeded_random, range(8))
    print(results)  # Same every run
```

**What to observe:**  
Same results every run (deterministic per index).

---

## 6. Consequence: Nondeterminism Bites When You Least Expect

**This section is not about *which* technique to choose, but about what happens when you ignore ordering and randomness.**

### Example 5 – Race-Dependent Algorithm (Anti-Pattern)

```python
# Example 5: Algorithm assumes submission order → wrong results
from threading import Thread
import time

results = []

def task(i):
    time.sleep(0.05 * (5 - i))
    results.append(i)

if __name__ == "__main__":
    threads = [Thread(target=task, args=(i,)) for i in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    print("Results:", results)
    if results != list(range(5)):
        print("Algorithm assumed order — failed!")
```

### Example 6 – Fix with Explicit Ordering

```python
# Example 6: Collect with index → sort later
from threading import Thread
from queue import Queue

q = Queue()

def task(i):
    q.put((i, i * i))

if __name__ == "__main__":
    threads = [Thread(target=task, args=(i,)) for i in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()

    items = [q.get() for _ in threads]
    results = [v for i, v in sorted(items)]
    print(results)  # Always ordered squares
```

---

## 7. Determinism in One Sentence

> Parallel code is nondeterministic by default — achieve reproducibility with ordered collection, per-worker seeding, and deterministic algorithms.

### Example 7 – Global RNG Race in Threads

```python
# Example 7: Shared random state → nondeterministic
import random
from threading import Thread

def rand5():
    return [random.randint(0, 100) for _ in range(5)]

if __name__ == "__main__":
    threads = [Thread(target=lambda: print(rand5())) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    # Different every run, interleaved state
```

---

## 8. Cost Model: Determinism Has a Price

* Ordered collection (`map`): slight overhead from result queue.
* Per-worker seeding: negligible.
* Sorting results: O(n log n) post-processing.
* Avoiding randomness: may force slower algorithms.

### Example 8 – Ordered vs Unordered Collection Cost

```python
# Example 8: Pool.map (ordered) vs imap_unordered (faster but unordered)
import time
from multiprocessing import Pool

def work(x):
    time.sleep(0.1 * (10 - x))  # Reverse duration
    return x * x

if __name__ == "__main__":
    data = list(range(10))

    start = time.perf_counter()
    with Pool() as pool:
        results = pool.map(work, data)
    print(f"Ordered map: {time.perf_counter() - start:.3f} s")

    start = time.perf_counter()
    with Pool() as pool:
        results = list(pool.imap_unordered(work, data))
    print(f"Unordered imap: {time.perf_counter() - start:.3f} s")
```

**Key point:**  
Ordered collection waits for slow tasks; unordered can return faster but needs sorting.

---

## 9. Practical Design Recipe: “Never assume order or timing. Seed, sort, and structure for reproducibility.”

```text
1. Accept nondeterminism or control it

2. For ordered results:
   - Use Pool.map / executor.map
   - Or collect (index, result) tuples and sort

3. For randomness:
   - Global seed before spawning
   - Per-worker: random.seed(global_seed + worker_id)

4. Avoid timing assumptions:
   - No "sleep then check"
   - Use Condition / Event / Queue for coordination

5. For reproducibility in research/ML:
   - Seed Python random, NumPy, PyTorch, etc.
   - Use deterministic algorithms (e.g., torch.backends.cudnn.deterministic = True)
   - Fix worker count and start method

6. Benchmark determinism vs performance (Example 30)
```

---

## 10. API Survey

| API / Technique              | Determinism Guarantee                  | Cost                                |
|------------------------------|----------------------------------------|-------------------------------------|
| `Pool.map` / `executor.map`  | Preserves input order                  | Result queue overhead               |
| `imap_unordered` / `as_completed` | Fastest return, arbitrary order   | Requires sorting                    |
| `random.seed` per worker     | Reproducible randomness                | Negligible                          |
| `torch.manual_seed` + deterministic | Full ML reproducibility             | May reduce performance              |
| `sorted(results, key=lambda r: r[0])` | Force order post-collection (when results are `(index, value)` tuples) | O(n log n)                          |

---

## 11. Worked Examples (1–30)

All runnable, guarded, deterministic where claimed.

### Example 8 – Unordered Raw Threads

```python
# Example 8: Raw threads → nondeterministic order
from threading import Thread
import time
import random

results = []

def task(i):
    time.sleep(random.random() * 0.1)
    results.append(i)

if __name__ == "__main__":
    threads = [Thread(target=task, args=(i,)) for i in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    print("Results:", results)  # Not guaranteed to be [0,1,2,3,4]
```

### Example 9 – Ordered with ThreadPoolExecutor.map

```python
# Example 9: Executor.map preserves order
from concurrent.futures import ThreadPoolExecutor
import time
import random

def task(i):
    time.sleep(random.random() * 0.1)
    return i

if __name__ == "__main__":
    with ThreadPoolExecutor() as exe:
        results = list(exe.map(task, range(5)))
    print("Ordered results:", results)  # Always [0,1,2,3,4]
```

### Example 10 – Unordered as_completed + Sort

```python
# Example 10: as_completed → fast but unordered; sort after
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

def task(i):
    time.sleep(random.random() * 0.1)
    return i

if __name__ == "__main__":
    with ThreadPoolExecutor() as exe:
        futures = [exe.submit(task, i) for i in range(5)]
        results = [f.result() for f in as_completed(futures)]
    print("Unordered:", results)
    print("Sorted:  ", sorted(results))
```

### Example 11 – Global Random Race

```python
# Example 11: Shared random state → nondeterministic
import random
from threading import Thread

def rand5():
    return [random.randint(0, 100) for _ in range(5)]

if __name__ == "__main__":
    threads = [Thread(target=lambda: print(rand5())) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
```

### Example 12 – Seeded Global Random

```python
# Example 12: Seed once → reproducible across runs
import random
from threading import Thread

random.seed(42)

def rand5():
    return [random.randint(0, 100) for _ in range(5)]

if __name__ == "__main__":
    threads = [Thread(target=lambda: print(rand5())) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    # Same numbers every run
```

### Example 13 – Per-Worker Seeding in Processes

```python
# Example 13: Deterministic per-worker random with index
import random
from multiprocessing import Pool

GLOBAL_SEED = 42

def seeded_random(i):
    random.seed(GLOBAL_SEED + i)
    return random.randint(0, 100)

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(seeded_random, range(8))
    print(sorted(results))  # Reproducible
```

### Example 14 – NumPy RNG with Global Seed

```python
# Example 14: NumPy random with global seed (often reproducible on simple fork setups;
# prefer per-worker seeding for robust reproducibility)
import numpy as np
from multiprocessing import Pool

np.random.seed(42)

def np_random(_):
    return np.random.rand(3)

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(np_random, range(4))
    print(results)
```

### Example 15 – Deterministic NumPy with Per-Worker Seed

```python
# Example 15: NumPy with explicit per-worker seed
import numpy as np
from multiprocessing import Pool

def seeded_np(i):
    rng = np.random.default_rng(42 + i)
    return rng.random(3)

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(seeded_np, range(4))
    print(results)  # Reproducible
```

### Example 16 – PyTorch Determinism

```python
# Example 16: PyTorch deterministic mode (requires torch)
import torch
from concurrent.futures import ThreadPoolExecutor

def torch_rand(i):
    g = torch.Generator()
    g.manual_seed(42 + i)
    return torch.randn(3, generator=g)

if __name__ == "__main__":
    with ThreadPoolExecutor() as exe:
        results = list(exe.map(torch_rand, range(4)))
    print(results)  # Reproducible
```

### Example 17 – Race-Dependent Sum (Anti-Pattern)

```python
# Example 17: Algorithm assumes order → wrong
from threading import Thread
import time

total = 0

def add(x):
    global total
    time.sleep(0.01)
    total += x

if __name__ == "__main__":
    threads = [Thread(target=add, args=(x,)) for x in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    print("Total:", total)  # May not be 45 due to races
```

### Example 18 – Atomic Sum with Lock

```python
# Example 18: Safe sum with lock
from threading import Thread, Lock
import time

total = 0
lock = Lock()

def add(x):
    global total
    with lock:
        total += x

if __name__ == "__main__":
    threads = [Thread(target=add, args=(x,)) for x in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    print("Total:", total)  # Always 45
```

### Example 19 – Map with Index for Sorting

```python
# Example 19: Collect with index → sort
from threading import Thread
from queue import Queue

q = Queue()

def task(i):
    q.put((i, i * i))

if __name__ == "__main__":
    threads = [Thread(target=task, args=(i,)) for i in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()

    items = [q.get() for _ in threads]
    results = [v for i, v in sorted(items)]
    print(results)  # Always ordered squares
```

### Example 20 – Unordered Pool with Sorting

```python
# Example 20: imap_unordered + sort for deterministic output
from multiprocessing import Pool

def work(x):
    return x * x

if __name__ == "__main__":
    with Pool() as pool:
        unordered = list(pool.imap_unordered(work, range(10)))
    print("Unordered:", unordered)
    print("Sorted:   ", sorted(unordered))
```

### Example 21 – Random Seed Inheritance Issue

```python
# Example 21: Process workers inherit RNG state → same sequences
import random
from multiprocessing import Pool

random.seed(42)

def rand5(_):
    return [random.random() for _ in range(5)]

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(rand5, range(4))
    print(results)  # Often identical sequences
```

### Example 22 – Fix with Explicit Reseed

```python
# Example 22: Reseed in worker
import random
from multiprocessing import Pool

def seeded_rand(i):
    random.seed(42 + i)
    return [random.random() for _ in range(5)]

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(seeded_rand, range(4))
    print(results)  # Different but reproducible
```

### Example 23 – Timing-Dependent Bug (Anti-Pattern)

```python
# Example 23: Sleep-based coordination (DO NOT)
from threading import Thread
import time

ready = False

def worker():
    global ready
    time.sleep(0.5)
    ready = True

def waiter():
    while not ready:
        time.sleep(0.01)  # Busy-wait
    print("Ready!")

if __name__ == "__main__":
    Thread(target=worker, daemon=True).start()
    Thread(target=waiter).start()
    time.sleep(1)
```

### Example 24 – Event for Timing-Independent Coordination

```python
# Example 24: Event instead of sleep/busy-wait
from threading import Thread, Event
import time

event = Event()

def worker():
    time.sleep(0.5)
    event.set()

def waiter():
    event.wait()
    print("Ready!")

if __name__ == "__main__":
    Thread(target=worker, daemon=True).start()
    Thread(target=waiter).start()
    time.sleep(1)
```

### Example 25 – Non-Deterministic Reduce

```python
# Example 25: Floating-point sum order matters
from multiprocessing import Pool

def sum_chunk(chunk):
    return sum(chunk)

if __name__ == "__main__":
    data = [1e-8] * 1_000_000 + [1.0]

    chunks = [data[i::4] for i in range(4)]

    with Pool() as pool:
        partials = pool.map(sum_chunk, chunks)

    total1 = sum(partials)
    total2 = sum(sorted(partials, reverse=True))
    print(f"Total1: {total1:.15f}")
    print(f"Total2: {total2:.15f}")  # Slightly different
```

### Example 26 – Deterministic Reduce with Sorted Partials

```python
# Example 26: Force order for reproducible FP sum
from multiprocessing import Pool

def sum_chunk(idx_chunk):
    idx, chunk = idx_chunk
    return idx, sum(chunk)

if __name__ == "__main__":
    data = [1e-8] * 1_000_000 + [1.0]

    chunks = [(i, data[i::4]) for i in range(4)]
    with Pool() as pool:
        partials = pool.map(sum_chunk, chunks)
    total = sum(v for i, v in sorted(partials))
    print(f"Total: {total:.15f}")  # Always the same
```

### Example 27 – ML Training Non-Reproducibility

```python
# Example 27: Torch training nondeterministic (requires torch)
import torch
from concurrent.futures import ThreadPoolExecutor

def train(i):
    g = torch.Generator()
    g.manual_seed(42 + i)
    model = torch.nn.Linear(1, 1)
    # ... training loop
    return model.weight.item()

if __name__ == "__main__":
    with ThreadPoolExecutor() as exe:
        weights = list(exe.map(train, range(4)))
    print(weights)  # Reproducible with per-worker generator
```

### Example 28 – Hash-Based Sharding (Deterministic Partition)

```python
# Example 28: Deterministic data sharding
from multiprocessing import Pool

def shard(data_key):
    key, data = data_key
    shard = hash(key) % 8
    return shard, data

if __name__ == "__main__":
    items = [("user1", "data1"), ("user2", "data2")]
    with Pool() as pool:
        sharded = pool.map(shard, items)
    print(sharded)  # Same shard assignment every run
```

### Example 29 – Non-Deterministic File Processing Order

```python
# Example 29: File order may vary with imap_unordered
from multiprocessing import Pool
import os

def process(path):
    return os.path.getsize(path), path

if __name__ == "__main__":
    files = ["core1.md", "core2.md", "core3.md"]
    with Pool() as pool:
        sizes = list(pool.imap_unordered(process, files))
    print(sizes)  # Order may vary
```

### Example 30 – Universal Determinism Benchmark Template

```python
# Example 30: Benchmark determinism techniques
import time
import random
from concurrent.futures import ProcessPoolExecutor

def benchmark(name, fn):
    start = time.perf_counter()
    results = fn()
    print(f"{name}: {time.perf_counter() - start:.3f} s")
    print("First 5 results:", results[:5])

def unseeded():
    def task(i):
        random.seed()
        return random.random()
    with ProcessPoolExecutor() as exe:
        return list(exe.map(task, range(100)))

def seeded():
    def task(i):
        random.seed(42 + i)
        return random.random()
    with ProcessPoolExecutor() as exe:
        return list(exe.map(task, range(100)))

if __name__ == "__main__":
    benchmark("Unseeded", unseeded)  # different each run
    benchmark("Seeded  ", seeded)    # identical each run
```

---

## 12. Pre-Core Quiz

1. `pool.map` preserves input order? → Yes  
2. Raw threads guarantee execution order? → No  
3. Global `random.seed()` sufficient for processes? → No (inherited state)  
4. Sorting results makes parallel map deterministic? → Yes (for order)  
5. Timing-based coordination reliable? → No  

## 13. Post-Core Reflection

Open your parallel code.

Find **one** place assuming order or unseeded randomness.

Add explicit seeding or sorting.

Run 10 times.

Did results become identical?

You now own **deterministic parallel execution** in Python.

**Next:** Core 9 – OS Scheduling, Affinity, and Process Start Methods.
