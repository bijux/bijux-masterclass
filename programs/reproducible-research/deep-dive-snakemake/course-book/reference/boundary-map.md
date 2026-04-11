<a id="top"></a>

# Boundary Map

<!-- page-maps:start -->
## Reference Position

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive Snakemake"]
  program --> reference["Boundary Map"]
  reference --> review["Design or review decision"]
  review --> capstone["Capstone proof surface"]
```

```mermaid
flowchart TD
  question["What kind of trust question is this"] --> surface["Choose the authoritative surface"]
  surface --> check["Read the supporting evidence that should agree with it"]
  check --> decision["Decide whether the boundary is still honest"]
```
<!-- page-maps:end -->

Deep Dive Snakemake only stays reviewable if each kind of question has a clear owner.
Use this page when the repository contains many plausible answers, but you need to know
which surface is actually allowed to settle the question.

---

## Which surface settles which question

| Question | Authoritative surface | Supporting evidence |
| --- | --- | --- |
| what does the workflow claim it will build | `Snakefile` and `workflow/rules/` | `list-rules.txt`, `dryrun.txt` |
| what did checkpoint discovery actually decide | `discovered_samples.json` and the checkpoint-owning rules | `CHECKPOINT_GUIDE.md`, `Snakefile` |
| which differences are execution policy rather than workflow meaning | `profiles/` plus validated config | `PROFILE_AUDIT_GUIDE.md`, dry-run comparisons |
| which files are safe for downstream trust | `FILE_API.md` and `publish/v1/` | `verify.json`, `manifest.json`, `PUBLISH_REVIEW_GUIDE.md` |
| what happened during an executed run | `run.txt`, `summary.txt`, logs, and benchmarks | `EXECUTION_EVIDENCE_GUIDE.md`, `TOUR.md` |
| where should a future change land | repository layer ownership | `ARCHITECTURE.md`, `EXTENSION_GUIDE.md` |

[Back to top](#top)

---

## Common boundary mistakes

| Mistake | Why it lowers trust |
| --- | --- |
| treating a profile change as semantically harmless without comparing dry-runs | policy can leak into meaning without anyone naming it |
| treating checkpoints as permission to rediscover inputs ad hoc | the dynamic part of the DAG becomes harder to audit |
| treating `results/` as if it were the downstream contract | internal workflow state turns into accidental public API |
| treating logs as the only trustworthy evidence | diagnostic output is not a substitute for a published contract |
| treating README prose as stronger than the workflow or the published files | trust shifts from executed evidence back to narration |

[Back to top](#top)

---

## Boundary tests

Ask these before you change a file or trust a claim:

1. which surface is allowed to define the meaning here
2. which artifact or bundle should agree with that source
3. who is the reader: workflow maintainer, operator, or downstream consumer
4. would this still be reviewable if the logs disappeared

[Back to top](#top)

---

## Companion pages

- [`repository-layer-guide.md`](repository-layer-guide.md)
- [`anti-pattern-atlas.md`](anti-pattern-atlas.md)
- [`glossary.md`](glossary.md)

[Back to top](#top)
