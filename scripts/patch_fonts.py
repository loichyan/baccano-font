#!/usr/bin/env python3

import argparse
import fontforge
import utils


def patch(font: fontforge.font):
    """
    Add customizations here.
    """

    # # Clear font hint instructions
    # for g in font.glyphs():
    #     g.ttinstrs = bytes()

    # # Ensure monospaced.
    # for g in font.glyphs():
    #     g.width = 1233

    # # Round coordinates.
    # for g in font.glyphs():
    #     utils.round(g)

    # # Fix position of 'hyphen' (-).
    # utils.align_with(font[ord("-")], font[ord("=")])

    # # Tweak 'at' (@) for better display with uppercase letters.
    # utils.align_with(font[ord("@")], font[ord("T")], 0.90)

    # # Tweak 'dollar' ($) for better display with uppercase letters.
    # utils.align_with(font[ord("$")], font[ord("T")])

    # # Enlarge and center 'asterisk' (*).
    # utils.scale(font[ord("*")], 1.15, 1.15)
    # utils.align_with(font[ord("*")], font[ord("-")], 1.05)

    # # Thicken 'quotesingle' (') and 'grave' (`).
    # utils.scale(font[ord("'")], 1.15, 1.00)
    # utils.scale(font[ord("`")], 1.10, 1.05)
    # utils.align_with(font[ord("`")], font[ord("'")])

    # # Center 'asciitilde' (~).
    # utils.align_with(font[ord("~")], font[ord("-")])

    # # Shrink 'ampersand' (&).
    # utils.scale(font[ord("&")], 0.95, 1.00)

    # # Thicken underline for better terminal display.
    # font.uwidth = int(font.uwidth * 1.15)
    # font.upos = int(-font.descent + font.uwidth)


def main():
    parser = argparse.ArgumentParser(description="Apply customizations to fonts")
    parser.add_argument("targets", nargs="+", help="Target font to which patches are applied")
    args = parser.parse_args()

    for p in args.targets:
        font = fontforge.open(p)
        patch(font)
        font.save()


if __name__ == "__main__":
    main()
