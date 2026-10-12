#!/usr/bin/env bash
# Documentation and program checks retain independent accepted source authorities.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

repo_root="$(git rev-parse --show-toplevel)"
cd "${repo_root}"
pin_path='.github/standards/bijux-docs.sha'
[[ -f "${pin_path}" && ! -L "${pin_path}" ]] || {
  echo 'ERROR: a regular documentation source pin is required' >&2
  exit 1
}
source_sha="$(cat "${pin_path}")"
[[ "${source_sha}" =~ ^[0-9a-f]{40}$ ]] || {
  echo 'ERROR: documentation source requires a full commit SHA' >&2
  exit 1
}

source_root="${BIJUX_STD_ROOT:-}"
if [[ -z "${source_root}" ]]; then
  source_root="${repo_root}/artifacts/docs/source/${source_sha}"
  for directory in artifacts artifacts/docs artifacts/docs/source "${source_root}"; do
    [[ ! -L "${directory}" ]] || {
      echo 'ERROR: documentation source cache cannot contain symlinks' >&2
      exit 1
    }
  done
  if [[ ! -d "${source_root}/.git" ]]; then
    mkdir -p "${source_root}"
    [[ -z "$(ls -A "${source_root}")" ]] || {
      echo 'ERROR: documentation source cache must be an owned Git checkout' >&2
      exit 1
    }
    git -C "${source_root}" init --quiet
    git -C "${source_root}" remote add origin https://github.com/bijux/bijux-std.git
    git -C "${source_root}" fetch --quiet --depth 1 origin "${source_sha}"
    [[ "$(git -C "${source_root}" rev-parse 'FETCH_HEAD^{commit}')" == "${source_sha}" ]]
    git -C "${source_root}" checkout --quiet --detach "${source_sha}"
  fi
fi

bash "${source_root}/shared/bijux-checks/scripts/verify-accepted-source.sh" \
  "${source_root}" "${source_sha}"
python3 "${source_root}/.github/scripts/check_workflow_projection.py" \
  --target "${repo_root}" --repo bijux-masterclass --source-sha "${source_sha}"
export BIJUX_STD_ROOT="${source_root}"
export BIJUX_STD_REF="${source_sha}"
source .bijux/shared/bijux-docs/tooling/scripts/docs_source_authority.sh
verify_docs_authority "${repo_root}" "${repo_root}/.bijux/shared/bijux-docs"
python3 .bijux/shared/bijux-docs/tooling/scripts/project_bijux_docs.py \
  "${repo_root}" "${repo_root}/.bijux/shared/bijux-docs" --check
python3 .bijux/shared/bijux-docs/tooling/scripts/sync_mkdocs_hub.py \
  "${repo_root}" "${repo_root}/.bijux/shared/bijux-docs" --check
