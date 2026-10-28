from __future__ import annotations

import json
import re
from pathlib import Path

from common import CAPSTONE


STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"')
COMMENT_RE = re.compile(r'(?m)#.*$|//.*$')
SECRET_RE = re.compile(
    r'(?i)(access_key\s*=|secret_key\s*=|AKIA[0-9A-Z]{16}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)'
)


def strip_strings_and_comments(text: str) -> str:
    return STRING_RE.sub('""', COMMENT_RE.sub('', text))


def balanced(text: str) -> bool:
    clean = strip_strings_and_comments(text)
    pairs = {'}': '{', ']': '[', ')': '('}
    stack: list[str] = []
    for char in clean:
        if char in '{[(':
            stack.append(char)
        elif char in '}])':
            if not stack or stack.pop() != pairs[char]:
                return False
    return not stack


def main() -> int:
    errors: list[str] = []
    hcl_files = sorted(CAPSTONE.rglob('*.tf')) + sorted(CAPSTONE.rglob('*.hcl'))
    for path in hcl_files:
        text = path.read_text(encoding='utf-8')
        rel = path.relative_to(CAPSTONE).as_posix()
        if not balanced(text):
            errors.append(f'unbalanced delimiters: {rel}')
        if SECRET_RE.search(text):
            errors.append(f'secret-like material in HCL: {rel}')
        if re.search(r'(?m)^(?:variable|output)\s+"[^"]+"\s*\{[^\n}]*,[^\n}]*\}\s*$', text):
            errors.append(f'comma-separated compact block is not accepted: {rel}')
        if re.search(r'(?s)from_port\s*=\s*22.*?cidr_blocks\s*=\s*\[\s*"0\.0\.0\.0/0"', text):
            errors.append(f'public SSH rule: {rel}')
    versions = list((CAPSTONE / 'modules').rglob('versions.tf')) + [
        CAPSTONE / 'bootstrap' / 'versions.tf',
        CAPSTONE / 'stacks' / 'foundation' / 'versions.tf',
        CAPSTONE / 'stacks' / 'workload-dev' / 'versions.tf',
    ]
    for path in versions:
        text = path.read_text(encoding='utf-8')
        if '>= 1.12.5, < 1.13.0' not in text:
            errors.append(f'OpenTofu pin missing: {path.relative_to(CAPSTONE)}')
        if 'version = "~> 6.58.0"' not in text:
            errors.append(f'AWS provider pin missing: {path.relative_to(CAPSTONE)}')
    report = {"hclFiles": len(hcl_files), "valid": not errors, "errors": errors}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
