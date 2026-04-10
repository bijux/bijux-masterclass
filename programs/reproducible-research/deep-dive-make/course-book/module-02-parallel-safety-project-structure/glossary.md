# Glossary

This glossary keeps the language of Module 02 stable.

| Term | Meaning in Module 02 |
| --- | --- |
| convergence | The build reaches a stable state where a repeated successful run has nothing left to do. |
| order-only prerequisite | A prerequisite that enforces existence or sequencing without making ordinary timestamp changes trigger rebuilds. |
| parallel safety | The condition where parallel execution changes speed but not build meaning. |
| recursive make | Splitting the build into separate make processes instead of keeping one top-level DAG. |
| repro pack | A set of intentionally broken Makefiles used to practice race diagnosis and repair. |
| runnable target | A target whose prerequisites are already up to date and which Make may schedule now. |
| selftest | A build-system test that proves properties such as convergence and serial/parallel equivalence. |
| serial/parallel equivalence | The requirement that declared artifacts match whether the build runs under `-j1` or `-jN`. |
| shared append | Multiple recipes appending to the same file, which makes the output nondeterministic. |
| single top-level DAG | One visible dependency graph owned by a top-level build entry point. |
