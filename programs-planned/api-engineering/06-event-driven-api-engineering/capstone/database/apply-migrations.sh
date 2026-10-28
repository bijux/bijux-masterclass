#!/usr/bin/env sh
set -eu
: "${TEST_DATABASE_URL:?TEST_DATABASE_URL is required}"
command -v psql >/dev/null 2>&1 || { echo "psql is required" >&2; exit 1; }
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
for migration in "$HERE"/migrations/*.sql; do
  printf 'applying %s\n' "$(basename "$migration")"
  psql "$TEST_DATABASE_URL" -v ON_ERROR_STOP=1 -f "$migration"
done
