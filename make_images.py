"""Generate 10 distinct, topic-relevant themed PNG illustrations for the
optik-tola presentation, using the pure-stdlib Canvas (pnglib).

Palette (deep-blue + neon), from presentation.html:
  bg0 #020b1a  bg1 #06162e  bg2 #0a2446
  cyan #22e0ff  blue #2f6bff  violet #8b5cff  gold #ffd166  green #4be3a0
  text #eef5fc  dim #a9c2da

Since outbound network is blocked (Unsplash unreachable), every slide image
is drawn locally so real image bytes can be embedded in the .pptx.
"""

import math
import os

from pnglib import Canvas

W, H = 1280, 720

BG0 = (2, 11, 26)
BG1 = (6, 22, 46)
BG2 = (10, 36, 70)
CYAN = (34, 224, 255)
BLUE = (47, 107, 255)
VIOLET = (139, 92, 255)
GOLD = (255, 209, 102)
GREEN = (75, 227, 160)
TEXT = (238, 245, 252)
DIM = (169, 194, 218)
GREY = (120, 140, 165)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")


def base_canvas():
    c = Canvas(W, H, bg=BG0)
    c.vertical_gradient(0, 0, W, H, BG2, BG0)
    # soft corner glows
    c.radial_glow(140, -40, 520, BLUE, 0.18)
    c.radial_glow(W + 40, H + 60, 560, CYAN, 0.14)
    # top neon edge
    for x in range(W):
        t = x / W
        if t < 0.2 or t > 0.8:
            a = 0.0
        else:
            a = math.sin((t - 0.2) / 0.6 * math.pi)
        if t < 0.5:
            col = CYAN
        else:
            col = VIOLET
        for yy in range(4):
            c.set_px(x, yy, col, a * 0.9)
    # bottom neon fiber accent line
    for x in range(80, W - 80):
        t = (x - 80) / (W - 160)
        a = math.sin(t * math.pi) * 0.7
        c.set_px(x, H - 40, CYAN, a)
        c.set_px(x, H - 39, CYAN, a * 0.6)
    return c


def draw_glow_dot(c, x, y, r, color, glow=True):
    if glow:
        c.radial_glow(x, y, r * 3.2, color, 0.5)
    c.filled_circle(x, y, r, color)
    c.filled_circle(x, y, r * 0.45, (255, 255, 255))


def light_streaks(c, count=7, color=CYAN):
    """Flowing fiber-light streaks across the canvas."""
    for i in range(count):
        y0 = 90 + i * (H - 180) / max(1, count - 1)
        amp = 26 + (i % 3) * 14
        prev = None
        for x in range(60, W - 60, 2):
            y = y0 + math.sin(x / 120.0 + i) * amp
            col = color if i % 2 == 0 else BLUE
            if prev:
                c.line(prev[0], prev[1], x, y, col, width=2, alpha=0.55)
            c.set_px(x, y, (255, 255, 255), 0.5)
            prev = (x, y)


# --------------------------------------------------------------------------
# Slide 1 — Title: fiber-optic cables and streams of light
# --------------------------------------------------------------------------
def slide1():
    c = base_canvas()
    c.radial_glow(W / 2, H / 2, 420, BLUE, 0.16)
    light_streaks(c, count=9, color=CYAN)
    # bright converging fiber bundle from left to a focal point
    fx, fy = W - 230, H / 2
    c.radial_glow(fx, fy, 220, CYAN, 0.6)
    for i in range(14):
        y = 120 + i * (H - 240) / 13
        c.line(70, y, fx, fy, CYAN if i % 2 == 0 else BLUE, width=2, alpha=0.5)
    draw_glow_dot(c, fx, fy, 26, CYAN)
    # travelling photons along a central beam
    for k in range(10):
        px = 90 + k * (fx - 90) / 9
        draw_glow_dot(c, px, fy + math.sin(k) * 6, 5, GOLD)
    return c


# --------------------------------------------------------------------------
# Slide 2 — Plan: macro view of glass fiber strands
# --------------------------------------------------------------------------
def slide2():
    c = base_canvas()
    # bundle of glowing glass strands
    cols = [CYAN, BLUE, VIOLET, GREEN, GOLD]
    for i in range(22):
        base_y = 110 + i * (H - 220) / 21
        color = cols[i % len(cols)]
        prev = None
        for x in range(70, W - 70, 2):
            y = base_y + math.sin(x / 90.0 + i * 0.6) * (18 + (i % 4) * 6)
            if prev:
                c.line(prev[0], prev[1], x, y, color, width=3, alpha=0.4)
            prev = (x, y)
    # glowing fiber tips on the right (cross-section dots)
    for i in range(8):
        for j in range(5):
            cx = W - 220 + j * 36
            cy = 180 + i * 46
            draw_glow_dot(c, cx, cy, 10, cols[(i + j) % len(cols)], glow=False)
            c.radial_glow(cx, cy, 26, cols[(i + j) % len(cols)], 0.35)
    return c


# --------------------------------------------------------------------------
# Slide 3 — What is fiber: laser + digital data pulses (1/0)
# --------------------------------------------------------------------------
def slide3():
    c = base_canvas()
    axis_y = H / 2
    # laser source box on the left
    c.rounded_rect(80, axis_y - 60, 150, 120, 16, (12, 40, 78))
    c.ring(155, axis_y, 42, 6, CYAN)
    c.radial_glow(155, axis_y, 90, CYAN, 0.5)
    draw_glow_dot(c, 155, axis_y, 16, CYAN)
    # the fiber as a horizontal tube
    c.fill_rect(230, axis_y - 30, W - 420, 60, (8, 28, 56))
    c.line(230, axis_y - 30, W - 190, axis_y - 30, CYAN, 2, 0.6)
    c.line(230, axis_y + 30, W - 190, axis_y + 30, CYAN, 2, 0.6)
    # binary pulse train riding inside the fiber (1 = bright block, 0 = gap)
    bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1]
    x = 250
    step = (W - 470) / len(bits)
    for b in bits:
        if b:
            c.radial_glow(x + step / 2, axis_y, step * 0.6, GOLD, 0.5)
            c.rounded_rect(x + 6, axis_y - 20, step - 12, 40, 8, GOLD)
        x += step
    # photodiode / detector on the right
    c.rounded_rect(W - 180, axis_y - 60, 110, 120, 16, (12, 40, 78))
    c.polygon([(W - 150, axis_y - 28), (W - 150, axis_y + 28), (W - 110, axis_y)], GREEN)
    # label pulses with 1/0 ticks (as small bars above)
    x = 250
    for b in bits:
        bar_h = 34 if b else 10
        c.fill_rect(x + step / 2 - 2, axis_y - 110, 4, bar_h, CYAN if b else GREY)
        x += step
    return c


# --------------------------------------------------------------------------
# Slide 4 — Internal structure: fiber cross-section (core/cladding/jacket)
# --------------------------------------------------------------------------
def slide4():
    c = base_canvas()
    cx, cy = W / 2, H / 2
    # layered cross-section circles
    c.radial_glow(cx, cy, 360, BLUE, 0.18)
    c.filled_circle(cx, cy, 250, (120, 140, 160))        # outer jacket (grey)
    c.filled_circle(cx, cy, 210, (70, 95, 130))          # buffer
    c.filled_circle(cx, cy, 165, CYAN)                   # cladding (cyan)
    c.filled_circle(cx, cy, 150, (14, 48, 92))
    c.radial_glow(cx, cy, 150, GOLD, 0.55)
    c.filled_circle(cx, cy, 70, GOLD)                    # core (gold)
    c.filled_circle(cx, cy, 30, (255, 245, 220))
    # light ray zig-zag bouncing inside the core (TIR preview)
    pts = []
    yspan = 55
    xx = cx - 150
    up = True
    while xx < cx + 150:
        pts.append((xx, cy - yspan if up else cy + yspan))
        xx += 60
        up = not up
    c.polyline(pts, (255, 255, 255), width=3, alpha=0.9)
    # leader lines/labels pointing out the three layers
    c.line(cx + 20, cy, cx + 330, cy - 150, CYAN, 2, 0.7)   # core
    c.line(cx + 110, cy - 110, cx + 330, cy - 10, CYAN, 2, 0.7)  # cladding
    c.line(cx + 190, cy - 150, cx + 330, cy + 120, CYAN, 2, 0.7)  # jacket
    draw_glow_dot(c, cx + 330, cy - 150, 7, GOLD, glow=False)
    draw_glow_dot(c, cx + 330, cy - 10, 7, CYAN, glow=False)
    draw_glow_dot(c, cx + 330, cy + 120, 7, GREY, glow=False)
    return c


# --------------------------------------------------------------------------
# Slide 5 — Total internal reflection: zig-zag ray diagram + critical angle
# --------------------------------------------------------------------------
def slide5():
    c = base_canvas()
    top = 200
    bot = 520
    left = 110
    right = W - 110
    # core region between two cladding boundaries
    c.fill_rect(left, top, right - left, bot - top, (10, 34, 66), 0.6)
    # cladding boundary lines (bright)
    c.line(left, top, right, top, CYAN, 3, 0.9)
    c.line(left, bot, right, bot, CYAN, 3, 0.9)
    c.radial_glow((left + right) / 2, top, 500, CYAN, 0.08)
    # zig-zag ray with total internal reflection
    x = left + 10
    y = top + 20
    going_down = True
    pts = [(x, y)]
    seg = 150
    while x < right - 10:
        x2 = min(x + seg, right - 10)
        y2 = bot - 20 if going_down else top + 20
        pts.append((x2, y2))
        x = x2
        going_down = not going_down
    # draw ray with glow and travelling photons
    for i in range(len(pts) - 1):
        c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], GOLD, width=4, alpha=0.95)
    # bounce points: mark reflections and critical-angle arcs
    for p in pts[1:-1]:
        c.radial_glow(p[0], p[1], 60, GOLD, 0.5)
        draw_glow_dot(c, p[0], p[1], 8, (255, 255, 255), glow=False)
        # normal line (dashed) at bounce
        ny0 = p[1] - 36 if p[1] < (top + bot) / 2 else p[1] + 36
        for d in range(0, 36, 6):
            yy = p[1] + (d if p[1] < (top + bot) / 2 else -d) * (1 if p[1] < (top+bot)/2 else 1)
        c.line(p[0], p[1], p[0], ny0, DIM, 1, 0.6)
    # travelling photon dots along first segment
    for k in range(5):
        t = k / 4
        px = pts[0][0] + (pts[1][0] - pts[0][0]) * t
        py = pts[0][1] + (pts[1][1] - pts[0][1]) * t
        draw_glow_dot(c, px, py, 5, CYAN, glow=False)
    return c


# --------------------------------------------------------------------------
# Slide 6 — Advantages: copper vs fiber comparison bar chart
# --------------------------------------------------------------------------
def slide6():
    c = base_canvas()
    base_y = 560
    cats = [
        ("Sig'im", 0.95, CYAN),
        ("Masofa", 0.85, GREEN),
        ("Tezlik", 0.9, BLUE),
        ("Xavfsizlik", 0.8, VIOLET),
    ]
    # axis
    c.line(150, base_y, W - 150, base_y, DIM, 2, 0.7)
    group_w = (W - 360) / len(cats)
    x = 230
    bw = 70
    for name, fiber_val, col in cats:
        copper_val = fiber_val * 0.32 + 0.08
        # copper bar (dim grey)
        ch = int(360 * copper_val)
        c.fill_rect(x, base_y - ch, bw, ch, (150, 110, 70))
        c.line(x, base_y - ch, x + bw, base_y - ch, (210, 160, 110), 2)
        # fiber bar (neon, glowing)
        fh = int(360 * fiber_val)
        c.radial_glow(x + bw + 20 + bw / 2, base_y - fh, 120, col, 0.4)
        c.fill_rect(x + bw + 20, base_y - fh, bw, fh, col)
        c.fill_rect(x + bw + 20, base_y - fh, bw, 6, (255, 255, 255))
        x += group_w
    # legend swatches
    c.fill_rect(900, 130, 26, 18, (150, 110, 70)); 
    c.fill_rect(900, 165, 26, 18, CYAN)
    # three stat dots row at top (represents 44px stats)
    for i, col in enumerate([CYAN, GREEN, GOLD]):
        cxk = 300 + i * 330
        c.radial_glow(cxk, 120, 70, col, 0.4)
        c.ring(cxk, 120, 40, 6, col)
    return c


# --------------------------------------------------------------------------
# Slide 7 — Submarine cables: stylised world map with network links
# --------------------------------------------------------------------------
def slide7():
    c = base_canvas()
    c.radial_glow(W / 2, H / 2, 480, BLUE, 0.14)
    # continents as rough blobs (very stylised)
    land = (20, 70, 120)
    # Americas
    c.polygon([(230, 180), (300, 160), (330, 260), (300, 360), (340, 470),
               (300, 560), (250, 540), (240, 420), (210, 320)], land)
    # Europe/Africa
    c.polygon([(600, 170), (700, 160), (720, 240), (690, 300), (720, 420),
               (680, 560), (610, 540), (600, 400), (590, 280)], land)
    # Asia/Australia
    c.polygon([(820, 180), (1010, 170), (1080, 250), (1030, 320), (960, 300),
               (900, 360), (860, 300), (830, 240)], land)
    c.polygon([(1000, 470), (1090, 470), (1100, 540), (1020, 560), (990, 520)], land)
    # submarine cable arcs connecting hubs
    hubs = [(280, 300), (660, 300), (940, 260), (1050, 520), (300, 470)]
    arcs = [(0, 1), (1, 2), (0, 4), (1, 3), (2, 3), (0, 3), (1, 4)]
    for a, b in arcs:
        x0, y0 = hubs[a]
        x1, y1 = hubs[b]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 70
        prev = None
        for t in [i / 40 for i in range(41)]:
            # quadratic bezier
            xx = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1
            yy = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1
            if prev:
                c.line(prev[0], prev[1], xx, yy, CYAN, 2, 0.6)
            prev = (xx, yy)
    for h in hubs:
        draw_glow_dot(c, h[0], h[1], 10, GOLD)
    return c


# --------------------------------------------------------------------------
# Slide 8 — Cable-laying ship over deep sea, dropping cable to the floor
# --------------------------------------------------------------------------
def slide8():
    c = base_canvas()
    sea_top = 230
    # sky glow
    c.vertical_gradient(0, 0, W, sea_top, (8, 26, 52), (6, 20, 42))
    # sea
    c.vertical_gradient(0, sea_top, W, H - sea_top, (10, 44, 86), (2, 12, 30))
    # surface waves
    for i in range(6):
        y = sea_top + i * 6
        prev = None
        for x in range(0, W, 3):
            yy = y + math.sin(x / 60.0 + i) * 4
            if prev:
                c.line(prev[0], prev[1], x, yy, CYAN, 1, 0.25)
            prev = (x, yy)
    # ship hull
    sx = 420
    c.polygon([(sx, sea_top - 10), (sx + 240, sea_top - 10),
               (sx + 210, sea_top + 34), (sx + 30, sea_top + 34)], (18, 60, 110))
    c.fill_rect(sx + 70, sea_top - 60, 110, 52, (30, 80, 130))
    c.fill_rect(sx + 150, sea_top - 90, 24, 82, (40, 95, 150))
    # big cable reel
    c.ring(sx + 120, sea_top - 34, 26, 10, GOLD)
    # cable dropping to the sea floor, curving
    floor_y = H - 90
    prev = (sx + 150, sea_top - 8)
    pts = []
    for t in [i / 60 for i in range(61)]:
        xx = (sx + 150) + t * (W - 180 - (sx + 150))
        yy = (sea_top) + (floor_y - sea_top) * (t ** 1.6)
        pts.append((xx, yy))
    for i in range(len(pts) - 1):
        c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], GOLD, 4, 0.9)
    c.radial_glow(pts[-1][0], pts[-1][1], 70, GOLD, 0.4)
    # sea floor
    c.fill_rect(0, floor_y, W, H - floor_y, (16, 30, 48))
    for x in range(0, W, 40):
        c.filled_circle(x + 10, floor_y + 10, 6, (24, 42, 64))
    return c


# --------------------------------------------------------------------------
# Slide 9 — Conclusion: Earth wrapped in a light/network mesh
# --------------------------------------------------------------------------
def slide9():
    c = base_canvas()
    cx, cy, R = W / 2, H / 2, 230
    c.radial_glow(cx, cy, R * 1.8, BLUE, 0.22)
    # planet
    c.filled_circle(cx, cy, R, (14, 52, 100))
    c.filled_circle(cx - 40, cy - 40, R * 0.5, (22, 70, 128))
    # continents hint
    c.polygon([(cx - 120, cy - 60), (cx - 60, cy - 90), (cx - 40, cy - 20),
               (cx - 90, cy + 20)], (20, 90, 70))
    c.polygon([(cx + 30, cy - 30), (cx + 120, cy - 10), (cx + 90, cy + 70),
               (cx + 20, cy + 60)], (20, 90, 70))
    # latitude/longitude network mesh
    for k in range(-3, 4):
        rr = R
        a = k / 4
        # longitude ellipses (approx by scaling x)
        prev = None
        for deg in range(0, 361, 6):
            ang = math.radians(deg)
            x = cx + math.cos(ang) * R * abs(a if a != 0 else 0.08)
            y = cy + math.sin(ang) * R
            if prev:
                c.line(prev[0], prev[1], x, y, CYAN, 1, 0.3)
            prev = (x, y)
        # latitude lines
        yy = cy + a * R
        half = math.sqrt(max(0.0, R * R - (a * R) ** 2))
        c.line(cx - half, yy, cx + half, yy, CYAN, 1, 0.3)
    # orbiting network nodes + links
    nodes = []
    for i in range(10):
        ang = math.radians(i * 36)
        x = cx + math.cos(ang) * (R + 40)
        y = cy + math.sin(ang) * (R + 40)
        nodes.append((x, y))
        draw_glow_dot(c, x, y, 6, GOLD, glow=False)
        c.radial_glow(x, y, 24, GOLD, 0.35)
    for i in range(len(nodes)):
        c.line(nodes[i][0], nodes[i][1], nodes[(i + 3) % len(nodes)][0], nodes[(i + 3) % len(nodes)][1], CYAN, 1, 0.25)
    c.ring(cx, cy, R, 2, CYAN, 0.8)
    return c


# --------------------------------------------------------------------------
# Slide 10 — Thank you: abstract neon fiber-optic background
# --------------------------------------------------------------------------
def slide10():
    c = base_canvas()
    c.radial_glow(W / 2, H / 2, 460, VIOLET, 0.16)
    # sweeping neon fiber ribbons
    cols = [CYAN, BLUE, VIOLET, GREEN, GOLD]
    for i in range(16):
        color = cols[i % len(cols)]
        amp = 120 + (i % 5) * 24
        phase = i * 0.5
        prev = None
        for x in range(0, W, 2):
            y = H / 2 + math.sin(x / 160.0 + phase) * amp * math.cos(x / 900.0)
            if prev:
                c.line(prev[0], prev[1], x, y, color, 2, 0.4)
            prev = (x, y)
    # central burst of light (focal point for the "Rahmat" title)
    c.radial_glow(W / 2, H / 2, 240, CYAN, 0.5)
    for k in range(28):
        ang = math.radians(k * (360 / 28))
        x = W / 2 + math.cos(ang) * 210
        y = H / 2 + math.sin(ang) * 210
        c.line(W / 2, H / 2, x, y, CYAN, 1, 0.25)
    draw_glow_dot(c, W / 2, H / 2, 20, (255, 255, 255))
    return c


BUILDERS = [slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8, slide9, slide10]


def generate_all():
    os.makedirs(ASSETS, exist_ok=True)
    paths = []
    for i, fn in enumerate(BUILDERS, start=1):
        c = fn()
        p = os.path.join(ASSETS, f"slide{i:02d}.png")
        c.write_png(p)
        paths.append(p)
        print(f"  generated {os.path.relpath(p, HERE)}")
    return paths


if __name__ == "__main__":
    generate_all()
