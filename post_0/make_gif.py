"""Generate a GIF illustrating the Two-Tower Matrix Multiplication idea for K=3.

Style follows the paper's skyscraper visualization (Section 3): blue / red / green
state-preparation operators stacked into two towers on disjoint registers, with a
"contraction" middle layer that pairs shared indices.
"""

from PIL import Image, ImageDraw, ImageFont
import math
from pathlib import Path

# -----------------------------------------------------------------------------
# Canvas / palette (matches the paper's skyscraper colors)
# -----------------------------------------------------------------------------
W, H = 1200, 675           # 16:9 to match LinkedIn preview ratio
BG = (10, 18, 35)          # deep navy
FG = (235, 240, 250)
DIM = (130, 140, 160)
ACCENT = (255, 200, 80)    # gold for highlights

MATRIX_BLUE = (0, 90, 180)
MATRIX_BLUE_FILL = (60, 130, 220)
MATRIX_RED = (200, 40, 40)
MATRIX_RED_FILL = (235, 90, 90)
MATRIX_GREEN = (40, 150, 40)
MATRIX_GREEN_FILL = (80, 200, 80)

OUT = Path(__file__).parent / "two_tower.gif"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = load_font(34, bold=True)
FONT_H = load_font(26, bold=True)
FONT_T = load_font(22)
FONT_S = load_font(18)
FONT_XS = load_font(15)
FONT_MONO = load_font(20)


def new_frame() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # subtle grid
    for x in range(0, W, 60):
        draw.line([(x, 0), (x, H)], fill=(18, 28, 50), width=1)
    for y in range(0, H, 60):
        draw.line([(0, y), (W, y)], fill=(18, 28, 50), width=1)
    return img


def text(draw: ImageDraw.ImageDraw, xy, msg, font=FONT_T, fill=FG, anchor=None):
    draw.text(xy, msg, font=font, fill=fill, anchor=anchor)


def draw_matrix_box(draw, x, y, w, h, color, fill, label, sublabel=None, alpha=255):
    # halo
    draw.rectangle([x - 4, y - 4, x + w + 4, y + h + 4], outline=color, width=2)
    # fill
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=color, width=3)
    # label
    cx, cy = x + w // 2, y + h // 2
    text(draw, (cx, cy - 8), label, font=FONT_H, fill=FG, anchor="mm")
    if sublabel:
        text(draw, (cx, cy + 18), sublabel, font=FONT_XS, fill=FG, anchor="mm")


def draw_register(draw, x, y, w, h, color, label):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, outline=color, width=2)
    text(draw, (x + w // 2, y + h // 2), label, font=FONT_XS, fill=DIM, anchor="mm")


def header(draw, title, subtitle=None):
    text(draw, (W // 2, 50), title, font=FONT_TITLE, fill=FG, anchor="mm")
    if subtitle:
        text(draw, (W // 2, 92), subtitle, font=FONT_S, fill=ACCENT, anchor="mm")


def footer(draw, msg):
    text(draw, (W // 2, H - 30), msg, font=FONT_XS, fill=DIM, anchor="mm")


# -----------------------------------------------------------------------------
# Frame 1 — the problem
# -----------------------------------------------------------------------------
def frame_problem():
    img = new_frame()
    d = ImageDraw.Draw(img)
    header(d, "Matrix chain multiplication", "Goal: compute  W = M⁽⁰⁾ · M⁽¹⁾ · M⁽²⁾")

    # three matrix boxes in a row + product equals
    box_w, box_h = 130, 130
    gap = 50
    total_w = 3 * box_w + 2 * gap + 90 + box_w + 60  # plus = and result
    start_x = (W - total_w) // 2
    y0 = 230

    colors = [(MATRIX_BLUE, MATRIX_BLUE_FILL),
              (MATRIX_RED, MATRIX_RED_FILL),
              (MATRIX_GREEN, MATRIX_GREEN_FILL)]
    labels = ["M⁽⁰⁾", "M⁽¹⁾", "M⁽²⁾"]
    sublabels = ["P₀ × P₁", "P₁ × P₂", "P₂ × P₃"]

    x = start_x
    for i in range(3):
        c, f = colors[i]
        draw_matrix_box(d, x, y0, box_w, box_h, c, f, labels[i], sublabels[i])
        x += box_w
        if i < 2:
            d.text((x + gap // 2, y0 + box_h // 2), "·",
                   font=FONT_TITLE, fill=FG, anchor="mm")
            x += gap

    # = result
    x += 30
    d.text((x, y0 + box_h // 2), "=", font=FONT_TITLE, fill=FG, anchor="mm")
    x += 60
    draw_matrix_box(d, x, y0, box_w, box_h, ACCENT, (90, 75, 30), "W", "P₀ × P₃")

    # costs
    text(d, (W // 2, 460), "Classical cost",
         font=FONT_H, fill=FG, anchor="mm")
    text(d, (W // 2, 500), "execution depth   O( K · N^2.37 )    -    memory   O( K · N^2 )",
         font=FONT_T, fill=DIM, anchor="mm")
    text(d, (W // 2, 540), "K matrices  ->  the cost grows with K.",
         font=FONT_T, fill=ACCENT, anchor="mm")

    footer(d, "Two-Tower Matrix Multiplication — Antonioli, Bernasconi, Berti, Del Corso, Poggiali · UniPi · ESA 2026")
    return img


# -----------------------------------------------------------------------------
# Frame 2 — prior quantum approaches still pay in K
# -----------------------------------------------------------------------------
def frame_prior():
    img = new_frame()
    d = ImageDraw.Draw(img)
    header(d, "Existing quantum approaches", "Depth still grows with the chain length K")

    rows = [
        ("Li et al.",        "A^K . b",      "Theta( sqrt(K) . polylog N )", "block / state"),
        ("Montanaro & Shao", "A^K",          "O( sqrt(K) . polylog N )",     "block-encoded"),
        ("Fang et al.",      "any K-tuple",  "O( K . polylog N )",           "block-encoded"),
        ("Two-Tower (ours)", "any K-tuple",  "O( polylog N )  --  K-free",   "quantum state"),
    ]

    col_x = [110, 380, 640, 1120]
    col_anchor = ["lm", "lm", "lm", "rm"]
    headers_text = ["Reference", "Setting", "Depth", "Encoding"]
    y = 175
    for hx, htxt, anc in zip(col_x, headers_text, col_anchor):
        text(d, (hx, y), htxt, font=FONT_H, fill=FG, anchor=anc)
    d.line([(80, y + 25), (W - 80, y + 25)], fill=DIM, width=2)

    y += 60
    row_font = FONT_T
    for i, row in enumerate(rows):
        is_us = (i == len(rows) - 1)
        col = ACCENT if is_us else FG
        for hx, val, anc in zip(col_x, row, col_anchor):
            text(d, (hx, y), val, font=row_font, fill=col, anchor=anc)
        if is_us:
            d.rectangle([80, y - 25, W - 80, y + 25], outline=ACCENT, width=3)
        y += 60

    footer(d, "Two-Tower Matrix Multiplication — Antonioli, Bernasconi, Berti, Del Corso, Poggiali · UniPi · ESA 2026")
    return img


# -----------------------------------------------------------------------------
# Frame 3 — Build the two towers (animated over a few frames)
# -----------------------------------------------------------------------------
def frame_towers(reveal: int):
    """reveal in {0,1,2,3} controls how many blocks of the towers are shown."""
    img = new_frame()
    d = ImageDraw.Draw(img)
    header(d, "The Two-Tower construction", "Two layers of state-preparation operators on disjoint registers")

    # Two parallel columns of blocks ("towers"), connected by a contraction.

    col_left_x = 320
    col_right_x = 760
    col_w = 220
    block_h = 70
    gap_v = 16

    # Tower bases (registers) — placed higher so labels below don't clip the footer
    base_y = 510
    draw_register(d, col_left_x - 10, base_y, col_w + 20, 28, MATRIX_BLUE, "register A   |0>")
    draw_register(d, col_right_x - 10, base_y, col_w + 20, 28, MATRIX_RED, "register B   |0>")

    # Tower L blocks (bottom → top): SP(M⁽⁰⁾) → contraction → MSP/SP(M⁽²⁾)
    # Tower R blocks (bottom → top): SP(M⁽¹⁾) → contraction (shared horizontally)
    # We highlight contraction lines that connect the two towers (the "pairing").

    blocks = [
        # (tower, label, color, fill)
        ("L", "SP( M⁽⁰⁾ )", MATRIX_BLUE, MATRIX_BLUE_FILL),
        ("R", "SP( M⁽¹⁾ )", MATRIX_RED, MATRIX_RED_FILL),
        ("L", "MSP( M⁽²⁾ )", MATRIX_GREEN, MATRIX_GREEN_FILL),
    ]

    # Stack y positions (going up from base)
    y_levels = [base_y - gap_v - block_h,
                base_y - gap_v - block_h,           # layer 1 (same level for L and R)
                base_y - 2 * gap_v - 2 * block_h]   # layer 2 (on top in L only)

    # Render blocks up to "reveal"
    for i, (tower, label, c, f) in enumerate(blocks[:reveal]):
        if tower == "L" and i == 0:
            y = y_levels[0]
            x = col_left_x
        elif tower == "R" and i == 1:
            y = y_levels[1]
            x = col_right_x
        else:  # tower L, layer 2
            y = y_levels[2]
            x = col_left_x
        draw_matrix_box(d, x, y, col_w, block_h, c, f, label)

    # Column labels — sit below the registers, well above the footer
    text(d, (col_left_x + col_w // 2, base_y + 60), "Tower L",
         font=FONT_H, fill=(120, 170, 240), anchor="mm")
    text(d, (col_right_x + col_w // 2, base_y + 60), "Tower R",
         font=FONT_H, fill=(240, 130, 130), anchor="mm")

    # Contraction arrows (between L's layer 1 and R's layer 1)
    if reveal >= 2:
        ay = y_levels[1] + block_h // 2
        # arrow from L to R
        d.line([(col_left_x + col_w, ay), (col_right_x, ay)],
               fill=ACCENT, width=3)
        d.polygon([(col_right_x, ay), (col_right_x - 12, ay - 7),
                   (col_right_x - 12, ay + 7)], fill=ACCENT)
        d.polygon([(col_left_x + col_w, ay), (col_left_x + col_w + 12, ay - 7),
                   (col_left_x + col_w + 12, ay + 7)], fill=ACCENT)
        text(d, ((col_left_x + col_w + col_right_x) // 2, ay - 22),
             "contraction (shared index r)", font=FONT_S, fill=ACCENT, anchor="mm")

    # Side annotation — uses ASCII-safe glyphs only
    notes = []
    if reveal >= 1:
        notes.append("(1)  load M(0) on register A")
    if reveal >= 2:
        notes.append("(2)  load M(1) on register B  ->  contract on the shared index")
    if reveal >= 3:
        notes.append("(3)  load M(2) on top of A   ->  amplitudes encode  W = M(0).M(1).M(2)")

    y = 165
    for n in notes:
        text(d, (90, y), n, font=FONT_T, fill=FG)
        y += 36

    footer(d, "Two-Tower Matrix Multiplication — Antonioli, Bernasconi, Berti, Del Corso, Poggiali · UniPi · ESA 2026")
    return img


# -----------------------------------------------------------------------------
# Frame 4 — The result, highlight: depth independent of K
# -----------------------------------------------------------------------------
def frame_result(pulse: int):
    img = new_frame()
    d = ImageDraw.Draw(img)
    header(d, "Two-Tower: depth independent of K")

    # Big formula
    text(d, (W // 2, 200),
         "Circuit depth   O( polylog N )",
         font=FONT_TITLE, fill=ACCENT if pulse else FG, anchor="mm")
    text(d, (W // 2, 250),
         "(independent of the chain length K)",
         font=FONT_T, fill=FG, anchor="mm")

    # bullets — draw the purple disc manually so we don't rely on emoji glyphs
    bullets = [
        "No optimal parenthesisation needed",
        "Theta( K . log N ) qubits   --   exponential compression vs O( K . N^2 )",
        "Output: amplitudes of a single quantum state encode  W = M(0) . M(1) . M(2)",
        "Open-source code in Qiskit + QCLAB",
    ]
    y = 330
    for b in bullets:
        # purple bullet disc
        bx, by = 130, y
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9],
                  fill=(155, 95, 220), outline=(200, 160, 255), width=2)
        text(d, (bx + 22, y), b, font=FONT_T, fill=FG, anchor="lm")
        y += 50

    # call-to-action
    text(d, (W // 2, 600), "ESA 2026 submission   ·   preprint + code in the first comment",
         font=FONT_S, fill=ACCENT, anchor="mm")

    footer(d, "Two-Tower Matrix Multiplication — Antonioli, Bernasconi, Berti, Del Corso, Poggiali · UniPi · ESA 2026")
    return img


# -----------------------------------------------------------------------------
# Assemble GIF
# -----------------------------------------------------------------------------
def build():
    frames = []
    durations = []

    # 1 — problem (held)
    frames.append(frame_problem()); durations.append(2200)
    # 2 — prior approaches (held)
    frames.append(frame_prior());   durations.append(2600)
    # 3 — towers built up step by step
    for r in (1, 2, 3):
        frames.append(frame_towers(r))
        durations.append(1300 if r < 3 else 1800)
    # 4 — result with pulsing highlight
    for p in (0, 1, 0, 1):
        frames.append(frame_result(p)); durations.append(450)
    # hold the result longer at the end
    frames.append(frame_result(1));     durations.append(2200)

    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"Wrote {OUT}  ({OUT.stat().st_size/1024:.1f} KB, {len(frames)} frames)")


if __name__ == "__main__":
    build()
