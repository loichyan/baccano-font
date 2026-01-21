#!/usr/bin/env python3

import argparse
import fontforge
import unicodedataplus as ud


basic_blocks = [
    # https://www.compart.com/en/unicode/block ->
    "Basic Latin",
    "Latin-1 Supplement",
    "Latin Extended-A",
    "Latin Extended-B",
    "IPA Extensions",
    "Spacing Modifier Letters",
    "Combining Diacritical Marks",
    "Greek and Coptic",
    "General Punctuation",
    "Superscripts and Subscripts",
    "Currency Symbols",
    "Number Forms",
    # "Arrows",
    "Mathematical Operators",
    "Miscellaneous Technical",
    # "Control Pictures",
    "Box Drawing",
    "Block Elements",
    "Geometric Shapes",
    "Dingbats",
    "Specials",
]


def main():
    parser = argparse.ArgumentParser(description="Clean glyphs from font")
    parser.add_argument("--include", action="append", default=[], help="Font in which glyphs are included")
    parser.add_argument("targets", nargs="+", help="Target font from which glyphs are removed")
    args = parser.parse_args()

    include = set()
    for p in args.include:
        font = fontforge.open(p)
        include.update(glyph.unicode for glyph in font.glyphs())
        font.close()

    include_blocks = set(basic_blocks)
    for p in args.targets:
        target = fontforge.open(p)
        for glyph in target.glyphs():
            if glyph.unicode <= 0:
                pass
            elif glyph.unicode in include:
                pass
            elif ud.block(chr(glyph.unicode)) in include_blocks:
                pass
            else:
                target.removeGlyph(glyph)
        target.save()
        target.close()


if __name__ == "__main__":
    main()
