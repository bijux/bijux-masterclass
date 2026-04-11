# Project Docs

Use this shelf when the question is about the executable Snakemake capstone repository
itself: public file contracts, review bundles, repository architecture, profile drift, or
safe extension. These pages are not another first-contact route into the course. They are
the stable public documentation set for the reference repository that the course points
to.

## Use this shelf when

- you are already inside the capstone repository or one of its saved review bundles
- a course page sends you to a repository-facing document rather than to a lesson
- you need the repository explanation of a file contract, bundle route, or profile surface

## Do not use this shelf when

- you still need the concept introduced for the first time
- you need help choosing which course module or support page to read next
- you are browsing because the repository feels large instead of because the question is specific

## Choose the document by question

| If the question is... | Start here | Then use |
| --- | --- | --- |
| what does this repository promise and how should I enter it | [walkthrough-guide.md](walkthrough-guide.md) | [proof-guide.md](proof-guide.md) |
| which outputs are safe for downstream trust | [file-api.md](file-api.md) | [publish-review-guide.md](publish-review-guide.md) |
| what claim does a bundle or route actually prove | [proof-guide.md](proof-guide.md) | [review-route-guide.md](review-route-guide.md) |
| which repository layer owns this change | [architecture.md](architecture.md) | [extension-guide.md](extension-guide.md) |
| how do local, CI, and scheduler policy differ | [profile-audit-guide.md](profile-audit-guide.md) | [proof-guide.md](proof-guide.md) |
| what does this workflow produce and why does the domain matter | [domain-guide.md](domain-guide.md) | [walkthrough-guide.md](walkthrough-guide.md) |

## Public project-doc set

- [architecture.md](architecture.md) for repository layers, ownership, and review boundaries
- [domain-guide.md](domain-guide.md) for the capstone’s domain story and output meaning
- [extension-guide.md](extension-guide.md) for safe repository evolution
- [file-api.md](file-api.md) for the downstream-facing file contract
- [profile-audit-guide.md](profile-audit-guide.md) for execution-policy review
- [proof-guide.md](proof-guide.md) for claim-to-evidence routing
- [publish-review-guide.md](publish-review-guide.md) for downstream trust review
- [review-route-guide.md](review-route-guide.md) for choosing the smallest honest repository route
- [walkthrough-guide.md](walkthrough-guide.md) for the bounded first pass

## Naming crosswalk

These exported pages use lowercase generated names. Inside the capstone repository, the
source documents appear under `docs/` with uppercase filenames such as
`docs/FILE_API.md`.

## Good stopping point

Stop when you can name the single project doc that owns the current repository question.
If you are still opening several documents at once, the question is probably still too
broad.
