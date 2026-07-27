.PHONY: all clean

all: build/root/a.choice build/generated/a.choice

build/root/%.choice: root/%.src | build/root/
	printf 'selected=%s\n' "$$(cat $<)" > $@

build/generated/%.choice: generated/%.src | build/generated/
	printf 'selected=%s\n' "$$(cat $<)" > $@

build/root/ build/generated/:
	mkdir -p $@

clean:
	rm -rf build
