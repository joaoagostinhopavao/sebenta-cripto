"""Figura da construção ChaCha20-Poly1305 (Cap04 / Aula 04), segundo o RFC 8439.

Gera:
  assets/images/fig-04-chacha20-poly1305.png
Com --en: rótulos em inglês, em en/assets/images/fig-04-chacha20-poly1305-en.png.

Correr a partir da raiz do projeto. A chave do Poly1305 (k_P) são os primeiros 32 bytes
do bloco 0 do ChaCha20; os blocos 1..m dão o fluxo de chave; a marca T cobre AAD e C
(o RFC acrescenta enchimento e os comprimentos de AAD e C, omitidos na figura).
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

DARK = "#1c0707"
CRIMSON = "#b0202a"
PINK = "#f9e4e4"
EN = "--en" in sys.argv
OUT = ("en/assets/images/fig-04-chacha20-poly1305-en.png" if EN
       else "assets/images/fig-04-chacha20-poly1305.png")
FS = 13


def t(pt, en):
    return en if EN else pt


def box(ax, x, y, w, h, text, fc="white", ec=CRIMSON, tc=DARK, bold=False, fs=FS):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=fc, ec=ec, lw=2.2, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", zorder=3, linespacing=1.3)


def dark(ax, x, y, w, h, text, fs=FS):
    box(ax, x, y, w, h, text, fc=DARK, ec=DARK, tc="white", bold=True, fs=fs)


def arrow(ax, x0, y0, x1, y1, label=None):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=DARK, lw=2.0,
                                mutation_scale=16, shrinkA=0, shrinkB=0), zorder=1)
    if label:
        ax.text((x0 + x1) / 2 + 0.15, (y0 + y1) / 2, label, fontsize=FS - 1,
                color=CRIMSON, ha="left", va="center", style="italic")


def line(ax, xs, ys, z=1, lw=2.0):
    ax.plot(xs, ys, color=DARK, lw=lw, zorder=z, solid_capstyle="butt")


fig, ax = plt.subplots(figsize=(9.6, 9.6), dpi=200)
ax.set_xlim(-0.8, 13.0)
ax.set_ylim(-0.1, 11.2)
ax.set_aspect("equal")
ax.axis("off")

XL, XR = 3.6, 9.0

# Entradas comuns
box(ax, 6.3, 10.6, 8.2, 0.9, t("Chave $K$ (256 bits)   ·   Nonce $N$ (96 bits)",
                              "Key $K$ (256 bits)   ·   Nonce $N$ (96 bits)"))
arrow(ax, XL, 10.15, XL, 9.35)
arrow(ax, XR, 10.15, XR, 9.35)

# ChaCha20
dark(ax, XL, 8.65, 4.0, 1.4, "ChaCha20$(K, N, 0)$")
dark(ax, XR, 8.65, 4.0, 1.4, "ChaCha20$(K, N, i)$\n$i$ = 1 … $m$")

# Bloco 0 -> k_P
arrow(ax, XL, 7.95, XL, 7.2, t("primeiros 32 bytes", "first 32 bytes"))
box(ax, XL, 6.6, 5.0, 1.2, t("$k_P$: chave do Poly1305\n(nova para cada mensagem)",
                             "$k_P$: Poly1305 key\n(new for each message)"))

# Blocos 1..m -> XOR -> C
xy, r = 6.6, 0.4
arrow(ax, XR, 7.95, XR, xy + r, t("fluxo de chave", "keystream"))
ax.add_patch(Circle((XR, xy), r, fc="white", ec=DARK, lw=2.4, zorder=2))
line(ax, [XR - r * 0.7, XR + r * 0.7], [xy, xy], z=3, lw=2.4)
line(ax, [XR, XR], [xy - r * 0.7, xy + r * 0.7], z=3, lw=2.4)
box(ax, 11.6, xy, 2.4, 1.0, t("Texto claro $P$", "Plaintext $P$"), fc=PINK)
arrow(ax, 10.4, xy, XR + r, xy)
arrow(ax, XR, xy - r, XR, 5.45)
box(ax, XR, 4.95, 4.4, 1.0, t("$C = P \\oplus$ fluxo de chave", "$C = P \\oplus$ keystream"), fc=PINK)

# AAD
box(ax, 0.55, 4.95, 2.1, 1.0, t("AAD\n(em claro)", "AAD\n(in clear)"), fc=PINK)

# Poly1305
yp = 3.4
dark(ax, XL, yp, 4.0, 1.0, "Poly1305")
arrow(ax, XL, 6.0, XL, yp + 0.5)                                         # k_P
line(ax, [0.55, 0.55], [4.45, yp]); arrow(ax, 0.55, yp, XL - 2.0, yp)    # AAD
line(ax, [XR, XR], [4.45, yp]); arrow(ax, XR, yp, XL + 2.0, yp)          # C

# Marca
arrow(ax, XL, yp - 0.5, XL, 2.35)
box(ax, XL, 1.85, 4.8, 1.0, "$T$ = Poly1305$(k_P,\\ $AAD ‖ $C)$\n128 bits", fc=PINK)

# Saída AEAD
yo = 0.45
dark(ax, 6.3, yo, 9.4, 0.9, t("Saída AEAD:   $C$ ‖ $T$", "AEAD output:   $C$ ‖ $T$"), fs=FS + 1)
arrow(ax, XL, 1.35, XL, yo + 0.45)
line(ax, [XR, XR], [yp, 1.6]); arrow(ax, XR, 1.6, XR, yo + 0.45)

fig.savefig(OUT, bbox_inches="tight", pad_inches=0.12)
print("ok", OUT)
