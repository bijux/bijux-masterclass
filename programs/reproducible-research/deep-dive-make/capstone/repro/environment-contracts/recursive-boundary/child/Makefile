.RECIPEPREFIX := >

.PHONY: all clean

all:
> printf 'child-plan: publish child.out\n'
> printf 'MAKELEVEL=%s\nMAKEFLAGS=%s\n' \
>   '$(MAKELEVEL)' '$(MAKEFLAGS)' > child.out

clean:
> rm -f child.out
