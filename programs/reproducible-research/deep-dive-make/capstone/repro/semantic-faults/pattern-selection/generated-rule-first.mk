.PHONY: all clean

all: build/a.choice

build/%.choice: generated/%.src | build/
	printf 'selected=%s\n' "$$(cat $<)" > $@

build/%.choice: root/%.src | build/
	printf 'selected=%s\n' "$$(cat $<)" > $@

build/:
	mkdir -p $@

clean:
	rm -rf build
