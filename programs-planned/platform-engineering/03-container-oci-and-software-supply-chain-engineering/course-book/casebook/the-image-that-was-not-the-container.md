# Incident case — the image that was not the container

## Situation

The Atlas team approved an image after reviewing its Containerfile, package inventory, and scanner report. The image declared `USER 65532`, contained no shell, exposed only port 8080, and had no known critical finding. During a production incident, an operator needed “more visibility” and launched it with host networking, the host PID namespace, a writable host-root bind at `/host`, all Linux capabilities, and the container-engine socket.

The application was then exploited through an unrelated request-parsing defect. The post-incident headline was: “The secure container was compromised.” That sentence directed the review toward image contents and away from the authority that actually mattered.

## Competing explanations

The image review established facts about immutable content and defaults. It did not establish the effective runtime boundary. At launch time the operator supplied a different execution request. That request gave the process:

- host network identity and access to host listeners;
- visibility into host process identifiers;
- a writable path to host files;
- the full capability set;
- an engine API capable of launching additional privileged workloads.

The attacker did not need a shell. Arbitrary code could invoke syscalls directly, modify files through `/host`, inspect process state, or issue engine API requests. The strongest image-level result—non-root default, small filesystem, clean inventory—could not compensate for launch-time authority.

## Evidence reconstruction

A useful investigation preserves evidence in dependency order:

1. the exact image index and platform-manifest digests;
2. the image configuration, including declared user, entrypoint, and history;
3. the runtime create request after every default and override was merged;
4. `/proc` evidence for UID/GID, capabilities, namespaces, mounts, and file descriptors;
5. container-engine and authorization audit records;
6. host filesystem and process changes;
7. the incident timeline, including who approved the debug exception and when it expired.

The scanner report remains valid evidence about components. It is simply not evidence about namespace selection, bind mounts, engine-socket exposure, or effective capabilities.

## Corrective design

Atlas now treats the runtime profile as an independently versioned contract. Policy rejects host PID/network namespaces, privileged mode, broad host mounts, engine sockets, UID 0, undeclared capabilities, and privilege escalation. Emergency diagnosis uses a separate digest-pinned diagnostic workload with the narrowest required namespace access, time-bounded authorization, and recorded operator identity.

The platform also retains an **effective configuration** record. Reviewing image defaults alone is insufficient because engines, orchestrators, and operators can override them.

## Transfer lesson

Container security is a composition:

```text
trusted artifact
+ approved runtime request
+ host enforcement
+ application authority
+ observed effective state
```

The incident occurred because the organization proved only the first term while assuming the rest. The correct statement is not “the image was insecure.” It is “a hardened image was launched under an unauthorized runtime authority profile.”
