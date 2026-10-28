# Exercises — Compute, Images, Bootstrap, and Replacement

## 1. Classify the artifacts

Classify these as image, launch definition, runtime configuration, or durable state: systemd unit, subnet ID, database password, Atlas binary, completed result, log destination.

## 2. Backup versus replaceability

Why is “the instance root disk is backed up nightly” not the same as a replaceable host design?

## 3. Deterministic bootstrap

What makes a bootstrap deterministic in addition to being idempotent?

## 4. Secrets in user data

Give four reasons not to place secrets in user data.

## 5. IMDSv2 and role authority

Explain the security relationship among IMDSv2, an instance profile, and the role’s permissions.

## 6. Desired capacity one

Why does an Auto Scaling group with desired capacity one not establish high availability?

## 7. Health layers

Distinguish instance status, liveness, readiness, and load-balancer health.

## 8. Limits of `create_before_destroy`

Give three ways `create_before_destroy` can fail to provide uninterrupted replacement.

## 9. Image release identity

What information should identify a machine image release besides the image ID?

## 10. Emergency in-place patch

When might an emergency in-place patch be defensible, and what must happen afterward?

## 11. Architecture

Why must architecture be an explicit launch concern?

## 12. Replacement evidence

Design the evidence needed to prove an Atlas host replacement without claiming multi-zone availability.
