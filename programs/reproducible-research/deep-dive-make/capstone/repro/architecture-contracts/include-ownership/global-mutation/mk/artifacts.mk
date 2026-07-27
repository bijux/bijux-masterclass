build/default.txt build/release.txt: | build/
> printf 'flags=%s\n' '$(CFLAGS)' > $@

build/:
> mkdir -p $@
