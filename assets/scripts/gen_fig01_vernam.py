"""Figura do Cap01 / Aula 1: cifra de Vernam (cifragem e decifragem por XOR).

Uso: python gen_fig01_vernam.py <pasta_saida> [pt|en]
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
FS = 17

out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
LANG = sys.argv[2] if len(sys.argv) > 2 else "pt"

T = {
    "pt": dict(enc="Cifragem", dec="Decifragem", gen="Gerador de fluxo\nde chave",
               seq="(sequência aleatória)", plain="Texto\nclaro $p_i$",
               cipher="Texto\ncifrado $c_i$", file="fig-01-vernam-gerador.png", bw=2.9,
               note="O texto claro não é \"cifrado\" por nenhum algoritmo: é apenas combinado bit a bit\n"
                    "com a chave por XOR ($\\oplus$). Toda a segurança está na imprevisibilidade da chave."),
    "en": dict(enc="Encryption", dec="Decryption", gen="Keystream\ngenerator",
               seq="(random sequence)", plain="Plaintext\n$p_i$",
               cipher="Ciphertext\n$c_i$", file="fig-01-vernam-gerador-en.png", bw=3.7,
               note="The plaintext is not \"encrypted\" by any algorithm: it is simply combined bit by bit\n"
                    "with the key via XOR ($\\oplus$). All the security lies in the unpredictability of the key."),
}[LANG]


def box(ax, cx, cy, w, h, text, dark=False, fill="white", fs=FS):
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h,
                           facecolor=DARK if dark else fill,
                           edgecolor=DARK if dark else RED, lw=2.4, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            color="white" if dark else DARK, fontweight="bold", zorder=3)


def arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=DARK, lw=2.4,
                                mutation_scale=20, shrinkA=0, shrinkB=0),
                zorder=1)


def panel(ax, cx, title, left_text, right_text):
    ax.text(cx, 8.2, title, ha="center", va="center", fontsize=FS + 4,
            fontweight="bold", color=DARK)
    box(ax, cx, 6.6, 5.0, 1.6, T["gen"], dark=True)
    xy, r = 3.0, 0.5
    arrow(ax, cx, 5.8, cx, xy + r)
    ax.text(cx + 0.35, 4.75, r"$k_i$  " + T["seq"], ha="left",
            va="center", fontsize=FS - 1, color=RED, style="italic")
    ax.add_patch(Circle((cx, xy), r, facecolor="white", edgecolor=DARK,
                        lw=2.6, zorder=2))
    ax.plot([cx - r * 0.7, cx + r * 0.7], [xy, xy], color=DARK, lw=2.6, zorder=3)
    ax.plot([cx, cx], [xy - r * 0.7, xy + r * 0.7], color=DARK, lw=2.6, zorder=3)
    bw, bh, gap = T["bw"], 1.5, 0.9
    box(ax, cx - r - gap - bw / 2, xy, bw, bh, left_text, fill=PINK)
    box(ax, cx + r + gap + bw / 2, xy, bw, bh, right_text, fill=PINK)
    arrow(ax, cx - r - gap, xy, cx - r, xy)
    arrow(ax, cx + r, xy, cx + r + gap, xy)


fig, ax = plt.subplots(figsize=(13, 5.6), dpi=200)
ax.set_xlim(-0.5 - T["bw"] - 1.4, 12.5 + T["bw"] + 1.4)
ax.set_ylim(0.2, 9.0)
ax.set_aspect("equal")
ax.axis("off")

panel(ax, 0.0, T["enc"], T["plain"], T["cipher"])
panel(ax, 12.0, T["dec"], T["cipher"], T["plain"])

ax.text(6.0, 0.9, T["note"], ha="center", va="center", fontsize=FS - 1,
        color=DARK, style="italic")

fig.savefig(out / T["file"], bbox_inches="tight", pad_inches=0.1)
plt.close(fig)
