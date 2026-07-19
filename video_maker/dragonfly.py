#!/usr/bin/env python3
"""Procedural dragonfly flight video. Pure Pillow + ffmpeg, no external assets.

Renders a stylized dragonfly skimming over an out-of-focus pond/meadow, with
fast wing-flaps and gentle banking. Encodes to MP4 with ffmpeg.
"""
import math, os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFilter

W, H = 640, 360
FPS = 30
SECS = 9
N = FPS * SECS
OUT = "/Users/Jeff/Smith/video_maker/dragonfly.mp4"
TMP = tempfile.mkdtemp(prefix="drfly_")

# ---------------------------------------------------------------- bokeh sprite
def soft_circle(r):
    s = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    for i in range(r, 0, -1):
        a = int(220 * (i / r) ** 2)
        d.ellipse([r - i, r - i, r + i, r + i], fill=(255, 255, 255, a))
    return s.filter(ImageFilter.GaussianBlur(r * 0.5))

BOKEH = soft_circle(64)

# ---------------------------------------------------------------- background
def background(t):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        f = y / H
        # hazy blue sky -> cool teal-green meadow/water
        r = int(150 - 60 * f)
        g = int(205 - 35 * f)
        b = int(235 - 95 * f)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    move_y = (t * 7) % H
    move_x = math.sin(t * 0.02) * 26
    for (bx, by, br, col, sp) in BOKEH_FIELD:
        yy = (by + move_y * sp) % (H + 140) - 70
        xx = bx + move_x * sp
        sprite = BOKEH.resize((br * 2, br * 2))
        tint = Image.new("RGBA", sprite.size, col + (0,))
        sprite = Image.alpha_composite(sprite, tint).convert("RGBA")
        img.paste(sprite, (int(xx - br), int(yy - br)), sprite)
    return img.filter(ImageFilter.GaussianBlur(1.4))

import random
random.seed(7)
BOKEH_FIELD = [
    (random.randint(-40, W + 40), random.randint(-70, H + 70),
     random.randint(16, 52),
     (random.randint(120, 205), random.randint(190, 235), random.randint(160, 210)),
     random.uniform(0.4, 1.6))
    for _ in range(26)
]

# ---------------------------------------------------------------- dragonfly
def make_wing(length, width, alpha, color):
    pad = 40
    side = 2 * length + pad
    c = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    cc = side // 2
    d.ellipse([cc - length, cc - width // 2, cc + length, cc + width // 2],
              fill=color + (alpha,))
    d.line([(cc - length, cc), (cc + length, cc)], fill=(255, 255, 255, alpha // 5))
    c = c.filter(ImageFilter.GaussianBlur(1.6))
    return c, (cc, cc)

def dragonfly(phase, bank, bob):
    CW, CH = 320, 400
    cx = CW // 2
    body = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))

    # --- wings (drawn BEHIND the body so roots tuck in) ---
    flap = math.sin(phase) * 0.28           # radians of flap swing
    fore, fc = make_wing(125, 24, 120, (195, 240, 250))
    hind, hc = make_wing(98, 32, 105, (170, 225, 240))
    specs = [
        (fore, fc, cx, 150, 0.56 + flap),   # left fore
        (hind, hc, cx, 188, 0.95 + flap),   # left hind
    ]
    for spr, sc, ax, ay, ang in specs:
        rot = spr.rotate(math.degrees(ang), resample=Image.BICUBIC, center=sc)
        body.alpha_composite(rot, (ax - sc[0], ay - sc[1]))
        # mirror for right side
        rot_r = spr.rotate(math.degrees(-ang), resample=Image.BICUBIC, center=sc)
        body.alpha_composite(rot_r, (ax - sc[0], ay - sc[1]))

    # --- body on top ---
    bd = ImageDraw.Draw(body)
    # abdomen: tapering segments from thorax down
    y = 150
    widths = [16, 15, 14, 12, 10, 8, 6, 5, 4]
    for w in widths:
        bd.ellipse([cx - w, y, cx + w, y + 22], fill=(22, 70, 80, 255))
        y += 20
    bd.ellipse([cx - 3, y, cx + 3, y + 14], fill=(22, 70, 80, 255))  # tail tip
    # thorax
    bd.ellipse([cx - 20, 132, cx + 20, 168], fill=(18, 58, 68, 255))
    # head
    bd.ellipse([cx - 20, 108, cx + 20, 140], fill=(14, 46, 56, 255))
    # big compound eyes
    bd.ellipse([cx - 26, 106, cx - 6, 132], fill=(40, 135, 145, 245))
    bd.ellipse([cx + 6, 106, cx + 26, 132], fill=(40, 135, 145, 245))

    # bank the whole insect
    body = body.rotate(math.degrees(bank), resample=Image.BICUBIC, center=(cx, CH // 2))
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(body, (W // 2 - cx, int(H // 2 - CH // 2 + bob)))
    return canvas

# ---------------------------------------------------------------- render
for t in range(N):
    bg = background(t)
    bank = math.sin(t * 0.03) * 0.22
    flap_phase = t * 0.62
    bob = math.sin(flap_phase * 0.5) * 12
    fly = dragonfly(flap_phase, bank, bob)
    frame = Image.alpha_composite(bg.convert("RGBA"), fly).convert("RGB")
    frame.save(os.path.join(TMP, f"f{t:04d}.png"))

subprocess.run([
    "ffmpeg", "-y", "-framerate", str(FPS), "-i", f"{TMP}/f%04d.png",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", OUT
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("WROTE", OUT)
