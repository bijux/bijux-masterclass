# Reference Answers — Module 09: Adversarial Verification and Supply-Chain Assurance

Read after attempting all twelve Adversarial Verification and Supply-Chain Assurance exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. What makes a negative test security-relevant?

**Answer.** It represents a named threat or invalid state and asserts the authoritative safe outcome, not merely any error.

**Capstone check.** Link the negative test to a named threat and authoritative safe outcome; “returned an error” is insufficient when the wrong error leaks data or mutates state.

## 2. Why plant defects?

**Answer.** A test suite that still passes after the control is removed does not support the intended security claim.

**Capstone check.** Disable the named control under `capstone/planted-defects/`; the suite must fail for the predicted security reason before the guard is restored.

## 3. What is a good fuzz oracle for strict JSON?

**Answer.** No crash/hang; either one deterministic parsed value satisfying the strict profile or one bounded rejection class, with cross-language agreement.

**Capstone check.** Fuzz strict JSON toward one deterministic parse or one bounded rejection class, then compare Python and TypeScript outcomes.

## 4. Why preserve minimized counterexamples?

**Answer.** They make the regression understandable, fast, deterministic, and resistant to accidental test weakening.

**Capstone check.** Store the minimized hostile input beside the shared vector so later refactors cannot weaken the oracle invisibly.

## 5. What does an SBOM prove?

**Answer.** It records a component inventory for the produced artifact under a method; it does not prove components are safe or complete in every runtime environment.

**Capstone check.** Treat the SBOM as component inventory evidence only; reconcile it with the built artifact and record unobserved runtime additions as limitations.

## 6. Why require lockfiles?

**Answer.** They capture transitive resolution so reviewed and rebuilt dependency graphs can match.

**Capstone check.** Verify direct pins and transitive lock evidence for both ecosystems; an unconstrained transitive graph fails the supply-chain gate.

## 7. What is a false positive disposition?

**Answer.** A documented explanation and evidence showing the finding does not apply in the actual reachable configuration—not silent suppression.

**Capstone check.** A suppression requires reachability/configuration evidence and an owner; the release record must preserve the disposition rather than hide the finding.

## 8. What is a false negative risk?

**Answer.** Tools may not model business authorization, runtime configuration, novel vulnerabilities, or language/framework interactions.

**Capstone check.** Name business-policy, runtime-configuration, and novel-vulnerability gaps that scanners cannot rule out; keep adversarial tests independent of scanner output.

## 9. Why separate core and full proofs?

**Answer.** Core evidence remains reproducible without external services; full proof exercises frameworks/databases/tools and cannot be silently skipped.

**Capstone check.** Core proof must fail when an available dependency is missing unexpectedly; full proof records explicit environment gates rather than silently skipping them.

## 10. What should secret scanning include?

**Answer.** Source, history/release staging as appropriate, generated reports, snapshots, docs, examples, archives, and outgoing handoff.

**Capstone check.** Scan source, fixtures, generated reports, documentation, release staging, and the final ZIP; allow only named synthetic secrets in bounded test paths.

## 11. Trace adversarial and supply-chain verification in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/tests_security/test_gateway.py` and `capstone/tracks/typescript-fastify/test-security-core/gateway.test.mjs`. The required invariant is that negative vectors, mutants, locks, SBOM/provenance evidence, and vulnerability disposition prove controls and build inputs.

## 12. Compare adversarial and supply-chain verification across Python and TypeScript

Both tracks must preserve this invariant: negative vectors, mutants, locks, SBOM/provenance evidence, and vulnerability disposition prove controls and build inputs. The intentional difference is that testing ecosystems differ; shared hostile cases and planted vulnerabilities must produce equivalent outcomes.
