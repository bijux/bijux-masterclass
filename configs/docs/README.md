# Catalogue environments

`requirements-docs.txt` owns the eight documentation capabilities used by the current
catalogue and publisher. The normal `make series-docs-install` path uses these declared
requirements and retains the production publisher's existing Python selection.

`environment-profiles.json` admits one local verification profile:
`darwin-arm64-cpython-314`. Its exact 44-distribution inventory and download hashes are
in `requirements-docs.lock`. The installer requires base CPython 3.14.4 on Darwin arm64
and uv 0.11.17. It checks package versions, interpreter and standard-library bytes,
installed environment files, source ownership, and the lock and Make recipes. Ready
or user-owned environments are never upgraded, replaced or repaired after drift.
Choose a new path under `artifacts/` when an admitted source or runtime changes.

```sh
make docs-nav-check \
  PYTHON=python3.14 \
  DOCS_PROFILE=darwin-arm64-cpython-314 \
  VENV_DIR=artifacts/venv/catalogue-verification
```

Set `BIJUX_STD_ROOT` and `BIJUX_STD_REF` to the independently fetched, exact accepted
standards source required by the repository's shared documentation checker. A local
verification profile does not approve a publication. No Linux production profile is
admitted by the locked installer; selecting an absent profile fails before creation.

When reviewing a dependency change, reconcile the direct requirements, full profile
inventory, and platform-appropriate distribution hashes together. Regenerate the lock
with the reviewed exact inventory as constraints, then prove a fresh installation,
package consistency, refusal controls, and the affected catalogue and navigation
checks. Package count alone is not proof of dependency identity.
