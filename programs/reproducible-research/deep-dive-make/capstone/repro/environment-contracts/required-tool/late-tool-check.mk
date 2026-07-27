.RECIPEPREFIX := >

REQUIRED_TOOL ?= bijux-missing-tool
RESULT := build/result.txt

.PHONY: all clean
all: $(RESULT)

$(RESULT): | build/
> $(REQUIRED_TOOL) --version > build/tool-version.txt
> printf 'result=complete\n' > $@

build/:
> mkdir -p $@

clean:
> rm -rf build
