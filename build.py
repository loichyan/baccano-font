#!/usr/bin/env python3

import argparse
import fontforge
import glob
import os
import subprocess
import sys


def run(*cmd):
    res = subprocess.run([*cmd])
    if res.returncode != 0:
        sys.exit(res.returncode)


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", "-d", default="build", help="Path of directory to save output")
    parser.add_argument("extensions", nargs="+", help="Type of font to generate")
    args = parser.parse_args()

    sources = glob.glob("src/*.sfd")
    for ext in args.extensions:
        outdir = os.path.join(args.outdir, ext.upper())
        os.makedirs(outdir, exist_ok=True)

        for srcpath in sources:
            srcname, _ = os.path.splitext(os.path.basename(srcpath))
            outpath = os.path.join(outdir, f"{srcname}.{ext}")
            print(f"Building '{srcpath}' to '{outpath}'")
            font = fontforge.open(srcpath)
            if ext == "otf":
                font.em = 1000
            font.generate(outpath, flags=("no-mac-names", "opentype"))


if __name__ == "__main__":
    main()
