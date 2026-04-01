# mk/common.mk — shared flags / conventions (keep small)

CPPFLAGS += -I$(INC_DIR) -I$(BLD_DIR)/include

# NOTE: Do not add platform-specific linker flags here.
# In particular, avoid `-Wl,-no_uuid` on macOS: suppressing LC_UUID can cause
# the dynamic loader to abort at runtime on modern systems.

# ---- deterministic compilation (Clang non-determinism fix) ----
# Seeds Clang's RNG for byte-identical objects across builds/machines.
# (LLVM/Clang ≥9; aligns with reproducible-builds.org macOS guidance)
CFLAGS += -frandom-seed=make-capstone

# ---- debug symbols (gated for performance in selftests) ----
# Enable via DEBUG=1; off by default to minimize .o size during hashing.
ifeq ($(DEBUG),1)
CFLAGS += -g
endif