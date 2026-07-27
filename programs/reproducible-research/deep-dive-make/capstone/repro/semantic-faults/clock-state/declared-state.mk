.PHONY: all clean

all: artifact.txt

artifact.txt: mode.txt state.stamp
	printf 'mode=%s\nstate=%s\n' "$$(cat mode.txt)" "$$(cat state.stamp)" > $@

state.stamp: mode.txt
	cp mode.txt $@

clean:
	rm -f artifact.txt state.stamp
