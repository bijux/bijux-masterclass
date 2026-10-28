# Worked Answers — Module 05: Hostile Input and File Handling

Use these solutions to audit your reasoning for **Hostile Input and File Handling**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is OpenAPI validation insufficient for file paths?

A schema can constrain string shape but does not prove decoded/resolved filesystem ancestry, symlink behavior, or race conditions.

The chapter’s decisive distinction is this: Treat an uploaded filename as optional display metadata. Generate storage keys on the server. For any path-like input, percent-decode once where the surrounding protocol requires it, reject control and bidirectional formatting characters, resolve against a fixed root, verify the resolved path remains beneath that root, and define symbolic-link behavior. Recheck at the operation boundary if an attacker can change the filesystem between validation and use.

## 2. What is the safe role of a client filename?

Display/audit metadata after sanitization; not an authoritative storage location.

In the cumulative capstone, the rule becomes concrete: Streaming limits must count actual bytes. Enforce per-file, per-request, per-tenant, and available-storage budgets while reading. Stage to a private location, compute the digest during the stream, verify declared checksum and media policy, then publish atomically. A failure or disconnect removes the staging object; an already-published object with the same digest is an idempotent result only if the bytes match.

## 3. Why check actual bytes when `Content-Length` is present?

The header may be absent, wrong, compressed, or interpreted differently; the receiver must enforce its own bound.

A useful way to reason about the boundary is: Archives require cumulative policy before or during extraction: member count, total uncompressed bytes, per-member size, compression ratio, path confinement, link rejection, nesting depth, and accepted member kinds. Checking only the archive file size does not constrain expansion.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 4. How does atomic publication reduce risk?

Unvalidated or partial bytes remain private, and the final object appears only after integrity checks in one no-clobber step.

The implementation consequence is: An OpenAPI or framework schema proves that a value has an expected syntactic shape. Security depends on what later interpreters do with that value: SQL planners, filesystems, shells, template engines, archive readers, URL parsers, image libraries, and downstream services. Validation must therefore be placed immediately before the interpretation whose assumptions it protects.

## 5. Why reject symlinks in uploaded archives?

Extraction or later reads can escape the intended root even when member names appear local.

The important nuance is: Parameter binding protects SQL values, not SQL structure. Sort columns, directions, table names, operators, and JSON-path expressions require fixed allowlists mapped to trusted fragments. The same rule applies to command-line flags and template names: pass data through typed APIs and never concatenate untrusted structure.

**Evidence.** Run the shared hostile-input corpus through raw edge parsing and both implementations, asserting rejection, bounded resource use, cleanup, and non-leaking problem responses.

## 6. When is Unicode normalization unsafe?

When the domain treats distinct sequences as meaningful or normalization silently changes user content; equivalence must be an explicit rule.

Under concurrency or failure, the distinction becomes: Unicode policy should be narrow and documented. Normalization can make visually equivalent labels compare consistently, but it can also change identifiers. Reject control and bidirectional override characters where they provide no legitimate value. Preserve the original value only if the display requirement is real and the output context handles it safely.

## 7. What is an archive expansion budget?

A maximum over member count, per-member bytes, total extracted bytes, and optionally compressed-to-expanded ratio.

The design remains honest only if: Archives require cumulative policy before or during extraction: member count, total uncompressed bytes, per-member size, compression ratio, path confinement, link rejection, nesting depth, and accepted member kinds. Checking only the archive file size does not constrain expansion.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 8. How do prepared statements help and not help?

They separate data values from SQL syntax; they do not secure dynamic identifiers, authorization, or semantic validation.

The consumer-facing consequence is: Error responses should identify the public field and rule without returning filesystem roots, SQL text, parser stack traces, antivirus output, or snippets of hostile content. Restricted events can record a bounded reason code and pseudonymous correlation data.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 9. Why reject dangerous JavaScript keys in a cross-language contract?

They can mutate prototypes or confuse object merging in JS; shared rejection gives both providers one external policy.

The operational consequence is: The Hostile Input and File Handling cases are bounded course fixtures. Trace the attacker-controlled value through every interpreter, then identify the policy decision and smallest rejection evidence; do not target external systems.

**Counterexample.** A happy-path control accepts semantically hostile input or leaks the evidence needed to refine an attack.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 10. What cleanup proof is required?

Injected failure at every staging step leaves no published object, no orphan temporary file, and no inconsistent database record.

The strongest engineering interpretation is: Streaming limits must count actual bytes. Enforce per-file, per-request, per-tenant, and available-storage budgets while reading. Stage to a private location, compute the digest during the stream, verify declared checksum and media policy, then publish atomically. A failure or disconnect removes the staging object; an already-published object with the same digest is an idempotent result only if the bytes match.

## 11. Trace semantic input and file confinement in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/input_security.py` and `capstone/tracks/typescript-fastify/src/security/input-security.ts`. The required invariant is that decoding, normalization, path resolution, symlink policy, byte budgets, and archive budgets are applied in the correct order.

The defect-oriented view is: An OpenAPI or framework schema proves that a value has an expected syntactic shape. Security depends on what later interpreters do with that value: SQL planners, filesystems, shells, template engines, archive readers, URL parsers, image libraries, and downstream services. Validation must therefore be placed immediately before the interpretation whose assumptions it protects.

## 12. Compare semantic input and file confinement across Python and TypeScript

Both tracks must preserve this invariant: decoding, normalization, path resolution, symlink policy, byte budgets, and archive budgets are applied in the correct order. The intentional difference is that path and stream libraries differ; the final confined object and rejection cases must match.

Across the Python and TypeScript tracks, the invariant is: The Hostile Input and File Handling cases are bounded course fixtures. Trace the attacker-controlled value through every interpreter, then identify the policy decision and smallest rejection evidence; do not target external systems.
