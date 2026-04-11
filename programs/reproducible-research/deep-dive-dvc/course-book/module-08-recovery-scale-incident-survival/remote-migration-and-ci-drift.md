# Remote Migration and CI Drift

Long-lived systems move.

Storage providers change, buckets are renamed, credentials rotate, CI images update, and
default tools shift. A DVC project that ignores those changes may still look clean in Git
while becoming harder to restore.

Module 08 treats remote migration and CI drift as recovery risks, not background chores.

## Remote migration is about continuity

A remote migration is not only changing a URL.

The recovery question is:

> Can every state we still promise to recover be restored from the new location?

A careful migration needs:

- an inventory of referenced states that still matter
- a copy plan for required DVC objects
- verification from a clean checkout
- a rollback plan if the new remote is incomplete
- updated documentation and credentials
- a clear cutover decision

Weak migration:

```bash
dvc remote default new-storage
```

Stronger migration:

```bash
dvc remote list
dvc remote add archive s3://new-bucket/archive
dvc push archive --all-commits
dvc pull -r archive
make -C capstone recovery-review
```

The exact command set depends on the project and DVC version. The principle is stable:
copy and verify before trusting the new boundary.

## Migration should respect retention policy

Do not blindly migrate every object if policy says some exploratory states can expire.

Do not migrate only recent objects if policy says older releases must remain recoverable.

Migration should follow the retention map:

- protected releases move first
- current mainline state must stay restorable
- audit or publication evidence gets explicit handling
- expired exploratory objects may be excluded intentionally

The difference between intentional exclusion and accidental loss should be documented.

## CI drift changes the executor

CI is part of the reproducibility surface.

It can drift through:

- base image updates
- language runtime changes
- default package upgrades
- operating system package changes
- hardware or runner changes
- credential or permission changes

If the same repository starts producing different results after a CI image update, the
workflow did not necessarily become dishonest. But the executor changed, so the evidence
story needs review.

## Pin what matters and report what matters

A durable CI strategy often includes:

- pinned base images or tool versions
- dependency lockfiles
- platform reports
- documented runner assumptions
- scheduled checks that detect drift
- release notes when executor changes affect results

Pinning everything forever is not the goal. Knowing when executor change affects evidence
is the goal.

## Review checkpoint

You understand this core when you can:

- explain why remote migration is a recovery continuity problem
- verify a new remote from a clean checkout
- use retention policy to decide what migrates
- identify CI drift that can change reproducibility evidence
- document executor changes that affect comparisons or releases

Storage and CI are not passive background. They are parts of the recovery system.
