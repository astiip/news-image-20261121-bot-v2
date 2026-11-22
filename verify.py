"""Verify news-image-20261121 v2 build.html: all 36 stories, 18 DATE CHECK
items, region counts summing to 36, strip figures tied to their stories,
and forbidden wrong figures absent; plus entry.png is 1024x1024 and <=1 MiB.
Run from the repo dir."""
import html
import re
import struct
import sys
from pathlib import Path

src = html.unescape(Path("build.html").read_text())
text = re.sub(r"<[^>]+>", " ", src)
text = re.sub(r"\s+", " ", text)
upper = text.upper()

stories = {
    1: ["COP31", "144 paragraphs", "80", "$120bn", "03:00 GMT", "06:00"],
    2: ["Three Missiles Down Over Riyadh", "three Houthi", "PIF Tower", "no one was hurt"],
    3: ["Double-Tap Strike Kills A Boy Of 7", "paramedic of 20", "58 people were hurt", "148 drones", "117 downed"],
    4: ["Quake Shakes The Andes", "M6.7", "00:09 UTC", "Junín", "one dead, 16 hurt"],
    5: ["Drones Set A Russian Freighter Ablaze", "Sparta II", "two drones", "16 crew"],
    6: ["Mexico Seizes", "Fausto Isidro Meza Flores", "Guasave", "$5m"],
    7: ["Indonesia And The EU Sign", "90.4%", "Brussels", "early 2027"],
    8: ["Killer-Robot Talks", "128 states", "2028", "no binding treaty"],
    9: ["England Rout The All Blacks 37", "Five tries", "25-point margin", "Twickenham"],
    10: ["Five-Place Penalty", "1:33.893", "Verstappen, 1:34.151", "Las Vegas"],
    11: ["Spacecraft Reaches Mercury", "37-minute burn", "18:24 UTC", "second mission"],
    12: ["Bitcoin Sinks Below $60,000", "$58,810", "ether $1,619", "first time since July"],
    13: ["146 Walk Down The Slides In Davao", "PX19", "137 passengers and 9 crew"],
    14: ["21 Chinese Warplanes", "15 crossed", "08:46", "median line"],
    15: ["Bolsonaro, 71, Moved To Intensive Care", "bowel obstruction", "Brasília", "feeding tube"],
    16: ["Rutte", "every inch", "Russian objects"],
    17: ["Rahul 124*", "344/2", "13th ton", "SENA"],
    18: ["Trump Vows A", "tremendous tax", "data centres abroad"],
    19: ["Wall Street", "Nasdaq", "5.3%", "Nvidia", "14%"],
    20: ["Trump Calls His Putin Talks", "very good", "no security guarantees"],
    21: ["Trump And Xi Agree", "humans must stay in charge", "military AI"],
    22: ["Iran Masses 14 Tankers", "Kharg Island", "US blockade"],
    23: ["LA Arsonist Convicted", "Rinderknecht", "12 died", "17 Mar 2027"],
    24: ["Bayer", "$7.25bn Roundup", "$10,000", "$165,000"],
    25: ["Turin Tonight", "Zverev v Medvedev", "20:30 CET", "Tiafoe"],
    26: ["Korean Freight Train", "Sejong", "5 of 21 cars", "05:37"],
    27: ["Gaza Truce Frays", "six killed", "1,600+ dead"],
    28: ["SCO Culture Forum", "Delhi", "20+ nations"],
    29: ["Zelenskyy", "Crimea bridge", "will not stay"],
    30: ["October Was The Warmest On Record", "1.80", "1850"],
    31: ["Kushner In Berlin", "NATO-style guarantees"],
    32: ["India", "H5N1", "2 a dose", "six months"],
    33: ["Beijing Tells Tokyo", "unchanged since 1972", "Taiwan"],
    34: ["Denmark Expels A Russian Envoy", "7 days to leave", "two men charged"],
    35: ["Two More Tankers Hit Near Khasab", "TORKEL", "ARINA"],
    36: ["Mlambo-Ngcuka", "state funeral", "first woman deputy president", "71"],
}
dc = ["UK–EU deal — Fri 20 Nov", "Kyiv barrage — Fri 20 Nov",
      "Poland missile landing — Fri 20 Nov", "Akvan landfall — Fri 20 Nov",
      "ICJ: Myanmar guilty — Thu 19 Nov", "Anthropic IPO — Thu 19 Nov",
      "GTA VI launch — Thu 19 Nov", "Somalia expels UAE envoy — Thu 19 Nov",
      "Mlambo-Ngcuka dies — Fri 20 Nov", "Jazan missiles — Fri 20 Nov",
      "Hodeidah strike — Fri 20 Nov", "Virginia measles death — Fri 20 Nov",
      "EU pays Kyiv €7.9bn — Fri 20 Nov", "APEC ends in Shenzhen — Thu 19 Nov",
      "ANC 31% — 7 Nov", "Starc’s 7-58 — 2025 Ashes",
      "AI chips, 879,000 — Thu 19 Nov", "Jurf al-Sakhar — Fri 20 Nov"]

fails = []
for n, phrases in stories.items():
    for p in phrases:
        if p.upper() not in upper:
            fails.append(f"story {n}: missing {p!r}")
for item in dc:
    if item.upper() not in upper:
        fails.append(f"DATE CHECK: missing {item!r}")

# forbidden wrong figures must NOT appear anywhere on the page
for bad in ["5 missiles", "five missiles", "900,000", "82 injured",
            "wound 82", "Article 4 invoked", "60 hurt in Kryvyi",
            "five Houthi", "FIVE missiles"]:
    if bad.upper() in upper:
        fails.append(f"FORBIDDEN present: {bad!r}")

# region bar sums to 36 across 9 regions
regions = [("AMERICAS", 9), ("EUROPE", 8), ("ASIA", 6), ("GLOBAL", 5),
           ("MIDDLE EAST", 4), ("OCEANIA", 2), ("SPACE", 1), ("AFRICA", 1)]
total = 0
for name, want in regions:
    if re.search(rf"{name}\s*</span>\s*<span class=\"bar\"[^>]*></span>\s*<span class=\"ct\">{want}</span>", src):
        total += want
    else:
        fails.append(f"region bar: missing {name} {want}")
if total != 36 or len(regions) != 8:
    fails.append(f"region bar: sums to {total}, want 8 rows = 36")

# UTC strip figures tied to their stories
for p in ["00:09", "03:45", "06:00", "08:46", "18:24", "19:03"]:
    if p not in text:
        fails.append(f"UTC strip: missing {p!r}")

# index must be numbered 16-36
for n in range(16, 37):
    if f"{n}." not in text:
        fails.append(f"index: missing number {n}.")

# entry.png: PNG, 1024x1024, <= 1 MiB
png = Path("entry.png").read_bytes()
if len(png) > 1048576:
    fails.append(f"entry.png too big: {len(png)} bytes")
if png[:8] != b"\x89PNG\r\n\x1a\n":
    fails.append("entry.png is not a PNG")
w, h = struct.unpack(">II", png[16:24])
if (w, h) != (1024, 1024):
    fails.append(f"entry.png size {w}x{h}, want 1024x1024")

print(f"stories checked: {len(stories)}, date-check items: {len(dc)}, regions sum: {total}")
print(f"entry.png: {len(png)} bytes, {w}x{h}")
if fails:
    print("FAILURES:")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
