"""Balance test for every PNG:
  - margins: the mark's left/right and top/bottom margins must match within 1 px
  - 180 turn: the share of the silhouette that lands on itself when turned upside down
"""
import glob, sys
from PIL import Image, ImageChops

BG = (0xF3, 0xF5, 0xF8)
bad = 0
for path in sorted(glob.glob("png/**/*.png", recursive=True)):
    im = Image.open(path).convert("RGBA")
    if "/macos/" in path:  # judge the mark against the icon body, not the shadowed canvas
        s = im.width / 1024
        im = im.crop((round(160 * s), round(160 * s), round(864 * s), round(864 * s)))  # inside the rounded corners
    if "-back" in path:
        continue
    px = im.load()
    mask = Image.new("1", im.size)
    mp = mask.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            mp[x, y] = a > 128 and abs(r - BG[0]) + abs(g - BG[1]) + abs(b - BG[2]) > 24
    l, t, r, b = mask.getbbox()
    ml, mr, mt, mb = l, im.width - r, t, im.height - b
    turned = mask.rotate(180)
    overlap = ImageChops.logical_and(mask, turned).histogram()[255]
    union = ImageChops.logical_or(mask, turned).histogram()[255]
    ok = abs(ml - mr) <= 1 and abs(mt - mb) <= 1
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'} {path:38s} margins L{ml:4d} R{mr:4d}  T{mt:4d} B{mb:4d}   180-turn match {overlap / union:6.1%}")
sys.exit(bad > 0)
