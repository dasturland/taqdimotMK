"""Minimal pure-stdlib raster drawing + PNG writer.

No Pillow / numpy required. Provides a simple RGB canvas with primitives
(gradients, rectangles, lines, circles, polygons, polylines) sufficient to
draw the themed slide illustrations for the optik-tola presentation.
"""

import math
import struct
import zlib


class Canvas:
    def __init__(self, width, height, bg=(2, 11, 26)):
        self.w = width
        self.h = height
        # flat bytearray, 3 bytes per pixel (RGB)
        self.buf = bytearray(width * height * 3)
        self.fill_rect(0, 0, width, height, bg)

    # ---- low level ----
    def _idx(self, x, y):
        return (y * self.w + x) * 3

    def set_px(self, x, y, color, alpha=1.0):
        xi = int(x)
        yi = int(y)
        if xi < 0 or yi < 0 or xi >= self.w or yi >= self.h:
            return
        i = self._idx(xi, yi)
        if alpha >= 1.0:
            self.buf[i] = color[0]
            self.buf[i + 1] = color[1]
            self.buf[i + 2] = color[2]
        else:
            a = max(0.0, min(1.0, alpha))
            self.buf[i] = int(self.buf[i] * (1 - a) + color[0] * a)
            self.buf[i + 1] = int(self.buf[i + 1] * (1 - a) + color[1] * a)
            self.buf[i + 2] = int(self.buf[i + 2] * (1 - a) + color[2] * a)

    # ---- fills ----
    def fill_rect(self, x, y, w, h, color, alpha=1.0):
        x0 = max(0, int(x))
        y0 = max(0, int(y))
        x1 = min(self.w, int(x + w))
        y1 = min(self.h, int(y + h))
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                self.set_px(xx, yy, color, alpha)

    def vertical_gradient(self, x, y, w, h, top_color, bot_color):
        x0 = max(0, int(x))
        y0 = max(0, int(y))
        x1 = min(self.w, int(x + w))
        y1 = min(self.h, int(y + h))
        span = max(1, y1 - y0 - 1)
        for yy in range(y0, y1):
            t = (yy - y0) / span
            r = int(top_color[0] + (bot_color[0] - top_color[0]) * t)
            g = int(top_color[1] + (bot_color[1] - top_color[1]) * t)
            b = int(top_color[2] + (bot_color[2] - top_color[2]) * t)
            c = (r, g, b)
            base = self._idx(x0, yy)
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.buf[i] = r
                self.buf[i + 1] = g
                self.buf[i + 2] = b

    def radial_glow(self, cx, cy, radius, color, intensity=0.6):
        r2 = radius * radius
        x0 = max(0, int(cx - radius))
        y0 = max(0, int(cy - radius))
        x1 = min(self.w, int(cx + radius))
        y1 = min(self.h, int(cy + radius))
        for yy in range(y0, y1):
            dy = yy - cy
            for xx in range(x0, x1):
                dx = xx - cx
                d2 = dx * dx + dy * dy
                if d2 > r2:
                    continue
                t = 1 - math.sqrt(d2) / radius
                self.set_px(xx, yy, color, intensity * t * t)

    # ---- strokes ----
    def line(self, x0, y0, x1, y1, color, width=1, alpha=1.0):
        x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
        dx = x1 - x0
        dy = y1 - y0
        dist = max(abs(dx), abs(dy))
        steps = int(dist) + 1
        r = max(1, width) / 2.0
        for s in range(steps + 1):
            t = s / steps
            px = x0 + dx * t
            py = y0 + dy * t
            if width <= 1:
                self.set_px(px, py, color, alpha)
            else:
                self.filled_circle(px, py, r, color, alpha)

    def polyline(self, points, color, width=1, alpha=1.0):
        for i in range(len(points) - 1):
            self.line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], color, width, alpha)

    def filled_circle(self, cx, cy, radius, color, alpha=1.0):
        r = radius
        x0 = int(cx - r - 1)
        x1 = int(cx + r + 1)
        y0 = int(cy - r - 1)
        y1 = int(cy + r + 1)
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                dx = xx - cx
                dy = yy - cy
                d = math.sqrt(dx * dx + dy * dy)
                if d <= r - 0.8:
                    self.set_px(xx, yy, color, alpha)
                elif d <= r + 0.5:
                    # antialias edge
                    a = alpha * (r + 0.5 - d)
                    self.set_px(xx, yy, color, max(0.0, min(alpha, a)))

    def ring(self, cx, cy, radius, thickness, color, alpha=1.0):
        outer = radius
        inner = radius - thickness
        x0 = int(cx - outer - 1)
        x1 = int(cx + outer + 1)
        y0 = int(cy - outer - 1)
        y1 = int(cy + outer + 1)
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                dx = xx - cx
                dy = yy - cy
                d = math.sqrt(dx * dx + dy * dy)
                if inner - 0.5 <= d <= outer + 0.5:
                    self.set_px(xx, yy, color, alpha)

    def rounded_rect(self, x, y, w, h, radius, color, alpha=1.0):
        x = float(x); y = float(y); w = float(w); h = float(h)
        r = min(radius, w / 2, h / 2)
        for yy in range(int(y), int(y + h)):
            for xx in range(int(x), int(x + w)):
                # determine if inside rounded region
                cx = min(max(xx, x + r), x + w - r)
                cy = min(max(yy, y + r), y + h - r)
                dx = xx - cx
                dy = yy - cy
                if dx * dx + dy * dy <= r * r:
                    self.set_px(xx, yy, color, alpha)

    def polygon(self, points, color, alpha=1.0):
        ys = [p[1] for p in points]
        ymin = int(min(ys))
        ymax = int(max(ys))
        n = len(points)
        for yy in range(ymin, ymax + 1):
            xs = []
            for i in range(n):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % n]
                if (y1 <= yy < y2) or (y2 <= yy < y1):
                    xi = x1 + (yy - y1) * (x2 - x1) / (y2 - y1)
                    xs.append(xi)
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                for xx in range(int(xs[k]), int(xs[k + 1]) + 1):
                    self.set_px(xx, yy, color, alpha)

    # ---- output ----
    def write_png(self, path):
        def chunk(tag, data):
            c = tag + data
            return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)  # filter type 0
            start = y * stride
            raw.extend(self.buf[start:start + stride])
        compressed = zlib.compress(bytes(raw), 9)
        sig = b"\x89PNG\r\n\x1a\n"
        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        with open(path, "wb") as f:
            f.write(sig)
            f.write(chunk(b"IHDR", ihdr))
            f.write(chunk(b"IDAT", compressed))
            f.write(chunk(b"IEND", b""))
