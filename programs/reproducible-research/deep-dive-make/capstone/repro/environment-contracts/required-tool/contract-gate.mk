.RECIPEPREFIX := >

REQUIRED_TOOL ?= bijux-missing-tool
RESULT := build/result.txt

.PHONY: all clean contract-check
all: contract-check $(RESULT)

contract-check:
> @command -v "$(REQUIRED_TOOL)" >/dev/null 2>&1 || { \
>   printf 'contract: missing required tool %s\n' "$(REQUIRED_TOOL)" >&2; \
>   exit 2; \
> }

$(RESULT): | build/
> $(REQUIRED_TOOL) --version > build/tool-version.txt
> printf 'result=complete\n' > $@

build/:
> mkdir -p $@

clean:
> rm -rf build
