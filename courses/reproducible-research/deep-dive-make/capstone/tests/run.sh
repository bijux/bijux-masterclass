#!/bin/sh
set -eu

MAKE_BIN="${MAKE:-make}"

fail() { echo "selftest: FAIL: $*" >&2; exit 1; }
pass() { echo "selftest: PASS: $*"; }

hash_cmd() {
  if [ "$(uname -s 2>/dev/null)" = "Darwin" ]; then
    shasum -a 256 "$@"
  elif command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$@"
  else
    cksum "$@" | awk '{print $1 "  " $3}'
  fi
}

tmp="${TMPDIR:-/tmp}/mkselftest.$$"
mkdir -p "$tmp"
trap 'rm -rf "$tmp"' EXIT INT TERM

# Copy repo excluding build outputs and VCS data
tar cf - --exclude=./build --exclude=./.git --exclude=./dist.tar.gz . | (cd "$tmp" && tar xf -)
cd "$tmp"

# Set DEBUG=0 for selftest (no -g; faster .o hashing)
export DEBUG=0

# Heuristic guardrail: trace line count is a proxy for "too much work at parse/decision time".
# Override in CI via TRACE_MAX=<n> or disable by setting TRACE_MAX=0.
TRACE_MAX="${TRACE_MAX:-500}"

# 1) Convergence
echo "Running convergence check..."
"$MAKE_BIN" clean >/dev/null
"$MAKE_BIN" -j1 all >/dev/null
"$MAKE_BIN" -q all || fail "convergence: repo not up-to-date after build (exit $(($?)))"
pass "convergence"

# 2) Serial vs parallel equivalence
echo "Running serial/parallel equivalence check..."
"$MAKE_BIN" clean >/dev/null
"$MAKE_BIN" -j1 all >/dev/null
echo "Computing serial hash..."
# Hash all artifacts (intermediates + exes for full equivalence; Module 02)
echo "  Listing files..."
find build -type f \( -name '*.o' -o -name '*.d' -o -name 'flags.stamp' \) -print | sort > filelist.tmp
echo "  Hashing files..."
while IFS= read -r f; do hash_cmd "$f"; done < filelist.tmp > serial_hash.tmp
rm -f filelist.tmp
# Note: some compilers introduce nondeterminism (debug info paths, timestamps).
# The capstone uses -frandom-seed and fixed flags to minimize this.
hash_cmd app build/include/dynamic.h build/bin/dyn1 build/bin/dyn2 >> serial_hash.tmp
echo "  Sorting hashes..."
LC_ALL=C sort serial_hash.tmp > serial.sum
rm -f serial_hash.tmp
echo "Serial hash complete."

"$MAKE_BIN" clean >/dev/null
echo "Running parallel build..."
# Bounded parallelism + timeout (Module 02/05: safe concurrency, failure modes)
if command -v timeout >/dev/null 2>&1; then
  timeout 30 "$MAKE_BIN" -j2 all >/dev/null || fail "parallel build timeout (consider reducing -j)"
else
  "$MAKE_BIN" -j2 all >/dev/null  # Fallback; monitor manually
fi
echo "Computing parallel hash..."
# Mirror serial hashing for symmetry
echo "  Listing files..."
find build -type f \( -name '*.o' -o -name '*.d' -o -name 'flags.stamp' \) -print | sort > filelist.tmp
echo "  Hashing files..."
while IFS= read -r f; do hash_cmd "$f"; done < filelist.tmp > parallel_hash.tmp
rm -f filelist.tmp
hash_cmd app build/include/dynamic.h build/bin/dyn1 build/bin/dyn2 >> parallel_hash.tmp
echo "  Sorting hashes..."
LC_ALL=C sort parallel_hash.tmp > parallel.sum
rm -f parallel_hash.tmp
echo "Parallel hash complete."

diff -u serial.sum parallel.sum >/dev/null || fail "serial/parallel: artifact mismatch"
pass "serial-parallel equivalence"

# Module 05: Performance baseline (trace expansions <500)
echo "Running performance baseline check..."
TRACE_LINES=$("$MAKE_BIN" --trace -n all 2>&1 | wc -l)
if [ "$TRACE_MAX" -ne 0 ] && [ "$TRACE_LINES" -gt "$TRACE_MAX" ]; then
  fail "performance: trace lines exceed TRACE_MAX=$TRACE_MAX (got $TRACE_LINES). Use: make trace-count; and see: make perf. (TRACE_MAX is a guardrail; set TRACE_MAX=0 to disable.)"
fi
pass "performance: trace within TRACE_MAX=$TRACE_MAX"

# 3) Negative test: hidden input must break convergence
echo "Running negative test check..."
test -f config.mk || : > config.mk
cp config.mk config.mk.bak
printf '%s\n' '' 'CPPFLAGS += -DHIDDEN_TS=$(shell date +%s)' >> config.mk

"$MAKE_BIN" clean >/dev/null
"$MAKE_BIN" -j1 all >/dev/null
sleep 1
if "$MAKE_BIN" -q all; then
  fail "negative: converged despite hidden input"
fi
pass "negative: hidden input detected (non-convergence)"

mv config.mk.bak config.mk