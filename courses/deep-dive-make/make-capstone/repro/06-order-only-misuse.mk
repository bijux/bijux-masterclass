.PHONY: all clean
all: dir/data out
out: dir/data
	@cp dir/data $@
dir/data: | dir/
	@echo "data" > $@
dir/:
	@mkdir -p $@
	@sleep 1 && touch $@  # force mtime change
clean:
	@rm -rf dir out