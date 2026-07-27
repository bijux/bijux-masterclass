.RECIPEPREFIX := >

MAKE_BIN ?= gmake

.PHONY: all clean

all:
> $(MAKE_BIN) -C child --no-print-directory all

clean:
> $(MAKE_BIN) -C child --no-print-directory clean
