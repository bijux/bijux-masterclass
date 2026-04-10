# Glossary

This glossary keeps the language of Module 01 stable. Use it when a word starts feeling
fuzzy or overloaded.

| Term | Meaning in Module 01 |
| --- | --- |
| artifact | A file the build intentionally publishes and expects other work to trust. |
| atomic publication | Writing to a temporary path first and moving into the final path only after success. |
| convergence | The build reaches a stable state where a repeated run without meaningful change has nothing to do. |
| dependency graph | The directed relationship between targets and the prerequisites that justify rebuilding them. |
| depfile | A file, usually emitted by the compiler, that records discovered header dependencies for later runs. |
| hidden input | A fact that can change output meaning without appearing as explicit build evidence. |
| ownership | The rule that a particular recipe is responsible for publishing a specific output path. |
| pattern rule | A rule that describes a family of targets using `%`. |
| phony target | A named command target that does not stand for a real file. |
| prerequisite | An input Make uses when deciding whether a target is out of date. |
| recipe | The shell commands that publish or update a target. |
| stamp | A file used to represent the state of a semantic input that would otherwise stay invisible. |
| target | The file or named goal a rule promises to produce or make available. |
| truth | The condition where the build graph tells Make enough accurate information to make the right rebuild decisions. |
