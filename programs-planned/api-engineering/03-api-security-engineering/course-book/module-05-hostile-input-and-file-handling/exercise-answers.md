# Reference Answers — Module 05: Hostile Input and File Handling

Read after attempting all twelve Hostile Input and File Handling exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is OpenAPI validation insufficient for file paths?

**Answer.** A schema can constrain string shape but does not prove decoded/resolved filesystem ancestry, symlink behavior, or race conditions.

## 2. What is the safe role of a client filename?

**Answer.** Display/audit metadata after sanitization; not an authoritative storage location.

## 3. Why check actual bytes when `Content-Length` is present?

**Answer.** The header may be absent, wrong, compressed, or interpreted differently; the receiver must enforce its own bound.

## 4. How does atomic publication reduce risk?

**Answer.** Unvalidated or partial bytes remain private, and the final object appears only after integrity checks in one no-clobber step.

## 5. Why reject symlinks in uploaded archives?

**Answer.** Extraction or later reads can escape the intended root even when member names appear local.

## 6. When is Unicode normalization unsafe?

**Answer.** When the domain treats distinct sequences as meaningful or normalization silently changes user content; equivalence must be an explicit rule.

## 7. What is an archive expansion budget?

**Answer.** A maximum over member count, per-member bytes, total extracted bytes, and optionally compressed-to-expanded ratio.

## 8. How do prepared statements help and not help?

**Answer.** They separate data values from SQL syntax; they do not secure dynamic identifiers, authorization, or semantic validation.

## 9. Why reject dangerous JavaScript keys in a cross-language contract?

**Answer.** They can mutate prototypes or confuse object merging in JS; shared rejection gives both providers one external policy.

## 10. What cleanup proof is required?

**Answer.** Injected failure at every staging step leaves no published object, no orphan temporary file, and no inconsistent database record.

## 11. Trace semantic input and file confinement in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/input_security.py` and `capstone/tracks/typescript-fastify/src/security/input-security.ts`. The required invariant is that decoding, normalization, path resolution, symlink policy, byte budgets, and archive budgets are applied in the correct order.

## 12. Compare semantic input and file confinement across Python and TypeScript

Both tracks must preserve this invariant: decoding, normalization, path resolution, symlink policy, byte budgets, and archive budgets are applied in the correct order. The intentional difference is that path and stream libraries differ; the final confined object and rejection cases must match.
