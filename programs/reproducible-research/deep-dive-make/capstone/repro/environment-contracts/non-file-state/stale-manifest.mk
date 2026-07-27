.RECIPEPREFIX := >

MODE ?= release
MANIFEST := build/environment.manifest
ARTIFACT := build/artifact.txt

.PHONY: all clean
all: $(ARTIFACT)

$(MANIFEST): | build/
> printf 'MODE=%s\n' '$(MODE)' > $@

$(ARTIFACT): source.txt $(MANIFEST) | build/
> printf 'manifest=%s\nsource=%s\n' \
>   "$$(cat $(MANIFEST))" "$$(cat source.txt)" > $@

build/:
> mkdir -p $@

clean:
> rm -rf build
