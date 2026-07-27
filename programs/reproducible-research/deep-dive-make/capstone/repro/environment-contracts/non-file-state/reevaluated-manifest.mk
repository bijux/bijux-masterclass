.RECIPEPREFIX := >

MODE ?= release
MANIFEST := build/environment.manifest
ARTIFACT := build/artifact.txt

.PHONY: all clean FORCE
all: $(ARTIFACT)

FORCE:

$(MANIFEST): FORCE | build/
> printf 'MODE=%s\n' '$(MODE)' > $@.candidate
> cmp -s $@.candidate $@ 2>/dev/null || mv $@.candidate $@
> rm -f $@.candidate

$(ARTIFACT): source.txt $(MANIFEST) | build/
> printf 'manifest=%s\nsource=%s\n' \
>   "$$(cat $(MANIFEST))" "$$(cat source.txt)" > $@

build/:
> mkdir -p $@

clean:
> rm -rf build
