"""
make_gif.py — "CV -> Orbis" pipeline loop for the OpenOrbis post.

Renders a square, dark, purple/cyan animation:
  - a CV.pdf document node on the left,
  - an ontology-parse stage,
  - a central knowledge GRAPH (the Orbis) of connected nodes,
  - a fan of MCP AGENT nodes on the right (ChatGPT / Claude / Agent),
  - a glowing token streaming left -> right through the pipeline, lighting
    each stage as it passes, with pulsing query connectors between the
    agents and the graph.

Glows are rendered as smooth radial-gradient stamps (imshow) for a soft,
production-grade look rather than stacked flat circles.

Outputs:
  orbis.gif   (the media to upload)
  preview.png (one representative frame, for visual QA)
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch, Polygon
from matplotlib.animation import FuncAnimation, PillowWriter

# ---- palette ---------------------------------------------------------------
BG = "#0B0E14"
CYAN = "#22D3EE"     # the human side / the CV / the agents
PURPLE = "#A855F7"   # the graph (the Orbis)
GOLD = "#FBBF24"     # the streaming token / active stage
WHITE = "#F4F6FB"
MUTED = "#7E879B"
RAIL = "#222A3A"

# ---- geometry --------------------------------------------------------------
CY = 5.15                         # vertical center of the composition
PDF = (1.65, CY)
ONTO = (3.65, CY)
GRAPH = (6.0, CY)
GR = 1.02
AGENT_X = 7.85
AGENTS = [("ChatGPT", CY + 1.75), ("Claude", CY), ("Agent", CY - 1.75)]
STAGES_X = [PDF[0], ONTO[0], GRAPH[0], AGENT_X]

_ang = np.linspace(0, 2 * np.pi, 6, endpoint=False) + 0.5
GNODES = [(GRAPH[0], GRAPH[1])] + [
    (GRAPH[0] + GR * np.cos(a), GRAPH[1] + GR * np.sin(a)) for a in _ang
]
GEDGES = [(0, k) for k in range(1, 6)] + [(1, 3), (2, 5), (4, 6), (6, 1)]

N_FRAMES = 90
N_TOKENS = 3
SPEED = 1.4   # animation pulse speed

# ---- smooth radial-gradient glow stamp -------------------------------------
_S = 160
_gy, _gx = np.mgrid[-1:1:_S * 1j, -1:1:_S * 1j]
_rr = np.sqrt(_gx ** 2 + _gy ** 2)
_FALLOFF = np.clip(np.exp(-(_rr * 2.35) ** 2) - np.exp(-(2.35) ** 2), 0, None)
_FALLOFF /= _FALLOFF.max()


def glow(ax, xy, radius, color, intensity, zorder=3):
    """Stamp a soft radial gradient centered at xy."""
    rgb = mcolors.to_rgb(color)
    img = np.empty((_S, _S, 4))
    img[..., 0], img[..., 1], img[..., 2] = rgb
    img[..., 3] = np.clip(_FALLOFF * intensity, 0, 1)
    ax.imshow(img, extent=[xy[0] - radius, xy[0] + radius,
                           xy[1] - radius, xy[1] + radius],
              origin="lower", zorder=zorder, interpolation="bilinear",
              aspect="auto")


def node(ax, xy, core_r, color, intensity, glow_mult=4.2, ring=True, z=4):
    """A glowing core node: soft halo + crisp core + faint ring."""
    glow(ax, xy, core_r * glow_mult, color, 0.55 * intensity, zorder=z)
    if ring:
        ax.add_patch(Circle(xy, core_r * 1.7, fc="none", ec=color,
                            lw=1.0, alpha=0.30 * intensity, zorder=z + 1))
    ax.add_patch(Circle(xy, core_r, fc=color, ec="none",
                        alpha=min(1.0, 0.85 * intensity + 0.15), zorder=z + 2))
    ax.add_patch(Circle(xy, core_r * 0.45, fc=WHITE, ec="none",
                        alpha=0.55 * intensity, zorder=z + 3))


def draw(frame):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_facecolor(BG)

    t = frame / N_FRAMES
    ph = 2 * np.pi * (t * SPEED)
    token_xs = [STAGES_X[0] + ((t + k / N_TOKENS) % 1.0) * (STAGES_X[-1] - STAGES_X[0])
                for k in range(N_TOKENS)]

    def hot(sx):
        return max(0.0, 1.0 - min(abs(tx - sx) for tx in token_xs) / 0.65)

    # ---- pipeline rail (PDF -> ontology -> graph) ----
    glow(ax, ((PDF[0] + GRAPH[0]) / 2, CY), 0.0, RAIL, 0)  # no-op safety
    ax.plot([PDF[0], GRAPH[0] - GR * 0.7], [CY, CY], color=RAIL, lw=2.2,
            solid_capstyle="round", zorder=1)

    # ---- CV.pdf document ----
    h = hot(PDF[0])
    col = GOLD if h > 0.45 else CYAN
    glow(ax, PDF, 1.5, col, 0.30 + 0.45 * h, zorder=2)
    ax.add_patch(FancyBboxPatch((PDF[0] - 0.40, PDF[1] - 0.58), 0.80, 1.16,
                                boxstyle="round,pad=0.02,rounding_size=0.10",
                                fc="#10151F", ec=col, lw=2.0 + 1.6 * h, zorder=5))
    ax.add_patch(Polygon([(PDF[0] + 0.40, PDF[1] + 0.58),
                          (PDF[0] + 0.18, PDF[1] + 0.58),
                          (PDF[0] + 0.40, PDF[1] + 0.34)],
                         closed=True, fc=BG, ec=col, lw=1.4, zorder=6))
    for j, yy in enumerate(np.linspace(PDF[1] + 0.26, PDF[1] - 0.34, 4)):
        x1 = PDF[0] - 0.24
        x2 = PDF[0] + (0.22 if j else 0.0)
        ax.plot([x1, x2], [yy, yy], color=MUTED, lw=1.5,
                solid_capstyle="round", zorder=7)
    ax.text(PDF[0], PDF[1] - 0.92, "CV.pdf", color=WHITE, ha="center",
            va="top", fontsize=12.5, fontweight="bold")

    # ---- ontology parse stage (a focusing ring) ----
    h = hot(ONTO[0])
    col = GOLD if h > 0.45 else CYAN
    glow(ax, ONTO, 0.95, col, 0.28 + 0.55 * h, zorder=2)
    for rr, aa in ((0.42, 0.35), (0.30, 0.55), (0.18, 0.85)):
        ax.add_patch(Circle(ONTO, rr, fc="none", ec=col,
                            lw=1.6, alpha=aa * (0.6 + 0.4 * h), zorder=5))
    ax.text(ONTO[0], ONTO[1] - 0.78, "ontology", color=MUTED, ha="center",
            va="top", fontsize=10.5, style="italic")

    # ---- knowledge graph (the Orbis) ----
    pulse = 0.5 + 0.5 * np.sin(ph)
    ghot = hot(GRAPH[0])
    for a, b in GEDGES:
        xa, ya = GNODES[a]
        xb, yb = GNODES[b]
        ax.plot([xa, xb], [ya, yb], color=PURPLE,
                alpha=0.45 + 0.35 * pulse, lw=3.2,
                solid_capstyle="round", zorder=2)          # soft edge glow
        ax.plot([xa, xb], [ya, yb], color="#D8B4FE",
                alpha=0.55 + 0.30 * pulse, lw=1.2,
                solid_capstyle="round", zorder=3)          # bright core line
    for idx, gxy in enumerate(GNODES):
        a = 0.75 + 0.25 * np.sin(ph + idx * 0.9)
        if idx == 0:
            node(ax, gxy, 0.20, PURPLE, min(1.0, a + 0.25 * ghot), glow_mult=5.0)
        else:
            node(ax, gxy, 0.115, PURPLE, min(1.0, a + 0.20 * ghot), glow_mult=4.0)
    ax.text(GRAPH[0], GRAPH[1] - GR - 0.42, "your Orbis", color=WHITE,
            ha="center", va="top", fontsize=12.5, fontweight="bold")

    # ---- MCP agents + pulsing query connectors ----
    for ai, (name, ay) in enumerate(AGENTS):
        qp = 0.5 + 0.5 * np.sin(ph - ai * 0.9)
        for lw, al in ((3.4, 0.18), (1.3, 0.45)):
            ax.add_patch(FancyArrowPatch(
                (AGENT_X - 0.42, ay), (GRAPH[0] + GR * 0.82, CY),
                arrowstyle="-", color=CYAN, alpha=al * (0.4 + 0.6 * qp),
                lw=lw * (0.6 + 0.6 * qp), zorder=2,
                connectionstyle="arc3,rad=0.14"))
        ah = hot(AGENT_X) if abs(ay - CY) < 0.1 else 0.0
        node(ax, (AGENT_X, ay), 0.205, GOLD if ah > 0.45 else CYAN,
             0.75 + 0.25 * qp, glow_mult=4.4)
        ax.text(AGENT_X + 0.40, ay, name, color=WHITE, ha="left",
                va="center", fontsize=10.5)

    # ---- streaming tokens ----
    for tx in token_xs:
        glow(ax, (tx, CY), 0.62, GOLD, 0.9, zorder=8)
        ax.add_patch(Circle((tx, CY), 0.075, fc=WHITE, ec=GOLD,
                            lw=1.4, zorder=9))


fig, ax = plt.subplots(figsize=(6, 6), dpi=140)
fig.patch.set_facecolor(BG)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

anim = FuncAnimation(fig, draw, frames=N_FRAMES, interval=50)
anim.save("orbis.gif", writer=PillowWriter(fps=20))

draw(int(N_FRAMES * 0.60))   # token inside the graph zone
fig.savefig("preview.png", facecolor=BG)
print("wrote orbis.gif and preview.png")
