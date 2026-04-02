<a id="top"></a>

# Course Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Course Guide"]
  page["Course Guide"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Deep Dive Make now has enough supporting material that learners need one stable hub for
choosing the right page quickly. The goal is not to memorize Make features. The goal is
to learn how truthful graphs, safe publication, and reviewable proof fit together over a
ten-module sequence.

## Course Spine

The course has four linked layers:

1. entry pages and orientation
2. module work from local build truth to larger build boundaries
3. capstone proof in one executable reference build
4. review surfaces for stewardship, incident response, and migration judgment

## The Four Arcs

### Build truth

Modules 01 to 03 establish the semantic floor:

- why Make is a graph engine instead of a shell convenience layer
- how parallel safety, determinism, and selftests change the meaning of "works"
- how to prove a build claim with native evidence instead of folklore

### Pressure and hardening

Modules 04 to 06 turn the basic graph into something survivable:

- CLI and include behavior stay legible under pressure
- portability, modeled inputs, and failure hygiene become explicit design work
- generated files and multi-output rules get real publication boundaries

### Reusable build surfaces

Modules 07 to 08 move from one honest build to a reusable build system:

- layered includes and build APIs stop large repositories from becoming private languages
- release and publication contracts define what downstream systems may trust

### Incident and governance judgment

Modules 09 to 10 finish the course where long-lived build systems actually fail:

- incidents become observable and reviewable instead of superstitious
- migration and governance decisions stay tied to proof, not preference

## How The Capstone Fits

- Modules 01 to 03 explain the capstone's graph truth, convergence checks, and selftest discipline.
- Modules 04 to 06 explain its failure modeling, portability boundaries, and generated-file handling.
- Modules 07 to 08 explain its layered `mk/` architecture, public targets, and release surfaces.
- Modules 09 to 10 explain its incident bundles, migration judgment, and stewardship rules.

## Support Pages To Keep Open

- [Module Promise Map](module-promise-map.md) when you want the module titles translated into explicit learner contracts
- [Module Checkpoints](module-checkpoints.md) when you need a module-end exit bar
- [Module Dependency Map](../reference/module-dependency-map.md) when the reading order needs justification
- [Command Guide](command-guide.md) when you need the right command surface
- [Proof Ladder](proof-ladder.md) and [Proof Matrix](proof-matrix.md) when you need to size or route proof correctly
- [Capstone Map](capstone-map.md) when you want the repository route by module

## Honest Expectation

If you rush, the course will feel like a pile of edge cases. If you read it in order and
keep the capstone in view, the later modules should feel like consequences of earlier
graph and publication decisions rather than unrelated advanced tricks.

## Best Three Entry Commands

```sh
make PROGRAM=reproducible-research/deep-dive-make capstone-walkthrough
make PROGRAM=reproducible-research/deep-dive-make test
make PROGRAM=reproducible-research/deep-dive-make inspect
```

Use `gmake` inside `capstone/` on macOS, where `/usr/bin/make` is not GNU Make 4.3+.

[Back to top](#top)
