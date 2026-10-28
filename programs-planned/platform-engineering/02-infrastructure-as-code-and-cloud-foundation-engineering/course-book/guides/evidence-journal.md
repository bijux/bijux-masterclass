# Guide — Build an Evidence Journal

Infrastructure work is easy to misremember because configuration, plan, state, provider response, and data-plane behavior are separate artifacts. An evidence journal lets another operator reconstruct what was tested without relying on screenshots or the original author’s memory.

Use one directory per experiment:

```text
lab-05-network/
├── README.md
├── environment.json
├── source.sha256
├── inputs.redacted.json
├── plan/
│   ├── plan.bin.sha256
│   ├── plan.json
│   └── review.md
├── apply/
│   ├── result.json
│   └── provider-request-ids.json
├── control-plane/
├── data-plane/
├── negative-tests/
├── cleanup.json
└── limitations.md
```

## The README is an argument

It should answer:

- What engineering question was tested?
- What result would have falsified the hypothesis?
- Which environment and identity were used?
- Which source, inputs, provider lock, and state generation were involved?
- What happened?
- Which evidence supports the conclusion?
- What remains unproved?
- Was cleanup completed?

Raw output without interpretation is not a conclusion. Interpretation without raw evidence is not reproducible.

## Identity every artifact

For a plan or apply, retain at least:

```text
source commit or source-tree digest
root stack
input digest
OpenTofu version
provider lock digest
module versions
backend key
state lineage and serial
target account and region
caller role class
plan digest
time window
```

Do not store the unredacted state or saved plan in a general evidence repository. Both can contain sensitive values. Record their cryptographic digest and store the protected artifact only in an approved location when retention is necessary.

## Prefer machine-readable evidence

Good evidence can be compared and checked:

- JSON plan output rather than a cropped terminal;
- route-table and security-group API responses rather than a console screenshot;
- target-health reason codes rather than “the load balancer is green”;
- checksum manifests and restore verification rather than “backup completed”;
- explicit caller identity rather than a shell profile name;
- cleanup inventory rather than a successful destroy message.

Screenshots can provide context, but they are difficult to diff, redact, and automate.

## Record negative tests

A platform claim needs forbidden behavior as well as success. Examples:

- a workload role reads its own configuration but not production configuration;
- the edge reaches the host port while the internet cannot;
- a stale saved plan is rejected;
- a wrong-lineage state snapshot cannot be restored as authoritative;
- an untrusted CI subject cannot assume the apply role;
- a restore refuses a non-empty destination.

The negative result should include the expected denial mechanism and the observed one. A timeout is not automatically proof of a firewall rule; it may be DNS, routing, or application failure.

## Redaction rules

Never retain:

- access keys, session tokens, passwords, or secret values;
- private production keys or unredacted certificates containing sensitive private material;
- complete state files in an unprotected repository;
- user data or plans containing credentials;
- personal data or customer payloads;
- public URLs that expose a still-running sandbox.

Redaction should preserve meaning. Replace an account ID consistently with a stable placeholder rather than deleting every identifier and making the evidence impossible to correlate.

## Cleanup is part of the result

`cleanup.json` should record:

```json
{
  "destroyAttempted": true,
  "inventoryEmpty": true,
  "retained": [],
  "pendingDeletion": [],
  "owner": "learner",
  "checkedAt": "..."
}
```

If resources remain, list exact identifiers, reason, owner, cost implications, and expiry. A laboratory with uncontrolled leftovers has not completed safely.

## Evidence quality test

Hand the journal to someone who did not run the lab. They should be able to answer:

1. Which claim was tested?
2. Which generation of code, dependencies, state, account, and region was involved?
3. Which observation proves or falsifies the claim?
4. Which claims are explicitly outside the experiment?
5. Which resources remain?

If they cannot, improve the journal before passing the checkpoint.
