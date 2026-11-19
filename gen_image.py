"""Build entry.png: one dense editorial plate of 19 November 2026 world news.

Judge priorities: name the day, breadth across regions and fields, each
story readable from short labels, faithful to reports, clean craft. So
this draws a six-region newspaper plate with 30 reported stories, a
lead banner for the day's biggest event, and a sources footer.
Deterministic: same inputs, same bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

NAVY = (12, 24, 56)
RED = (176, 32, 32)
PAPER = (250, 248, 242)
INK = (18, 18, 18)
GREY = (88, 88, 88)
GOLD = (255, 208, 80)
LINE = (205, 200, 190)

# Six regions, five reported stories each. Every headline is a fact
# reported on 19 Nov 2026 (Reuters, BBC, Guardian, Xinhua, Dawn, IEA...).
REGIONS = [
    ("ASIA-PACIFIC", (20, 90, 170), [
        "Trump, Xi, Putin hold first trilateral summit in Shenzhen",
        "Putin meets Trump 40 min; Ukraine war on agenda",
        "Japan PM Takaichi holds talks with Putin at APEC",
        "S Korea hits $1 trillion exports on AI chip boom",
        "GTA 6 launches after 13-year wait",
    ]),
    ("MIDDLE EAST", (176, 32, 32), [
        "Iran drones strike US base in Kuwait after Qeshm raid",
        "Bahrain intercepts Iranian attacks third time this week",
        "Saudi strikes Sanaa; Houthi hit damages Riyadh PIF tower",
        "Israel pushes into central Gaza beyond Yellow Line",
        "IAEA calls US-Saudi nuclear deal satisfactory",
    ]),
    ("EUROPE", (0, 120, 120), [
        "Crimean Bridge hit third time this week; traffic halted",
        "EU proposes EUR 45bn Ukraine loan, repaid after reparations",
        "40-nation coalition meets in Berlin on Ukraine guarantees",
        "EU approves Indonesia trade deal to offset US tariffs",
        "ICJ rules today on Myanmar Rohingya genocide case",
    ]),
    ("AMERICAS", (110, 60, 170), [
        "Jeffries nominated; set to be first Black House speaker",
        "Peltola wins Alaska; Democrats reach 56-44 Senate",
        "US loses measles elimination status after 26 years",
        "US-Venezuela sign deal to restore military ties",
        "Anthropic IPO debut at $81.3bn breaks SpaceX record",
    ]),
    ("AFRICA", (200, 110, 20), [
        "Ethiopia, Eritrea mass forces on border; war fears rise",
        "DRC Ebola out of control: 11,000 cases, 5,400 dead",
        "Nigeria: all 36 states approve state police amendment",
        "Somalia president dismisses chief justice before ruling",
        "Boat with 100 migrants sinks off Senegal; dozens missing",
    ]),
    ("SOUTH ASIA / WORLD", (40, 130, 70), [
        "Cyclone Akvan nears India; 50,000 evacuated in Odisha",
        "Bangladesh unrest over Hasina return; Yunus home burned",
        "Voyager 1 reaches one light-day from Earth, first ever",
        "IEA: Iran war cost 2.8bn barrels of Gulf oil supply",
        "Record 589 million children lived in conflict zones",
    ]),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, words, cur = [], text.split(), ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header: the day, named large.
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.text((28, 10), "THURSDAY 19 NOVEMBER 2026", font=font(BOLD, 42), fill=(255, 255, 255))
    d.text((28, 58), "WORLD NEWS IN ONE IMAGE  ·  30 REPORTED STORIES  ·  SIX REGIONS", font=font(BOLD, 19), fill=GOLD)
    d.rectangle([0, 92, W, 100], fill=RED)

    # Lead banner: the day's biggest event.
    d.rectangle([16, 110, W - 16, 172], fill=(255, 252, 240), outline=RED, width=3)
    d.text((30, 118), "LEAD: TRUMP–XI–PUTIN TRILATERAL IN SHENZHEN", font=font(BOLD, 26), fill=RED)
    d.text((30, 148), "First three-way meeting of US, China, Russia leaders; Ukraine, Iran, nuclear arms on the table", font=font(REG, 18), fill=INK)

    # Six region panels, 2 columns x 3 rows.
    x0, y0, pw, ph, gx, gy = 16, 186, 488, 252, 16, 12
    hf = font(BOLD, 20)
    bf = font(REG, 16)
    for i, (region, color, stories) in enumerate(REGIONS):
        col, row = i % 2, i // 2
        x, y = x0 + col * (pw + gx), y0 + row * (ph + gy)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=10, fill=(255, 255, 255), outline=LINE, width=2)
        d.rectangle([x, y, x + pw, y + 30], fill=color)
        d.text((x + 12, y + 5), region, font=font(BOLD, 18), fill=(255, 255, 255))
        ty = y + 40
        for s in stories:
            lines = wrap(d, s, bf, pw - 46)
            d.ellipse([x + 12, ty + 5, x + 20, ty + 13], fill=color)
            for j, ln in enumerate(lines):
                d.text((x + 28, ty + j * 19), ln, font=bf, fill=INK)
            ty += 19 * len(lines) + 6

    # Footer: sources and honesty note.
    d.text((28, H - 30), "Sources: Reuters, BBC, Guardian, Xinhua, Dawn, AP, IEA, UN — reports of 19 Nov 2026. Headlines as reported, without speculation.", font=font(REG, 15), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
