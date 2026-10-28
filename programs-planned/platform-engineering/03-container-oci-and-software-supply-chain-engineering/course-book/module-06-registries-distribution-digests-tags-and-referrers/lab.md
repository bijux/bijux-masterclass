# Laboratory — Move a tag without moving the release

## Goal

Push Atlas and its evidence to the local registry, then demonstrate that mutable tag behavior cannot change a digest-pinned deployment.

## Safety boundary

Bind the registry to loopback. Use only synthetic repositories and course fixture credentials. Do not expose the private fixture key or registry port publicly.

## Baseline

Push the accepted API index and its SBOM/provenance artifacts. Create tag `candidate` pointing to the approved digest.

## Hypothesis

A digest pull remains byte-identical after the `candidate` tag is moved, while a tag pull resolves the new object. Evidence discovery is subject-specific.

## Controlled action

1. pull by tag and digest;
2. move `candidate` to a rejected synthetic index;
3. repeat both pulls;
4. enumerate referrers for both subjects;
5. delete only the tag;
6. evaluate the retention policy for the approved digest.

## Oracle

Digest pulls always return the approved bytes. Tag pulls change after movement. Referrers do not cross subjects. Tag deletion does not remove digest reachability under the course retention policy.

## Evidence

Submit HTTP request/response trace, digest verification, before/after tag mapping, referrer lists, and retention decision.

## Interpretation

Explain why registry success is transport evidence and why promotion must occur in a separate policy layer.

## Cleanup

Stop the registry cleanly and delete its temporary storage after preserving the report.

## Completion gate

The deployment record never depends on a mutable tag, and every evidence artifact discovered from the registry is verified against the exact approved subject.

## Continue

- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
