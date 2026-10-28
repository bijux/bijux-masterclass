# Analysis RPC capstone

The capstone adds an internal typed RPC control plane to the Analysis Runs Platform inherited from Courses 1–6.

## Responsibilities

- `contracts/` owns proto source, the Editions frontier, descriptors, and compatibility policy.
- `rpc-case/` owns interaction decisions, method catalogue, status, deadline, retry, streaming, version, and consumer policy.
- `tracks/python-grpc/` provides the complete live network reference.
- `tracks/typescript-grpc/` provides the complete dependency-light semantic reference and optional grpc-js dependency profile.
- `shared/` contains cross-language vectors and golden wire fixtures.
- `security/` and `operations/` own method and lifecycle policy.
- `database/` contains migrations 001–015.
- `releases/` and `final-defense/` contain release evidence.
- `handoff/` is the sanitized Course 8 boundary.

## First tour

```bash
make capstone-tour
```

The tour creates and replays a run, observes a state transition, uploads a dataset through client streaming, downloads an artifact through server streaming, and verifies checksums over a real local gRPC channel.
