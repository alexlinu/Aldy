"""Builds every platform asset from emblem.py.  Run: python3 build.py"""
import json, os, subprocess
import emblem as e

HERE = os.path.dirname(os.path.abspath(__file__))
jobs = []


def write(rel, w, h, body, bg=None, extra="", sizes=()):
    """Write an SVG master and queue PNG renders (square scale only)."""
    path = os.path.join(HERE, "svg", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(e.svg(w, h, body, bg, extra))
    for name, pw, ph in sizes or [(rel.replace(".svg", ".png"), w, h)]:
        scaled = os.path.join(HERE, "build", "tmp", name.replace("/", "_") + ".svg")
        os.makedirs(os.path.dirname(scaled), exist_ok=True)
        with open(scaled, "w") as f:  # same artwork, rendered at the target pixel size
            f.write(open(path).read().replace(f'width="{w}" height="{h}"', f'width="{pw}" height="{ph}"', 1))
        out = os.path.join(HERE, "png", name)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        jobs.append({"svg": scaled, "png": out, "w": pw, "h": ph})


# Emblem alone, transparent, with a 10% pad.
write("emblem.svg", 720, 960, e.placed(360, 480, 800),
      sizes=[(f"emblem/emblem-{h}.png", h * 3 // 4, h) for h in (256, 512, 1024, 2048)])

# iOS / iPadOS: full-bleed 1024 square, the system applies the corner mask.
# The emblem is 72% of the canvas height, so the mask never comes near it.
IOS = [1024, 180, 167, 152, 120, 87, 80, 76, 60, 58, 40, 29, 20]
write("icon-ios.svg", 1024, 1024, e.placed(512, 512, 737), bg=e.BG,
      sizes=[(f"ios/AppIcon-{s}.png", s, s) for s in IOS])

# macOS: 824 rounded-rect body on a 1024 canvas with Apple's grid shadow.
shadow = ('<filter id="sh" x="-20%" y="-20%" width="140%" height="140%">'
          '<feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000" flood-opacity="0.28"/></filter>')
MAC = [1024, 512, 256, 128, 64, 32, 16]
write("icon-macos.svg", 1024, 1024,
      f'<rect x="100" y="100" width="824" height="824" rx="185.4" fill="{e.BG}" filter="url(#sh)"/>'
      + e.placed(512, 512, 593), extra=shadow,
      sizes=[(f"macos/AppIcon-{s}.png", s, s) for s in MAC])

# tvOS: layered icon (back = background, front = emblem), 1280x768 App Store
# and 400x240 home-screen sizes, plus Top Shelf images.
for name, w, h in [("tvos/app-store", 1280, 768), ("tvos/app", 400, 240), ("tvos/app@2x", 800, 480)]:
    write(f"{name}-back.svg", w, h, "", bg=e.BG)
    write(f"{name}-front.svg", w, h, e.placed(w / 2, h / 2, h * 0.66))
    write(f"{name}-flat.svg", w, h, e.placed(w / 2, h / 2, h * 0.66), bg=e.BG)
for name, w, h in [("tvos/top-shelf", 1920, 720), ("tvos/top-shelf@2x", 3840, 1440),
                   ("tvos/top-shelf-wide", 2320, 720), ("tvos/top-shelf-wide@2x", 4640, 1440)]:
    write(f"{name}.svg", w, h, e.placed(w / 2, h / 2, h * 0.6), bg=e.BG)

with open(os.path.join(HERE, "build", "jobs.json"), "w") as f:
    json.dump(jobs, f)
subprocess.run(["node", os.path.join(HERE, "render.js"), os.path.join(HERE, "build", "jobs.json")], check=True)

# The art is exactly symmetric, but the rasterizer's anti-aliasing can differ by a
# pixel at a few edges. Averaging each render with its mirror images makes the
# pixels match the geometry. The macOS shadow falls downward, so it is only
# averaged left-right.
from PIL import Image, ImageChops, ImageOps
for j in jobs:
    im = Image.open(j["png"]).convert("RGBA")
    if "/macos/" in j["png"]:
        im = ImageChops.blend(im, ImageOps.mirror(im), 0.5)
    else:
        lr = ImageChops.blend(im, ImageOps.mirror(im), 0.5)
        im = ImageChops.blend(lr, ImageOps.flip(lr), 0.5)
    im.save(j["png"], optimize=True)
print(len(jobs), "PNGs rendered")
