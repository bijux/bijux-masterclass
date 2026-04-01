.PHONY: all clean
all: log1 log2
log1:
	printf 'A\n' >> shared.log
log2:
	printf 'B\n' >> shared.log
clean:
	rm -f shared.log
