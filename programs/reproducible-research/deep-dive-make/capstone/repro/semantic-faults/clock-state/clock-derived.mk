.PHONY: all clean

PYTHON ?= python3

all: artifact.txt

artifact.txt: mode.txt state.stamp
	printf 'mode=%s\nstate=%s\n' "$$(cat mode.txt)" "$$(cat state.stamp)" > $@

state.stamp:
	$(PYTHON) -c 'import time; print(time.time_ns())' > $@

clean:
	rm -f artifact.txt state.stamp
