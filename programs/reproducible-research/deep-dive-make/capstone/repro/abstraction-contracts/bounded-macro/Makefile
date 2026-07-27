.RECIPEPREFIX := >

MODE := ordinary
OWNERS := alpha beta
OUTPUTS := $(addprefix build/,$(addsuffix .txt,$(OWNERS)))
MACRO_CALLS := $(addprefix publish_owned_file:,$(OWNERS))

define publish_owned_file
build/$1.txt: data/$1.txt | build/
> { printf 'mode=%s\nsource=%s\n' '$$(MODE)' '$$<'; cat '$$<'; } > '$$@.tmp'
> mv '$$@.tmp' '$$@'
endef

$(foreach owner,$(OWNERS),$(eval $(call publish_owned_file,$(owner))))

.PHONY: all clean help show-contract
all: $(OUTPUTS)

build/:
> mkdir -p '$@'

show-contract:
> @printf 'mode=%s\n' '$(MODE)'
> @printf 'outputs=%s\n' '$(OUTPUTS)'
> @printf 'macro-calls=%s\n' '$(MACRO_CALLS)'

help:
> @printf '%-14s %s\n' \
>   'all' 'publish both declared artifacts' \
>   'show-contract' 'print the publication contract'

clean:
> rm -rf build
