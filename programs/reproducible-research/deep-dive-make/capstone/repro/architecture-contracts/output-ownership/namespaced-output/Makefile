.RECIPEPREFIX := >

SOURCES := src/app/util.txt src/lib/util.txt
OUTPUTS := $(patsubst src/%,build/%,$(SOURCES))

.PHONY: all clean show-map
all: $(OUTPUTS)

show-map:
> @printf 'sources=%s\n' '$(SOURCES)'
> @printf 'outputs=%s\n' '$(OUTPUTS)'

build/app/%.txt: src/app/%.txt | build/app/
> { printf 'selected=%s\n' '$<'; cat '$<'; } > $@

build/lib/%.txt: src/lib/%.txt | build/lib/
> { printf 'selected=%s\n' '$<'; cat '$<'; } > $@

build/app/ build/lib/:
> mkdir -p $@

clean:
> rm -rf build
