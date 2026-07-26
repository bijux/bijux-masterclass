.PHONY: all clean
all: dir/file1 dir/file2
dir/file1:
	mkdir dir
	printf '1\n' > $@
dir/file2:
	mkdir dir
	printf '2\n' > $@
clean:
	rm -rf dir
