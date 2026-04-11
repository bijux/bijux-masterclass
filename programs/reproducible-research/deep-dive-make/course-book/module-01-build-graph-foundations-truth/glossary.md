# Glossary

This glossary keeps the language of Module 01 stable. Use it when a word starts feeling
fuzzy or overloaded.

| Term | Meaning in Module 01 | Why it matters |
| --- | --- | --- |
| artifact | A file the build intentionally publishes and expects other work to trust. | It separates "real output" from convenience targets like `all` and `clean`. |
| atomic publication | Writing to a temporary path first and moving into the final path only after success. | It prevents failed builds from leaving behind half-truths at trusted paths. |
| convergence | The build reaches a stable state where a repeated run without meaningful change has nothing to do. | It is the shortest practical test for whether the graph is telling the truth. |
| dependency graph | The directed relationship between targets and the prerequisites that justify rebuilding them. | It is the real subject of this module; recipes only make sense inside it. |
| depfile | A file, usually emitted by the compiler, that records discovered header dependencies for later runs. | It turns header usage into evidence Make can reuse. |
| hidden input | A fact that can change output meaning without appearing as explicit build evidence. | Hidden inputs are the usual reason a build works once and lies later. |
| order-only prerequisite | A prerequisite used to guarantee setup without making normal timestamp changes force a rebuild. | It helps with directory creation and similar setup edges that are not semantic inputs. |
| ownership | The rule that a particular recipe is responsible for publishing a specific output path. | Clear ownership makes review and debugging much easier. |
| pattern rule | A rule that describes a family of targets using `%`. | It reduces repetition, but only works well when the mapping stays obvious in review. |
| phony target | A named command target that does not stand for a real file. | Phony targets are useful, but they should not be confused with artifact contracts. |
| prerequisite | An input Make uses when deciding whether a target is out of date. | If an input matters and is not here, the graph is incomplete. |
| recipe | The shell commands that publish or update a target. | Recipes do not define truth by themselves; they act inside the graph contract. |
| semantic input | A fact that changes the meaning of an output even if no source file changed. | Compiler flags and tool versions often belong here. |
| stamp | A file used to represent the state of a semantic input that would otherwise stay invisible. | It gives the graph durable evidence about non-file facts. |
| target | The file or named goal a rule promises to produce or make available. | Thinking of a target as a promise is more useful than thinking of it as a label. |
| truth | The condition where the build graph tells Make enough accurate information to make the right rebuild decisions. | It is the standard by which every Module 01 design choice should be judged. |
