# Containerfile semantics

A Containerfile is a frontend description of a build graph. It is not the image format and not the runtime configuration.

## Review by semantic effect

- `FROM` selects a base subject. Prefer immutable digest and record the human-readable tag separately.
- `COPY`/`ADD` transfer build-context content into a snapshot. Review context authority, ownership, modes, archive/URL semantics, and destination.
- `RUN` executes with build-time authority. Review shell behavior, network, secret/SSH/cache mounts, package state, and generated output.
- `ARG` is build-time input and can leak through history, logs, or output. It is not a secret channel.
- `ENV` becomes image configuration and runtime default. Do not place secrets there.
- `USER`, `WORKDIR`, `ENTRYPOINT`, `CMD`, `EXPOSE`, `HEALTHCHECK`, `STOPSIGNAL`, `VOLUME` create defaults/metadata that runtime policy may override.
- multi-stage `COPY --from` transfers selected output between build authorities; it does not make the builder stage trustworthy automatically.

## Shell and exec forms

Shell form adds shell parsing and often inserts a shell as PID 1 for runtime commands. Exec form preserves argument boundaries and direct signal delivery. Choose deliberately; do not mechanically rewrite commands that genuinely need shell features without understanding expansion/error behavior.

## Review questions

1. Which source files can enter the build context?
2. Which instructions can access network, secrets, SSH, caches, or host integrations?
3. Are base/toolchain/package inputs immutable and policy authorized?
4. Can build-only tools or credentials cross into the runtime stage?
5. Does the final image contain only required runtime content?
6. Do image defaults agree with the Course 2 workload contract?
7. Which claims require inspecting the resulting OCI graph rather than the Containerfile text?

A secure-looking Containerfile is only source-level evidence. Always inspect the produced layers, config, manifest/index, platform binaries, and runtime request.
