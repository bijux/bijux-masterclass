<a id="top"></a>

# State Glossary

This glossary keeps the language of the course precise.

The goal is not to define every DVC feature. The goal is to define the state concepts the
course repeatedly depends on for reasoning.

---

## Core State Terms

| Term | Meaning in this course |
| --- | --- |
| state identity | what makes a result, dataset, or artifact the same state over time |
| content addressing | identifying data by bytes rather than path names |
| workspace state | mutable visible files in the working tree |
| Git state | versioned references such as code, `dvc.yaml`, `dvc.lock`, and params |
| cache state | content-addressed local storage used to materialize tracked data |
| remote durability | off-machine storage that survives local cache loss |
| publish boundary | the stable promoted surface that downstream users are allowed to trust |

[Back to top](#top)

---

## Pipeline Terms

| Term | Meaning in this course |
| --- | --- |
| truthful DAG | a pipeline graph that declares the real change surface |
| stage contract | the declared relationship among command, inputs, params, and outputs |
| lock evidence | recorded execution state in `dvc.lock` |
| parameter surface | the declared set of controls that meaningfully affect a run |
| metric surface | the declared comparison outputs that retain semantic meaning |
| baseline state | the trustworthy non-experimental reference point |
| experimental state | a controlled deviation that is comparable but not yet promoted |

[Back to top](#top)

---

## Stewardship Terms

| Term | Meaning in this course |
| --- | --- |
| promotion | turning a state into something downstream users may rely on |
| recovery drill | a practiced proof that state can be restored after loss |
| retention policy | a rule for which historical state remains worth keeping reproducible |
| audit evidence | params, metrics, manifests, locks, and reports that defend a promoted result |
| authoritative state | the layer or artifact the repository treats as truth for recovery or trust |

[Back to top](#top)

---

## Terms Often Confused

| Pair | Course distinction |
| --- | --- |
| path vs identity | a path is a locator; identity is what content and evidence claim the data actually is |
| Git versioning vs DVC state | Git versions references and code; DVC adds data-oriented state contracts |
| baseline vs promoted state | baseline is comparable and stable; promoted state is what downstream consumers may trust |
| tracked metric vs meaningful metric | a metric can be tracked mechanically and still fail semantic comparability |
| remote copy vs durable recovery source | a remote is only authoritative if the repository treats it as part of a rehearsed recovery story |

[Back to top](#top)
