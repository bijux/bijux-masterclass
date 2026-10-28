from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys


def call_json(command: list[str]):
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return json.loads(result.stdout)


def main() -> int:
    errors = []
    if shutil.which('tofu') is None:
        errors.append('tofu is not installed')
    if shutil.which('aws') is None:
        errors.append('AWS CLI is not installed')
    expected_account = os.environ.get('ATLAS_AWS_ACCOUNT_ID')
    expected_region = os.environ.get('ATLAS_AWS_REGION')
    if not expected_account:
        errors.append('ATLAS_AWS_ACCOUNT_ID is required')
    if not expected_region:
        errors.append('ATLAS_AWS_REGION is required')
    observed = None
    if not errors:
        observed = call_json(['aws', 'sts', 'get-caller-identity'])
        if observed.get('Account') != expected_account:
            errors.append('caller account does not match ATLAS_AWS_ACCOUNT_ID')
        configured_region = subprocess.run(
            ['aws', 'configure', 'get', 'region'], text=True, capture_output=True, check=False
        ).stdout.strip()
        if configured_region and configured_region != expected_region:
            errors.append('AWS CLI configured region differs from ATLAS_AWS_REGION')
    report = {
        'expectedAccount': expected_account,
        'expectedRegion': expected_region,
        'caller': observed,
        'allowApply': os.environ.get('ALLOW_AWS_APPLY') == '1',
        'valid': not errors,
        'errors': errors,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
