.RECIPEPREFIX := >

MODE := ordinary
OUTPUTS := build/alpha.txt build/beta.txt

.PHONY: all clean help show-contract
all: $(OUTPUTS)

build/alpha.txt: data/alpha.txt | build/
> { printf 'mode=%s\nsource=%s\n' '$(MODE)' '$<'; cat '$<'; } > '$@.tmp'
> mv '$@.tmp' '$@'

build/beta.txt: data/beta.txt | build/
> { printf 'mode=%s\nsource=%s\n' '$(MODE)' '$<'; cat '$<'; } > '$@.tmp'
> mv '$@.tmp' '$@'

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
