#!/usr/bin/env python3
"""Make the boot splash panel: the logo and the name, as raw RGBA for unseenet_gui.splash.

    python3 make_splash.py ICON.svg OUT.rgba [OUT.png]

Needs rsvg-convert (librsvg) and Pillow, which the image build installs.
"""
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAPER, MUTED = (0xE8, 0xF3, 0xEF, 255), (0x9C, 0xC3, 0xB6, 255)
FONTS = ["/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"]
FONTS_REG = [f.replace("-Bold", "") for f in FONTS]


def font(paths, size):
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main() -> None:
    icon_svg, out = Path(sys.argv[1]), Path(sys.argv[2])
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "icon.png"
        subprocess.run(["rsvg-convert", "-w", "120", "-h", "120", "-o", str(png), str(icon_svg)], check=True)
        icon = Image.open(png).convert("RGBA")
    W, H = 420, 210
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    panel.alpha_composite(icon, ((W - icon.width) // 2, 0))
    d = ImageDraw.Draw(panel)
    big, small = font(FONTS, 40), font(FONTS_REG, 15)
    for text, f, y, colour in (("Unseenet", big, 126, PAPER), ("Usenet, unseen.", small, 178, MUTED)):
        tw = d.textlength(text, font=f)
        d.text(((W - tw) / 2, y), text, font=f, fill=colour)
    out.write_bytes(struct.pack("<II", W, H) + panel.tobytes())
    if len(sys.argv) > 3:
        panel.save(sys.argv[3])


if __name__ == "__main__":
    main()
