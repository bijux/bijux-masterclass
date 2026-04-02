# Deep Dive DVC Capstone

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"] --> program["Deep Dive DVC"]
  program --> capstone["Capstone"]
  capstone --> readme["README"]
  readme --> docs["docs/"]
  readme --> proof["State and review routes"]
```

```mermaid
flowchart LR
  question["Name the current question"] --> route["Choose the smallest capstone route"]
  route --> review["Read the matching guide or bundle"]
  review --> next["Escalate only if the question changes"]
```
<!-- page-maps:end -->

Read the first diagram as the capstone shape. Read the second diagram as the entry rule:
choose the smallest route that answers the current question, then escalate only when the
question changes.

This capstone is the executable reference repository for Deep Dive DVC. It turns the
course's claims about state identity, truthful pipelines, params, metrics, experiments,
promotion, and recovery into one repository that can be inspected end to end. It is not
meant to be a first-contact playground for DVC commands.

## Use this capstone when

- the module idea is already legible and you want executable corroboration
- you need one repository that keeps declaration, recorded state, and promoted contract visible together
- you are reviewing whether a small DVC repository can survive release and recovery pressure honestly

## Do not use this capstone when

- state layers still feel abstract
- you want to browse the whole repository before naming a question
- the strongest proof route feels safer than choosing the right one

## Choose the entry route by question

| If the question is... | Start here | Escalate only if needed |
| --- | --- | --- |
| what this repository promises | `make walkthrough` | `make tour` |
| does the current state still match the declared contract | `make verify` | `make confirm` |
| how should I compare experiment candidates | `make experiment-review` | `make confirm` |
| what survives cache loss and remote restore | `make recovery-review` | `make confirm` |
| what is safe for downstream trust | `make release-review` | `make confirm` |

From the repository root, the matching course-level commands are:

```sh
make PROGRAM=reproducible-research/deep-dive-dvc capstone-walkthrough
make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify
make PROGRAM=reproducible-research/deep-dive-dvc capstone-release-review
```

## First honest pass

1. Run `make walkthrough`.
2. Read [DOMAIN_GUIDE.md](docs/DOMAIN_GUIDE.md).
3. Read [STATE_LAYER_GUIDE.md](docs/STATE_LAYER_GUIDE.md).
4. Read [STAGE_CONTRACT_GUIDE.md](docs/STAGE_CONTRACT_GUIDE.md).
5. Read `dvc.yaml`, `dvc.lock`, and `params.yaml`.
6. Run `make verify`.
7. Read [REVIEW_ROUTE_GUIDE.md](docs/REVIEW_ROUTE_GUIDE.md).

Stop there first. That is enough to see the domain, state boundaries, pipeline contract,
and one bounded proof route without turning the capstone into a browsing exercise.

## What the main targets prove

| Target | What it proves | Why it matters |
| --- | --- | --- |
| `walkthrough` | the learner-facing reading route is bounded and explicit | first capstone contact stays humane |
| `verify` | the current repository state matches the declared contract | proof starts from state truth, not presentation |
| `tour` | the executed proof bundle can be reviewed in one place | learners can inspect the evidence path end to end |
| `experiment-review` | changed params can be compared without mutating baseline meaning | experiments stay bounded |
| `release-review` | the promoted bundle is smaller and clearer than the internal repository | downstream trust has a contract |
| `recovery-review` | remote-backed restoration can be reviewed as evidence, not folklore | recovery is inspectable |
| `confirm` | the strongest built-in review route still passes | final review is stronger than first-pass learning |

## Repository shape

Use these surfaces deliberately:

- `data/raw/` for committed source data
- `dvc.yaml` and `dvc.lock` for declared versus recorded pipeline state
- `params.yaml` for the declared control surface
- `metrics/` for recorded evaluation surfaces
- `publish/v1/` for the downstream release boundary
- `src/incident_escalation_capstone/` for implementation
- `docs/` for bounded review routes

## Capstone docs

All capstone documentation lives under `docs/`:

- [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [BUNDLE_MANIFEST_GUIDE.md](docs/BUNDLE_MANIFEST_GUIDE.md)
- [CHANGE_PLACEMENT_GUIDE.md](docs/CHANGE_PLACEMENT_GUIDE.md)
- [CONTROL_SURFACE_GUIDE.md](docs/CONTROL_SURFACE_GUIDE.md)
- [DATA_PROFILE_GUIDE.md](docs/DATA_PROFILE_GUIDE.md)
- [DOMAIN_GUIDE.md](docs/DOMAIN_GUIDE.md)
- [EXPERIMENT_GUIDE.md](docs/EXPERIMENT_GUIDE.md)
- [MODEL_GUIDE.md](docs/MODEL_GUIDE.md)
- [PREDICTION_REVIEW_GUIDE.md](docs/PREDICTION_REVIEW_GUIDE.md)
- [PUBLISH_CONTRACT.md](docs/PUBLISH_CONTRACT.md)
- [RECOVERY_GUIDE.md](docs/RECOVERY_GUIDE.md)
- [RELEASE_REVIEW_GUIDE.md](docs/RELEASE_REVIEW_GUIDE.md)
- [REVIEW_ROUTE_GUIDE.md](docs/REVIEW_ROUTE_GUIDE.md)
- [SOURCE_BASELINE_GUIDE.md](docs/SOURCE_BASELINE_GUIDE.md)
- [SOURCE_GUIDE.md](docs/SOURCE_GUIDE.md)
- [STAGE_CONTRACT_GUIDE.md](docs/STAGE_CONTRACT_GUIDE.md)
- [STATE_LAYER_GUIDE.md](docs/STATE_LAYER_GUIDE.md)

## Good stopping point

Stop when you can name:

- the current state question
- the smallest route that proves it
- the next stronger route only if the current one stops being enough
