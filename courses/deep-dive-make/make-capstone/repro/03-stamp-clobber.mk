.PHONY: all clean
all: a b
a: stamp
	printf 'a\n' > a.out
b: stamp
	printf 'b\n' > b.out

stamp:
	printf '%s\n' "$$(date +%s%N)" > stamp

clean:
	rm -f a.out b.out stamp
