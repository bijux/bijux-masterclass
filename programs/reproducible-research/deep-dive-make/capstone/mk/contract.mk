# mk/contract.mk — required feature gates and diagnostic identity

# The core build requires capabilities introduced in GNU Make 4.3. Gate the
# capabilities themselves so a future version such as 4.10 is not rejected by
# a prefix list. Keep MAKE_VERSION for diagnostic identity only.
ifeq ($(origin MAKE_VERSION),undefined)
  $(error This repository requires GNU Make (MAKE_VERSION not defined).)
endif

REQUIRED_MAKE_FEATURES := grouped-target second-expansion
MISSING_MAKE_FEATURES := $(filter-out $(.FEATURES),$(REQUIRED_MAKE_FEATURES))
ifneq ($(strip $(MISSING_MAKE_FEATURES)),)
  $(error GNU Make $(MAKE_VERSION) lacks required features: $(MISSING_MAKE_FEATURES))
endif

# Optional demos consume advertised capability evidence too.
HAVE_GROUPED_TARGETS := $(filter grouped-target,$(.FEATURES))

# .WAIT is not advertised by .FEATURES in the supported GNU Make releases and
# the core build does not use it. Report that it is unprobed instead of
# inferring support from another brittle version prefix.
WAIT_SUPPORT := not-probed
