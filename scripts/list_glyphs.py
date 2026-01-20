#!/usr/bin/env python3

import argparse
import json
import unicodedataplus as ud
import fontforge


def collect_glyphs(sources: list[str], intersection):
    glyphs: dict[int, fontforge.glyph] | None = None
    for p in sources:
        font = fontforge.open(p)
        d = {g.unicode: g for g in font.glyphs() if g.unicode > 0}
        if glyphs is None:
            glyphs = d
        elif intersection:
            glyphs = {g.unicode: g for g in d.values() if g.unicode in glyphs}
        else:
            glyphs.update({g.unicode: g for g in font.glyphs() if g.unicode > 0})
    return sorted((glyphs or {}).values(), key=lambda g: g.unicode)


def main():
    parser = argparse.ArgumentParser(description="List glyphs in a font")
    parser.add_argument("--intersection", action="store_true", help="Select glyph intersection instead of union")
    parser.add_argument("--unicode", action="store_true", help="Show unicode block")
    parser.add_argument("--json", action="store_true", help="Output in JSON")
    parser.add_argument("sources", nargs="+", help="Base font in which glyphs are skipped")
    args = parser.parse_args()

    glyphs = collect_glyphs(args.sources, intersection=args.intersection)
    if args.unicode:
        blocks, blockset = list(), set()
        for g in glyphs:
            block = ud.block(chr(g.unicode))
            if block in blockset:
                continue
            blockset.add(block)
            blocks.append(block)
        if args.json:
            print(json.dumps(blocks, indent="  "))
        else:
            print("\n".join(blocks))
    else:
        names = list(map(lambda g: g.glyphname, glyphs))
        if args.json:
            print(json.dumps(names, indent="  "))
        else:
            print("\n".join(names))


if __name__ == "__main__":
    main()
