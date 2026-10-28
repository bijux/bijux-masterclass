# Standards, Profiles, and Evidence — API Performance, Capacity, and Traffic Engineering

## Version boundary

| Axis | Value in this course |
|---|---|
| Public interface | 1.2 preserved |
| Interface specification | 3.1.2 baseline preserved |
| Engineering profiles | Security and Reliability Profiles 1.0 preserved; Performance Profile 1.0 introduced |
| Database migration history | 001–009 |

## Four labels for claims

**Normative requirement.** A published specification defines required behavior or document structure.

**Interoperability recommendation.** Several legal choices exist, but one reduces ambiguity across clients, providers, operators, or consumers.

**Course policy.** The capstone adopts a stricter or more specific rule so the design can be reviewed and tested consistently.

**Observed tool boundary.** A pinned tool supports, transforms, partially supports, or rejects a feature. Tool behavior must not be presented as the normative standard.

## Reading standards without wasting time

Start with the chapter’s engineering question. Read the cited normative section needed to settle that question. Write the rule in your own words, one counterexample, and the cheapest oracle that can falsify your implementation. Do not read an entire specification linearly unless you are conducting a broader standards review.

## Evidence boundary

A local structural checker does not establish full standards conformance. A fixture validator does not establish live provider behavior. A passing unit test does not establish process recovery. A local benchmark does not establish production capacity. A broker emulator does not establish a real broker’s retention and failure behavior. Every report must name the evidence class and missing environment explicitly.

## Stable program sources

The course references official specifications and primary project documentation where normative or tool behavior matters. The repository pins the versions used by executable routes. When a living specification advances, update the version ledger, compatibility analysis, examples, and proof expectations together rather than silently changing one citation.
