# Laboratory 88 — Attack Surface and Supply-Chain Audit

**Course 9 · Module 88: Security and Supply-Chain Engineering**

[Chapter](../../course-book/module-88-security-and-supply-chain-engineering/index.md) · [Workbook](../../course-book/module-88-security-and-supply-chain-engineering/workbook.md) · [MetricRail guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Security and Supply-Chain Engineering**: Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions? The product must make **Identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **threat and dependency dossier** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a deterministic policy checker for two small inventories: external boundaries and dependencies. It does not discover vulnerabilities automatically. It converts declared security expectations into review findings so omissions are visible and repeatable.

A `Boundary` names assets, whether input is untrusted, whether the operation is privileged, and the controls claimed at that boundary. A `Dependency` records exact version text, default-feature use, build-script presence, and review status. `review` returns ordered `Finding`s; `summarize` counts them by severity.

## Inventory integrity

The audit is only meaningful if subjects are unambiguous. Reject or flag:

- empty boundary/dependency names;
- duplicate names;
- empty asset sets where the boundary claims to protect nothing;
- malformed exact versions;
- missing review status;
- critical controls represented only by vague prose.

Use stable identifiers and ordered collections so the same inventory yields the same findings.

## Boundary policy

For an untrusted-input boundary, require explicit controls such as size/resource limits and validation. For a privileged operation, require authorization or least-privilege controls. For boundaries protecting sensitive assets, require redaction/confidentiality or integrity controls appropriate to the asset.

The checker should not pretend that the string `"validated"` proves validation is correct. It proves only that the inventory claims the control. The laboratory teaches policy completeness; code review and tests supply deeper evidence.

## Dependency policy

An exact version must use the declared `=major.minor.patch` shape. A dependency with a build script requires explicit review because it executes during build. Default features require a finding unless intentionally reviewed. Unreviewed dependencies are findings regardless of popularity.

Do not claim that exact versions or a clean advisory scan prove security. Findings should say what decision or evidence is missing.

## Construction route

1. Define a small fixed severity vocabulary with deterministic ordering.
2. Validate inventory identity and produce causal findings for duplicates/empties.
3. Review each boundary against rules derived from its properties.
4. Review each dependency’s version, feature, build, and review state.
5. Sort findings by severity/subject/message or another declared stable order.
6. Summarize counts in an ordered map.
7. Add tests showing both compliant and incomplete inventories.

## Adversarial cases

Test duplicate names, empty names, no assets, untrusted input without limits, privileged operations without authorization, non-exact versions, version strings containing extra text, build scripts marked reviewed/unreviewed, and default features accepted without review. Ensure one malformed subject does not suppress findings for others.

## Transfer

Add runtime capability inventory—filesystem paths, network listeners, environment secrets, and child-process execution. Define least-privilege findings without hard-coding one deployment platform.

## Completion

The laboratory is complete when the same inventory yields byte-stable ordered findings, high-risk omissions are distinguishable from review notes, malformed inventory is not silently accepted, and the report states what it can and cannot prove.

Inspect `solution/` only after writing your rule table. Compare policy coverage and causal messages. A checker with more rules is not better if its inventory or severity model is incoherent.

## Threat and dependency dossier

Produce a threat table with columns for asset, attacker capability, entry point, precondition, impact, prevention, detection, containment, and residual risk. Cover parser abuse, allocation exhaustion, identifier cardinality, tenant isolation, diagnostic disclosure, configuration tampering, and build compromise. Every control must point to code, configuration, or an explicitly external deployment responsibility.

Create a dependency dossier listing direct and transitive crates, exact versions, features, licenses, build scripts, native-code use, advisory evidence, and update ownership. Remove at least one unnecessary feature or justify why none can be removed. Record the timestamp and source of advisory data so the result is not mistaken for a permanent guarantee. Conclude with the three highest residual risks and the next concrete control for each.

## Abuse-case execution

Turn at least three threat-table rows into executable tests or bounded experiments. Examples include a near-limit identifier flood, malformed frames that advertise hostile lengths, and diagnostic input containing secrets or control characters. Record which layer rejects the input, how much work occurs before rejection, what the caller observes, and what operators observe. A written control receives credit only when its enforcement point and failure behavior are demonstrable.

## Completion question

Which residual risk would cause the greatest real harm despite all implemented controls, and who owns the next mitigation? Support the answer with an attack path and observable evidence. Avoid ranking risks solely by theoretical severity when exploitability, exposure, and detection differ.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Attack Surface and Supply-Chain Audit**.
2. Draw the smallest **threat and dependency dossier** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to MetricRail so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service.
- Connect validation, authentication, authorization, confidentiality, integrity, and availability to specific boundaries.
- Enforce size, time, concurrency, recursion, and decompression limits before expensive work.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 88 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **threat and dependency dossier**. Defend why your design is simpler than one plausible alternative under the new requirements.
