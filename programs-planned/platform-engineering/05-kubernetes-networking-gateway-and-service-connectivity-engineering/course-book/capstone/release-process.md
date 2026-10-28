# Capstone release process

The release gate is categorical.

## Blocker gates

A candidate fails when it:

- changes the predecessor workload without an approved cross-course decision;
- uses mutable image identity;
- has no effective policy enforcement evidence;
- permits broad unowned egress;
- cannot resolve Gateway references;
- disables TLS verification;
- loses required client or workload identity semantics;
- omits the Course 6 dependency handoff;
- labels local evidence as production evidence.

## Review gates

A candidate can require review when a supported implementation feature is non-portable, a real environment proof is pending, or the architecture adds a mesh, FQDN policy, backend TLS, or another operationally significant extension.

## Accepted release

The accepted candidate includes exact inputs, proof results, environment boundaries, cleanup, and a content-addressed handoff. It does not claim that unexecuted cloud behavior passed.
