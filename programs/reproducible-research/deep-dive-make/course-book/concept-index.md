<a id="top"></a>

# Concept Index

This page answers one recurring learner question: "Where in the course do I actually
learn this idea?"

Use it when you remember the concept but not the module, or when you want to revisit one
theme across the whole course.

---

## Core Build Truth

| Concept | Primary modules | Typical proof |
| --- | --- | --- |
| DAG evaluation | 01, 02 | `make --trace all` |
| hidden inputs | 01, 05, 06 | non-convergence after changing an unmodeled input |
| convergence | 01, 03, 05 | `make all && make -q all` |
| depfiles | 01, 03, 06 | touch a header and inspect the rebuild |
| single writer per output | 01, 02, 06 | compare serial and parallel behavior |

[Back to top](#top)

---

## Parallel Safety And Structure

| Concept | Primary modules | Typical proof |
| --- | --- | --- |
| parallel safety | 02, 03 | `make -j2 all` plus artifact equivalence |
| order-only prerequisites | 02, 04 | controlled repro with directory creation or boundary drift |
| recursive make boundaries | 02, 05, 07 | inspect the top-level DAG and jobserver behavior |
| rooted discovery | 02, 03, 07 | sorted discovery audit and stable object mapping |

[Back to top](#top)

---

## Diagnostics And Semantics

| Concept | Primary modules | Typical proof |
| --- | --- | --- |
| `--trace` | 01, 03, 04, 09 | line-by-line causality output |
| `make -p` | 01, 03, 04, 09 | resolved rule and variable dump |
| variable precedence | 04 | `origin`, `flavor`, and controlled overrides |
| includes and restart semantics | 04, 07 | minimal include repro plus inspected database |
| incident ladder | 04, 05, 09 | stepwise diagnosis from preview to repro |

[Back to top](#top)

---

## Boundaries, Packaging, And Stewardship

| Concept | Primary modules | Typical proof |
| --- | --- | --- |
| modeled stamps and manifests | 05, 06, 08 | boundary file change triggers intended rebuild |
| generated files | 06 | trace the generator and its consumers |
| build APIs and public targets | 03, 07, 08 | inspect `help` and stable documented targets |
| release contracts | 08 | `dist`, `install`, and artifact inspection |
| migration and governance | 05, 09, 10 | written review or migration rubric |

[Back to top](#top)

---

## Best Companion Pages

When using this index, the most useful companion pages are:

* [`build-graph-glossary.md`](build-graph-glossary.md)
* [`incident-ladder.md`](incident-ladder.md)
* [`capstone-map.md`](capstone-map.md)
* [`completion-rubric.md`](completion-rubric.md)

[Back to top](#top)
