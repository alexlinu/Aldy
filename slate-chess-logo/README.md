# Slate Chess mark

The knight-S, rebuilt so it sits dead-center and balanced on iPhone, iPad, Mac and Apple TV.
The dark band keeps one width from the middle of the S through the bottom turn, so the bottom carries the same weight as the top.

- **Turns onto itself.** The outline is one set of curves plus the same set rotated 180°: ear tip ↔ slate point, snout ↔ slate corner, left curve ↔ right curve. The one exception is the knight's jaw notch, kept on the head only.
- **Equal margins.** On every asset the left/right and top/bottom margins match within 1 px.

`before-after.png` compares the old and new marks; `preview.png` shows each platform asset.

- `mark.py`: the geometry
- `build.py`: writes the SVG masters (`svg/`) and every PNG (`png/`). Run `python3 build.py` (needs Playwright + Pillow).
- `check_balance.py`: fails if any asset's margins are off by more than 1 px; also reports how much of the outline lands on itself when turned upside down (~98%, the rest is the jaw notch and anti-aliasing).

| Platform | Files | Notes |
|---|---|---|
| iPhone / iPad | `png/ios/AppIcon-*.png` | Full-bleed square; iOS applies the corner mask. Mark is 72% of the height. |
| macOS | `png/macos/AppIcon-*.png` | 824 px rounded body on Apple's 1024 grid, with drop shadow. |
| Apple TV | `png/tvos/app*-{back,front}.png` | Layered icon for parallax (`-flat` is a single-layer preview). Top Shelf: `top-shelf*.png`. |
| Anywhere | `png/mark/`, `svg/mark.svg` | Transparent mark on its own. |
