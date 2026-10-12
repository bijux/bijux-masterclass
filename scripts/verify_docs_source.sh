#!/usr/bin/env bash
# Documentation and program checks retain independent accepted source authorities.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

mode="${1:-check}"
[[ "$#" -le 1 ]] && [[ "${mode}" == check || "${mode}" == sync ]] || {
  echo 'ERROR: documentation source mode must be check or sync' >&2
  exit 1
}

repo_root="$(git rev-parse --show-toplevel)"
cd "${repo_root}"
pin_path='.github/standards/bijux-docs.sha'
[[ -f "${pin_path}" && ! -L "${pin_path}" ]] || {
  echo 'ERROR: a regular documentation source pin is required' >&2
  exit 1
}
git ls-files --error-unmatch "${pin_path}" >/dev/null
source_sha="$(cat "${pin_path}")"
[[ "${source_sha}" =~ ^[0-9a-f]{40}$ ]] || {
  echo 'ERROR: documentation source requires a full commit SHA' >&2
  exit 1
}

if [[ -n "${BIJUX_STD_REF:-}" && "${BIJUX_STD_REF}" != "${source_sha}" ]]; then
  echo 'ERROR: documentation source override differs from the declared source pin' >&2
  exit 1
fi

policy_path='.github/standards/dependency-notification-source.json'
[[ -f "${policy_path}" && ! -L "${policy_path}" ]] || {
  echo 'ERROR: a regular workflow policy authority is required' >&2
  exit 1
}
git ls-files --error-unmatch "${policy_path}" >/dev/null
policy_record="$(python3 - "${policy_path}" <<'PY_POLICY'
import hashlib
import json
from pathlib import Path
import re
import sys
path = Path(sys.argv[1])
body = path.read_bytes()
record = json.loads(body)
required = {"schema", "repository", "baseline_sha", "execution_policy_sha"}
if not isinstance(record, dict) or set(record) != required or type(record["schema"]) is not int or record["schema"] != 1 or record["repository"] != "bijux-masterclass" or record["baseline_sha"] != "1ad55aafdb44e2d47890632653e7d9c312cc7968" or not isinstance(record["execution_policy_sha"], str) or not re.fullmatch(r"[0-9a-f]{40}", record["execution_policy_sha"]):
    raise SystemExit("ERROR: workflow policy requires the exact Masterclass source authority")
print(record["execution_policy_sha"], hashlib.sha256(body).hexdigest())
PY_POLICY
)"
read -r policy_sha policy_digest <<<"${policy_record}"
policy_root="${repo_root}/artifacts/github-policy-source/${policy_sha}"
for directory in artifacts artifacts/github-policy-source "${policy_root}"; do
  [[ ! -L "${directory}" ]] || {
    echo 'ERROR: workflow policy cache cannot contain symlinks' >&2
    exit 1
  }
done

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
if [[ ! -d "${policy_root}/.git" ]]; then
  mkdir -p "${policy_root}"
  [[ -z "$(ls -A "${policy_root}")" ]] || {
    echo 'ERROR: workflow policy cache must be an owned Git checkout' >&2
    exit 1
  }
  git -C "${policy_root}" init --quiet
  git -C "${policy_root}" remote add origin https://github.com/bijux/bijux-std.git
  git -C "${policy_root}" fetch --quiet --depth 1 origin "${policy_sha}"
  [[ "$(git -C "${policy_root}" rev-parse 'FETCH_HEAD^{commit}')" == "${policy_sha}" ]]
  git -C "${policy_root}" checkout --quiet --detach "${policy_sha}"
fi
# Policy and documentation have distinct accepted owners. Environment overrides
# describe the documentation source only; they cannot choose workflow authority.
BIJUX_STD_ALLOW_LOCAL_SOURCE=0 BIJUX_STD_GIT_URL=https://github.com/bijux/bijux-std.git \
  bash .bijux/shared/bijux-checks/scripts/verify-accepted-source.sh "${policy_root}" "${policy_sha}"
python3 "${policy_root}/.github/scripts/check_workflow_projection.py" \
  --target "${repo_root}" --repo bijux-masterclass --source-sha "${policy_sha}"
export BIJUX_STD_ROOT="${source_root}"
export BIJUX_STD_REF="${source_sha}"
source .bijux/shared/bijux-docs/tooling/scripts/docs_source_authority.sh
verify_docs_authority "${repo_root}" "${repo_root}/.bijux/shared/bijux-docs"
if [[ "${mode}" == sync ]]; then
  bash .bijux/shared/bijux-docs/tooling/scripts/sync_bijux_docs.sh
fi
python3 .bijux/shared/bijux-docs/tooling/scripts/project_bijux_docs.py \
  "${repo_root}" "${repo_root}/.bijux/shared/bijux-docs" --check
python3 .bijux/shared/bijux-docs/tooling/scripts/sync_mkdocs_hub.py \
  "${repo_root}" "${repo_root}/.bijux/shared/bijux-docs" --check
python3 .bijux/shared/bijux-docs/tooling/quality/validate_source_layout.py "${repo_root}"

[[ -f "${pin_path}" && ! -L "${pin_path}" && "$(cat "${pin_path}")" == "${source_sha}" ]] || {
  echo 'ERROR: documentation source pin changed during verification' >&2
  exit 1
}
python3 - "${policy_path}" "${policy_digest}" <<'PY_POLICY_FINAL'
import hashlib
from pathlib import Path
import sys
path = Path(sys.argv[1])
if path.is_symlink() or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != sys.argv[2]:
    raise SystemExit("ERROR: workflow policy authority changed during verification")
PY_POLICY_FINAL
bash "${source_root}/shared/bijux-checks/scripts/verify-accepted-source.sh" "${source_root}" "${source_sha}"
BIJUX_STD_ALLOW_LOCAL_SOURCE=0 BIJUX_STD_GIT_URL=https://github.com/bijux/bijux-std.git \
  bash .bijux/shared/bijux-checks/scripts/verify-accepted-source.sh "${policy_root}" "${policy_sha}"
