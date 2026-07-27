.PHONY: all clean

all: output.txt

output.txt: | input.txt
	cp input.txt $@

clean:
	rm -f output.txt
