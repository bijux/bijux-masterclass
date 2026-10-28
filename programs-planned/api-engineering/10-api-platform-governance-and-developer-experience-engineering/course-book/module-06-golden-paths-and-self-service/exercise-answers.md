# Worked answers — Golden Paths, Templates, and Self-Service Provisioning

## 1. What makes a golden path different from a code template?

A code template copies files. A golden path combines maintained defaults, ownership, documentation, tests, policy hooks, publication workflow, upgrade responsibility, and a support model. Its value continues after generation.

## 2. Why must a template have an owner and version?

Generated projects depend on its assumptions. Ownership provides maintenance and support; versioning explains what defaults were used and permits controlled upgrades.

## 3. Which decisions should remain parameters?

Decisions that represent real context—owner, protocol, system, exposure, data class, or lifecycle—must be explicit. Parameters should not expose every low-level tool option that the paved road intends to standardize.

## 4. Why is “generate and forget” dangerous?

Security fixes, policy changes, dependency updates, and improved defaults never reach existing users. A platform needs template release notes, upgrade guidance, and a way to identify generated consumers.

## 5. How can a template centralize architecture incorrectly?

It can force one database, framework, or deployment shape where different domain needs exist. The template should encode common invariants and supported defaults, not pretend one implementation is universal.

## 6. Why must generated output contain ownership metadata?

A new API without an owner immediately creates catalog debt. Ownership is a prerequisite, not a later administrative task.

## 7. What should happen when parameters are invalid?

Fail before writing partial output. A deterministic generator should validate all inputs, render into a staging location, scan for unresolved placeholders or secrets, and publish atomically.

## 8. Why include tests in the scaffold?

Tests make the generated contract and policy hooks executable from the first commit. Without them, the template produces a structure but no maintained guarantee.

## 9. Should teams be able to leave the paved road?

Yes when they have a justified need, explicit owner, equivalent evidence, and accepted support boundary. The platform may decline to support every alternative.

## 10. How do you measure golden-path value?

Measure time to a compliant first release, defect rate, upgrade effort, and support demand. Counting template runs does not reveal whether generated systems succeed.

## 11. Why scan generated text for secrets?

Template repositories and examples are copied widely. An embedded fixture credential can become a real secret through reuse and is hard to revoke across generated projects.

## 12. What proves a generated project is reproducible?

The template version, parameter set, source digest, rendered file manifest, and deterministic output digest allow another run to reproduce or explain the project baseline.
