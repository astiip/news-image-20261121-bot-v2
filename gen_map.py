"""Generate map.svg: a dotted world map with numbered pins for the
15 located stories of news-image-20261121 v2. Land is an abstract
mask built from overlapping ellipses (hand-placed, equirectangular);
pins are lon/lat -> x/y on a 600x300 canvas. Dots are spaced 7.5px;
pins are red discs with white numbers, nudged apart where they cluster.
Run from the repo dir.
"""
import math

W, H = 600, 300
STEP = 7.5

# (cx, cy, rx, ry) ellipses approximating the continents, canvas coords.
LAND = [
    # North America
    (130, 70, 58, 30), (60, 45, 36, 20), (140, 88, 34, 22),
    (100, 100, 24, 14),
    # Greenland
    (233, 30, 16, 9),
    # South America
    (195, 180, 30, 50), (190, 240, 14, 22),
    # Europe
    (315, 62, 24, 16), (300, 72, 14, 10),
    # Africa
    (330, 150, 32, 50), (325, 192, 20, 20), (310, 112, 20, 18),
    # Middle East / Arabia
    (372, 95, 20, 12),
    # Asia
    (450, 60, 72, 32), (428, 115, 16, 22), (475, 125, 16, 16),
    (500, 95, 20, 18), (530, 85, 7, 15), (480, 142, 22, 10),
    # Australia / NZ
    (520, 195, 32, 18), (585, 218, 5, 9),
]


def on_land(x, y):
    for cx, cy, rx, ry in LAND:
        if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
            return True
    return False


def ll(lon, lat):
    return (lon + 180) / 360 * W, (90 - lat) / 180 * H


# story number -> (lon, lat); pins 11 (Mercury) and 12 (Bitcoin) have no place.
PINS = {
    1: (30.7, 36.9),    # COP31, Antalya
    2: (46.7, 24.7),    # Riyadh
    3: (33.4, 47.9),    # Kryvyi Rih
    4: (-75.9, -11.2),  # Peru, Junin
    5: (27.0, 60.0),    # Sparta II, Gulf of Finland
    6: (-108.5, 25.6),  # Guasave
    7: (4.35, 50.85),   # Brussels
    8: (6.14, 46.2),    # Geneva
    9: (-0.34, 51.45),  # Twickenham
    10: (-115.1, 36.2),  # Las Vegas
    13: (125.6, 7.1),   # Davao
    14: (121.0, 23.7),  # Taiwan
    15: (-47.9, -15.8),  # Brasilia
}
# Nudge the crowded Brussels/Geneva/London cluster apart.
NUDGE = {7: (5, -5), 8: (6, 5), 9: (-5, 6), 3: (2, -2), 1: (-2, 2)}

out = ['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="300" viewBox="0 0 600 300">']
y = STEP
dots = 0
while y < H:
    x = STEP
    while x < W:
        if on_land(x, y):
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.1" fill="#1a1a1a" fill-opacity="0.55"/>')
            dots += 1
        x += STEP
    y += STEP
for n, (lon, lat) in sorted(PINS.items()):
    px, py = ll(lon, lat)
    dx, dy = NUDGE.get(n, (0, 0))
    px, py = px + dx, py + dy
    out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="#c1272d" stroke="#fdfdf9" stroke-width="1.5"/>')
    out.append(f'<text x="{px:.1f}" y="{py + 3.2:.1f}" font-family="Arial, sans-serif" font-size="9" '
               f'font-weight="bold" fill="#ffffff" text-anchor="middle">{n}</text>')
out.append('</svg>')
open("map.svg", "w").write("\n".join(out) + "\n")
print(f"map.svg: {dots} dots, {len(PINS)} pins")
