# Worked answers — Containers as Linux process isolation

These are worked engineering arguments, not slogans. Compare the conclusion, the mechanism that supports it, the counterexample it excludes, and the evidence that would make the decision reviewable.
## 1. A process has a private PID namespace but shares the host network namespace. State exactly what is and is not isolated.

The process sees a separate PID tree and can appear as PID 1, while host processes outside the namespace are not enumerated through that PID view. Network identity is still shared: the process sees the host interfaces, routes, listening sockets, and network-namespace firewall state. It can bind addresses and ports according to its credentials in that shared stack. PID isolation therefore does not imply port isolation or network-policy isolation.

## 2. Compare a user-namespace mapping of container UID 0 to host UID 100000 with a direct UID 0 mapping. Which risks change, and which remain?

Mapping container UID 0 to host UID 100000 makes namespace-root operations occur under an unprivileged host identity. A namespace escape that does not also break the user-namespace boundary is less likely to yield host root. The mapping does not remove shared-kernel attack surface, dangerous mounted files, runtime-daemon compromise, or capabilities granted in a parent namespace. Filesystem ownership and subordinate-ID configuration also become operational dependencies.

## 3. Explain why a cgroup memory maximum is not the same as a memory reservation.

A maximum rejects or reclaims memory use beyond a ceiling and may lead to cgroup-local OOM killing. It does not guarantee that the memory will be available when needed. Other cgroups and the host can create pressure first. Reservation is a scheduling or capacity commitment; a limit is an enforcement boundary. Course 3 can enforce a limit, while a later scheduler must decide whether enough capacity exists.

## 4. Atlas runs as UID 65532 but receives `CAP_DAC_OVERRIDE`. What filesystem assumption has been weakened?

The capability permits bypassing many discretionary read, write, and execute permission checks. The claim “UID 65532 cannot read root-owned files because mode bits deny it” is no longer reliable. The process still lacks every root power, but least-privilege review must treat the capability as authority, not be distracted by the numeric UID.

## 5. A workload writes to `/tmp`, `/var/cache/atlas`, and `/var/lib/atlas/results`. Classify the paths and design a read-only-root mount plan.

`/tmp` is ephemeral and can be a bounded tmpfs. `/var/cache/atlas` is recomputable cache and can be a separate ephemeral writable mount, also bounded. `/var/lib/atlas/results` is durable business state and must be mounted from separately owned persistent storage with UID/GID 65532 access. The remainder of the image root stays read-only. The plan should specify cleanup, capacity, and behavior when each writable mount fills.

## 6. Why can shell-form `CMD` make graceful shutdown unreliable?

Shell form inserts `/bin/sh -c` as the initial process. A runtime SIGTERM may reach the shell rather than the application, and shells differ in whether they forward signals and wait for children. Exec form starts the application directly as PID 1. If a shell is genuinely needed, it should `exec` the final process or use a supervised entrypoint with explicit signal behavior.

## 7. A team says, “The container is safe because it has no shell.” Give four counterexamples.

The workload may still contain an exploitable application, a language runtime capable of executing code, writable host mounts, excessive capabilities, an exposed container socket, or secrets in readable files. An attacker does not need `/bin/sh` to invoke syscalls or network clients. Removing the shell can reduce convenience and attack surface, but it is not a security boundary.

## 8. When would a lightweight VM-backed runtime be preferable to a conventional shared-kernel runtime?

Choose it when tenant separation requires a distinct kernel boundary, workloads run untrusted code, kernel-version independence matters, or platform risk policy does not accept shared-kernel isolation. The cost is usually more startup time, memory, operational complexity, and reduced access to some host integrations. The choice should follow a threat and workload model, not a slogan about “stronger isolation.”

## 9. Design an observation that proves Atlas is PID 1 inside its namespace without assuming the host PID.

Run a probe inside the namespace that reads `/proc/self/status` or calls `getpid()` and records `1`. Separately record the process’s host PID from the parent runtime. Showing both values proves the namespace translation. Merely seeing PID 1 in one command is weaker because the command itself might be in the host namespace or the observation source may be ambiguous.

## 10. A PID limit is 100. The application uses eight processes and twelve threads per process. Explain the likely failure.

The cgroup `pids.max` counts tasks, including threads. Eight processes with twelve threads each can require roughly ninety-six tasks before helper processes, runtime threads, or temporary workers. A limit of 100 leaves almost no headroom. Thread or process creation will fail with a resource error even though the team may believe only eight “processes” exist.

## 11. Distinguish an image default from an enforced runtime control, using the runtime user as the example.

`USER 65532` in image configuration is a default consumed by runtimes. A caller can override it. An admission or runtime policy that rejects UID 0 and configures UID 65532 is enforcement. Effective evidence inspects the running process credentials. The image default, policy decision, runtime configuration, and observed process state are separate records.

## 12. Write a bounded isolation claim for Atlas that is strong enough to be useful and narrow enough to be honest.

A defensible claim is: “Atlas API and worker run as mapped UID/GID 65532 in private PID, mount, UTS, IPC, and network namespaces; have an empty capability set, `no_new_privs`, a read-only image root, bounded tmpfs and persistent state mounts, and cgroup CPU/memory/PID controls. They share the host kernel, depend on the runtime and kernel, and are not claimed safe for mutually hostile tenant code.”

## Continue

- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
