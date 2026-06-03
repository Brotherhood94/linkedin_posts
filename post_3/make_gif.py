"""
make_gif.py — "101 Orbis" milestone animation.

Renders "101" in the visual language of the open-orbis app: the two outer "1"s
are knowledge-graph subgraphs, and the middle digit is the OpenOrbis logo mark
itself — a translucent purple disc + core orb, rebuilt from docs/assets/logo.svg
(outer circle #7c3aed @0.3 with a #8b5cf6 stroke; core orb #a78bfa; core/outer
ratio 18/44). It breathes and drifts gently, so the number reads as  1 ◎ 1.

  - pure-black canvas (#000000),
  - nodes drawn as white-core + colored-body + soft-glow halos,
  - one concentric-purple "person" hub per "1" (the orbis logo motif),
  - curved, faint white links (rgba(255,255,255,~0.2)) tinted by the source node,
  - a field of drifting background particles (purple / indigo / teal),
  - a few faint shooting stars streaking quietly behind the graph,
  - per-node jitter so the graph "breathes" while each digit keeps its shape.

The two subgraphs never connect to each other — flanking the central logo they
read as 1 ◎ 1.

Glows are smooth radial-gradient stamps (imshow) for a soft, production look.
All motion is periodic in the frame index, so the GIF loops seamlessly.

Outputs:
  orbis_101.gif  (the media to upload)
  preview.png    (one representative frame, for visual QA)
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch
from matplotlib.animation import FuncAnimation, PillowWriter

# ---- palette (lifted from open-orbis: NodeColors.ts + OrbGraph3D.tsx) -------
BG = "#000000"
WHITE = "#FFFFFF"

# per-type node palette (colorblind-safe Wong + IBM, as in the app)
TYPE_COLORS = [
    "#0072B2",  # education  — blue
    "#009E73",  # work       — green
    "#E69F00",  # cert       — orange
    "#56B4E9",  # publication— sky
    "#D55E00",  # project    — vermillion
    "#648FFF",  # skill      — periwinkle
    "#DC267F",  # patent     — magenta
    "#FFB000",  # award      — gold
    "#20B2AA",  # outreach   — teal
    "#F0E442",  # language   — yellow
]

# the "person" hub (concentric purple, like the myorbis logo)
PERSON_CORE = "#9333ea"
PERSON_MID = "#c084fc"
PERSON_DOT = "#e9d5ff"
PERSON_RING = "#a78bfa"

# the OpenOrbis logo mark (docs/assets/logo.svg): translucent disc + core orb
LOGO_FILL = "#7c3aed"
LOGO_STROKE = "#8b5cf6"
LOGO_CORE = "#a78bfa"
LOGO_HI = "#c4b5fd"

# drifting background particles
PART_COLORS = ["#8b5cf6", "#6366f1", "#a78bfa", "#3b82f6", "#14b8a6"]

# ---- canvas / geometry ------------------------------------------------------
LIM = 12.0                 # square data range -> round nodes
CY = 6.0                   # vertical center of the digits
H = 5.0                    # digit height
SPACING = 0.52             # node spacing along a stroke
DIGIT_CX = [2.95, 6.0, 9.05]    # x-centers: "1", OpenOrbis logo, "1"
LOGO_CX, LOGO_CY = DIGIT_CX[1], CY   # the middle slot is the logo, not a "0"
LOGO_R = 1.95                   # logo outer-disc radius
LOGO_CORE_R = LOGO_R * 0.41     # core/outer ratio from logo.svg (18 / 44)

N_FRAMES = 80
FPS = 20

np.random.seed(7)


# ---- stroke sampling --------------------------------------------------------
def resample(p0, p1, spacing):
    """Evenly spaced points from p0 to p1, both endpoints included."""
    p0 = np.array(p0, float)
    p1 = np.array(p1, float)
    length = float(np.hypot(*(p1 - p0)))
    n = max(1, int(round(length / spacing)))
    return [tuple(p0 + (p1 - p0) * (k / n)) for k in range(n + 1)]


def build_one_local():
    """A '1': vertical bar + top-left flag + base. Returns (points, edges, hub)."""
    pts, edges = [], []

    bar = resample((0.0, H / 2), (0.0, -H / 2), SPACING)   # top -> bottom
    b0 = len(pts)
    pts += bar
    edges += [(b0 + k, b0 + k + 1) for k in range(len(bar) - 1)]
    bar_top, bar_bot = b0, b0 + len(bar) - 1

    flag = resample((-0.62, H / 2 - 0.72), (0.0, H / 2), SPACING)[:-1]  # drop shared top
    f0 = len(pts)
    pts += flag
    edges += [(f0 + k, f0 + k + 1) for k in range(len(flag) - 1)]
    if flag:
        edges.append((f0 + len(flag) - 1, bar_top))       # join flag -> bar top

    base = resample((-0.72, -H / 2), (0.72, -H / 2), SPACING)
    g0 = len(pts)
    pts += base
    edges += [(g0 + k, g0 + k + 1) for k in range(len(base) - 1)]
    arr = np.array(base)
    near = g0 + int(np.argmin(np.hypot(arr[:, 0], arr[:, 1] + H / 2)))
    if near != bar_bot:
        edges.append((near, bar_bot))                     # join base -> bar bottom

    hub = bar_top + len(bar) // 2                          # hub at the bar's middle
    return pts, edges, hub


# ---- assemble the two "1" subgraphs into global arrays ----------------------
ANCHOR, EDGES, COLOR, IS_HUB = [], [], [], []
_type_i = 0
for di, cx in enumerate(DIGIT_CX):
    if di == 1:
        continue                       # middle slot is the OpenOrbis logo
    pts, edges, hub = build_one_local()
    off = len(ANCHOR)
    for j, (x, y) in enumerate(pts):
        ANCHOR.append((x + cx, y + CY))
        if j == hub:
            IS_HUB.append(True)
            COLOR.append(PERSON_MID)
        else:
            IS_HUB.append(False)
            COLOR.append(TYPE_COLORS[_type_i % len(TYPE_COLORS)])
            _type_i += 1
    EDGES += [(a + off, b + off) for (a, b) in edges]

ANCHOR = np.array(ANCHOR)
N = len(ANCHOR)

# per-node jitter (integer cycles -> seamless loop); small amp keeps the shape
FREQ_X = np.random.choice([1.0, 1.0, 2.0], N)
FREQ_Y = np.random.choice([1.0, 2.0, 2.0], N)
PH_X = np.random.rand(N)
PH_Y = np.random.rand(N)
AMP = 0.05 + 0.05 * np.random.rand(N)
GLOW_PH = np.random.rand(N) * 2 * np.pi

# ---- background particles ---------------------------------------------------
NP = 220
P_BASE = np.random.rand(NP, 2) * LIM
P_DRIFT = 0.06 + 0.20 * np.random.rand(NP)
P_PH = np.random.rand(NP) * 2 * np.pi
P_FREQ = np.random.choice([1.0, 1.0, 2.0], NP)
P_SIZE = 2.0 + 7.0 * np.random.rand(NP)
P_RGB = np.array([mcolors.to_rgb(PART_COLORS[i % len(PART_COLORS)]) for i in range(NP)])


# ---- faint shooting stars (gentle background motion, behind the graph) ------
def _star(x, y, ang, dist, t0, dur, trail, peak, color):
    return dict(p0=np.array([x, y]), ang=ang,
                vec=dist * np.array([np.cos(ang), np.sin(ang)]),
                t0=t0, dur=dur, trail=trail, peak=peak, color=color)


# all enter from the LEFT and streak to the RIGHT (slight descent); staggered
# t0 so usually only one is on screen at a time; low peak = unobtrusive
STARS = [
    _star(-0.4, 11.0, -0.46, 8.5, 0.06, 0.22, 2.0, 0.42, "#dbeafe"),  # top band
    _star(-0.6, 8.4, -0.38, 8.0, 0.42, 0.20, 1.8, 0.38, "#ffffff"),   # upper-mid
    _star(0.2, 5.6, -0.30, 7.0, 0.72, 0.22, 1.6, 0.30, "#e9d5ff"),    # mid band
]


# ---- smooth radial-gradient glow stamp --------------------------------------
_S = 150
_gy, _gx = np.mgrid[-1:1:_S * 1j, -1:1:_S * 1j]
_rr = np.sqrt(_gx ** 2 + _gy ** 2)
_FALLOFF = np.clip(np.exp(-(_rr * 2.35) ** 2) - np.exp(-(2.35) ** 2), 0, None)
_FALLOFF /= _FALLOFF.max()


def glow(ax, xy, radius, color, intensity, zorder=3):
    rgb = mcolors.to_rgb(color)
    img = np.empty((_S, _S, 4))
    img[..., 0], img[..., 1], img[..., 2] = rgb
    img[..., 3] = np.clip(_FALLOFF * intensity, 0, 1)
    ax.imshow(img, extent=[xy[0] - radius, xy[0] + radius,
                           xy[1] - radius, xy[1] + radius],
              origin="lower", zorder=zorder, interpolation="bilinear",
              aspect="auto")


def shooting_star(ax, head, ang, trail_len, alpha, color):
    """A faint streak: tapered fading trail + soft head, drawn behind the graph."""
    if alpha <= 0.01:
        return
    dx, dy = np.cos(ang), np.sin(ang)
    nseg = 7
    for k in range(nseg):
        f0, f1 = k / nseg, (k + 1) / nseg
        x0, y0 = head[0] - dx * trail_len * f1, head[1] - dy * trail_len * f1
        x1, y1 = head[0] - dx * trail_len * f0, head[1] - dy * trail_len * f0
        ax.plot([x0, x1], [y0, y1], color=color, lw=0.5 + 1.7 * (1 - f0),
                alpha=alpha * (1 - f0) ** 1.6, solid_capstyle="round", zorder=1)
    glow(ax, head, 0.40, color, 0.5 * alpha, zorder=1)
    ax.add_patch(Circle(head, 0.048, fc=WHITE, ec="none", alpha=alpha, zorder=1.5))


def reg_node(ax, xy, color, inten):
    """open-orbis regular node: colored glow halo + colored body + white core."""
    glow(ax, xy, 0.52, color, 0.18 * inten, zorder=4)
    ax.add_patch(Circle(xy, 0.15, fc=color, ec="none",
                        alpha=min(1.0, 0.85 * inten + 0.12), zorder=6))
    ax.add_patch(Circle(xy, 0.062, fc=WHITE, ec="none",
                        alpha=0.85 * inten, zorder=7))


def hub_node(ax, xy, inten, t):
    """open-orbis 'person' hub: concentric purple discs + a rotating orbital ring."""
    glow(ax, xy, 0.95, PERSON_CORE, 0.24 * inten, zorder=4)
    ang = np.degrees(2 * np.pi * t)                        # one rotation per loop
    ax.add_patch(Ellipse(xy, 1.10, 0.42, angle=ang, fill=False,
                         ec=PERSON_RING, lw=1.1, alpha=0.34 * inten, zorder=5))
    ax.add_patch(Circle(xy, 0.34, fc=PERSON_CORE, ec="none",
                        alpha=0.35 * inten, zorder=6))
    ax.add_patch(Circle(xy, 0.20, fc=PERSON_MID, ec="none",
                        alpha=0.95 * inten, zorder=7))
    ax.add_patch(Circle(xy, 0.092, fc=PERSON_DOT, ec="none",
                        alpha=min(1.0, inten), zorder=8))


def draw_logo(ax, t):
    """The OpenOrbis mark in the middle slot: translucent disc + core orb,
    gently breathing + drifting, with one faint rotating orbital ring."""
    s = 1.0 + 0.05 * np.sin(2 * np.pi * t)                 # breathing scale
    c = (LOGO_CX + 0.07 * np.cos(2 * np.pi * t),           # tiny circular drift
         LOGO_CY + 0.07 * np.sin(2 * np.pi * t))
    pulse = 0.5 + 0.5 * np.sin(2 * np.pi * t)

    glow(ax, c, LOGO_R * 1.20 * s, LOGO_FILL, 0.22 + 0.08 * pulse, zorder=4)
    ang = np.degrees(2 * np.pi * t)                        # slow orbital ring
    ax.add_patch(Ellipse(c, LOGO_R * 2.05 * s, LOGO_R * 0.80 * s, angle=ang,
                         fill=False, ec=PERSON_RING, lw=1.2, alpha=0.22, zorder=5))
    ax.add_patch(Circle(c, LOGO_R * s, fc=LOGO_FILL, ec="none",
                        alpha=0.32, zorder=6))             # outer disc
    ax.add_patch(Circle(c, LOGO_R * s, fc="none", ec=LOGO_STROKE,
                        lw=2.0, alpha=0.45, zorder=7))     # outer stroke
    glow(ax, c, LOGO_CORE_R * 2.0 * s, LOGO_CORE, 0.42, zorder=7)
    ax.add_patch(Circle(c, LOGO_CORE_R * s, fc=LOGO_CORE, ec="none",
                        alpha=0.97, zorder=8))             # core orb
    ax.add_patch(Circle(c, LOGO_CORE_R * 0.42 * s, fc=LOGO_HI, ec="none",
                        alpha=0.80, zorder=9))             # core highlight


def positions(t):
    """Anchor + small periodic jitter -> nodes move but the digits hold."""
    dx = AMP * np.sin(2 * np.pi * (FREQ_X * t + PH_X))
    dy = AMP * np.sin(2 * np.pi * (FREQ_Y * t + PH_Y))
    return ANCHOR + np.stack([dx, dy], axis=1)


def draw(frame):
    ax.clear()
    ax.set_xlim(0, LIM)
    ax.set_ylim(0, LIM)
    ax.axis("off")
    ax.set_facecolor(BG)

    t = frame / N_FRAMES
    pulse = 0.5 + 0.5 * np.sin(2 * np.pi * t)

    # ---- drifting background particles ----
    px = P_BASE[:, 0] + P_DRIFT * np.cos(2 * np.pi * P_FREQ * t + P_PH)
    py = P_BASE[:, 1] + P_DRIFT * np.sin(2 * np.pi * P_FREQ * t + P_PH)
    tw = np.clip(0.16 + 0.10 * np.sin(2 * np.pi * t + P_PH), 0, 0.32)
    ax.scatter(px, py, s=P_SIZE, c=np.concatenate([P_RGB, tw[:, None]], axis=1),
               edgecolors="none", zorder=1)

    # ---- faint shooting stars (behind the graph) ----
    for st in STARS:
        local = (t - st["t0"]) % 1.0
        if local < st["dur"]:
            p = local / st["dur"]
            shooting_star(ax, st["p0"] + st["vec"] * p, st["ang"],
                          st["trail"], np.sin(np.pi * p) * st["peak"], st["color"])

    pos = positions(t)

    # ---- curved links: faint white core + source-tinted under-glow ----
    for a, b in EDGES:
        pa, pb = pos[a], pos[b]
        ax.add_patch(FancyArrowPatch(
            pa, pb, arrowstyle="-", color=COLOR[a],
            alpha=0.13 * (0.7 + 0.3 * pulse), lw=3.0, zorder=2,
            connectionstyle="arc3,rad=0.15"))
        ax.add_patch(FancyArrowPatch(
            pa, pb, arrowstyle="-", color=WHITE, alpha=0.20, lw=1.0, zorder=3,
            connectionstyle="arc3,rad=0.15"))

    # ---- nodes ----
    for i in range(N):
        inten = 0.78 + 0.22 * np.sin(2 * np.pi * t + GLOW_PH[i])
        if IS_HUB[i]:
            hub_node(ax, pos[i], inten, t)
        else:
            reg_node(ax, pos[i], COLOR[i], inten)

    # ---- the OpenOrbis logo in the middle slot (a gently breathing orb) ----
    draw_logo(ax, t)


fig, ax = plt.subplots(figsize=(6, 6), dpi=140)
fig.patch.set_facecolor(BG)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

anim = FuncAnimation(fig, draw, frames=N_FRAMES, interval=1000 // FPS)
anim.save("orbis_101.gif", writer=PillowWriter(fps=FPS))

draw(N_FRAMES // 2)
fig.savefig("preview.png", facecolor=BG)
print("wrote orbis_101.gif and preview.png")
