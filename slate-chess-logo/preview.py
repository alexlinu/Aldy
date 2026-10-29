"""Contact sheet: each asset as the device presents it, with fold guides."""
from PIL import Image, ImageDraw
W, H = 2400, 1500
sheet = Image.new("RGB", (W, H), "#E4E8EE")
d = ImageDraw.Draw(sheet)

def paste(path, x, y, w, h, mask_r=None, guides=True):
    im = Image.open(path).convert("RGBA").resize((w, h), Image.LANCZOS)
    if mask_r:  # the corner mask the OS applies
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], mask_r, fill=255)
        im.putalpha(Image.composite(im.getchannel("A"), m, m))
    sheet.alpha_composite(im, (x, y)) if sheet.mode == "RGBA" else sheet.paste(im, (x, y), im)
    if guides:
        for i in range(0, h, 12):
            d.line([(x + w // 2, y + i), (x + w // 2, y + i + 5)], fill="#E0475B", width=2)
        for i in range(0, w, 12):
            d.line([(x + i, y + h // 2), (x + i + 5, y + h // 2)], fill="#E0475B", width=2)

paste("png/ios/AppIcon-1024.png", 80, 120, 560, 560, mask_r=126)      # iPhone / iPad
paste("png/macos/AppIcon-1024.png", 720, 120, 560, 560)                 # macOS
paste("png/tvos/app-store-flat.png", 1360, 120, 960, 576, mask_r=40)    # Apple TV app icon
paste("png/tvos/top-shelf-wide.png", 80, 800, 1450, 450)                # Top Shelf
x = 1620
for s in (180, 120, 87, 60, 40, 29):                                     # small sizes, unscaled
    im = Image.open(f"png/ios/AppIcon-{s}.png").convert("RGBA")
    sheet.paste(im, (x, 1250 - s), im); x += s + 24
sheet.save("preview.png")
