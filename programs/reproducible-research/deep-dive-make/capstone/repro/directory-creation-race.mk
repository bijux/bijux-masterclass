.PHONY: all clean
all: dir/file1 dir/file2

dir/file1:
	touch .file1-ready
	while test ! -f .file2-ready; do sleep 0.01; done
	mkdir dir
	printf '1\n' > $@

dir/file2:
	touch .file2-ready
	while test ! -f .file1-ready; do sleep 0.01; done
	mkdir dir
	printf '2\n' > $@

clean:
	rm -rf dir .file1-ready .file2-ready
