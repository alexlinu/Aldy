# Slate Chess emblem

A mirror-symmetric redesign of the Slate Chess mark: fold it left-right or top-bottom and it lines up exactly.

- `emblem.py`: the geometry (one rounded diamond and its inset slate; every value is defined once and reflected)
- `build.py`: writes the SVG masters (`svg/`) and every PNG (`png/`). Run `python3 build.py` (needs Playwright + Pillow).
- `check_symmetry.py`: the fold test. It fails if any PNG differs from its own mirror image.

| Platform | Files | Notes |
|---|---|---|
| iPhone / iPad | `png/ios/AppIcon-*.png` | Full-bleed square; iOS applies the corner mask. Emblem is 72% of the height. |
| macOS | `png/macos/AppIcon-*.png` | 824 px rounded body on the 1024 grid, with a drop shadow (symmetric left-right only, since the shadow falls downward). |
| Apple TV | `png/tvos/app*-{back,front}.png` | Layered icon for parallax (`-flat` is a single-layer preview). Top Shelf: `top-shelf*.png`. |
