#!/usr/bin/env python3
import argparse

p = argparse.ArgumentParser()
p.add_argument("--h", action="store_true", help="emit header")
p.add_argument("--c", action="store_true", help="emit C file")
args = p.parse_args()

if args.h == args.c:
    raise SystemExit("choose exactly one of --h or --c")

if args.h:
    print("#pragma once")
    print("#define MULTI_VAL 7")
else:
    print('#include "multi.h"')
    print("int multi_val(void) { return MULTI_VAL; }")
