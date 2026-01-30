#!/usr/bin/env python3

import argparse
import itertools as it
from PIL import Image, ImageDraw, ImageFont, ImageColor

glyphs = [
    ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"],
    ["N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
    ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"],
    ["n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ",", ";", "."],
    ["!", "@", "#", "$", "%", "^", "&", "*", "-", "=", "+", "~", "/"],
    ["(", ")", "[", "]", "{", "}", "<", ">", "'", '"', "`", "_", "|"],
]
nrow = 13
ncol = 7
gsize = 50
cell = None
pad = int(gsize / 3)


def layer(ttf: str, color: str) -> Image.Image:
    global cell

    font = ImageFont.truetype(ttf, size=gsize)
    if cell is None:
        w, h = 0, 0
        for row in glyphs:
            for g in row:
                x1, y1, x2, y2 = font.getbbox(g)
                w = max(w, int(x2 - x1))
                h = max(h, int(y2 - y1))
        cell = (w, h)
    w, h = cell

    isize = (pad + (w + pad) * nrow, pad + (h + pad) * ncol)
    img = Image.new("RGBA", isize)
    canvas = ImageDraw.Draw(img)

    for y, row in enumerate(glyphs):
        for x, g in enumerate(row):
            pos = (pad + (w + pad) * x, pad + (h + pad) * y)
            canvas.text(pos, g, fill=color, font=font)
    return img


def main():
    parser = argparse.ArgumentParser(description="List glyphs in a font")
    parser.add_argument("--output", "-o", required=True, help="Path to save output image")
    parser.add_argument("main", help="Main font to draw glyphs")
    parser.add_argument("diff", nargs="*", default=[], help="Fonts to compare with")
    args = parser.parse_args()

    img = layer(args.main, "black")
    colors = it.chain(["red", "blue"], ImageColor.colormap.keys())
    for p, cl in zip(args.diff, colors):
        d = layer(p, cl)
        d.alpha_composite(img)
        img = d

    # Add background
    res = Image.new("RGBA", img.size, color="white")
    res.alpha_composite(img)
    res.save(args.output)


if __name__ == "__main__":
    main()
