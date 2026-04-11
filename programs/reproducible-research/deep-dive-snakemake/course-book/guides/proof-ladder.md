<a id="top"></a>

# Proof Ladder

Use this page when you know the question but not the right amount of evidence. The common
failure in this program is not too little effort. It is jumping straight to the strongest
bundle, then losing the original claim inside the output.

## Rule for using the ladder

Start at the smallest route that could honestly falsify your claim. Move down only when
the smaller route leaves an important part of the question unanswered.

That means:

- first contact should not start with `proof` or `capstone-confirm`
- a publish-boundary question does not need a full stewardship pass
- a profile question should start with profile evidence, not a generic run log

[Back to top](#top)

## The ladder

| Level | Start here when the question is... | First route |
| --- | --- | --- |
| 1 | what does this repository even claim to do | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` |
| 2 | how does the repository behave when executed once end to end | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` |
| 3 | does the workflow still execute and validate its published outputs | `make PROGRAM=reproducible-research/deep-dive-snakemake test` |
| 4 | do I need a saved publish-contract bundle I can review later | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report` |
| 5 | do I need to compare local, CI, and scheduler policy surfaces | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-profile-audit` |
| 6 | do I need the sanctioned multi-bundle stewardship route | `make PROGRAM=reproducible-research/deep-dive-snakemake proof` |
| 7 | am I ready for the strongest clean-room confirmation pass | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm` |

[Back to top](#top)

## Start points by claim

| Claim | Start here |
| --- | --- |
| "I need a bounded first pass through the capstone." | capstone-walkthrough |
| "I need one executed workflow story with saved evidence." | capstone-tour |
| "I need to know whether the repository still works normally." | test |
| "I need durable publish-contract evidence, not terminal scrollback." | capstone-verify-report |
| "I need to review execution-policy differences across contexts." | capstone-profile-audit |
| "I need the full review route another maintainer could repeat." | proof |
| "I need the strongest confirmation before major change." | capstone-confirm |

[Back to top](#top)

## Bad escalation habits

If you are using the ladder badly, it usually looks like one of these:

- choosing `capstone-confirm` because you feel uncertain, not because the question needs it
- using `proof` when `capstone-verify-report` would answer the publish question directly
- reading large saved bundles before you know what claim they are supposed to support
- treating a stronger route as automatically more honest than a narrower one

The stronger route is only better when it answers a different question.

[Back to top](#top)

## Best companion pages

- [Proof Matrix](proof-matrix.md) when you know the claim but need the first evidence surface
- [Command Guide](../capstone/command-guide.md) when the command layer itself is unclear
- [Capstone Map](../capstone/capstone-map.md) when you know the module but not the repository route

[Back to top](#top)
