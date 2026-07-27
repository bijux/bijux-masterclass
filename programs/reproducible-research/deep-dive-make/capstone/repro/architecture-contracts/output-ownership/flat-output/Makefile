.RECIPEPREFIX := >

SOURCES := src/app/util.txt src/lib/util.txt
OUTPUTS := $(sort $(addprefix build/,$(notdir $(SOURCES))))

.PHONY: all clean show-map
all: $(OUTPUTS)

show-map:
> @printf 'sources=%s\n' '$(SOURCES)'
> @printf 'outputs=%s\n' '$(OUTPUTS)'

build/util.txt: $(SOURCES) | build/
> { printf 'selected=%s\n' '$<'; cat '$<'; } > $@

build/:
> mkdir -p $@

clean:
> rm -rf build
