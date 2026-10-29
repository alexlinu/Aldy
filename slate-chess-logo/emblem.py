"""Slate Chess emblem: mirror-symmetric on both axes.

Design units: origin at the center, y down, emblem spans x -300..300, y -400..400.
A rounded diamond (a chess square turned 45 degrees) built from the original
mark's parts: ear-radius points top and bottom, S-bulge radius left and right,
a dark frame, and a ruled slate in the middle. Every element is defined once
and reflected, so folding along either axis lines up exactly.
"""
import math

BG = "#F3F5F8"
DARK_IN, DARK_OUT = "#3E5A75", "#122032"
PAGE, RULE = "#D6DEE7", "#889CB1"

A, B = 300, 400          # half-width, half-height of the outer diamond
FRAME = 104              # frame thickness, measured perpendicular to the edges
R_POINT, R_SIDE = 44, 150  # corner radii: top/bottom (ear), left/right (bulge)
RULE_PITCH, RULE_W = 28, 4


def rounded_poly(pts, radii):
    """Closed path through pts with each corner filleted by its radius."""
    n, out = len(pts), []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        v1 = (p0[0] - p1[0], p0[1] - p1[1]); v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1, l2 = math.hypot(*v1), math.hypot(*v2)
        ang = math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (l1 * l2))
        d = radii[i] / math.tan(ang / 2)
        a = (p1[0] + v1[0] / l1 * d, p1[1] + v1[1] / l1 * d)
        b = (p1[0] + v2[0] / l2 * d, p1[1] + v2[1] / l2 * d)
        out.append((a, b, radii[i]))
    s = f"M{out[0][1][0]:.3f},{out[0][1][1]:.3f} "
    for i in range(1, n + 1):
        a, b, r = out[i % n]
        s += f"L{a[0]:.3f},{a[1]:.3f} A{r},{r} 0 0 1 {b[0]:.3f},{b[1]:.3f} "
    return s + "Z"


def diamond(a, b, r_point, r_side):
    return rounded_poly([(0, -b), (a, 0), (0, b), (-a, 0)],
                        [r_point, r_side, r_point, r_side])


# Inner slate: the outer diamond offset inward by FRAME (same slopes, so the
# frame has an even thickness all round; fillet radii shrink by FRAME too).
_k = 1 - FRAME * math.hypot(A, B) / (A * B)
OUTER = diamond(A, B, R_POINT, R_SIDE)
INNER = diamond(A * _k, B * _k, max(R_POINT * _k * 0.5, 6), max(R_SIDE - FRAME, 10))


def defs(uid=""):
    n = int(A // RULE_PITCH)
    rules = "".join(f'<rect x="{k * RULE_PITCH - RULE_W / 2}" y="{-B}" width="{RULE_W}" height="{2 * B}"/>'
                    for k in range(-n, n + 1))   # centred on x=0, so the fold maps rule onto rule
    return (f'<radialGradient id="g{uid}" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="{B}" '
            f'gradientTransform="scale({A / B} 1)">'
            f'<stop offset="0.25" stop-color="{DARK_IN}"/><stop offset="1" stop-color="{DARK_OUT}"/></radialGradient>'
            f'<clipPath id="c{uid}"><path d="{INNER}"/></clipPath>'
            f'<g id="r{uid}" fill="{RULE}">{rules}</g>')


def emblem(uid=""):
    return (f'<path d="{OUTER}" fill="url(#g{uid})"/>'
            f'<path d="{INNER}" fill="{PAGE}"/>'
            f'<use href="#r{uid}" clip-path="url(#c{uid})"/>')


def placed(cx, cy, height, uid=""):
    return f'<g transform="translate({cx} {cy}) scale({height / (2 * B):.6f})">{emblem(uid)}</g>'


def svg(w, h, body, bg=None, extra_defs="", uid=""):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs(uid)}{extra_defs}</defs>{b}{body}</svg>')
