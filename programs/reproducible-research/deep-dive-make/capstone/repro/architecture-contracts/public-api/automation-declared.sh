#!/bin/sh
set -eu

: "${MAKE_BIN:?MAKE_BIN must name GNU Make}"

"$MAKE_BIN" -f declared-caller.mk verify
