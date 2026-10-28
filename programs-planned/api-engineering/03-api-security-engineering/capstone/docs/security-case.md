# Security Case

The security case is the course's argument that the Analysis Runs API satisfies a bounded set of security requirements in a named environment. It is not a statement that the system is invulnerable.

## Claim structure

Every security claim must have six parts:

1. **asset or behavior protected**;
2. **threat and attacker capability**;
3. **security requirement**;
4. **control and ownership boundary**;
5. **executable or reviewable evidence**;
6. **residual risk and operating assumption**.

The machine-readable source is under `capstone/security-case/`. The human-readable working method is taught in Module 01.

## Top-level claims

- Only a trusted, unambiguous HTTP interpretation reaches application code.
- Credentials are accepted only through named channels and validated against an explicit resource-server profile.
- Authorization is default-deny and combines operation permission with tenant, relationship, and resource ownership.
- Hostile representations cannot escape storage roots, cause unbounded parsing, or reach SQL/shell/template interpreters as code.
- Outbound destinations are constrained after URL parsing and DNS resolution; redirects and connected peers remain subject to policy.
- Webhook authenticity, freshness, key identity, and replay state are verified over exact bytes.
- Secrets do not render by default; logs and audit evidence follow explicit data-classification and redaction rules.
- Expensive operations consume named budgets and fail in bounded, contract-compatible ways.
- Security tests include counterexamples and planted defects, not only positive control checks.
- Incident operations can revoke credentials, rotate keys, preserve evidence, issue a compatible release, and rerun the proof ladder.

## Evidence boundary

Dependency-light proofs establish pure logic, vectors, source structure, and deterministic fixtures. They do not establish reverse-proxy behavior on every deployment, live database locking, operated key management, network egress enforcement, or Internet resilience. Those require environment-backed proof and operational ownership.
