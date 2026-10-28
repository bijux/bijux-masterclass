# Exercises — Module 08: Virtualization, Images, Boot, and Cloud Compute

Complete these before opening the worked answers. Each response must name the mechanism, failure boundary, and decisive evidence where relevant.

## Exercise 1 — VM versus container

State the kernel boundary difference between a virtual machine and a container.

## Exercise 2 — Boot stage

The provider reports a VM running but SSH and Atlas are unavailable. Name three independent boot layers to inspect.

## Exercise 3 — Image content

Which of these belong in an image: OS packages, instance private key, Atlas durable spool, baseline hardening?

## Exercise 4 — cloud-init idempotence

Why should initialization tolerate a retry or expose an explicit one-shot boundary?

## Exercise 5 — User-data secret

Why is a database password in cloud user data unsafe even if the VM is private?

## Exercise 6 — Identity source

Why is the VM hostname a poor authorization identity?

## Exercise 7 — Disk lifecycle

A root disk survives reboot. Which stronger events must be tested before calling it durable?

## Exercise 8 — Ephemeral disk use

Give a safe Atlas use for instance-local ephemeral storage.

## Exercise 9 — Maintenance event

How should an application treat a provider maintenance notice from metadata?

## Exercise 10 — Immutable replacement

What state must exist outside the image before Atlas can be replaced safely?

## Exercise 11 — Image drift

Why does patching one running VM without rebuilding the image create future inconsistency?

## Exercise 12 — Replacement oracle

What proves a replacement rather than a restart?
