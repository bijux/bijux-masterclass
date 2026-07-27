.RECIPEPREFIX := >

include mk/policy.mk
include mk/release.mk
include mk/artifacts.mk

.PHONY: all release clean
all: build/default.txt
release: build/release.txt

clean:
> rm -rf build
