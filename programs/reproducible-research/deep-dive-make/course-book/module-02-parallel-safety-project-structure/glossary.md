# Glossary

This glossary keeps the language of Module 02 stable.

| Term | Meaning in Module 02 | Why it matters |
| --- | --- | --- |
| convergence | The build reaches a stable state where a repeated successful run has nothing left to do. | It tells you the graph can reach a quiet resting state instead of rebuilding forever. |
| order-only prerequisite | A prerequisite that enforces existence or sequencing without making ordinary timestamp changes trigger rebuilds. | It keeps setup edges honest without creating rebuild noise. |
| parallel safety | The condition where parallel execution changes speed but not build meaning. | It is the standard this whole module is trying to enforce. |
| recursive make | Splitting the build into separate make processes instead of keeping one top-level DAG. | It often hides real dependencies behind private sub-builds. |
| repro pack | A set of intentionally broken Makefiles used to practice race diagnosis and repair. | It teaches prediction, not just repair. |
| runnable target | A target whose prerequisites are already up to date and which Make may schedule now. | This is the basic unit of scheduling you need to reason about under `-j`. |
| selftest | A build-system test that proves properties such as convergence and serial/parallel equivalence. | It turns "seems fine" into something the build can defend. |
| serial/parallel equivalence | The requirement that declared artifacts match whether the build runs under `-j1` or `-jN`. | It is the clearest proof that concurrency did not change build meaning. |
| shared append | Multiple recipes appending to the same file, which makes the output nondeterministic. | It violates single ownership of the final file. |
| single top-level DAG | One visible dependency graph owned by a top-level build entry point. | It keeps cross-directory truth visible instead of scattering it. |
| single writer | The rule that one recipe owns one output path. | It is the strongest default defense against parallel races. |
| temporary collision | Two recipes writing the same temporary path. | It is still a multi-writer output bug even if the path is short-lived. |
