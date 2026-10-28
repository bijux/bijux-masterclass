# Worked Answers — Module 06: Golden Paths, Templates, and Self-Service Provisioning

Use these solutions to audit your reasoning for **Golden Paths, Templates, and Self-Service Provisioning**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. What makes a golden path different from a code template?

A code template copies files. A golden path combines maintained defaults, ownership, documentation, tests, policy hooks, publication workflow, upgrade responsibility, and a support model. Its value continues after generation.

The chapter’s decisive distinction is this: A golden path is the easiest supported route from an idea to a trustworthy release. It provides a maintained project shape, contract location, owner metadata, documentation skeleton, tests, policy hooks, and publication workflow. It does not decide the business domain or erase protocol choice.

## 2. Why must a template have an owner and version?

Generated projects depend on its assumptions. Ownership provides maintenance and support; versioning explains what defaults were used and permits controlled upgrades.

In the cumulative capstone, the rule becomes concrete: A template needs its own owner, version, changelog, support policy, compatibility promise, and usage inventory. Teams generated from version 1.0 still exist when the template reaches 1.4. The platform must explain whether an update is required, optional, or irrelevant. A template without an upgrade story transfers maintenance debt to every consumer.

## 3. Which decisions should remain parameters?

Decisions that represent real context—owner, protocol, system, exposure, data class, or lifecycle—must be explicit. Parameters should not expose every low-level tool option that the paved road intends to standardize.

A useful way to reason about the boundary is: Avoid one template per team or framework permutation. Organize paths by meaningful product boundary: public HTTP API, event consumer, internal RPC service, graph extension, or API documentation package. If two templates differ only in naming, consolidate. If they have different security or operational ownership, keep the difference explicit.

## 4. Why is “generate and forget” dangerous?

Security fixes, policy changes, dependency updates, and improved defaults never reach existing users. A platform needs template release notes, upgrade guidance, and a way to identify generated consumers.

The implementation consequence is: Maintain a generation receipt with template ID, version, parameters, and file digests. An upgrade tool can classify files as unchanged, owner-modified, or platform-obsolete. Apply safe changes automatically, propose merges for conflicts, and record declined upgrades. Security-critical changes can become policy blockers after a notice period.

## 5. How can a template centralize architecture incorrectly?

It can force one database, framework, or deployment shape where different domain needs exist. The template should encode common invariants and supported defaults, not pretend one implementation is universal.

The important nuance is: Defaults should encode evidence: supported contract versions, safe authentication boundaries, standard documentation shape, known observability hooks, and maintained build paths. An escape hatch is appropriate when a team has a real requirement the golden path cannot meet. The exception must name who supports the alternative and what equivalent evidence replaces the paved road.

## 6. Why must generated output contain ownership metadata?

A new API without an owner immediately creates catalog debt. Ownership is a prerequisite, not a later administrative task.

Under concurrency or failure, the distinction becomes: The scaffold emits catalog-info.yaml, a contract stub, quickstart, API metadata, and a contract-presence test. It begins in proposed, not active. Generation creates a credible starting point; it does not grant release status. The owner must replace the stub, define semantics, and collect evidence through the lifecycle.

## 7. What should happen when parameters are invalid?

Fail before writing partial output. A deterministic generator should validate all inputs, render into a staging location, scan for unresolved placeholders or secrets, and publish atomically.

The design remains honest only if: Validate inputs before writing. Write into an empty staging directory. Reject unresolved placeholders and embedded credentials. Compare actual outputs with the declared set. Run syntax and policy checks on the result. Only then publish or copy it to the destination. A partially generated repository is a failure, not a starting point the learner must repair manually.

## 8. Why include tests in the scaffold?

Tests make the generated contract and policy hooks executable from the first commit. Without them, the template produces a structure but no maintained guarantee.

The consumer-facing consequence is: A golden path has an input contract, output contract, upgrade policy, support owner, and tests. Course 10’s api-capability-v1 requires a canonical API name, title, owner, protocol, and system. It emits exactly six files: ownership metadata, a contract location, quickstart, policy metadata, test, and README. Exact outputs make review and regression possible. An open-ended generator that quietly changes dozens of files is difficult to trust.

## 9. Should teams be able to leave the paved road?

Yes when they have a justified need, explicit owner, equivalent evidence, and accepted support boundary. The platform may decline to support every alternative.

The operational consequence is: Track generated projects, template versions, upgrade state, first release time, and support categories. A large number of old unupgraded projects signals that the path is not maintainable. Survey owners about removed work, not only satisfaction. The best path may be one teams rarely notice because it eliminates routine failure.

## 10. How do you measure golden-path value?

Measure time to a compliant first release, defect rate, upgrade effort, and support demand. Counting template runs does not reveal whether generated systems succeed.

The strongest engineering interpretation is: Treat a template release as an API. Its inputs, outputs, defaults, failure modes, and support promise form a contract. Validate backward compatibility for parameters and generated structure. Removing a parameter or changing a default can break automation even if the template still renders.

## 11. Why scan generated text for secrets?

Template repositories and examples are copied widely. An embedded fixture credential can become a real secret through reuse and is hard to revoke across generated projects.

The defect-oriented view is: The Python renderer validates patterns and enumerations, creates only declared outputs, rejects unresolved placeholders, and scans rendered text for secret-like assignments. The TypeScript core demonstrates the same parameter and text rules. The final generated fixture is compared by manifest rather than by visual inspection.

## 12. What proves a generated project is reproducible?

The template version, parameter set, source digest, rendered file manifest, and deterministic output digest allow another run to reproduce or explain the project baseline.

Across the Python and TypeScript tracks, the invariant is: Record template version, parameters, source digest, and rendered manifest. Deterministic generation makes review and regeneration possible. It also allows the platform to identify which projects are affected by a template defect. This is the beginning of template supply-chain management, not merely convenience.
