# Capstone Glossary

Use this page when the capstone route pages start to blur together. The capstone shelf is
not a second course book. It is a small set of routes into one executable DVC repository,
and the terms here keep those routes distinct.

## Route terms

| Term | Meaning here | Why it matters |
| --- | --- | --- |
| walkthrough | the bounded first pass through the repository without executing proof routes | keeps first contact human-scale |
| verify | the ordinary executable check that current repository state still matches the contract | separates current-state truth from broader stewardship review |
| verify report | the saved verification bundle for later inspection | helps you review promotion and enforcement without rerunning live |
| experiment review | the focused comparison route for changed runs against the baseline | keeps experiment discussion from mutating the baseline story |
| recovery review | the bundle that shows what survives local loss and remote restore | keeps durability claims distinct from release claims |
| release review | the bundle that audits what downstream users may trust | keeps promoted state distinct from internal repository state |
| confirm | the strongest overall repository confirmation pass | for final confidence after narrower routes already make sense |
| authoritative layer | the file or state surface that should win when surfaces disagree | keeps review attached to state ownership |
| promoted contract | the smaller downstream-facing bundle that another consumer is allowed to trust | prevents the whole repository from masquerading as a release |

## Page names in plain language

| Page | What it helps you do |
| --- | --- |
| [DVC Capstone Guide](index.md) | enter the repository with the right expectations |
| [Capstone Map](capstone-map.md) | choose the right route by module or question |
| [Command Guide](command-guide.md) | pick the right command layer and first command |
| [Capstone File Guide](capstone-file-guide.md) | know which repository files to open first and why |
| [Repository Layer Guide](repository-layer-guide.md) | read the repository by ownership rather than folder names |
| [Experiment Review Guide](experiment-review-guide.md) | compare changed runs without muddying the baseline story |
| [Recovery Review Guide](recovery-review-guide.md) | review restore guarantees and what they depend on |
| [Release Audit Checklist](release-audit-checklist.md) | make one downstream-trust judgment |
| [Release Review Guide](release-review-guide.md) | inspect promoted state as a contract, not a dump |
| [Capstone Review Worksheet](capstone-review-worksheet.md) | review the repository as a steward, not just a reader |

## Reading rule

If two pages sound interchangeable, do not open both. Name the job first: entry,
command choice, state authority, file ownership, experiment review, recovery review,
release review, or stewardship. Then open the one page that owns that job.
