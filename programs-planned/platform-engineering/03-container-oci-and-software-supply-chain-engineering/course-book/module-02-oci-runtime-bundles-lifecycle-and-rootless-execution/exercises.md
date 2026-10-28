# Exercises — OCI runtime bundles and lifecycle

Work these problems before opening the answer file. Each question asks for a decision, failure analysis, or evidence argument—not a recalled definition. Record assumptions and name the strongest claim your evidence can support.
## 1. Distinguish an OCI image layout from an OCI runtime bundle in purpose, structure, and lifecycle.

Write your answer and evidence plan here before comparing it with the worked solution.

## 2. Why does the runtime lifecycle separate `create` from `start`?

Write your answer and evidence plan here before comparing it with the worked solution.

## 3. A state file records PID 4120, but that process exited and the PID was reused. What must a force-delete implementation avoid?

Write your answer and evidence plan here before comparing it with the worked solution.

## 4. Explain how a read-only root can contain writable submounts without contradiction.

Write your answer and evidence plan here before comparing it with the worked solution.

## 5. Design UID/GID mappings so inner UID 65532 owns one host state directory but not the rootfs.

Write your answer and evidence plan here before comparing it with the worked solution.

## 6. A privileged prestart hook reads a bundle annotation and executes it through a shell. Analyze the trust violation.

Write your answer and evidence plan here before comparing it with the worked solution.

## 7. Why can a valid seccomp JSON profile still fail at runtime on another architecture?

Write your answer and evidence plan here before comparing it with the worked solution.

## 8. What evidence distinguishes a rootless workload from a rootless runtime architecture?

Write your answer and evidence plan here before comparing it with the worked solution.

## 9. A network namespace exists but has only loopback. Is network isolation working? Is application connectivity working?

Write your answer and evidence plan here before comparing it with the worked solution.

## 10. Give a safe cleanup order after failure between rootfs mount and process start.

Write your answer and evidence plan here before comparing it with the worked solution.

## 11. Explain why mounting a container-engine socket defeats many other restrictions.

Write your answer and evidence plan here before comparing it with the worked solution.

## 12. Review this profile: UID 65532, writable root, `CAP_SYS_ADMIN`, host PID namespace, 256 MiB memory max. Which property dominates the risk review and why?

Write your answer and evidence plan here before comparing it with the worked solution.

## Continue

- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Chapter](index.md)
