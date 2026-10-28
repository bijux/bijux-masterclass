# TypeScript reference track

The TypeScript track implements the same externally relevant invariants as the
Python track while using idiomatic TypeScript types, modules, maps, and explicit
64-bit-safe representations. It includes signed high-water cursors, a bounded
operation parser, demand analysis, trusted-operation registration,
request-scoped loaders, owner clients, authorization, mutation delegation,
partial responses, subscription resume, transport policy, and release gates.

The semantic core compiles with TypeScript alone and runs its dependency-light
tests through Node's built-in test runner. It is not represented as a complete
GraphQL implementation. `src/adapters/yoga-server.ts` is the optional GraphQL
Yoga integration point for an environment with the declared registry-backed
dependencies.

Run the track from the course root with:

```bash
make typescript-proof
```

Learners using TypeScript as the primary track should compare observable results
with the Python vectors rather than force identical internal class structures.
Operation hashes, cursor population, authorization timing, source call counts,
error paths, and release decisions must agree.
