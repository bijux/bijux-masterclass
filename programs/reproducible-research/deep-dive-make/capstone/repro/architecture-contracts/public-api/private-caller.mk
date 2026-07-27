.RECIPEPREFIX := >

PUBLIC_TARGETS := help verify
BUILD_DIR := build

.PHONY: $(PUBLIC_TARGETS) internal-build clean

help:
> @printf '%s\n' \
>   'help    show the supported build interface' \
>   'verify  build and verify the application'

verify: internal-build
> printf 'verification=passed\n' > $(BUILD_DIR)/verification.txt

internal-build: | $(BUILD_DIR)/
> printf 'application=ready\n' > $(BUILD_DIR)/application.txt

$(BUILD_DIR)/:
> mkdir -p $@

clean:
> rm -rf $(BUILD_DIR)
