# Worked Answers — Module 09: Adversarial Verification and Supply-Chain Assurance

Use these solutions to audit your reasoning for **Adversarial Verification and Supply-Chain Assurance**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. What makes a negative test security-relevant?

It represents a named threat or invalid state and asserts the authoritative safe outcome, not merely any error.

**Capstone check.** Link the negative test to a named threat and authoritative safe outcome; “returned an error” is insufficient when the wrong error leaks data or mutates state.

The chapter’s decisive distinction is this: Calling an input malicious does not make a test adversarial. State the attacker capability, the control being challenged, and the prohibited outcome. Then construct the smallest input that would produce that outcome if the control were absent.

## 2. Why plant defects?

A test suite that still passes after the control is removed does not support the intended security claim.

**Capstone check.** Disable the named control under `capstone/planted-defects/`; the suite must fail for the predicted security reason before the guard is restored.

In the cumulative capstone, the rule becomes concrete: Keep controlled mutants or planted defects outside the release path. Remove one audience check, reverse one ownership predicate, permit one private address range, omit one replay write, or log one secret. The relevant test must fail for the predicted reason. If the entire suite stays green, the security claim was not actually covered. If hundreds of unrelated tests fail, minimize the oracle so future regressions remain diagnosable.

## 3. What is a good fuzz oracle for strict JSON?

No crash/hang; either one deterministic parsed value satisfying the strict profile or one bounded rejection class, with cross-language agreement.

**Capstone check.** Fuzz strict JSON toward one deterministic parse or one bounded rejection class, then compare Python and TypeScript outcomes.

A useful way to reason about the boundary is: Shared hostile vectors prevent the Python and TypeScript tracks from quietly defining different security profiles. Each vector should name the expected category and public outcome; framework-specific exception text is not a parity requirement.

## 4. Why preserve minimized counterexamples?

They make the regression understandable, fast, deterministic, and resistant to accidental test weakening.

**Capstone check.** Store the minimized hostile input beside the shared vector so later refactors cannot weaken the oracle invisibly.

The implementation consequence is: Use Node test for local vectors and Vitest/fast-check in the full profile. Compile core security modules separately from Fastify. Add source guards for unsafe parser/auth shortcuts, but label them structural checks rather than semantic proof.

## 5. What does an SBOM prove?

It records a component inventory for the produced artifact under a method; it does not prove components are safe or complete in every runtime environment.

**Capstone check.** Treat the SBOM as component inventory evidence only; reconcile it with the built artifact and record unobserved runtime additions as limitations.

The important nuance is: Supply-chain evidence begins with deterministic dependency inputs. Pin direct dependencies and retain the ecosystem lockfile that resolves transitives. Separate build, development, and runtime dependencies. Generate an SBOM from the resolved graph and artifact, record provenance for the build, scan source and artifacts for secrets, and review licenses or policy restrictions where relevant.

## 6. Why require lockfiles?

They capture transitive resolution so reviewed and rebuilt dependency graphs can match.

**Capstone check.** Verify direct pins and transitive lock evidence for both ecosystems; an unconstrained transitive graph fails the supply-chain gate.

Under concurrency or failure, the distinction becomes: Security evidence must be sensitive to control removal, reproducible, scoped, and linked to requirements. Scanners and dependency reports are useful inputs, but only interpreted findings, lock integrity, provenance, and executable counterexamples support a defensible claim.

## 7. What is a false positive disposition?

A documented explanation and evidence showing the finding does not apply in the actual reachable configuration—not silent suppression.

**Capstone check.** A suppression requires reachability/configuration evidence and an owner; the release record must preserve the disposition rather than hide the finding.

The design remains honest only if: A scanner result is a lead, not a verdict. Triage affected component and version, reachability, exploit preconditions, available fix, compensating controls, and deadline. False positives must be documented; false negatives remain possible. “The scanner passed” is not a security case.

## 8. What is a false negative risk?

Tools may not model business authorization, runtime configuration, novel vulnerabilities, or language/framework interactions.

**Capstone check.** Name business-policy, runtime-configuration, and novel-vulnerability gaps that scanners cannot rule out; keep adversarial tests independent of scanner output.

The consumer-facing consequence is: Assemble the complete adversarial proof ladder. Execute at least six planted defects, minimize failures, generate dependency/SBOM evidence with available tools, triage a fixture vulnerability, and prove private fixture material is absent from release staging.

## 9. Why separate core and full proofs?

Core evidence remains reproducible without external services; full proof exercises frameworks/databases/tools and cannot be silently skipped.

**Capstone check.** Core proof must fail when an available dependency is missing unexpectedly; full proof records explicit environment gates rather than silently skipping them.

The operational consequence is: The final proof ladder links threat, requirement, code, negative vector, mutant sensitivity, dependency evidence, and residual limitation. That is stronger than a long list of tools because it explains which security property each result supports.

## 10. What should secret scanning include?

Source, history/release staging as appropriate, generated reports, snapshots, docs, examples, archives, and outgoing handoff.

**Capstone check.** Scan source, fixtures, generated reports, documentation, release staging, and the final ZIP; allow only named synthetic secrets in bounded test paths.

The strongest engineering interpretation is: Negative tests should cover boundary combinations, not only isolated invalid values. A valid token with the wrong audience, a correct scope for the wrong owner, a public webhook hostname that resolves partly private, and a safe archive member combined with an excessive cumulative size are more informative than random malformed strings.

## 11. Trace adversarial and supply-chain verification in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/tests_security/test_gateway.py` and `capstone/tracks/typescript-fastify/test-security-core/gateway.test.mjs`. The required invariant is that negative vectors, mutants, locks, SBOM/provenance evidence, and vulnerability disposition prove controls and build inputs.

The defect-oriented view is: Reproducibility claims need a clean, network-controlled build and byte or semantic comparison of produced artifacts. A dependency install performed against a changing registry during the proof does not establish the same input graph. Signing a non-reproducible artifact can establish origin, not correctness.

## 12. Compare adversarial and supply-chain verification across Python and TypeScript

Both tracks must preserve this invariant: negative vectors, mutants, locks, SBOM/provenance evidence, and vulnerability disposition prove controls and build inputs. The intentional difference is that testing ecosystems differ; shared hostile cases and planted vulnerabilities must produce equivalent outcomes.

Across the Python and TypeScript tracks, the invariant is: Shared hostile vectors prevent the Python and TypeScript tracks from quietly defining different security profiles. Each vector should name the expected category and public outcome; framework-specific exception text is not a parity requirement.
