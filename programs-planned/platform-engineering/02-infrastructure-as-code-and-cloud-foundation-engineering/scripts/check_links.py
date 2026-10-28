from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

from common import COURSE

LINK_RE = re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')


def main() -> int:
    errors: list[str] = []
    checked = 0
    for path in sorted(COURSE.rglob('*.md')):
        text = path.read_text(encoding='utf-8')
        for raw in LINK_RE.findall(text):
            target = raw.strip().split()[0].strip('<>')
            if target.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            target = unquote(target.split('#', 1)[0])
            if not target:
                continue
            checked += 1
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(COURSE.resolve())
            except ValueError:
                errors.append(f'{path.relative_to(COURSE)} escapes course: {target}')
                continue
            if not resolved.exists():
                errors.append(f'{path.relative_to(COURSE)} missing target: {target}')
    print(json.dumps({"checked": checked, "valid": not errors, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
