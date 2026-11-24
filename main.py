#!/usr/bin/env python3
"""Copy the pre-drawn news poster into the output directory.

The entry image is produced by draw.py in this same directory. This
program only copies entry.png to MAKEFUN_OUTPUT_DIR (or /output when
unset). It performs no network access and reads no clock, so repeated
runs produce byte-identical output.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    if os.path.abspath(src) == os.path.abspath(dst):
        return 0
    shutil.copyfile(src, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
