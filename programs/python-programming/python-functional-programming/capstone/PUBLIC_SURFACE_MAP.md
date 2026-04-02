# FuncPipe Public Surface Map


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  command["Published command"] --> output["Saved output or terminal surface"]
  output --> owner["Owning guide or package route"]
  owner --> proof["Next proof route"]
```

```mermaid
flowchart LR
  question["What did this command really expose?"] --> output["Name the output or artifact"]
  output --> owner["Trace it to the owning guide or package map"]
  owner --> proof["Escalate only if the current surface is not enough"]
```
<!-- page-maps:end -->

Use this guide when you already ran a published command but still need to know what part
of the capstone you actually learned from it.

## Command to surface map

| Command | Main output | What it exposes | Best next route |
| --- | --- | --- | --- |
| `make inspect` | `summary.txt`, `summary.json`, and the inspection bundle | package groups, test groups, and guide routing as a learning surface | `PACKAGE_GUIDE.md` or `TEST_GUIDE.md` |
| `make test` | pytest terminal output | executable behavior across algebra, domain, boundaries, and interop | `TEST_GUIDE.md` or `PROOF_GUIDE.md` |
| `make verify-report` | `pytest.txt`, `review-summary.txt`, `review-summary.json` | saved executable proof plus the review inventory | `PROOF_GUIDE.md` |
| `make tour` | `package-tree.txt`, `test-tree.txt`, `focus-areas.txt`, and `TOUR.md` | the human walkthrough route through the repository and proof surface | `WALKTHROUGH_GUIDE.md` or `TOUR.md` |
| `make proof` | test, inspect, and tour together | the published learner route end to end | `PROOF_GUIDE.md` |
| `make confirm` | lint, build, verify-report, and proof together | the strongest public contract for the capstone | `PROOF_GUIDE.md` |

## Good questions after every route

- Did this route show repository shape, executable behavior, or the full published proof path?
- Which guide owns the next step if I still need context?
- Which route would be too large for the question I actually have?

## Best companion files

- `COMMAND_GUIDE.md`
- `PROOF_GUIDE.md`
- `PACKAGE_GUIDE.md`
- `TEST_GUIDE.md`
