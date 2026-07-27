.PHONY: all clean
all: alpha beta

alpha:
	printf 'alpha:start\n' >> shared.log
	touch .alpha-ready
	while test ! -f .beta-ready; do sleep 0.01; done
	printf 'alpha:end\n' >> shared.log

beta:
	printf 'beta:start\n' >> shared.log
	touch .beta-ready
	while test ! -f .alpha-ready; do sleep 0.01; done
	printf 'beta:end\n' >> shared.log

clean:
	rm -f shared.log .alpha-ready .beta-ready
