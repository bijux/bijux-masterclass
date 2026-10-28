# Guide — Kustomize design and review

Review a Kustomize change at three levels: source structure, rendered resources, and ownership consequences.

## Source structure

A base should contain stable behavior. An overlay should contain real environmental differences. Repeated patches across every overlay indicate a misplaced concern. Remote bases must be pinned and included in render identity.

## Rendered resources

Generate the complete resource set for every affected environment. Compare logical identities, not filenames. Highlight additions, deletions, API-version changes, image digests, selectors, security context, storage references, and protected resources.

## Ownership

Determine which fields the delivery manager will own through Server-Side Apply. A patch that changes another manager's field is an authority migration. Force-conflict is permitted only with explicit review of the transferred paths.

## Review questions

- Did the resource identity change?
- Did a selector or immutable field change?
- Did an overlay alter a platform invariant?
- Did a remote input move?
- Did the renderer version change?
- Did protected-resource eligibility change?
- Is every deletion intentional and authorized?

The review is complete only when the canonical render digest is reproducible in a clean environment.

## Extended reader notes

Review Kustomize in this order: pin every resource source; identify the base API; name each transformer; inspect patches with their semantics; render twice with the pinned native version; reject duplicate identities; compute the canonical digest; validate schemas; and review the final object diff.

Pay special attention to name and namespace transforms, selectors, ServiceAccount and ConfigMap references, list merging, image replacement, generators, and remote bases. A patch that looks small can alter an immutable selector or replace a complete list. Store the renderer version and input subjects with the result.

Use the semantic Atlas renderer to understand invariants and the native tool to verify the full implementation. Differences are investigation triggers, not reasons to discard one result silently.
