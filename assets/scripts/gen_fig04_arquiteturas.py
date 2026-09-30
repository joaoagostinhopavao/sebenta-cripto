"""Figuras do Cap04: cifra de fluxo com estado e cifra de fluxo por contador.

Uso: python gen_fig04_arquiteturas.py <pasta_saida>
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

DARK = "#1c0707"
RED = "#b0202a"
PINK = "#f9e4e4"
FS = 14

out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")


def box(ax, cx, cy, w, h, text, dark=False, fill="white", fs=FS, bold=False):
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h,
                           facecolor=DARK if dark else fill,
                           edgecolor=DARK if dark else RED, lw=2.2, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            color="white" if dark else DARK,
            fontweight="bold" if bold else "normal", zorder=3)


def arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=DARK, lw=2.2,
                                mutation_scale=18, shrinkA=0, shrinkB=0),
                zorder=1)


def xor_column(ax, cx, idx, top_y):
    """Seta de top_y para o XOR, P_i à esquerda, C_i em baixo."""
    xy, r = 2.6, 0.38
    arrow(ax, cx, top_y, cx, xy + r)
    ax.add_patch(Circle((cx, xy), r, facecolor="white", edgecolor=DARK, lw=2.4, zorder=2))
    ax.plot([cx - r * 0.7, cx + r * 0.7], [xy, xy], color=DARK, lw=2.4, zorder=3)
    ax.plot([cx, cx], [xy - r * 0.7, xy + r * 0.7], color=DARK, lw=2.4, zorder=3)
    box(ax, cx - 1.75, xy, 1.3, 0.95, f"$P_{idx}$", fill=PINK)
    arrow(ax, cx - 1.1, xy, cx - r, xy)
    arrow(ax, cx, xy - r, cx, 1.25)
    box(ax, cx, 0.85, 1.3, 0.8, f"$C_{idx}$", fill=PINK)


def new_ax():
    fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=200)
    ax.set_xlim(0, 20)
    ax.set_ylim(0.2, 8.4)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


# --- Cifra com estado: K e N entram no Init; Updates encadeados ---
fig, ax = new_ax()
uy, uh, uw = 5.3, 1.5, 3.0
init_cx = 3.2
box(ax, init_cx, uy, uw, uh, "Init", dark=True, bold=True, fs=FS + 2)
for cx, lab in ((init_cx - 0.75, "$K$"), (init_cx + 0.75, "$N$")):
    box(ax, cx, 7.6, 1.1, 0.8, lab)
    arrow(ax, cx, 7.2, cx, uy + uh / 2)
ups = (8.2, 12.8, 17.4)
prev_right = init_cx + uw / 2
for i, cx in enumerate(ups, start=1):
    arrow(ax, prev_right, uy, cx - uw / 2, uy)
    box(ax, cx, uy, uw, uh, "Update", dark=True, bold=True)
    xor_column(ax, cx, i, uy - uh / 2)
    prev_right = cx + uw / 2
fig.savefig(out / "fig-04-cifra-fluxo-stateful.png", bbox_inches="tight", pad_inches=0.1)
plt.close(fig)

# --- Cifra por contador: cada bloco a partir de K, N, Ctr+i ---
fig, ax = new_ax()
labels = ("$K, N,$ Ctr", "$K, N,$ Ctr+1", "$K, N,$ Ctr+2")
for i, (cx, lab) in enumerate(zip((3.6, 10.0, 16.4), labels), start=1):
    ax.text(cx, 7.6, lab, ha="center", va="center", fontsize=FS, color=RED)
    arrow(ax, cx, 7.2, cx, uy + uh / 2)
    box(ax, cx, uy, uw, uh, "SC", dark=True, bold=True, fs=FS + 2)
    xor_column(ax, cx, i, uy - uh / 2)
fig.savefig(out / "fig-04-cifra-fluxo-contador.png", bbox_inches="tight", pad_inches=0.1)
plt.close(fig)
print("ok")
