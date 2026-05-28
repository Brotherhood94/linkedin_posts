"""
make_gif.py — "Researcher + AI co-pilot" loop for the F**K, Research post.

Renders a square, dark, purple/cyan animation:
  - a single RESEARCHER node on the left,
  - a fan of AI AGENT nodes on the right (Writer / Coder / Reviewer / Critic),
  - a central IDEA -> DRAFT -> REVIEW -> REFINE loop with a glowing token
    travelling clockwise and the active stage lighting up,
  - pulsing connectors between the human and the agents.

Outputs:
  research_copilot.gif   (the media to upload)
  preview.png            (one representative frame, for visual QA)
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
from matplotlib.animation import FuncAnimation, PillowWriter

# ---- palette ---------------------------------------------------------------
BG = "#0E1117"
CYAN = "#22D3EE"     # the human / researcher
PURPLE = "#A855F7"   # the AI agents
GOLD = "#FBBF24"     # the active stage / token
WHITE = "#F5F5F7"
MUTED = "#8B93A7"
DIM = "#2A3344"

# ---- geometry --------------------------------------------------------------
CX, CY, R = 5.0, 5.05, 1.55                       # central loop
RES = (1.95, 5.05)                                # researcher node center
AGENTS = [("Writer", 3.05), ("Coder", 4.45),
          ("Reviewer", 5.85), ("Critic", 7.25)]   # right-hand fan (label, y)
AGENT_X = 8.25

# stages placed at left/top/right/bottom; token travels clockwise through them
STAGES = [("IDEA", 180.0), ("DRAFT", 90.0), ("REVIEW", 0.0), ("REFINE", 270.0)]

N_FRAMES = 64
FPS = 18


def _pol(angle_deg, r=R):
    a = np.deg2rad(angle_deg)
    return CX + r * np.cos(a), CY + r * np.sin(a)


def _chip(ax, x, y, label, active):
    fill = GOLD if active else DIM
    edge = GOLD if active else "#3B475C"
    txt = "#1A1205" if active else MUTED
    w, h = 1.34, 0.62
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.18",
                                fc=fill, ec=edge, lw=2.0, zorder=5,
                                alpha=1.0 if active else 0.9))
    ax.text(x, y, label, ha="center", va="center", color=txt,
            fontsize=12.5, fontweight="bold", zorder=6,
            family="DejaVu Sans")


def _glow_dot(ax, x, y, color, base=170):
    for r, a in [(0.42, 0.10), (0.30, 0.18), (0.20, 0.35)]:
        ax.add_patch(Circle((x, y), r, fc=color, ec="none", alpha=a, zorder=7))
    ax.add_patch(Circle((x, y), 0.11, fc=WHITE, ec=color, lw=2, zorder=8))


def update(frame):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    t = frame / N_FRAMES
    active = int(t * 4) % 4
    pulse = 0.30 + 0.50 * (0.5 + 0.5 * np.sin(2 * np.pi * t * 2))

    # --- headline + footer ---
    ax.text(5.0, 9.35, "ONE RESEARCHER,  A TEAM OF AGENTS",
            ha="center", va="center", color=WHITE, fontsize=18,
            fontweight="bold", family="DejaVu Sans")
    ax.text(5.0, 0.62, "The bar just dropped.   The vision is still yours.",
            ha="center", va="center", color=MUTED, fontsize=12.5,
            fontstyle="italic", family="DejaVu Sans")

    # --- faint ring of the loop ---
    ring = plt.Circle((CX, CY), R, fill=False, ec="#33415A", lw=2.0,
                      ls=(0, (1, 2)), zorder=1)
    ax.add_patch(ring)

    # --- connectors: researcher -> loop -> agents (pulsing) ---
    lx, _ = _pol(180.0)
    ax.add_patch(FancyArrowPatch((RES[0] + 0.82, RES[1]), (lx - 0.12, CY),
                                 arrowstyle="-|>", mutation_scale=16,
                                 color=CYAN, lw=2.4, alpha=pulse, zorder=2))
    rx, _ = _pol(0.0)
    for label, ay in AGENTS:
        ax.add_patch(FancyArrowPatch((rx + 0.12, CY), (AGENT_X - 0.55, ay),
                                     arrowstyle="-|>", mutation_scale=12,
                                     color=PURPLE, lw=1.8,
                                     alpha=0.25 + 0.45 * pulse,
                                     connectionstyle="arc3,rad=0.12", zorder=2))

    # --- the four stage chips ---
    for i, (label, ang) in enumerate(STAGES):
        x, y = _pol(ang)
        _chip(ax, x, y, label, active == i)

    # --- travelling token (clockwise from the left) ---
    theta = 180.0 - 360.0 * t
    tx, ty = _pol(theta)
    _glow_dot(ax, tx, ty, GOLD)

    # --- researcher node ---
    for r, a in [(1.02, 0.10), (0.90, 0.16)]:
        ax.add_patch(Circle(RES, r, fc=CYAN, ec="none", alpha=a, zorder=3))
    ax.add_patch(Circle(RES, 0.78, fc="#0B2A33", ec=CYAN, lw=3, zorder=4))
    ax.text(RES[0], RES[1] + 0.06, "YOU", ha="center", va="center",
            color=CYAN, fontsize=15, fontweight="bold", family="DejaVu Sans",
            zorder=9)
    ax.text(RES[0], RES[1] - 1.18, "researcher", ha="center", va="center",
            color=MUTED, fontsize=11, family="DejaVu Sans", zorder=9)

    # --- agent nodes ---
    ax.text(AGENT_X + 0.35, 8.25, "AI agents", ha="center", va="center",
            color=PURPLE, fontsize=12, fontweight="bold", family="DejaVu Sans")
    for label, ay in AGENTS:
        ax.add_patch(Circle((AGENT_X, ay), 0.30, fc="#241036", ec=PURPLE,
                            lw=2.4, zorder=4))
        ax.add_patch(Circle((AGENT_X, ay), 0.12, fc=PURPLE, ec="none",
                            alpha=0.9, zorder=5))
        ax.text(AGENT_X + 0.55, ay, label, ha="left", va="center",
                color=WHITE, fontsize=11.5, family="DejaVu Sans")

    return []


fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

anim = FuncAnimation(fig, update, frames=N_FRAMES, interval=1000 / FPS,
                     blit=False)
anim.save("research_copilot.gif", writer=PillowWriter(fps=FPS))

# one representative frame (DRAFT active) for visual QA
update(int(N_FRAMES * 0.30))
fig.savefig("preview.png", facecolor=BG, dpi=100)
print("wrote research_copilot.gif and preview.png")
