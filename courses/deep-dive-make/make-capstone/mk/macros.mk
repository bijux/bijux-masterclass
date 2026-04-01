# mk/macros.mk — safe shell-snippet helpers (Module 03 discipline)

# require_tool(tool): exit 127 if missing
define require_tool
command -v $(1) >/dev/null 2>&1 || { \
  echo "error: required tool '$(1)' not found" >&2; \
  exit 127; \
}
endef

# atomic_write(path, cmd): run cmd, write stdout atomically to path
define atomic_write
set -eu; tmp="$(1).tmp.$$"; \
( $(2) ) > "$$tmp" && mv -f "$$tmp" "$(1)" || { rm -f "$$tmp"; exit 1; }
endef

# assert_stdout_eq(cmd, expected): exact stdout equality
define assert_stdout_eq
set -eu; got="$$( $(1) )"; exp="$(2)"; \
[ "$$got" = "$$exp" ] || { \
  echo "assertion failed" >&2; \
  echo "  expected: $$exp" >&2; \
  echo "  got:      $$got" >&2; \
  exit 1; \
}
endef
