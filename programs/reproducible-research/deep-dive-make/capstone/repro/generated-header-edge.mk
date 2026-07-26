.PHONY: all clean
all: a b

a: gen.h
	printf '#include "gen.h"\nint main(){return X;}\n' > a.c
	$(CC) a.c -o a

b: gen.h
	printf '#include "gen.h"\nint main(){return X;}\n' > b.c
	$(CC) b.c -o b

gen.h:
	printf '#define X 42\n' > gen.h

clean:
	rm -f a b a.c b.c gen.h
