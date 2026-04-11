# Module 02: Data Identity and Content Addressing

Module 02 turns the first big DVC claim into something concrete:

paths are not identity.

If a workflow still treats `data/train.csv` as if the filename itself were the truth, the
rest of the program will stay brittle. Pipelines, experiments, release bundles, and
recovery drills all depend on a more durable idea:

- identity comes from content, not location
- mutable workspace files are not the same thing as authoritative recorded state
- caches and remotes are part of the trust model, not implementation trivia

This module is where learners stop saying "the file is over there" and start saying "the
system is claiming these exact bytes."

The capstone corroboration surface for this module is the set of files and review routes
that separate state layers and recovery: `dvc.lock`, `publish/v1/`, `make state-summary`,
`make recovery-review`, `docs/STATE_LAYER_GUIDE.md`, and `docs/RECOVERY_GUIDE.md`.

## Why this module exists

Many teams can describe where a file lives today and still cannot answer:

- whether the same bytes existed last month
- which copy is authoritative
- how a lost workspace gets rebuilt honestly
- why a renamed file can still represent the same data

This module repairs that confusion by replacing location-based thinking with
content-based identity and explicit state layers.

## Study route

```mermaid
flowchart LR
  overview["Overview"] --> core1["Core 1: paths are locators"]
  core1 --> core2["Core 2: content addressing and pointer files"]
  core2 --> core3["Core 3: workspace, Git, cache, remote, publish"]
  core3 --> core4["Core 4: add, push, pull, checkout as state moves"]
  core4 --> core5["Core 5: failure, recovery, and trust"]
  core5 --> example["Worked example"]
  example --> practice["Exercises and answers"]
  practice --> glossary["Glossary"]
```

Read the module in that order the first time.

If the problem is already partly clear, use this shortcut:

- open Core 1 when the main confusion is "why isn't the path enough?"
- open Core 2 when the main confusion is "what does DVC actually record?"
- open Core 3 when the main confusion is "which copy is authoritative?"
- open Core 4 when the main confusion is "what is `dvc add` or `dvc pull` really doing?"
- open Core 5 when the main confusion is "how does this help recovery rather than folklore?"

## Module map

| Page | Purpose |
| --- | --- |
| `index.md` | explains the module promise and study route |
| `paths-are-locators-not-data-identity.md` | teaches why filenames and directories are not durable identity |
| `content-addressing-cache-and-pointer-files.md` | teaches how DVC records content identity and references it |
| `workspace-git-cache-remote-and-published-state.md` | teaches how the major DVC state layers differ |
| `dvc-add-push-pull-and-checkout-as-state-moves.md` | teaches the main DVC commands as movements between state layers |
| `failure-modes-recovery-and-trust.md` | teaches how identity and recovery failures should be interpreted |
| `worked-example-restoring-a-dataset-after-local-loss.md` | walks through one realistic recovery-oriented identity story |
| `exercises.md` | gives five mastery exercises |
| `exercise-answers.md` | explains model answers and review logic |
| `glossary.md` | keeps the module vocabulary stable |

## What should be clear by the end

By the end of this module, you should be able to explain:

- why a path is only a locator and not the identity of the data
- how content addressing changes the trust story
- how workspace, Git, cache, remote, and published state differ
- what `dvc add`, `dvc push`, `dvc pull`, and `dvc checkout` actually move or restore
- how identity and recovery failures should be read without mysticism

## Commands to keep close

These commands form the evidence loop for Module 02:

```bash
make -C capstone state-summary
make -C capstone manifest-summary
make -C capstone recovery-review
```

The point is not to memorize commands. It is to tie each state layer to a concrete file or
bundle so the learner stops treating the repository as one undifferentiated blob.

## Capstone route

Use the capstone only after the state layers are already legible in your head.

Best corroboration surfaces for this module:

- `capstone/dvc.lock`
- `capstone/publish/v1/manifest.json`
- `capstone/docs/STATE_LAYER_GUIDE.md`
- `capstone/docs/RECOVERY_GUIDE.md`
- `capstone/docs/PUBLISH_CONTRACT.md`
- `capstone/Makefile`

Useful proof route:

```bash
make -C capstone state-summary
make -C capstone manifest-summary
make -C capstone recovery-review
```

The point of that route is not to admire the capstone. It is to practice naming which
layer is authoritative for which fact before trusting what you see.
