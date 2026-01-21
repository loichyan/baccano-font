#!/usr/bin/env python3

import argparse
import fontforge
import glob
import os


def modify_line_height(font: fontforge.font, factor):
    btb = font.os2_winascent + font.os2_windescent
    offset = int((factor - 1.0) * btb * 0.5)

    font.os2_winascent += offset
    font.os2_windescent += offset  # positive

    if font.hhea_linegap != 0:
        font.hhea_linegap += offset * 2
    else:
        font.hhea_ascent += offset
        font.hhea_descent -= offset

    if font.os2_typolinegap != 0:
        font.os2_typolinegap += offset * 2
    else:
        font.os2_typoascent += offset
        font.os2_typodescent -= offset


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("--line-height", default=1.05, type=float, help="Line height by percentage of generated font")
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
            modify_line_height(font, args.line_height)
            if ext == "otf":
                font.em = 1000
            font.generate(outpath, flags=("no-mac-names", "opentype"))


if __name__ == "__main__":
    main()
