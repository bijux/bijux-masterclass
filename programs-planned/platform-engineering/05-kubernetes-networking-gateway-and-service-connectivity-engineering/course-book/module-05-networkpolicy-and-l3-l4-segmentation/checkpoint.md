# Checkpoint — NetworkPolicy segmentation

## Required evidence

- flow and dependency inventory
- selector-authority assumptions
- ingress/egress isolation truth table
- DNS and node-local resolver policy
- default-deny rollout and rollback plan
- completed policy lab

## Decision defense

Defend why segmentation and application authorization are independent controls and name the evidence that proves actual plugin enforcement.

## Progression gate

You may progress only when every required artifact is reproducible from a clean checkout and your explanation separates intent, controller observation, data-plane behavior, and protocol evidence.
