<a id="top"></a>

# Practice Map


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Practice Map"]
  page["Practice Map"]
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

The course should make it obvious what to build, what to run, and what success looks like
at each stage.

This page collects that information in one place.

---

## Module Practice Surfaces

| Module | Primary practice surface | Main proof loop | Best capstone follow-up |
| --- | --- | --- | --- |
| 01 | tiny local C project | `make --trace all`, `make -q all` | inspect `capstone/Makefile` after local convergence makes sense |
| 02 | scaling simulator plus repro pack | `make -j2 all`, repro execution | inspect `capstone/repro/` and discovery surfaces |
| 03 | production simulator | `make selftest` | compare with `capstone/tests/run.sh` |
| 04 | scratch Makefiles | `make -n`, `make --trace`, `make -p` | use `show-origins` and capstone target surfaces |
| 05 | hardened local build | convergence, trace count, portability checks | inspect `mk/contract.mk` and `mk/stamps.mk` |
| 06 | generator playground | `make --trace all`, `make -q all` | trace `make --trace dyn` in the capstone |
| 07 | layered local project | `make help`, `make -p` | inspect `capstone/mk/*.mk` |
| 08 | local release surface | `make dist`, `make install`, `make -q dist` | inspect `dist` and `attest` in the capstone |
| 09 | measured working build | `make trace-count`, `make -p > build/make.dump` | compare with capstone selftest guardrails |
| 10 | written build review | review rubric plus proof commands | use the capstone as the review specimen |

[Back to top](#top)

---

## Three Reusable Proof Loops

### Truth loop

Use when you are checking whether the graph itself is honest.

```sh
make --trace all
make all
make -q all
```

### Concurrency loop

Use when you are checking whether scheduling changes meaning.

```sh
make clean
make -j1 all
make clean
make -j2 all
```

### Diagnostics loop

Use when you are investigating a confusing behavior.

```sh
make -n <target>
make --trace <target>
make -p > build/make.dump
```

[Back to top](#top)

---

## Best Study Habit

For each module:

1. run the local exercise first
2. write down what the proof command is supposed to demonstrate
3. run the proof command
4. enter the capstone only after the local result is legible

This keeps the course centered on comprehension instead of file tourism.

[Back to top](#top)
