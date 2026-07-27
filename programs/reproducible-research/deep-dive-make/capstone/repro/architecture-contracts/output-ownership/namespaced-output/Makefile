.RECIPEPREFIX := >

SOURCES := src/cli/util.txt src/lib/util.txt
OUTPUTS := $(patsubst src/%,build/%,$(SOURCES))

.PHONY: all clean show-map
all: $(OUTPUTS)

show-map:
> @printf 'sources=%s\n' '$(SOURCES)'
> @printf 'outputs=%s\n' '$(OUTPUTS)'

build/cli/%.txt: src/cli/%.txt | build/cli/
> { printf 'selected=%s\n' '$<'; cat '$<'; } > $@

build/lib/%.txt: src/lib/%.txt | build/lib/
> { printf 'selected=%s\n' '$<'; cat '$<'; } > $@

build/cli/ build/lib/:
> mkdir -p $@

clean:
> rm -rf build
