from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "screenshots"
BG = "#07111d"
CARD = "#102033"
CARD_ALT = "#16283f"
TEXT = "#f5eedd"
MUTED = "#b1bed0"
ACCENT = "#84cbff"
PINK = "#f6bfd8"
GREEN = "#93e3b1"
YELLOW = "#f4d17c"
EDGE = "#294a70"


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def rounded(draw, box, fill, outline=EDGE, width=2, radius=24):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def write(draw, xy, text, fill, size, bold=False, spacing=8):
    draw.multiline_text(xy, text, fill=fill, font=font(size, bold), spacing=spacing)


def hero():
    img = Image.new("RGB", (1600, 920), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, 1550, 880), CARD, radius=32)
    write(draw, (95, 95), "KNOWLEDGE MEMORY WORKBENCH", ACCENT, 24)
    write(draw, (95, 155), "Recover context before\noperators recover it by hand.", TEXT, 56, True)
    write(draw, (95, 325), "A Python memory engine for snapshot packets, context aging,\nretrieval scoring, and briefing-safe operator recall.", MUTED, 28)

    stats = [("Packets", "18"), ("Live threads", "6"), ("Stale notes", "3"), ("Recovery risk", "2")]
    x = 95
    for label, value in stats:
        rounded(draw, (x, 450, x + 300, 620), CARD_ALT, radius=22)
        write(draw, (x + 22, 480), label.upper(), MUTED, 16)
        write(draw, (x + 22, 524), value, TEXT, 42, True)
        x += 320

    rounded(draw, (95, 690, 1505, 810), CARD_ALT, radius=22)
    write(draw, (125, 718), "CURRENT MEMORY PRIORITY", PINK, 18)
    write(draw, (125, 752), "Board, retention, and model notes should anchor the next executive briefing recovery path.", TEXT, 25, True)
    return img


def lanes():
    img = Image.new("RGB", (1600, 920), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, 1550, 880), CARD, radius=32)
    write(draw, (95, 95), "MEMORY LANES", ACCENT, 24)
    write(draw, (95, 155), "Snapshots grouped by domain,\nfreshness, and trust.", TEXT, 54, True)
    items = [
        (PINK, "Executive Ops", "Board briefing pressure chain\nfreshness: 1 day\nconfidence: 0.92"),
        (YELLOW, "Platform Security", "Tenant bleed response memory\nfreshness: 5 days\nconfidence: 0.84"),
        (GREEN, "Release Management", "Release gate escalation memory\nfreshness: 2 days\nconfidence: 0.88"),
    ]
    x = 95
    for tone, title, body in items:
        rounded(draw, (x, 360, x + 440, 710), CARD_ALT, radius=24)
        write(draw, (x + 24, 392), title.upper(), tone, 18, True)
        write(draw, (x + 24, 460), body, TEXT if "\n" not in body else MUTED, 27 if "\n" not in body else 23, True if "\n" not in body else False)
        x += 470
    return img


def retrieval():
    img = Image.new("RGB", (1600, 960), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, 1550, 920), CARD, radius=32)
    write(draw, (95, 95), "RETRIEVAL ENGINE", ACCENT, 24)
    write(draw, (95, 155), "The workbench ranks the best\nmemory packet before briefing time.", TEXT, 54, True)
    rounded(draw, (95, 340, 760, 790), "#071421", radius=24)
    write(draw, (130, 378), "> POST /api/analyze/retrieval", GREEN, 24, True)
    write(draw, (130, 452), "{", MUTED, 24)
    write(draw, (160, 492), "\"prompt\": \"Need board pipeline retention model briefing recovery\",", MUTED, 22)
    write(draw, (160, 532), "\"freshness_budget_days\": 7", MUTED, 22)
    write(draw, (130, 572), "}", MUTED, 24)

    rounded(draw, (820, 340, 1505, 790), CARD_ALT, radius=24)
    write(draw, (855, 378), "TOP PACKET", PINK, 18)
    write(draw, (855, 432), "mem-101 · Board briefing pressure chain", TEXT, 28, True)
    write(draw, (855, 502), "Status: Ready", GREEN, 24, True)
    write(draw, (855, 548), "Domain: Executive Ops", MUTED, 22)
    write(draw, (855, 592), "Action: attach one fresh operator note before distribution", YELLOW, 22)
    return img


def anatomy():
    img = Image.new("RGB", (1600, 940), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, 1550, 900), CARD, radius=32)
    write(draw, (95, 95), "PROJECT ANATOMY", ACCENT, 24)
    write(draw, (95, 155), "A local-first memory system with\nboth graph and operator flavor.", TEXT, 54, True)
    rows = [
        ("1", "Sample memory packets", "Seeded executive, security, search, and release memory lanes."),
        ("2", "Retrieval scoring", "Ranks packets by keyword fit, freshness budget, and confidence."),
        ("3", "Proof layer", "Demo report, tests, and PNG screenshots keep the repo inspectable."),
    ]
    y = 330
    for badge, title, body in rows:
        rounded(draw, (95, y, 1505, y + 150), CARD_ALT, radius=22)
        rounded(draw, (125, y + 42, 190, y + 107), "#223b59", radius=18)
        write(draw, (149, y + 63), badge, ACCENT, 18, True)
        write(draw, (220, y + 45), title, TEXT, 28, True)
        write(draw, (220, y + 90), body, MUTED, 20)
        y += 176
    return img


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, image in [
        ("01-hero.png", hero()),
        ("02-memory-lanes.png", lanes()),
        ("03-retrieval-engine.png", retrieval()),
        ("04-anatomy.png", anatomy()),
    ]:
        image.save(OUT_DIR / name)


if __name__ == "__main__":
    main()

