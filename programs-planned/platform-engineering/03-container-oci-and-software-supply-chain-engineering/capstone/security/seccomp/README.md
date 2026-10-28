# Seccomp profiles

The runtime profiles contain a deliberately small teaching allowlist. It is
useful for reasoning about default-deny syscall policy, but it has not been
validated against every Python runtime path, architecture, libc, resolver,
TLS, or debugging operation. A real release either uses a reviewed
runtime-default profile or derives and tests a stricter profile from native
execution. Static acceptance of this JSON is not enforcement evidence.
