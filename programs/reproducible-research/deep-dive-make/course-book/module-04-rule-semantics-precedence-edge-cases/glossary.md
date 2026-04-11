# Glossary

Use this glossary to keep the language of Module 04 stable while you move between the core
lessons, worked example, and exercises.

The purpose is not to create extra jargon. The purpose is to make sure the same idea keeps
the same name whenever you explain a failure, design a fix, or review a Makefile with
someone else.

## How to use this glossary

If a page feels slippery or a debugging conversation becomes vague, stop and look up the
term that is doing the most work in the argument. A lot of Make confusion disappears once
the team agrees on the right noun.

## Terms in this module

| Term | Meaning in this module |
| --- | --- |
| capability gate | A named condition such as `HAVE_GROUPED_TARGETS` that represents whether a required feature exists. |
| command-line assignment | A variable setting passed at invocation time, such as `make MODE=debug`, which usually has very high precedence. |
| convergence | The property that a successful build reaches a stable state where the next run does not claim more work is needed. |
| deferred variable | A recursively expanded variable defined with `=`, whose value is computed later when it is expanded. |
| deterministic include | A generated included makefile whose contents stay stable when its semantic inputs have not changed. |
| exit code `1` in `-q` mode | The signal that a target would rebuild. In query mode this is not a crash; it is evidence that the target is not up to date. |
| flavor | Make's word for how a variable is stored and expanded, usually `simple` or `recursive`. |
| grouped targets | GNU Make's `&:` form for declaring that several outputs are produced by one logical recipe execution. |
| include order | The order in which makefiles are read, which can affect which assignments win and which rules are in scope. |
| `MAKEFILE_LIST` | The built-in variable that records the makefiles read so far and helps explain include order. |
| origin | Make's word for where a variable came from, such as the command line, environment, makefile, or built-in defaults. |
| phony target | A target declared under `.PHONY`, used for orchestration commands rather than for publishing a real file artifact. |
| publication event | The moment a recipe makes an output or set of outputs real. For multi-output generation, this needs one clear owner. |
| recursive variable | Another name for a deferred variable created with `=`. Its expression is stored and expanded later. |
| restart | What Make does after remaking an included makefile: it reads the makefiles again so evaluation matches the updated build definition. |
| search path | A path resolution policy such as `VPATH` or `vpath` that lets Make find prerequisites outside the literal path named in the rule. |
| simple variable | A variable defined with `:=`, expanded immediately and then stored as a stable value. |
| special target | A built-in control target such as `.PHONY`, `.NOTPARALLEL`, or `.ONESHELL` that changes Make's behavior. |
| stamp | A file that represents a build event or semantic fact when there is no natural single output to hang the dependency on. |
| target-specific variable | A variable value that applies while building a particular target and its prerequisites, rather than globally. |
| trace line | The line emitted by `make --trace` that explains why a target became eligible to run. |
| `VPATH` | A global search-path feature that tells Make where else to look for prerequisites. Useful at times, but easy to make opaque. |

## The vocabulary standard for this module

When you explain an incident after Module 04, aim to say things like:

- "the build did not converge"
- "the environment won because of precedence"
- "the included file was regenerated and Make restarted"
- "the generator needs one publication event"
- "the search path hid which prerequisite actually won"

Those sentences are better than saying only "Make got confused."
