# Atlas workload sources

The workload contains three small real Go binaries:

- `atlas-api` exposes `/live` and `/ready`, uses bounded HTTP timeouts, and drains on SIGTERM;
- `atlas-worker` models a long-running worker role with signal-aware shutdown;
- `atlas-probe` reports effective runtime identity and filesystem writability.

The binaries are deliberately statically linked (`CGO_ENABLED=0`) and built for amd64 and arm64. The checked semantic builder packages them into scratch-style root filesystems. The Containerfiles provide an independent BuildKit lane and intentionally require the base image digest to be resolved before native promotion.

The probe is verification-only. It must not be deployed as an application service by default.
