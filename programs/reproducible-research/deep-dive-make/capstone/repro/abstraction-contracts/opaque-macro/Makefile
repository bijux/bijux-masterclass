.RECIPEPREFIX := >

MODE := ordinary
OWNERS := alpha beta
OUTPUTS := $(addprefix build/,$(addsuffix .txt,$(OWNERS)))

define define_component
MODE := release
build/$1.txt: data/$1.txt | build/
> { printf 'mode=%s\nsource=%s\n' '$$(MODE)' '$$<'; cat '$$<'; } > '$$@.tmp'
> mv '$$@.tmp' '$$@'
.PHONY: publish-$1
publish-$1: build/$1.txt
> @printf 'published=%s\n' '$1'
endef

$(foreach owner,$(OWNERS),$(eval $(call define_component,$(owner))))

.PHONY: all clean help show-contract
all: $(OUTPUTS)

build/:
> mkdir -p '$@'

show-contract:
> @printf 'mode=%s\n' '$(MODE)'
> @printf 'outputs=%s\n' '$(OUTPUTS)'

help:
> @printf '%-14s %s\n' \
>   'all' 'publish both declared artifacts' \
>   'show-contract' 'print the publication contract'

clean:
> rm -rf build
