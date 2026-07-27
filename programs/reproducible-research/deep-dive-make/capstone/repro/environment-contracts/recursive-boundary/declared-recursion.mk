.RECIPEPREFIX := >

.PHONY: all clean

all:
> +$(MAKE) -C child --no-print-directory all

clean:
> +$(MAKE) -C child --no-print-directory clean
