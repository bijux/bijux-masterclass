.PHONY: clean
all: x y

x:
	printf 'X\n' > shared.staging
	touch .x-ready
	while test ! -f .y-ready; do sleep 0.01; done
	sleep 0.1
	mv -f shared.staging x.out

y:
	printf 'Y\n' > shared.staging
	touch .y-ready
	while test ! -f .x-ready; do sleep 0.01; done
	mv -f shared.staging y.out

clean:
	rm -f shared.staging x.out y.out .x-ready .y-ready
