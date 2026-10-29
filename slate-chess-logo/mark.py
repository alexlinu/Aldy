"""Slate Chess knight-S, rebuilt so it is balanced on every screen.

Design units: origin at the center, y down; the mark spans x -306..306, y -404..404.
The outline is one chain of curves plus that same chain rotated 180 degrees, so
turned upside down the silhouette lands on itself: ear tip <-> slate point,
snout <-> slate corner, left bulge <-> right bulge, counter V <-> counter L.
The one deliberate exception is the knight's jaw notch, kept on the head only.
The dark band keeps one thickness from the middle through the bottom turn.
"""
import math
import re

BG = "#F3F5F8"
DARK_A, DARK_B = "#3E5A75", "#122032"
PAGE, RULE = "#D6DEE7", "#889CB1"
HALF_H = 404


def _rot(chain):
    return re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)",
                  lambda m: f"{-float(m[1]):g},{-float(m[2]):g}", chain)


def _chain(jaw):  # counter V -> head -> ear -> top band -> left bulge -> counter L
    return (jaw + "L84,-392 Q64,-404 44,-392 L-216,-190 "
            "C-256,-159 -280,-140 -280,-100 C-280,-20 -136,18 -16,66 ")


JAW = "L150,-94 L228,-66 Q238,-62 244,-68 L292,-104 Q306,-116 298,-132 "
SMOOTH = "L286,-100 Q306,-112 298,-132 "
SILHOUETTE = "M16,-66 " + _chain(JAW) + _rot(_chain(SMOOTH)) + "Z"
# The slate's inner edge is a straight line parallel to the bottom outer edge,
# one middle-band thickness in, so the dark band keeps the same width through
# the bottom turn. It meets the middle band's lower edge (extended past counter
# L) in a sharp corner, the way the mouth line meets counter V at the top.
STROKE = 136


def _slate():
    (x0, y0), (x1, y1) = (216, 190), (-44, 392)          # bottom outer edge
    n = math.hypot(x1 - x0, y1 - y0)
    dx, dy = (x1 - x0) / n, (y1 - y0) / n
    ax, ay = x0 - dy * STROKE, y0 + dx * STROKE           # cut line: outer edge moved up-left
    ex, ey = 120 / 130, 48 / 130                          # middle band's lower edge leaving L
    k = ((ax + 16) * ey - (ay - 66) * ex) / (dy * ex - dx * ey)   # solve L + s*e = A + k*d
    cx, cy = ax + k * dx, ay + k * dy                     # the sharp inner corner
    fx, fy = cx + 600 * dx, cy + 600 * dy                 # run past the outline
    return f"M-16,66 L{cx:.1f},{cy:.1f} L{fx:.1f},{fy:.1f} L-420,{fy:.1f} L-420,66 Z"


SLATE = _slate()


def defs(uid=""):
    rules = "".join(f'<rect x="{k * 28 - 2}" y="-420" width="4" height="840"/>' for k in range(-11, 12))
    return (f'<linearGradient id="g{uid}" gradientUnits="userSpaceOnUse" x1="-158" y1="-195" x2="183" y2="226">'
            f'<stop offset="0" stop-color="{DARK_A}"/><stop offset="1" stop-color="{DARK_B}"/></linearGradient>'
            f'<clipPath id="s{uid}"><path d="{SILHOUETTE}"/></clipPath>'
            f'<clipPath id="p{uid}"><path d="{SLATE}"/></clipPath>'
            f'<g id="r{uid}" fill="{RULE}">{rules}</g>')


def mark(uid=""):
    return (f'<path d="{SILHOUETTE}" fill="url(#g{uid})"/>'
            f'<g clip-path="url(#s{uid})"><path d="{SLATE}" fill="{PAGE}"/>'
            f'<use href="#r{uid}" clip-path="url(#p{uid})"/>'
            f'</g>')


def placed(cx, cy, height, uid=""):
    return f'<g transform="translate({cx} {cy}) scale({height / (2 * HALF_H):.6f})">{mark(uid)}</g>'


def svg(w, h, body, bg=None, extra_defs="", uid=""):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs(uid)}{extra_defs}</defs>{b}{body}</svg>')
