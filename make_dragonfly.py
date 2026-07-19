import math, subprocess, os
from PIL import Image, ImageDraw

W, H = 640, 360
FPS = 25
FRAMES = 150  # 6 seconds
OUT_DIR = "/Users/Jeff/Smith/_frames"
os.makedirs(OUT_DIR, exist_ok=True)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def sky(x, y):
    # vertical gradient: top deep blue -> horizon pale
    t = y / H
    top = (90, 150, 220)
    bot = (200, 225, 245)
    return lerp(top, bot, t)

def draw_cloud(d, cx, cy, s):
    for dx, dy, r in [(0,0,18),(22,4,14),(-22,4,14),(10,-6,12),(-10,-6,12)]:
        d.ellipse([cx+dx-s, cy+dy-s, cx+dx+s, cy+dy+s], fill=(255,255,255,180))

def draw_dragonfly(d, x, y, flap):
    # body
    d.line([x, y-22, x, y+22], fill=(20,30,40), width=4)
    d.ellipse([x-3, y-26, x+3, y-20], fill=(30,40,50))  # head
    # wings (two pairs), flap modulates spread
    a = 14 + 8 * flap
    for side in (-1, 1):
        for pair in (0, 1):
            yy = y - 12 + pair * 16
            tipx = x + side * (40 + 6 * (1 - flap))
            tipy = yy - a * (0.6 if pair == 0 else 0.9)
            d.line([x, yy, tipx, tipy], fill=(255,255,255,140), width=2)
            d.ellipse([min(x, tipx)-2, min(yy, tipy)-2, max(x, tipx)+2, max(yy, tipy)+2],
                      outline=(255,255,255,120))

for f in range(FRAMES):
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        for x in range(0, W, 4):
            c = sky(x, y)
            for xx in range(x, min(x+4, W)):
                px[xx, y] = c
    d = ImageDraw.Draw(img, "RGBA")
    # clouds drifting
    for i, (bx, by, sc) in enumerate([(120, 80, 10), (430, 140, 14), (300, 60, 8)]):
        draw_cloud(d, (bx + f * 0.4 * (1+i*0.2)) % (W+120) - 60, by, sc)
    # dragonfly path: gentle sine across screen
    t = f / FRAMES
    x = int(40 + t * (W - 80))
    y = int(H/2 + math.sin(t * math.pi * 2) * 50)
    flap = (math.sin(f * 0.9) + 1) / 2
    draw_dragonfly(d, x, y, flap)
    img.save(f"{OUT_DIR}/f{f:04d}.png")

# encode
cmd = [
    "ffmpeg", "-y", "-framerate", str(FPS),
    "-i", f"{OUT_DIR}/f%04d.png",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23",
    "/Users/Jeff/Smith/dragonfly_sky.mp4"
]
r = subprocess.run(cmd, capture_output=True, text=True)
print("exit", r.returncode)
print("stderr tail:", r.stderr[-400:])
print("exists:", os.path.exists("/Users/Jeff/Smith/dragonfly_sky.mp4"))
