#!/usr/bin/env python3

import argparse
import sys
import fontforge


def main():
    parser = argparse.ArgumentParser(description="Check whether a font is really monospaced")
    parser.add_argument("font", help="Font to check")
    args = parser.parse_args()

    font = fontforge.open(args.font)
    width = -1
    for g in font.glyphs():
        if width < 0:
            width = g.width
        elif g.width != width:
            print(f"{g.glyphname} is not monospaced")
            sys.exit(1)
    print("yes")


if __name__ == "__main__":
    main()
