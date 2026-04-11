# Course Map

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Orientation"]
  page["Course Map"]
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

Use this page when you need the whole course visible on one screen before you choose a
reading path. The goal is to stop the program from feeling like ten isolated topics.

## Arc 1: truthful graph thinking

Modules 01 to 02 establish the build graph as the course's semantic floor.

- Module 01 teaches targets, prerequisites, recipes, and rebuild truth.
- Module 02 teaches parallel safety, structure, and the failure classes that appear when
  the graph is stressed.

Leave this arc able to explain why a rebuild happened and why `-j` can expose graph lies.

## Arc 2: production discipline

Modules 03 to 05 turn correctness into a maintenance habit.

- Module 03 teaches deterministic targets, selftests, and diagnostics.
- Module 04 teaches semantics under pressure: precedence, includes, and rule behavior.
- Module 05 teaches portability, hardening, and semantically relevant non-file inputs.

Leave this arc able to debug a build with evidence instead of folklore.

## Arc 3: system design and release trust

Modules 06 to 08 scale the build into a real engineered surface.

- Module 06 teaches generated files and pipeline boundaries.
- Module 07 teaches layered includes, macros, and stable build APIs.
- Module 08 teaches release surfaces, manifests, and trustworthy publication.

Leave this arc able to explain which surface is public, which is internal, and why.

## Arc 4: operations and governance

Modules 09 to 10 finish with long-lived ownership judgment.

- Module 09 teaches observability, performance, and incident response.
- Module 10 teaches migration, governance, and tool-boundary decisions.

Leave this arc able to review a real Make system and justify what should change next.

## Route markers

- Read [First-Contact Map](first-contact-map.md) when you need the smallest honest
  starting route.
- Read [Mid-Course Map](mid-course-map.md) when Modules 01 to 03 already feel stable and
  you need the bridge into semantics under pressure, hardening, release trust, and
  incidents.
- Read [Mastery Map](mastery-map.md) when the pressure is stewardship, migration, or
  long-lived trust review.
