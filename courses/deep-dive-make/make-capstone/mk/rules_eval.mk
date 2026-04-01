# mk/rules_eval.mk — quarantined rule generation (Module 03B)
#
# Contract:
#   - This file is included ONLY when USE_EVAL=yes.
#   - All generated rules must be transparent and debuggable.
#   - No discovery outside declared roots; no shelling out to find the world.
#
# Demo: a tiny multi-output generator using grouped targets (&:) when available,
# with an explicit fallback when not.

# Inputs/outputs (stay in build/)
GEN_MULTI := scripts/gen_multi.py
GEN_H := $(BLD_DIR)/include/multi.h
GEN_C := $(BLD_DIR)/include/multi.c

EVAL_DEMO_TARGETS := $(GEN_H) $(GEN_C)

# GNU Make >= 4.3: grouped targets guarantee single recipe invocation.
ifeq ($(HAVE_GROUPED_TARGETS),)
$(GEN_H): $(GEN_MULTI) | $(BLD_DIR)/include/
	$(PYTHON) $< --h > $@.tmp.$$ && mv -f $@.tmp.$$ $@
$(GEN_C): $(GEN_MULTI) | $(BLD_DIR)/include/
	$(PYTHON) $< --c > $@.tmp.$$ && mv -f $@.tmp.$$ $@
else
$(GEN_H) $(GEN_C) &: $(GEN_MULTI) | $(BLD_DIR)/include/
	set -eu; \
	tmp_h="$(GEN_H).tmp.$$"; tmp_c="$(GEN_C).tmp.$$"; \
	$(PYTHON) $< --h > "$$tmp_h"; \
	$(PYTHON) $< --c > "$$tmp_c"; \
	mv -f "$$tmp_h" "$(GEN_H)"; \
	mv -f "$$tmp_c" "$(GEN_C)"
endif
