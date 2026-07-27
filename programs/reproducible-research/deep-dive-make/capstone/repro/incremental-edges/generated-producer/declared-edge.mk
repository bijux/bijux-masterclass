MAKEFLAGS += -rR
.SUFFIXES:
.DELETE_ON_ERROR:

SHELL := /bin/sh
.SHELLFLAGS := -eu -c
.RECIPEPREFIX := >

CC ?= cc
CC := $(if $(strip $(CC)),$(CC),cc)
PYTHON ?= python3
PYTHON := $(if $(strip $(PYTHON)),$(PYTHON),python3)

.PHONY: all clean
all: app

app: main.c generated.h
> $(CC) -I. main.c -o $@

generated.h: scripts/render_header.py
> $(PYTHON) scripts/render_header.py > $@.tmp
> mv -f $@.tmp $@

clean:
> rm -f app generated.h generated.h.tmp
