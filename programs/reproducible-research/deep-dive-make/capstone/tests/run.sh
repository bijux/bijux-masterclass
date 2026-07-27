#!/bin/sh
set -eu

MAKE_BIN="${MAKE:-make}"
PYTHON_BIN="${PYTHON:-python3}"
SELFTEST_REPORT_DIR="${SELFTEST_REPORT_DIR:-}"
SELFTEST_WORK_DIR="${SELFTEST_WORK_DIR:-../../../../artifacts/proof/reproducible-research/deep-dive-make/selftest/workspace}"
SELFTEST_FAULT="${SELFTEST_FAULT:-none}"

CURRENT_CHECK="setup"
FAILURE_REASON="command exited unexpectedly"
CONVERGENCE="NOT_RUN"
SERIAL_PARALLEL_EQUIVALENCE="NOT_RUN"
TRACE_GUARDRAIL="NOT_RUN"
HIDDEN_INPUT_DETECTION="NOT_RUN"
QUARANTINED_EVAL_DEMO="NOT_RUN"

fail() {
  FAILURE_REASON="$*"
  echo "selftest: FAIL: $*" >&2
  exit 1
}
pass() { echo "selftest: PASS: $*"; }
step() { echo "selftest: STEP: $*"; }

record() {
  [ -n "${SELFTEST_REPORT_DIR}" ] || return 0
  mkdir -p "${SELFTEST_REPORT_DIR}"
  printf '%s\n' "$2" > "${SELFTEST_REPORT_DIR}/$1"
}

run_logged() {
  log_name=$1
  shift
  printf '%s:' "$log_name" >> "$SELFTEST_COMMANDS"
  printf ' %s' "$@" >> "$SELFTEST_COMMANDS"
  printf '\n' >> "$SELFTEST_COMMANDS"
  if "$@" > "${SELFTEST_LOG_DIR}/${log_name}.log" 2>&1; then
    return 0
  else
    command_status=$?
  fi
  FAILURE_REASON="${log_name} command failed with exit ${command_status}"
  cat "${SELFTEST_LOG_DIR}/${log_name}.log" >&2
  return "$command_status"
}

finish() {
  status=$?
  trap - EXIT INT TERM
  if [ "$status" -eq 0 ]; then
    result="PASS"
    failed_check="none"
    failure_reason="none"
  else
    result="FAIL"
    failed_check="$CURRENT_CHECK"
    failure_reason="$FAILURE_REASON"
    case "$CURRENT_CHECK" in
      convergence) CONVERGENCE="FAIL" ;;
      serial_parallel_equivalence) SERIAL_PARALLEL_EQUIVALENCE="FAIL" ;;
      trace_guardrail) TRACE_GUARDRAIL="FAIL" ;;
      hidden_input_detection) HIDDEN_INPUT_DETECTION="FAIL" ;;
      quarantined_eval_demo) QUARANTINED_EVAL_DEMO="FAIL" ;;
    esac
  fi
  record summary.txt "result=${result}
failed_check=${failed_check}
failure_reason=${failure_reason}
convergence=${CONVERGENCE}
serial_parallel_equivalence=${SERIAL_PARALLEL_EQUIVALENCE}
trace_guardrail=${TRACE_GUARDRAIL}
hidden_input_detection=${HIDDEN_INPUT_DETECTION}
quarantined_eval_demo=${QUARANTINED_EVAL_DEMO}
workspace=${SELFTEST_WORK_DIR}"
  if [ "$status" -ne 0 ]; then
    echo "selftest: INFO: preserved workspace at ${SELFTEST_WORK_DIR}" >&2
  fi
  exit "$status"
}

trap finish EXIT
trap 'FAILURE_REASON="selftest interrupted"; exit 130' INT TERM

write_inventory() {
  output=$1
  run_logged "${output%.json}" "$PYTHON_BIN" scripts/write_build_inventory.py \
    --root . \
    --output "$output" \
    --path app \
    --path build/include/dynamic.h \
    --path build/bin/dyn1 \
    --path build/bin/dyn2 \
    --path build/flags.stamp \
    --pattern 'build/**/*.o' \
    --pattern 'build/**/*.d'
}

case "$SELFTEST_WORK_DIR" in
  ""|"/") fail "unsafe SELFTEST_WORK_DIR: ${SELFTEST_WORK_DIR}" ;;
esac
case "$SELFTEST_FAULT" in
  none|parallel-artifact-drift) ;;
  *) fail "unsupported SELFTEST_FAULT: ${SELFTEST_FAULT}" ;;
esac
rm -rf "$SELFTEST_WORK_DIR"
mkdir -p "$SELFTEST_WORK_DIR"
SELFTEST_WORK_DIR="$(cd "$SELFTEST_WORK_DIR" && pwd)"
SELFTEST_LOG_DIR="${SELFTEST_REPORT_DIR:-${SELFTEST_WORK_DIR}/evidence}/logs"
SELFTEST_COMMANDS="${SELFTEST_REPORT_DIR:-${SELFTEST_WORK_DIR}/evidence}/commands.txt"
rm -rf "$SELFTEST_LOG_DIR"
mkdir -p "$SELFTEST_LOG_DIR"
: > "$SELFTEST_COMMANDS"

# Copy repo excluding build outputs and VCS data
tar cf - --exclude=./build --exclude=./.git . | (cd "$SELFTEST_WORK_DIR" && tar xf -)
cd "$SELFTEST_WORK_DIR"

# Set DEBUG=0 for selftest (no -g; faster .o hashing)
export DEBUG=0

# A clean planning trace must stay bounded and retain target/rule attribution.
TRACE_PLAN_MAX="${TRACE_PLAN_MAX:-500}"
record settings.env "MAKE_BIN=${MAKE_BIN}
PYTHON_BIN=${PYTHON_BIN}
TRACE_PLAN_MAX=${TRACE_PLAN_MAX}
SELFTEST_FAULT=${SELFTEST_FAULT}
SELFTEST_WORK_DIR=${SELFTEST_WORK_DIR}"

# 1) Convergence
CURRENT_CHECK="convergence"
step "convergence"
run_logged convergence-clean "$MAKE_BIN" clean
run_logged convergence-build "$MAKE_BIN" -j1 all
run_logged convergence-query "$MAKE_BIN" -q all ||
  fail "convergence: repo not up-to-date after build"
record convergence.txt "PASS"
CONVERGENCE="PASS"
pass "convergence"

# 2) Serial vs parallel equivalence
CURRENT_CHECK="serial_parallel_equivalence"
step "serial-parallel equivalence"
run_logged serial-clean "$MAKE_BIN" clean
run_logged serial-build "$MAKE_BIN" -j1 all
write_inventory serial-inventory.json

run_logged parallel-clean "$MAKE_BIN" clean
echo "selftest: INFO: running bounded parallel build"
# Bounded parallelism + timeout to expose concurrency defects safely
if command -v timeout >/dev/null 2>&1; then
  run_logged parallel-build timeout 30 "$MAKE_BIN" -j2 all ||
    fail "parallel build timeout or failure (consider reducing -j)"
else
  run_logged parallel-build "$MAKE_BIN" -j2 all
fi
if [ "$SELFTEST_FAULT" = "parallel-artifact-drift" ]; then
  printf '\nselftest fault: parallel artifact drift\n' >> build/include/dynamic.h
fi
write_inventory parallel-inventory.json
record serial-inventory.json "$(cat serial-inventory.json)"
record parallel-inventory.json "$(cat parallel-inventory.json)"
if run_logged schedule-comparison "$PYTHON_BIN" scripts/compare_build_inventories.py \
  --baseline serial-inventory.json \
  --candidate parallel-inventory.json \
  --output schedule-comparison.json; then
  :
else
  record schedule-comparison.json "$(cat schedule-comparison.json)"
  fail "serial/parallel artifact contract differs; inspect schedule-comparison.json"
fi
record schedule-comparison.json "$(cat schedule-comparison.json)"
SERIAL_PARALLEL_EQUIVALENCE="PASS"
pass "serial-parallel equivalence"

# Trace evidence from a declared clean planning state
CURRENT_CHECK="trace_guardrail"
step "trace guardrail"
run_logged trace-clean "$MAKE_BIN" clean
run_logged trace-plan "$MAKE_BIN" --trace -n all
if run_logged trace-analysis "$PYTHON_BIN" scripts/analyze_trace_evidence.py \
  --trace "${SELFTEST_LOG_DIR}/trace-plan.log" \
  --output trace-evidence.json \
  --route all \
  --state clean-plan \
  --focus all \
  --maximum-lines "$TRACE_PLAN_MAX"; then
  :
else
  record trace-evidence.json "$(cat trace-evidence.json)"
  fail "trace evidence lost attribution, focus visibility, or bounded volume"
fi
record trace-evidence.json "$(cat trace-evidence.json)"
TRACE_GUARDRAIL="PASS"
pass "trace evidence is bounded and attributable"

# 3) Negative test: hidden input must break convergence
CURRENT_CHECK="hidden_input_detection"
step "hidden input detection"
test -f config.mk || : > config.mk
cp config.mk config.mk.bak
printf '%s\n' \
  '' \
  'CPPFLAGS += -DHIDDEN_COUNTER=$(shell $(PYTHON) scripts/advance_hidden_input.py --state .selftest/hidden-counter)' \
  >> config.mk

run_logged hidden-input-clean "$MAKE_BIN" clean
run_logged hidden-input-build "$MAKE_BIN" -j1 all
printf '%s:' "hidden-input-query" >> "$SELFTEST_COMMANDS"
printf ' %s' "$MAKE_BIN" -q all >> "$SELFTEST_COMMANDS"
printf '\n' >> "$SELFTEST_COMMANDS"
if "$MAKE_BIN" -q all > "${SELFTEST_LOG_DIR}/hidden-input-query.log" 2>&1; then
  fail "negative: converged despite hidden input"
else
  hidden_query_status=$?
fi
hidden_counter=$(cat .selftest/hidden-counter)
record hidden-input.txt "result=PASS
mechanism=parse-time counter outside the declared graph
query_exit=${hidden_query_status}
counter_after_query=${hidden_counter}"
HIDDEN_INPUT_DETECTION="PASS"
pass "negative: hidden input detected (non-convergence)"

mv config.mk.bak config.mk

# 4) Optional eval demo must remain executable without controlling the core build
CURRENT_CHECK="quarantined_eval_demo"
step "quarantined eval demo"
run_logged eval-demo "$MAKE_BIN" USE_EVAL=yes eval-demo
test -s build/include/multi.h || fail "eval demo did not publish multi.h"
test -s build/include/multi.c || fail "eval demo did not publish multi.c"
record eval-demo.txt "PASS"
QUARANTINED_EVAL_DEMO="PASS"
pass "quarantined eval demo"

CURRENT_CHECK="complete"
echo "selftest: PASS: all checks completed"
