# RPO and RTO calculations

## Recovery point objective

For a failure at time `F` and the newest verified recovery point at time `P`:

```text
observed data loss window = F - P
```

The service meets its RPO only if the selected point is complete and restorable. A snapshot timestamp alone is insufficient when later logs, manifests, or keys are missing.

## Recovery time objective

Break RTO into owned phases:

```text
T_detect
+ T_decide
+ T_provision
+ T_transfer
+ T_replay
+ T_validate
+ T_redirect
+ T_confirm
```

For a full backup of size `S` and effective transfer rate `R`, the theoretical transfer floor is `S / R`. Real recovery adds request overhead, throttling, decompression, decryption, filesystem work, log replay, and validation.

## Example

A 600 GiB base backup transfers at an effective 150 MiB/s:

```text
600 × 1024 MiB / 150 MiB/s ≈ 4096 s ≈ 68 min
```

If provisioning takes 15 minutes, replay 25 minutes, validation 20 minutes, and traffic restoration 10 minutes, the practical RTO is at least 138 minutes before contingency. An advertised “five-minute snapshot restore” does not satisfy a two-hour service RTO unless the complete path fits.

## Evidence rule

Measure the executed restore phases and report p50/p95 across drills where possible. Estimated values remain planning evidence, not recovery proof.
