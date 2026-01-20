#!/usr/bin/env python3

import argparse
import fontforge
import utils


def patch(font: fontforge.font):
    """
    Add customizations here.
    """


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
