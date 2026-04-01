.PHONY: all clean
all: build/a.o build/b.o
build/%.o: %.c
	@echo "generic rule" > $@
build/%.o: extra/%.c
	@echo "specific rule" > $@
clean:
	@rm -f build/*.o