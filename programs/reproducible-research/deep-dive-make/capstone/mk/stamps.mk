# mk/stamps.mk — modeling hidden inputs (Modules 01 + 05)
#
# Hard constraint: `make -q all` must be meaningful.
# So: no FORCE in the transitive closure of `all`.
#
# Strategy:
#   1) Compute a short signature for the current flag/env knobs at parse-time.
#   2) Materialize a content-stable stamp file for that signature.
#   3) Point the canonical name `build/flags.stamp` at it (copy).
#
# Changing knobs => different signature => new real stamp => objects rebuild.

# Use '>' as recipe prefix to avoid TAB footgun (GNU Make ≥4.0)
.RECIPEPREFIX := >

# Prefer sha256sum (widely available, cryptographic) with cksum fallback.
# Documented risk: cksum collision probability higher on large flag sets,
# but sufficient for short semantic signatures. sha256sum absent on minimal systems.
ifneq ($(shell command -v sha256sum 2>/dev/null),)
  HASH_CMD := sha256sum
  HASH_CUT := cut -c1-12
else ifneq ($(shell command -v shasum 2>/dev/null),)
  HASH_CMD := shasum -a 256
  HASH_CUT := cut -c1-12
else
  HASH_CMD := cksum
  HASH_CUT := awk '{print $$1}' | cut -c1-12
endif

FLAGS_LINE := CC=$(CC) CPPFLAGS=$(CPPFLAGS) CFLAGS=$(CFLAGS) DEPFLAGS=$(DEPFLAGS) LDFLAGS=$(LDFLAGS) LDLIBS=$(LDLIBS) INC_DIR=$(INC_DIR)
FLAGS_ID   := $(shell printf '%s' "$(FLAGS_LINE)" | $(HASH_CMD) | $(HASH_CUT))

FLAGS_STAMP_REAL := $(BLD_DIR)/flags.$(FLAGS_ID).stamp
FLAGS_STAMP      := $(BLD_DIR)/flags.stamp

# Real stamp: name changes when knobs change; content is the semantic state.
$(FLAGS_STAMP_REAL): | $(BLD_DIR)/
>     printf '%s\n' "$(FLAGS_LINE)" > $@

# Canonical name for humans/tools; rebuilt only when REAL changes.
$(FLAGS_STAMP): $(FLAGS_STAMP_REAL) | $(BLD_DIR)/
>     cp -f $< $@

# Optional tool/environment attestations (NOT dependencies of `all` by default)
stamps/tool/cc.txt: FORCE | stamps/tool/
>     $(CC) --version > $@ || true

stamps/env.txt: FORCE | stamps/
>     printf 'PATH=%s\nLC_ALL=%s\nTZ=%s\n' "$$PATH" "$${LC_ALL:-}" "$${TZ:-}" > $@

stamps/:
>     mkdir -p $@

stamps/tool/:
>     mkdir -p $@
