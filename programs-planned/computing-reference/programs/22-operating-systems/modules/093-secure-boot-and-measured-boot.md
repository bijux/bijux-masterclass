---
module_id: OS-093
program: Operating Systems
level: 2
module_number: 93
title: Secure Boot and Measured Boot
status: complete
last_verified: 2026-09-04
---

# Secure Boot and Measured Boot

## One-Page Review

### Governing question

How can a platform admit only boot artifacts authorized by current policy, produce fresh evidence of what actually influenced startup, and recover safely when keys, software, measurements, or policy change?

### Essential definitions

- **verified boot** authenticates an artifact under configured policy before allowing it to execute or become trusted input.
- **UEFI Secure Boot** is a UEFI image-validation policy built from platform mode, authenticated variables, allowed signatures or hashes, and forbidden entries.
- A **root of trust** is a component or assumption accepted without proof by the mechanism that builds later trust claims.
- A **measurement** is a digest plus contextual event information recorded for later appraisal; measuring does not itself block execution.
- A **platform configuration register**, or **PCR**, is TPM state commonly updated by a one-way hash extension rather than ordinary assignment.
- An **event log** records ordered measurement events whose digests can be replayed to explain PCR state; the log is informative until replay and quotation bind it.
- A **quote** is TPM-signed attestation data covering selected PCR state and caller-supplied freshness data under an attestation key.
- **sealing** authorizes use of an object or secret only when a TPM policy, potentially including selected PCR state, is satisfied.

### Central model, mechanism, or theorem

Secure boot and measured boot answer different questions. Verification applies an admission predicate before a handoff. Measurement extends ordered evidence into protected state. Attestation becomes meaningful only when a verifier authenticates the attestation key, checks a fresh challenge, validates the quote, replays the event log to the quoted PCRs, appraises each event under an explicit reference policy, and accounts for everything outside the measured boundary.

### Critical invariants

- Every executable or policy-bearing boot input is either authenticated before use, measured before it influences trusted state, or explicitly outside the claim.
- Allow databases, deny databases, platform mode, keys, algorithms, authenticated-update state and rollback policy are themselves governed and observable.
- PCR replay uses the same bank, event order, digest encoding and initial/reset semantics as the platform.
- A quote binds the verifier's fresh challenge, intended PCR selection, attestation key and current attested state.
- Reference values describe acceptable configurations and transitions, not merely one permanently frozen digest.
- Recovery and update artifacts meet an explicit trust policy and cannot silently restore a revoked or vulnerable state.
- Boot integrity claims stop at their measured and enforced boundary; they do not imply software correctness or runtime safety.

### Common failures

Frequent failures include trusting any signed image, neglecting forbidden-signature updates, accepting an old vulnerable but valid image, measuring a file after using it, omitting command lines or configuration, trusting an event log without PCR replay, accepting a quote without a fresh nonce, sealing to brittle PCRs, confusing an attestation key with device authorization, losing keys during ownership changes, and making recovery less trustworthy than normal boot.

### Compact example

A fleet signs one unified kernel image containing the kernel, initrd and command line. Firmware admits its signed UEFI loader, while boot components measure firmware policy and image state into documented PCRs. An attestation service sends a nonce, validates the TPM quote and attestation-key credential, replays the supplied event log, and accepts either of two rollout versions under a time-bounded policy. Disk-key release additionally requires the approved image measurement and expected boot phase. A signed but revoked loader, stale quote, unexplained log event, or rescue image outside policy goes to recovery rather than receiving production secrets.

### Connections

Secure and measured boot connect firmware, cryptographic key management, TPM state, bootloaders, kernels, initrds, update frameworks, disk encryption, fleet identity, remote authorization, incident response and supply-chain provenance.

## Governing Question

Boot begins before ordinary operating-system controls exist. Firmware selects executable images, consumes mutable variables and device configuration, and passes privileged inputs to loaders and kernels. If any early component is replaced, rolled back or reconfigured, later access controls may start from a false foundation.

Signature checking alone is incomplete: an authorized signer can ship a defect, an old signed artifact can remain vulnerable, and not every configuration input is necessarily covered. Measurement alone is also incomplete: a platform can faithfully record malicious execution and continue running it. The governing question therefore spans admission, evidence, appraisal, update, rollback, recovery and runtime transition.

The design target is not a universal “trusted” bit. It is a bounded statement such as: this physical or virtual platform, anchored in these keys and TPM credentials, booted through these measured and verified components, with this mutable configuration, under this freshness condition and reference policy, and has not yet crossed a declared runtime boundary.

## Why This Matters

An attacker who persists in firmware, a bootloader, an initrd or early kernel state can often run beneath endpoint controls, steal disk-unlock material, suppress logs or reinstall runtime malware. Verified boot raises the cost of unauthorized replacement. Measured boot can expose state to a local key-release policy or remote verifier even when prevention was unavailable or deliberately permissive.

The mechanisms are also operationally dangerous. A malformed deny-list update or lost signing key can make a fleet unbootable. Sealing directly to volatile measurements can strand data after legitimate firmware changes. A permissive recovery route can bypass the normal chain. Attestation policy that recognizes only one digest can turn routine updates into outages, while policy that accepts any vendor signature may admit known-vulnerable software.

Trust evidence crosses organizations. Platform vendors provision roots and firmware. OS vendors sign loaders and kernels. Operators enroll keys and approve versions. TPM manufacturers provision endorsement credentials. Attestation services decide which claims earn network access or secrets. Assurance depends on the complete governance chain and on privacy-preserving treatment of device identity.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace reset, firmware, loader, kernel, initrd and initial user-space handoffs;
- distinguish a cryptographic digest, signature, certificate chain, authenticated update and revocation;
- explain freshness challenges, replay attacks and key authorization;
- reason about immutable versus mutable boot inputs and update rollback;
- distinguish prevention, detection, appraisal, authorization and recovery.

Retrieve the platform model and firmware version; UEFI or other boot mode; Secure Boot, setup and deployed state; platform key, key-exchange keys, allow and forbid databases; supported algorithms; authenticated-variable update history; boot order; firmware, option-ROM and device-firmware coverage; bootloader, shim, kernel, microcode, initrd and command-line provenance; TPM version and implementation; active PCR banks; PCR allocation, reset and locality semantics; event logs; attestation-key credential and certificate path; reference values; nonce and quote transcript; sealing policy; update counters; recovery paths; and evidence retention rules.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish verified boot, UEFI Secure Boot, measured boot, attestation and sealing;
2. model UEFI image admission using platform mode, `PK`, `KEK`, `db` and `dbx`;
3. explain why signed artifacts still require revocation and rollback policy;
4. compute and replay a simplified PCR extend chain;
5. validate a fresh quote and event log against reference policy;
6. identify measurement gaps involving configuration, initrds, devices and recovery;
7. design update, key-rotation, deny-list and disaster-recovery procedures;
8. scope local and remote claims to their actual roots, lifecycle and runtime boundary.

## Core Exposition

### Separate admission from evidence

Verified boot decides whether an artifact is authorized before using it. Measured boot records a digest and event context, commonly extending protected state, but may execute the artifact regardless. A robust platform often uses both: verification prevents known-disallowed execution, while measurement supports diagnosis, conditional secret release and remote appraisal.

Neither mechanism establishes correctness. A valid signature identifies an authorization path, not absence of vulnerabilities. A matching measurement establishes equality to measured bytes under the recorded process, not safety. State the exact predicate and threat model instead of saying a machine “is trusted.”

### Locate the root of trust

A static root begins from code or data accepted at reset, such as immutable hardware behavior and a firmware root key. A dynamic root establishes a later measured launch under architecture-specific controls. A virtual TPM may ultimately depend on a hypervisor and host key service. Each claim must name what is assumed, who provisions it, and what physical or administrative attacks remain.

The root is not automatically the first software component. It includes cryptographic algorithms, key storage, update logic, reset semantics, hardware buses and any authority able to replace them. A compromised verifier or enrollment service can invalidate an otherwise sound device chain.

### Understand UEFI Secure Boot policy state

UEFI Secure Boot operates through image validation plus security policy variables. In the familiar model, the platform key `PK` governs platform ownership, key-exchange keys in `KEK` authorize selected database updates, `db` contains allowed signatures or hashes, and `dbx` contains forbidden entries. Exact authorization and mode rules come from the UEFI specification and implementation.

Setup mode, user mode, deployed mode and audit mode affect enrollment or enforcement behavior. Reading only a `SecureBoot` indicator is insufficient. Inspect mode variables, enrolled databases, vendor-key state, authenticated-update properties and the actual image-execution record where available.

### Treat allow and forbid decisions together

An image may be admitted because its hash is allowed or its signature chains to an allowed certificate, subject to required image format and verification rules. A matching forbidden hash or revoked certificate entry must defeat the allow path under the applicable policy. Verification failures and policy failures should select a defined next boot option or recovery response.

Trusting a broad signing certificate delegates admission for every conforming image it signs. Hash allow-listing is narrower but increases operational churn. Design `db` and `dbx` ownership, size limits, update ordering, audit and rollback as one control plane.

### Authenticate policy updates

Secure Boot policy variables use authenticated update mechanisms in enforcing modes. Protect the offline private keys, signing service, counters or timestamps, update packaging and enrollment ceremony. Test malformed, replayed, reordered, power-interrupted and partially applied updates.

Key rotation is a graph migration. New verification keys must be accepted before artifacts depend on them; old keys are removed only after recovery and rollback artifacts are replaced. A rotation plan that updates normal boot but not rescue media creates an outage waiting for failure.

### Add explicit anti-rollback policy

A correctly signed older image may contain a known exploitable defect. Signature validity therefore cannot be the entire admission predicate. Use authenticated version metadata, security-generation values, monotonic state, deny-list entries or an update framework that prevents rollback below an approved floor.

Rollback protection must cover dependent components consistently. Rejecting an old kernel while accepting its vulnerable loader, initrd, device firmware or recovery environment leaves a path around the floor. Provide a break-glass process whose exceptional authority, duration and evidence are explicit.

### Revoke without destroying recoverability

Revocation can target a certificate, image digest, component generation or vendor-defined metadata. Broad certificate revocation removes many artifacts at once but can strand valid recovery paths. Fine-grained revocation preserves compatibility but grows policy and may miss repackaged vulnerable code.

Stage deny-list updates only after every supported machine has a non-revoked boot and recovery path. Simulate storage limits, firmware bugs, failed updates and battery loss. Preserve an independently validated recovery route rather than weakening enforcement globally.

### Cover the entire influential input set

The executable chain may include firmware volumes, option ROMs, device firmware, boot managers, shims, loaders, kernels and early drivers. Influential data includes Secure Boot variables, boot order, hardware descriptions, microcode, initrds, command lines, loader entries, root-image identifiers and recovery selections.

Authenticate or measure each input before it affects trusted state. When a platform cannot cover an input, exclude dependent claims or add a compensating control. Measuring a parsed object after it has already influenced execution cannot establish pre-use integrity.

### Prefer cohesive signed boot artifacts where useful

A unified kernel image can package a UEFI stub, kernel, initrd, embedded command line and related metadata into one signed PE image. This reduces unsigned seams and can make selected measurements predictable. It remains one ecosystem design, not a universal requirement.

External loader configuration, dynamically selected initrds, firmware tables, device state and runtime extensions may still influence the result. Verify which sections are signed, which are measured, which can be overridden and how updates revoke the complete artifact.

### Understand PCR extension

A TPM PCR is commonly updated by hashing the old PCR value concatenated with a new event digest. This makes order matter and prevents ordinary software from assigning an arbitrary final value through the extend interface. Separate algorithm banks can produce different PCR widths and values for the same event sequence.

Extension does not store meaning. Two equal PCR values indicate equal initial state and ordered digest sequence under the modeled bank, absent a hash break; they do not explain the events. The event log supplies descriptions and component data for appraisal.

### Respect PCR reset and locality semantics

PCRs do not all share identical reset or extend authority. Some reset only at platform reset; some may reset during dynamic launch or under authorized locality and policy. Firmware and platform profiles allocate conventional meanings to PCR indices, but the verifier must use the applicable profile and observed bank.

Sleep, hibernation, kexec, virtual-machine snapshot and TPM clear can cross lifecycle boundaries without the same semantics as a cold boot. Define when attestation expires and when secrets must be resealed or sessions re-established.

### Use an event log to explain protected state

The firmware event log records ordered events and one or more digests associated with PCR extensions. Later components may maintain additional logs, such as Linux IMA measurements. Logs can contain variable data, event types, component identifiers and informational entries that were not extended.

Treat the log as attacker-supplied until its extended entries replay to the quoted PCR values. Successful replay establishes consistency with protected state for the modeled events; it does not prove event descriptions are honest, that every influential byte was measured or that reference policy accepts the content.

### Parse logs defensively

Event logs cross a privileged and often implementation-diverse boundary. Bound record lengths, digest counts, algorithms, index values, integer arithmetic and total resource use. Reject ambiguous truncation, duplicate interpretation, unsupported banks and trailing bytes according to a documented parser policy.

Preserve the raw log and parser version for incident analysis. Normalization that discards unknown events can make two materially different boots appear equal. An appraiser should distinguish malformed evidence from an explicitly unsupported but well-formed configuration.

### Replay the selected bank exactly

Initialize each modeled PCR according to the applicable TPM reset state. For every extended event targeting that PCR and bank, concatenate the current PCR bytes with the event digest bytes and hash using the bank algorithm. The result must equal the quoted PCR value.

Do not hash textual hexadecimal, event descriptions or a digest from another bank. Verify that the logged digest equals a fresh hash of event data when the event format makes that comparison meaningful; PCR replay alone only proves the logged digest sequence.

### Bind quotes to freshness and intent

A verifier sends unpredictable qualifying data, commonly a nonce, and specifies the intended PCR selection. The TPM signs attestation data under an attestation key. The verifier checks structure, signature, key identity and authorization, nonce, PCR selection and digest, then applies replay and reference policy.

Without a fresh challenge, an attacker can replay old healthy evidence. Without checking the requested selection, a valid quote over irrelevant PCRs proves little. Channel binding or request context may be included so evidence for one service, tenant or transaction cannot be redirected to another.

### Validate attestation-key provenance

An attestation key proves possession and TPM-mediated signing according to its attributes; it does not by itself reveal which device or TPM should be trusted. Enrollment may use an endorsement credential, manufacturer chain, privacy CA, enterprise provisioning or another registration process.

Verify certificate constraints, key attributes, name, policy, revocation and lifecycle. Keep endorsement identity and operational pseudonyms separate where privacy requires it. A verifier database mapping any self-generated key to an approved host defeats hardware-rooted identity.

### Appraise events, not only final PCRs

A final PCR digest is opaque without an expected digest or explainable log. Static “golden PCR” comparison is brittle when firmware data, hardware enumeration or boot configuration legitimately varies. Reference integrity manifests and policy can describe acceptable component identities, versions, transitions and dependencies.

An appraiser first establishes cryptographic consistency, then evaluates semantics: known firmware, non-revoked loader, approved security settings, allowed kernel generation, expected command line, and no unexplained critical events. Keep cryptographic failure distinct from policy noncompliance.

### Design policy for controlled change

Production attestation policy usually accepts a set or graph of states during rollout: current version, next version, perhaps a time-bounded rollback version and a separate recovery state with restricted privileges. Bind approvals to device class and dependencies rather than one global list.

Require an explicit expiry for transitional states. Record who approved each reference value, its source artifact, build provenance, vulnerability status and retirement condition. Acceptance should contract after rollout, not accumulate forever.

### Use sealing as local conditional authorization

TPM sealing or policy-bound keys can make secret use conditional on PCR values and other authorization assertions. This can protect disk-unlock keys from an altered boot path without requiring a remote decision for every boot.

Direct binding to unstable firmware PCRs creates availability risk. Prefer a policy structure that permits signed, reviewed PCR policies or a manageable set of authorized states while protecting the policy-signing key. Combine PCR state with user authorization, rate limits or remote approval when the threat model requires them.

### Distinguish sealing from attestation

Sealing is a local authorization decision: the TPM releases or uses an object when policy succeeds. Attestation exports signed evidence for a verifier that applies its own policy. A sealed secret can unlock a platform without telling a remote party why; a valid quote need not release any local secret.

Do not use one as a vague substitute for the other. Identify the relying party, decision, freshness, audit record and failure mode for each flow.

### Extend measurement into runtime deliberately

Firmware measurement ends before most runtime state exists. Linux IMA can measure selected file and buffer events under a configured policy and extend them into a PCR, producing a separate measurement list. Appraisal can enforce signatures or hashes in configured cases, which is distinct from measurement.

Runtime measurement coverage depends on policy, hook timing, templates and namespace or filesystem behavior. It does not automatically cover JIT code, already-open data, DMA, in-memory modification, remote input or every kernel subsystem. State the last event and evidence horizon accepted by the verifier.

### Connect boot integrity to kernel enforcement

After an authenticated kernel starts, module signature policy, lockdown, immutable root verification, LSM policy and update controls determine whether runtime can replace trusted code or read sensitive kernel state. Secure Boot may trigger platform-specific kernel restrictions, but verify live enforcement rather than inferring it from firmware state.

A chain that authenticates the kernel but lets privileged user space load arbitrary code into it has a short useful lifetime. Conversely, runtime confinement cannot repair firmware that subverted the kernel before it initialized.

### Handle virtual and confidential platforms explicitly

A virtual TPM's persistence, monotonic state and attestation keys are implemented or protected by a virtualization stack. Snapshot rollback can restore old virtual TPM state unless the design binds it to external freshness or protected counters. Migration changes host and hardware trust dependencies.

Confidential-computing attestation may cover a measured launch of a guest or workload under a processor-backed root rather than traditional firmware PCRs. Keep evidence formats and roots separate; composing host, hypervisor, virtual TPM and guest claims requires a declared trust model.

### Protect the attestation service

The verifier holds reference policy and gates valuable access, so it is a high-value control plane. Authenticate evidence channels, isolate signing and policy keys, log decisions, rate-limit requests, support key revocation and make policy changes reviewable and reproducible.

Failure policy matters. Fail-open may expose secrets during outage; fail-closed can remove an entire fleet. Use cached grants with bounded lifetime, quarantine tiers and emergency policy signed by separate authority where availability requirements justify them.

### Design trustworthy recovery

Recovery code often has broader disk and key access than normal boot. Authenticate and measure it under a distinct policy, require suitable physical or remote authorization, minimize networking, and record why it was selected. Never enroll a universal rescue key whose compromise bypasses all tenant or device boundaries.

Recovery must work after key rotation, deny-list updates, corrupted normal images and partial storage updates. Test it on real hardware without exposing production recovery secrets. Returning to service requires remeasurement, evidence appraisal and correction of the cause, not merely a successful reboot.

### Govern ownership transfer and retirement

Device sale, board replacement, TPM clear, firmware reset and tenant reassignment change identity and key ownership. Define when platform keys, endorsement-derived registrations, attestation keys, sealed objects and verifier records are destroyed, regenerated or transferred.

Do not treat a re-enrolled machine as continuous with its prior identity without evidence. Retirement should revoke credentials and erase secrets even when physical hardware remains operational.

## Definitions and Notation

Let `H_b` be the digest algorithm for PCR bank `b`, `p_i^(0)` the initial byte value of PCR `i`, and `d_k` the event digest for the same bank. For an event targeting PCR `i`, extension is

$$
p_i^{(k+1)}=H_b\!\left(p_i^{(k)}\mathbin{\|}d_k\right),
$$

where $\|$ denotes byte concatenation. Ordering, exact bytes, PCR selection, bank and reset state are part of the statement.

Let `Allowed(x, S)` mean image `x` is authorized by allowed database `S`, `Forbidden(x, R)` mean a forbidden entry applies, and `ModeEnforces(m)` mean current platform mode performs image validation. A simplified admission predicate is

$$
admit(x)=ModeEnforces(m)\land Allowed(x,db)\land \neg Forbidden(x,dbx)\land FreshEnough(x,v_{min}),
$$

with image-format, certificate, timestamp, firmware and authenticated-variable rules left to the actual specification. `FreshEnough` makes anti-rollback explicit rather than pretending signature validity supplies it.

For quote `Q`, event log `L`, challenge `n`, attestation key `AK`, reference policy `R`, selected PCRs `S`, and contextual assumptions `A`, define the assurance obligation

$$
Accept(Q,L)=SigOK(Q,AK)\land CredentialOK(AK)\land Nonce(Q)=n
$$

$$
\land Selection(Q)=S\land Replay(L,S)=PCRs(Q)\land Appraise(L,R)\land AssumptionsHold(A).
$$

This is an engineering decomposition, not a proof that a specific firmware, TPM, log parser, verifier or reference policy is correct.

## Mechanisms, Invariants, or Proof Structure

1. **Root obligation:** identify immutable or initially trusted code, keys, TPM credentials, provisioning authorities and physical assumptions.
2. **Admission obligation:** authenticate every executed or policy-bearing artifact before use, including recovery, or exclude it from the verified claim.
3. **Policy-state obligation:** verify enforcement mode, allowed and forbidden databases, authenticated-update history, algorithms and rollback floor.
4. **Measurement obligation:** measure influential inputs before use into documented PCR banks with unambiguous event encodings.
5. **Replay obligation:** parse the complete log defensively and reproduce the selected quoted PCR values from correct initial state and event order.
6. **Freshness obligation:** bind the quote to an unpredictable challenge and intended transaction, selection, device enrollment and attestation key.
7. **Appraisal obligation:** compare explained events with versioned acceptable-state policy, revocation and dependency constraints.
8. **Secret-release obligation:** distinguish remote authorization from local sealing and bound each grant to its relying party and lifetime.
9. **Transition obligation:** keep update, rotation, rollout, rollback and recovery states bootable without preserving vulnerable admission paths indefinitely.
10. **Runtime obligation:** identify when boot evidence expires and which kernel, storage and runtime controls preserve the claim afterward.
11. **Privacy obligation:** disclose only necessary device identity and configuration evidence, with retention and unlinkability controls.
12. **Recovery obligation:** preserve raw evidence, quarantine rejected systems, restore through separately governed artifacts and re-attest before service.

## Alternatives and Trade-Offs

- **Certificate trust versus hash allow-listing:** certificates scale updates but delegate broadly; hashes minimize delegation but create database churn.
- **Firmware enforcement versus later verification:** earlier enforcement narrows exposure; later stages may be easier to update and express richer policy.
- **Static expected PCRs versus event appraisal:** exact values are simple but brittle; semantic appraisal handles change but expands parser and policy complexity.
- **Local sealing versus remote release:** local release survives network failure; remote policy changes faster and can incorporate fleet intelligence.
- **Stable attestation identity versus pseudonymous keys:** stable identity simplifies inventory; pseudonyms reduce cross-service tracking.
- **Broad certificate revocation versus component generations:** broad revocation is decisive but disruptive; generations are precise but ecosystem-specific.
- **Immutable command line versus operator override:** embedding closes a configuration seam; overrides aid diagnosis but require independent authentication or measurement.
- **Unified kernel image versus separate artifacts:** one signed object reduces gaps; separate components allow flexible composition and smaller updates.
- **Cold-boot-only evidence versus resume-aware evidence:** cold boot has clearer reset semantics; resume support improves availability but needs explicit lifecycle handling.
- **Fail-closed attestation versus degraded access:** fail-closed protects assets; quarantine or cached grants may better satisfy recovery objectives.
- **Firmware PCR binding versus signed PCR policy:** direct binding is mechanically simple; authorized policy supports updates but protects another signing authority.
- **Full event disclosure versus minimized claims:** full logs aid appraisal and forensics; selective evidence reduces privacy leakage but complicates completeness claims.
- **Physical TPM versus firmware or virtual TPM:** discrete protection can narrow software compromise; integrated or virtual designs improve deployment while inheriting different roots.
- **Golden images versus acceptable-state graphs:** golden images simplify inventory; graphs represent staged rollouts, dependencies and recovery honestly.
- **Continuous runtime measurement versus boot-only scope:** extended evidence observes more state; it increases log volume, policy complexity and privacy surface.
- **Automatic recovery versus human authorization:** automation restores availability quickly; high-impact recovery may need independent approval and stronger evidence.

## Failure Modes and Misconceptions

1. **“Signed means safe.”** A signature proves an authorization path over particular bytes; authorized software can be defective or malicious.
2. **“Secure Boot measures the boot.”** UEFI image verification and TPM measurement are different mechanisms even when deployed together.
3. **“Measured means blocked.”** Measurement can record an unapproved component and continue executing it.
4. **“The SecureBoot variable proves the chain.”** Mode, databases, update state, executed artifacts and implementation behavior must also be inspected.
5. **“Anything signed by an enrolled CA is appropriate.”** Broad certificate trust may authorize tools, old images or another product class.
6. **“Revocation is just another update.”** A deny-list can irreversibly remove the only bootable or recovery path on affected devices.
7. **“Signatures prevent rollback.”** Old signed images remain authentic unless a version or revocation policy rejects them.
8. **“The event log is protected because it mentions a TPM.”** Replay it to freshly quoted PCRs; the log itself commonly resides in ordinary memory.
9. **“Matching PCRs explain the boot.”** PCRs authenticate an ordered digest chain but are opaque without events and reference meaning.
10. **“Replaying hexadecimal text is equivalent.”** Extend exact digest bytes under the correct bank algorithm and initial state.
11. **“A valid quote is fresh.”** A quote over a stale challenge can be replayed.
12. **“Any PCR selection is sufficient.”** The verifier must require PCRs that cover its claim and confirm the quote used exactly that selection.
13. **“An attestation key proves an approved device.”** Enrollment and credential validation connect the key to the intended root and inventory.
14. **“A golden digest is permanent.”** Firmware, keys, configuration and legitimate devices change; reference policy needs controlled evolution.
15. **“PCR replay proves completeness.”** Unmeasured inputs and dishonest event descriptions remain outside that result.
16. **“Measure after parsing is good enough.”** The parser may already have acted on malicious bytes before their digest entered protected state.
17. **“Sealing proves health remotely.”** Sealing authorizes a local object; attestation supplies evidence to an external verifier.
18. **“Binding a disk key to every firmware PCR is strongest.”** It may turn benign firmware or hardware changes into permanent data loss.
19. **“Unified images cover all configuration.”** Loader variables, firmware data, external extensions and device state may still influence boot.
20. **“Boot integrity persists forever.”** Runtime code loading, kernel writes, DMA and updates can invalidate the useful claim horizon.
21. **“IMA automatically measures everything.”** Coverage follows the active policy, hooks, templates and timing.
22. **“A virtual TPM equals a discrete TPM.”** Its state, rollback resistance and keys inherit hypervisor and migration assumptions.
23. **“Recovery may bypass policy because it is exceptional.”** Recovery often has more authority and requires at least as careful governance.
24. **“Fail-closed has no security cost.”** Fleet-wide unavailability can force unsafe manual bypasses; design bounded degraded modes deliberately.
25. **“More attestation data is always better.”** Detailed logs can leak hardware, software, tenant and vulnerability information.
26. **“A reboot repairs a rejected host.”** Preserve evidence, identify the mismatch, restore approved state and obtain fresh attestation.

## Worked Examples

### Example 1

A signed loader's signing certificate is in `db`, but the loader's digest is in `dbx`. The forbidden match wins under the simplified policy; selecting the next approved boot entry is correct, not ignoring revocation because the signature verifies.

### Example 2

A fleet blocks a vulnerable loader before deploying its replacement to remote sites. Those machines have no non-revoked recovery image and stop booting. A safe rollout inventories paths, deploys and tests replacements, then applies revocation with outage recovery prepared.

### Example 3

A quote signature and device credential validate, but the challenge equals yesterday's stored nonce. The verifier rejects the evidence as replayable even though its PCR values describe an approved historical boot.

### Example 4

The event log lists loader A and kernel B, but replay yields a PCR different from the quote. The verifier reports cryptographic inconsistency before debating whether A or B is acceptable; policy appraisal cannot repair an unauthenticated log.

### Example 5

A signed kernel loads an unsigned external initrd named by mutable loader configuration. Kernel authentication alone does not cover early user space. Embedding the initrd in a signed image or authenticating and measuring it before use closes the gap.

### Example 6

A disk key is sealed to exact firmware PCRs. A legitimate firmware update changes a measurement and the host cannot unlock. A signed PCR-policy scheme can admit reviewed old and new states during rollout without exposing the key to arbitrary measurements.

### Example 7

A remote appraiser accepts PCR 7 alone because Secure Boot is enabled. It misses an approved but obsolete loader. Adding the relevant image and configuration PCRs, replayed events and a minimum-version policy addresses the actual rollback question.

### Example 8

A VM snapshot restores both guest disk and software-emulated TPM state. The guest produces an internally consistent old quote. An external nonce prevents quote replay, but detecting rolled-back acceptable state also requires version policy or freshness anchored outside the snapshot.

### Example 9

IMA measures executables but its policy omits configuration buffers consumed by a privileged daemon. A quote can validate the executable chain while the daemon follows hostile configuration. The claim must exclude configuration integrity or extend the measurement policy deliberately.

### Example 10

A rescue image is correctly signed by a permanent fleet-wide key and automatically releases tenant disks. Compromise of that key bypasses every normal version floor. Separate recovery authorization, per-device or tenant policy, restricted networking and audited human approval reduce the blast radius.

## Cross-Program Connections

- **Computer architecture:** reset, privilege, TPM locality, memory protection and dynamic launch define hardware roots and transitions.
- **Security engineering:** key ceremonies, least privilege, revocation, threat models and recovery governance bound every trust claim.
- **Cryptography:** digest collision resistance, signature verification, nonce freshness, certificate validation and algorithm agility support the mechanism.
- **Supply-chain engineering:** build provenance, artifact identities, signer authorization and vulnerability response populate reference policy.
- **Platform engineering:** image construction, fleet rollout, firmware management, quarantine and secret brokers operationalize admission and appraisal.
- **Distributed systems:** remote attestation faces freshness, partial failure, cached authorization, identity and policy-consistency problems.
- **Data engineering:** event logs, reference manifests and decision evidence require schema evolution, retention and reproducible interpretation.
- **Privacy engineering:** stable device credentials and detailed measurements can enable tracking or disclose sensitive configuration.
- **Reliability engineering:** deny-list sequencing, fallback slots, offline recovery and key rotation trade security against availability.
- **Formal methods:** hash-chain replay and composed acceptance predicates expose assumptions and counterexamples explicitly.

## References

1. UEFI Forum, [UEFI Specification 2.11: Secure Boot and Driver Signing](https://uefi.org/specs/UEFI/2.11/32_Secure_Boot_and_Driver_Signing.html), platform modes, authenticated variables, `PK`, `KEK`, signature databases and image validation; retrieved 2026-09-04.
2. Trusted Computing Group, [TPM 2.0 Library Specification](https://trustedcomputinggroup.org/resource/tpm-library-specification/), current TPM architecture, structures and commands including PCRs, policies and attestation; retrieved 2026-09-04.
3. Trusted Computing Group, [PC Client Platform Firmware Profile Specification](https://trustedcomputinggroup.org/resource/pc-client-specific-platform-firmware-profile-specification/), firmware TPM initialization, PCR allocation and event-log requirements; retrieved 2026-09-04.
4. Trusted Computing Group, [PC Client Reference Integrity Manifest Specification](https://trustedcomputinggroup.org/resource/tcg-pc-client-reference-integrity-manifest-specification/), reference information and verifier use of event logs and quotes; retrieved 2026-09-04.
5. Linux Kernel Documentation, [TPM Event Log](https://docs.kernel.org/security/tpm/tpm_event_log.html), firmware measurement-log handoff, replay purpose and UEFI final-event handling; retrieved 2026-09-04.
6. Linux Kernel Documentation, [IMA Template Management Mechanism](https://docs.kernel.org/security/IMA-templates.html), runtime measurement templates, digest fields, event names and signature data; retrieved 2026-09-04.
7. UAPI Group, [Unified Kernel Images](https://uapi-group.org/specifications/specs/unified_kernel_image/), signed PE composition, embedded boot inputs and predictable section measurement; retrieved 2026-09-04.
8. UAPI Group, [Linux TPM PCR Registry](https://uapi-group.org/specifications/specs/linux_tpm_pcr_registry/), documented Linux PCR uses for firmware, boot policy, images, configuration and phases; retrieved 2026-09-04.
9. systemd project, [TPM2 PCR Measurements Made by systemd](https://systemd.io/TPM2_PCR_MEASUREMENTS/), concrete boot-manager, stub and user-space measurement behavior; retrieved 2026-09-04.
10. National Institute of Standards and Technology, [SP 800-193: Platform Firmware Resiliency Guidelines](https://csrc.nist.gov/pubs/sp/800/193/final), protection, detection and recovery principles for platform firmware; retrieved 2026-09-04.

## Exercises

### Exercise 1

Explain the distinct decisions made by UEFI Secure Boot, measured boot, remote attestation and sealing. Name the relying party and failure effect for each.

### Exercise 2

Using SHA-256, an all-zero 32-byte initial PCR and event digests `SHA256("firmware")`, `SHA256("loader")` and `SHA256("kernel")`, compute the final PCR by ordered extension. Then reverse loader and kernel and explain the result.

### Exercise 3

Design a verifier for a fleet that permits current version 42, next version 43 during rollout, and a restricted recovery image. Include enrollment, nonce, quote, PCR selection, log parsing, replay, reference appraisal, expiry and decision evidence.

### Exercise 4

An update must rotate a loader signing key and revoke the old loader generation without making remote devices unbootable. Specify artifact, key, database, rollback-floor and recovery sequencing plus negative tests.

### Exercise 5

Audit a platform that authenticates its kernel but accepts a mutable command line and external initrd, seals its disk key to exact firmware PCRs, accepts quotes without nonces and permits an unsigned recovery shell. Produce a corrective design and bounded assurance claim.

## Answers to the Exercises

### Answer 1

UEFI Secure Boot is a local pre-execution admission decision: firmware or a conforming boot component validates a UEFI image under current mode and allowed/forbidden policy, then executes or rejects it. Its immediate relying party is the next boot stage; failure selects another path, recovery or halt.

Measured boot records digests and events into protected state; its producer does not necessarily reject anything. Remote attestation supplies signed, fresh evidence to an external verifier, which authenticates the key, replays logs and applies reference policy before granting access or quarantining. Sealing is local TPM authorization for using a secret or key when a policy such as approved PCR state succeeds. None of these decisions proves software correctness.

### Answer 2

The exact recurrence is `p = SHA256(p || SHA256(event))`, where both values are raw 32-byte strings. A deterministic recomputation is:

<!-- bijux-verify: {"id":"pcr-sha256-event-replay","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"firmware-loader-kernel c031287e1c32468eb4d8f4e3c9cd14e72b92781a6152cbba7971a3feba55fd31\nfirmware-kernel-loader f165dd68c526f9764dc675b46651f503bd416c748a408245fb7165d3d6392815\norder_matters true\n"}} -->
```python
from hashlib import sha256


def replay(events: tuple[str, ...]) -> str:
    pcr = bytes(32)
    for event in events:
        event_digest = sha256(event.encode()).digest()
        pcr = sha256(pcr + event_digest).digest()
    return pcr.hex()


ordered = replay(("firmware", "loader", "kernel"))
reversed_tail = replay(("firmware", "kernel", "loader"))
print("firmware-loader-kernel", ordered)
print("firmware-kernel-loader", reversed_tail)
print("order_matters", str(ordered != reversed_tail).lower())
```

The unequal results demonstrate order sensitivity for this toy sequence. They do not reproduce a real TCG log, whose event encodings, bank selection, initial values, informational events and PCR allocations must follow the applicable profile.

### Answer 3

Enroll each device by validating its TPM credential path and registering an operational attestation key with attributes and revocation state. For every decision, send an unpredictable nonce bound to the service request and demand a quote over the PCRs that cover firmware policy, boot images and relevant configuration. Validate structure, signature, key, nonce, selection and PCR digest; parse the raw event log under strict bounds; replay extended events in the correct banks; and reject gaps or inconsistencies before policy appraisal.

Reference policy accepts version 42 until a stated retirement date and version 43 from its approved rollout time. It accepts the recovery image only with its separate measurement, declared recovery event and restricted network/secret tier. Store raw-evidence digest, parser/policy versions, nonce, device identity, decision and reasons. Expire transitional version 42, revoke affected artifacts when replacement and recovery coverage are proven, and require fresh evidence after reboot or a bounded authorization lifetime.

### Answer 4

First generate and protect the new key, publish its public half through an authenticated database update and verify that existing machines still boot. Build and sign normal and recovery artifacts with the new key, deploy them to inactive slots, verify their bytes and boot them on representative hardware. Preserve a tested path to roll back only to a non-vulnerable generation.

Advance the authenticated minimum generation or install fine-grained revocation only after inventory proves each target has a new normal and rescue path. Then remove old broad trust if required. Negative tests cover old key, old loader, mixed old/new dependencies, tampered database update, replayed update, interrupted writes, full variable storage, corrupt primary slot, revoked rescue media and loss of network. Evidence records exact firmware versions and database digests; emergency bypass requires separate authorization and cannot silently lower the durable floor.

### Answer 5

The original claim covers only the signed kernel bytes. Authenticate or embed the initrd and command line in a cohesive signed image, or independently verify and measure them before use. Replace brittle direct sealing with a signed, reviewed PCR policy that admits current and next firmware states while requiring the approved kernel/initrd/configuration state. Protect the policy-signing key and keep an independently authorized recovery object.

Require a fresh per-request nonce, intended PCR selection, enrolled attestation key, signature validation, exact log replay and semantic appraisal. Authenticate and measure recovery under a separate restricted policy; require suitable human or remote authorization and deny ordinary production secret release. A defensible resulting claim is: under the enrolled firmware/TPM roots and current reference policy, this fresh boot used an approved, non-revoked image containing the measured kernel, initrd and command line and reached the declared boot phase. It does not prove application correctness, runtime immutability, peripheral firmware coverage or resistance to attacks outside the roots.
