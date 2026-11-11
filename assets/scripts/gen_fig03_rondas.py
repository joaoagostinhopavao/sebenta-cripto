"""Figura do Cap03 / Aula 3: estrutura completa do AES (ronda inicial, rondas, ronda final).

Substitui a figura do deck fonte (que tinha "Encripted Text" e setas "Derivates"
a sugerir que o AddRoundKey inicial usava a 1.ª subchave expandida): o
AddRoundKey inicial usa a própria chave, K0 = w0..w3.

Uso: python gen_fig03_rondas.py <pasta_saida> [pt|en]
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

DARK = "#1c0707"
RED = "#b0202a"
PINK = "#f9e4e4"
GREY = "#f2f2f2"

out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
LANG = sys.argv[2] if len(sys.argv) > 2 else "pt"

T = {
    "pt": dict(pt="Texto claro\n(16 bytes)", key="Chave (16, 24 ou 32 bytes)", exp="Expansão da chave",
               ark="AddRoundKey", sub="SubBytes", shift="ShiftRows", mix="MixColumns",
               rnd="Ronda (repetida $N_r - 1$ vezes)", fin="Ronda final (sem MixColumns)",
               ct="Texto cifrado\n(16 bytes)", nr="$N_r$ = 10, 12, 14\npara chaves de\n128/192/256 bits",
               k0="$K_0$", ki="$K_i$", kn="$K_{N_r}$", file="fig-03-aes-rondas-estrutura.png"),
    "en": dict(pt="Plaintext\n(16 bytes)", key="Key (16, 24 or 32 bytes)", exp="Key expansion",
               ark="AddRoundKey", sub="SubBytes", shift="ShiftRows", mix="MixColumns",
               rnd="Round (repeated $N_r - 1$ times)", fin="Final round (no MixColumns)",
               ct="Ciphertext\n(16 bytes)", nr="$N_r$ = 10, 12, 14\nfor 128/192/256-bit\nkeys",
               k0="$K_0$", ki="$K_i$", kn="$K_{N_r}$", file="fig-03-aes-rondas-estrutura-en.png"),
}[LANG]

fig, ax = plt.subplots(figsize=(7.4, 7.6), dpi=200)
ax.set_xlim(0, 12.6)
ax.set_ylim(-0.4, 13.4)
ax.set_aspect("equal")
ax.axis("off")

CX, BW, BH = 3.4, 3.8, 0.78      # coluna principal
KX = 8.2                          # coluna da chave


def box(cx, cy, text, w=BW, h=BH, fill="white", edge=DARK, fs=13, bold=False, dark=False):
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, facecolor=DARK if dark else fill,
                           edgecolor=DARK if dark else edge, lw=2, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color="white" if dark else DARK,
            fontweight="bold" if bold else "normal", zorder=4, linespacing=1.15)


def arrow(x0, y0, x1, y1, color=DARK):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2, mutation_scale=16,
                                shrinkA=0, shrinkB=0), zorder=2)


def group(cy_top, cy_bot, label):
    ax.add_patch(FancyBboxPatch((CX - BW / 2 - 0.5, cy_bot), BW + 1.0, cy_top - cy_bot,
                                boxstyle="round,pad=0,rounding_size=0.25", facecolor=GREY,
                                edgecolor=RED, lw=2, zorder=1))
    ax.text(CX, cy_top - 0.3, label, ha="center", va="center", fontsize=10.5, color=RED,
            fontweight="bold")


# --- coluna principal ---
y_pt, y_ark0 = 12.55, 11.0
box(CX, y_pt, T["pt"], fill=PINK, edge=RED, h=1.0)
arrow(CX, y_pt - 0.5, CX, y_ark0 + BH / 2)
box(CX, y_ark0, T["ark"], dark=True, bold=True)

# ronda intermédia
r_top, r_bot = 10.15, 5.7
group(r_top, r_bot, T["rnd"])
ys = [9.15, 8.2, 7.25, 6.3]
labels = [T["sub"], T["shift"], T["mix"] + "*", T["ark"]]
arrow(CX, y_ark0 - BH / 2, CX, r_top + 0.02)
for y, lab in zip(ys, labels):
    box(CX, y, lab, dark=(lab == T["ark"]), bold=(lab == T["ark"]))
for a, b in zip(ys[:-1], ys[1:]):
    arrow(CX, a - BH / 2, CX, b + BH / 2)

# ronda final
f_top, f_bot = 4.95, 1.65
group(f_top, f_bot, T["fin"])
fy = [4.0, 3.05, 2.1]
flabels = [T["sub"], T["shift"], T["ark"]]
arrow(CX, r_bot, CX, f_top + 0.02)
for y, lab in zip(fy, flabels):
    box(CX, y, lab, dark=(lab == T["ark"]), bold=(lab == T["ark"]))
for a, b in zip(fy[:-1], fy[1:]):
    arrow(CX, a - BH / 2, CX, b + BH / 2)
box(CX, 0.45, T["ct"], fill=PINK, edge=RED, h=0.95)
arrow(CX, f_bot, CX, 0.45 + 0.475)

# --- coluna da chave ---
box(KX, 12.55, T["key"], w=5.0, h=1.0, fs=10.5)
box(KX, 11.0, T["exp"], w=4.4, dark=True, bold=True, fs=11.5)
arrow(KX, 12.05, KX, 11.0 + BH / 2)
BUS = 7.15
ax.plot([KX, KX], [11.0 - BH / 2, 2.1], color=DARK, lw=2, zorder=2)
for y, lab in ((y_ark0, T["k0"]), (6.3, T["ki"]), (2.1, T["kn"])):
    x_from = KX - 2.2 if lab == T["k0"] else KX
    arrow(x_from, y, CX + BW / 2, y)
    if lab == T["k0"]:
        ax.text((x_from + CX + BW / 2) / 2, y + 0.18, lab, ha="center", va="bottom", fontsize=12, color=RED)
    else:
        ax.text((x_from + CX + BW / 2) / 2, y + 0.18, lab, ha="center", va="bottom", fontsize=12, color=RED)

ax.text(KX + 0.45, 4.1, T["nr"], ha="left", va="center", fontsize=11, style="italic", color=DARK)
ax.text(KX + 0.45, 8.0, "* " + ("só nas rondas\n  intermédias" if LANG == "pt" else "intermediate\n  rounds only"),
        ha="left", va="center", fontsize=10.5, color=DARK)

fig.savefig(out / T["file"], bbox_inches="tight", pad_inches=0.12)
plt.close(fig)
