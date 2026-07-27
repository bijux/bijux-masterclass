MAKEFLAGS += -rR
.SUFFIXES:
.DELETE_ON_ERROR:

SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.RECIPEPREFIX := >

CC ?= cc
CC := $(if $(strip $(CC)),$(CC),cc)

.PHONY: all clean
all: app

app: main.c config.h
> $(CC) -I. main.c -o $@

clean:
> rm -f app
