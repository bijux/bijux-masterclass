.PHONY: clean
all: x y
x:
	printf 'X\n' > shared.staging
	sleep 1
	mv -f shared.staging x.out
y:
	printf 'Y\n' > shared.staging
	mv -f shared.staging y.out
clean:
	rm -f shared.staging x.out y.out
