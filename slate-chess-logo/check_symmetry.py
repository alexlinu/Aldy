"""Fold test: every PNG must match its own left-right and top-bottom mirror."""
import glob, sys
from PIL import Image, ImageChops, ImageOps

worst = 0
for path in sorted(glob.glob("png/**/*.png", recursive=True)):
    im = Image.open(path).convert("RGBA")
    if "macos" in path:  # the drop shadow falls downward by design, so fold macOS left-right only
        folds = {"L|R": ImageOps.mirror(im)}
    else:
        folds = {"L|R": ImageOps.mirror(im), "T|B": ImageOps.flip(im)}
    res = {k: max(b[1] for b in ImageChops.difference(im, f).getextrema()) for k, f in folds.items()}
    worst = max(worst, *res.values())
    print(f"{path:42s} " + "  ".join(f"{k} max diff {v:3d}/255" for k, v in res.items()))
print("worst:", worst)
sys.exit(worst > 8)
