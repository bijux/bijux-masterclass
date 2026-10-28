# Exercises — Backup, Restore, RPO, RTO, and Disaster Recovery

Work from the chapter and executable artifacts, but write your own reasoning before reading the solutions. Each answer should name the authoritative state, the unsafe shortcut, and the evidence that would decide the case.

## 1. Calculate effective RPO

Backups run hourly. The last successful backup is 75 minutes old, and 20 minutes of transaction logs after it are retained. What loss might a restore face?

## 2. Decompose RTO

List the phases that make up Atlas database RTO and explain why copy speed alone is insufficient.

## 3. Design the backup manifest

What fields must a manifest contain so an operator can restore Atlas without the source cluster?

## 4. Why restore into an empty destination?

Explain which false dependencies an in-place restore can hide.

## 5. Include encryption keys in recovery design

A backup is stored cross-account but encrypted by a key available only in the failed source account. What is the recovery classification?

## 6. Place copies across failure domains

Choose locations for local snapshots, regional backups, and account-level recovery copies.

## 7. Protect a point-in-time recovery chain

What happens if one archived transaction-log segment is missing between the base backup and target time?

## 8. Garbage-collect deduplicated backup objects

How can content-addressed deduplication make deletion dangerous?

## 9. Define domain validation after restore

What Atlas checks should run after restoring files or a database successfully?

## 10. Assign drill authority

Who may initiate a disaster restore, accept data loss, and cut traffic to the recovered environment?

## 11. Reject backup-job success as proof

A CronJob exits zero and uploads 10,000 objects. Why might the backup still be unusable?

## 12. Design a regional disaster exercise

What would be required to classify regional DR as executed rather than documented?
