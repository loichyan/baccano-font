import fontforge
import psMat


def get_center(glyph: fontforge.glyph):
    bbox = glyph.boundingBox()  # (x_min, y_min, x_max, y_max)
    return (bbox[0] + bbox[2]) * 0.5, (bbox[1] + bbox[3]) * 0.5


def round(glyph: fontforge.glyph):
    glyph.round(1000)


# TODO: rebase
def transform(glyph: fontforge.glyph, matrix):
    """
    Transform a glyph with its width preserved.
    """
    width, vwidth = glyph.width, glyph.vwidth
    glyph.transform(matrix)
    round(glyph)
    glyph.width, glyph.vwidth = width, vwidth


def scale(glyph: fontforge.glyph, *args):
    """
    Scale a glyph with its position preserved.
    """
    cx, cy = get_center(glyph)
    matrix = psMat.translate(-cx, -cy)
    matrix = psMat.compose(matrix, psMat.scale(*args))
    matrix = psMat.compose(matrix, psMat.translate(cx, cy))
    transform(glyph, matrix)


def move(glyph: fontforge.glyph, *args):
    """
    Center `glyph` on x-asis.
    """
    transform(glyph, psMat.translate(*args))


def center_x(glyph: fontforge.glyph):
    """
    Center `glyph` on x-asis.
    """
    cx, _ = get_center(glyph)
    move(glyph, (glyph.width / 2) - cx, 0)


def align_with(glyph: fontforge.glyph, target: fontforge.glyph, overflow=1.0):
    """
    Align the vertical center of `glyph` with that of `target`.
    """
    cx1, cy1 = get_center(glyph)
    cx2, cy2 = get_center(target)
    _, ymin, _, ymax = glyph.boundingBox()
    offset = (ymax - ymin) * (overflow - 1.0)
    transform(glyph, psMat.translate(cx2 - cx1, cy2 - cy1 + offset))
