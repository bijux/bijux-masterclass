# Build cache key map

A build cache is a claim that an existing output is equivalent to recomputing a build vertex. The claim is sound only when the key includes every input capable of changing the output and the cached result comes from an authorized scope.

## Input classes

| Class | Examples | Common omission |
|---|---|---|
| Source | files, generated sources, submodules | ignored/untracked file not represented |
| Instruction | command, environment, workdir, user | shell expansion or implicit environment |
| Toolchain | compiler, linker, package manager | mutable tool image/tag |
| Platform | OS, architecture, variant, ABI | target architecture omitted |
| Dependency state | lockfile, repository metadata, base digest | floating package index |
| Build capability | network, secret, SSH agent, cache mount | secret-derived output cached globally |
| Builder behavior | frontend version, filesystem normalization | builder upgrade changes layer bytes |

## Scope and authority

A perfect key is still unsafe when an untrusted actor can populate the cache. Separate or authenticate cache namespaces across pull requests, protected branches, release builders, tenants, and architectures. Verify imported cache metadata and do not treat a cache hit as origin evidence.

## Secret mounts

Secret value normally should not become layer output or cache content. The instruction’s behavior may still depend on secret-protected remote state. Decide whether a rotation should invalidate the result and how dependency locks make the fetched result stable. Do not place secret bytes directly in a key that is logged or exported.

## Reproducibility experiment

A controlled rebuild records:

- source and material digests;
- builder identity/version;
- frontend and build arguments;
- platform;
- network policy;
- cache mode (warm/cold and source);
- timestamps and normalization rules;
- resulting layer/config/manifest/index digests.

Equal output under this experiment is evidence for that scope. It is not proof against a compromised builder, hidden network input, or an independently implemented toolchain.

## Cache review questions

1. Which input can change output without changing the key?
2. Who can write the cache namespace?
3. Does platform identity participate in every compiled output?
4. Can secret-bearing files or logs enter cache exports?
5. Can a protected release build consume an untrusted pull-request cache?
6. Is provenance capable of showing whether cache was used and from which scope?
