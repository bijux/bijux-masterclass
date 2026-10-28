# Exercises — Containers as Linux process isolation

Work these problems before opening the answer file. Each question asks for a decision, failure analysis, or evidence argument—not a recalled definition. Record assumptions and name the strongest claim your evidence can support.
## 1. A process has a private PID namespace but shares the host network namespace. State exactly what is and is not isolated.

Write your answer and evidence plan here before comparing it with the worked solution.

## 2. Compare a user-namespace mapping of container UID 0 to host UID 100000 with a direct UID 0 mapping. Which risks change, and which remain?

Write your answer and evidence plan here before comparing it with the worked solution.

## 3. Explain why a cgroup memory maximum is not the same as a memory reservation.

Write your answer and evidence plan here before comparing it with the worked solution.

## 4. Atlas runs as UID 65532 but receives `CAP_DAC_OVERRIDE`. What filesystem assumption has been weakened?

Write your answer and evidence plan here before comparing it with the worked solution.

## 5. A workload writes to `/tmp`, `/var/cache/atlas`, and `/var/lib/atlas/results`. Classify the paths and design a read-only-root mount plan.

Write your answer and evidence plan here before comparing it with the worked solution.

## 6. Why can shell-form `CMD` make graceful shutdown unreliable?

Write your answer and evidence plan here before comparing it with the worked solution.

## 7. A team says, “The container is safe because it has no shell.” Give four counterexamples.

Write your answer and evidence plan here before comparing it with the worked solution.

## 8. When would a lightweight VM-backed runtime be preferable to a conventional shared-kernel runtime?

Write your answer and evidence plan here before comparing it with the worked solution.

## 9. Design an observation that proves Atlas is PID 1 inside its namespace without assuming the host PID.

Write your answer and evidence plan here before comparing it with the worked solution.

## 10. A PID limit is 100. The application uses eight processes and twelve threads per process. Explain the likely failure.

Write your answer and evidence plan here before comparing it with the worked solution.

## 11. Distinguish an image default from an enforced runtime control, using the runtime user as the example.

Write your answer and evidence plan here before comparing it with the worked solution.

## 12. Write a bounded isolation claim for Atlas that is strong enough to be useful and narrow enough to be honest.

Write your answer and evidence plan here before comparing it with the worked solution.

## Continue

- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Chapter](index.md)
