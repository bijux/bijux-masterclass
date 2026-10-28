# Manifest review checklist

## Identity and ownership

- exact API version and kind;
- namespace and stable labels;
- immutable image digest;
- selector matches template;
- owner and field manager identified;
- finalizers have cleanup owners.

## Runtime contract

- non-root user/group;
- no privilege escalation;
- read-only root filesystem;
- dropped capabilities;
- seccomp profile;
- explicit writable mounts;
- configuration and secret sources;
- service-account token only if needed.

## Resources and lifecycle

- requests and limits supported by evidence class;
- startup/liveness/readiness questions are distinct;
- termination grace and drain behavior align;
- rollout integers are computed;
- PDB and topology constraints are feasible.

## Evidence boundary

- networking and storage claims belong to their owning courses;
- local-cluster evidence is labelled local;
- optional tool absence is recorded as not executed;
- mutable tags, hidden credentials, and unsupported production claims reject release.
