#!/usr/bin/env python3

import argparse
import fontforge
import utils


def main():
    parser = argparse.ArgumentParser(description="Copy glyphs from one font to another")
    parser.add_argument("--source", "-s", required=True, help="Source font from which glyphs are copied")
    parser.add_argument("--target", "-t", required=True, help="Target font from which glyphs are pasted")
    parser.add_argument("glyphs", nargs="*", default=[], help="Selected glyphs to copy")
    args = parser.parse_args()

    target = fontforge.open(args.target)
    if len(args.glyphs) > 0:
        selected = set(ord(g) for g in args.glyphs)
    else:
        selected = set(g.unicode for g in target.glyphs())

    source = fontforge.open(args.source)
    source.em = target.em
    for c in selected:
        if c not in source:
            print(f"Not found '{chr(c)}' form source")
            continue
        print(f"Copying '{chr(c)}'")
        g = target[c]
        width, vwidth = g.width, g.vwidth  # to restore width
        cx1, cy1 = utils.get_center(g)  # to restore position

        g.clear()
        source.selection.select(("unicode",), c)
        source.copy()
        target.selection.select(("unicode",), c)
        target.paste()

        g.width, g.vwidth = width, vwidth
        cx2, cy2 = utils.get_center(g)
        utils.move(g, cx1 - cx2, cy1 - cy2)

    target.save()
    source.close()
    target.close()


if __name__ == "__main__":
    main()
