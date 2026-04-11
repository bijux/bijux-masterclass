# Self-Review Prompts

Use this page when you want short prompts that turn DVC concepts into active recall and
design judgment instead of passive recognition.

## State and authority

- Which file is authoritative for declaration here, and which file only records execution?
- What would break if you confused workspace visibility with durable repository truth?
- Which question would force you to read the remote instead of the local cache?

## Comparison and promotion

- Which params and metrics are still safe to compare across runs?
- What belongs in the promoted contract, and what must stay internal repository state?
- What evidence would another maintainer need before trusting a changed run downstream?

## Recovery and stewardship

- What survives local loss because the remote still has authority?
- Which command would you run first for a recovery question, and why not a broader one?
- What change would force you to revisit the promotion or recovery boundary before approval?
