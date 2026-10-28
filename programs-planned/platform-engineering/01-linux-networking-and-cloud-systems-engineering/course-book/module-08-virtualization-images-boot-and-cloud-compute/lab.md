# Lab — Module 08: Virtualization, Images, Boot, and Cloud Compute

## Goal

Demonstrate the VM boot and replacement model without hiding mutable state inside the image.

## Safety boundary

Use a disposable local VM or optional cloud instance with a strict cost and deletion boundary. Never embed real credentials in course cloud-init.

## Baseline

Record image identity, boot time, root and durable mount identities, cloud-init status, Atlas unit ordering, and instance metadata policy.

## Hypothesis

A fresh instance reconstructs code and configuration, `/run` is recreated, and durable state survives only through the explicitly selected resource or restore path.

## Controlled action

Reboot the VM, observe ephemeral/runtime changes, then create a replacement from the declared image. Attach or restore durable Atlas state and validate HTTPS and existing results. Inspect metadata access with provider-required headers/session controls.

## Oracle

Replacement has a new instance identity, exact release/config identity, restored durable results, no secret in user data, and a passing verified request.

## Evidence

Boot chain, image/instance IDs, cloud-init log, mount identities, metadata configuration, state hash, and old-instance deletion evidence.

## Interpretation

Explain whether the hypothesis was supported, falsified, or remained untested. Distinguish a mechanism result from a production claim and identify the first observation that changed your diagnosis.

## Cleanup

Delete replacement and unattached lab resources according to the cost ledger, revoke temporary access, and verify no public address or disk remains.

## Completion gate

Separate the evidence for reboot, stop/start, termination, and replacement.

Do not progress with an ambiguous cleanup state or an unexplained deviation from the expected oracle.
