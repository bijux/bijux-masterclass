# mk/objects.mk — deterministic discovery + mapping (Modules 02–03)

SRCS := $(sort \
	$(wildcard $(SRC_DIR)/*.c) \
	$(wildcard $(SRC_DIR)/sub/*.c) \
)

OBJS := $(patsubst $(SRC_DIR)/%.c,$(BLD_DIR)/%.o,$(SRCS))
DEPS := $(OBJS:.o=.d)

DYN_SRCS := $(sort $(wildcard $(SRC_DIR)/dynamic/*.c))
DYN_BINS := $(patsubst $(SRC_DIR)/dynamic/%.c,$(BLD_DIR)/bin/%,$(DYN_SRCS))

DYN_HDR := $(BLD_DIR)/include/dynamic.h

# Dynamic depfiles (for header staleness; Module 01)
DYN_DEPS := $(patsubst $(SRC_DIR)/dynamic/%.c,$(BLD_DIR)/bin/%.d,$(DYN_SRCS))