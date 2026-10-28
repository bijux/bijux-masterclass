# Lab reset procedure

1. Stop every local gRPC server and client.
2. Remove `dist/`, `__pycache__/`, `.tmp/`, generated logs, and scratch transfer files.
3. Restore vector and release fixtures from version control.
4. Reset fixture clocks, revocation sets, lifecycle state, and in-memory stores.
5. Verify the Course 6 predecessor handoff.
6. Run the module proof and then `make hygiene-proof`.
