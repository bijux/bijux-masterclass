.PHONY: clean
all: x y
x:
	printf 'X\n' > x.tmp && mv -f x.tmp x.out
y:
	printf 'Y\n' > y.tmp && mv -f y.tmp y.out
clean:
	rm -f *.tmp x.out y.out
