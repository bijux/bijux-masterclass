# Lab — source update, projection, and process adoption

## Goal

Prove that configuration rotation has three distinct stages and that each has its own evidence.

## Safety boundary

Use the semantic projection model with fixture values. Never place real credentials in course files or command history.

## Baseline

Atlas worker starts with configuration version `v1` and one projected audience-bound token.

## Hypothesis

Updating the source object does not change an environment snapshot, a subPath file, or an application cache. A directory projection updates eventually, and the process must validate/adopt it explicitly.

## Controlled action

1. Update the source to version `v2`.
2. Advance projection time.
3. Compare environment, directory, and subPath views.
4. Trigger application reload with one deliberately invalid file.
5. Correct the file and repeat.
6. Advance token time across rotation and expiry.

## Oracle

Environment and subPath remain v1 until restart. The directory reaches v2. Invalid v2 is rejected without losing v1 service. Correct v2 is adopted atomically. Token consumers reject wrong audience and reload the rotated token.

## Evidence

Preserve object versions, projection timestamps/hashes, application accepted version, rejection reason, token audience/expiry metadata, and restart requirement.

## Interpretation

Assign ownership for every transition and explain which evidence is safe to retain without secret bytes.

## Cleanup

Delete generated fixture state and reports after copying redacted evidence.

## Completion gate

Advance only after source update, projection, reload, and credential retirement are reported as separate events.
