# Capstone evidence dossier

The final dossier includes predecessor proof, repository graph, artifact catalogue, render records, diffs, inventory, policy results, sync and health observations, progressive metrics, fleet state, incident timeline, release decisions, and successor handoff.

Secrets are represented only by version identity and policy result. Machine-readable files remain authoritative; the Markdown summary explains their meaning and limitations.

## Extended reader notes

The final dossier should let another engineer reproduce the decision without access to ephemeral CI logs. Include source commit, artifact set, renderer and version, input subjects, canonical render digest, target profiles, object inventory diff, policy outcomes, protected deletions, controller revision, sync and health observations, actual traffic, analysis populations, secret adoption, data phase, restore evidence, approvals, limitations, and decision.

Every record identifies its subject. Evidence about image digest `A` cannot support digest `B`; evidence from staging cannot support a production-specific identity or storage claim unless the invariant is explicitly portable. The dossier is both a release argument and the starting index for incident response.
