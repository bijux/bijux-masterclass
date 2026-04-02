# Workflow Review Checklist

Use this checklist when a workflow change needs evidence, not intuition.

## Contract review

- Read `workflow/CONTRACT.md`
- Read `workflow/contracts/FILE_API.md`
- Confirm whether the change is contract-preserving or contract-changing
- If a publish surface changed, decide whether `publish/v1/` still tells the truth

## Declared workflow review

Run:

```bash
make wf-lint
make wf-dryrun
```

Check:

- the workflow still lints cleanly
- the dry-run plan still matches the declared repository story
- new rules or targets appear only where intended

## Drift review

Run:

```bash
snakemake --profile profiles/local --list-changes code || true
snakemake --profile profiles/local --list-changes params || true
snakemake --profile profiles/local --list-changes input || true
```

Check:

- code drift is visible when workflow implementation changed
- parameter drift is visible when config meaning changed
- input drift is visible when file dependencies changed

## Executed evidence review

Run:

```bash
make verify
make verify-report
make profile-audit
```

Check:

- published artifacts still parse and match the expected boundary
- profile differences remain execution policy, not hidden semantic drift
- logs, benchmarks, and provenance remain inspectable

## Escalation rule

If any answer is still unclear after this checklist, stop and update the contract docs
before extending the workflow further.
