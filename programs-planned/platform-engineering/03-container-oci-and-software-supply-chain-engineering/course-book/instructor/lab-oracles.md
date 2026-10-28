# Lab oracle guide

A lab oracle must distinguish competing explanations.

## Strong oracle characteristics

- names exact subject and baseline;
- fails for the planted defect;
- preserves raw evidence;
- is independent from the mechanism under test where feasible;
- checks cleanup and negative behavior;
- does not pass on missing execution.

## Examples

| Lab | Weak oracle | Strong oracle |
|---|---|---|
| layer integrity | tool printed success | recomputed bytes/size/digest plus independent parse |
| platform | label says arm64 | ELF architecture plus target evidence class |
| rootless runtime | process UID not zero | inner/outer mapping, capabilities, namespaces, mounts |
| secret hygiene | final root has no token | no token in all layers/history/cache/evidence |
| signing | signature valid | signature + identity + subject + provenance + policy |
| promotion | tag exists | exact target digest/evidence and immutable release record |

## Fault injection

Inject one variable at a time and predict the first failing phase. Restore baseline and rerun after cleanup. If multiple controls fail simultaneously, the lab may show defense in depth but is poor for diagnosing causal understanding.
