"""Figura do Cap02 / Aula 2: duas permutações dos 16 valores hexadecimais.

Reproduz a figura fig-02-permutacoes-16.png (PT) com os rótulos em inglês.
Cada linha liga o valor v da fila de entrada à caixa com o mesmo valor v da
permutação (azul: A, +5; vermelho: B, livre), como na figura original.

Uso: python gen_fig02_permutacoes.py <pasta_saida>
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

HEX = "0123456789ABCDEF"
PERM_A = [HEX[(i + 5) % 16] for i in range(16)]
PERM_B = list("5D29" + "0B7E" + "3F18" + "64AC")
assert sorted(PERM_B) == sorted(HEX)

BLUE_FILL, BLUE_EDGE = "#dae8fc", "#6c8ebf"
RED_FILL, RED_EDGE = "#f8cecc", "#b85450"
DARK = "#1c0707"

W, H = 0.62, 0.62            # caixa
STEP = 0.78                  # passo horizontal
X0 = 2.9                     # x da 1.ª caixa
Y_IN, Y_A, Y_B = 6.0, 3.2, 0.4

fig, ax = plt.subplots(figsize=(9.6, 5.0), dpi=200)
ax.set_xlim(0, 15.6)
ax.set_ylim(-1.2, 7.0)
ax.set_aspect("equal")
ax.axis("off")


def cx(i):
    return X0 + i * STEP + W / 2


def row(y, labels, fill, edge):
    for i, lab in enumerate(labels):
        ax.add_patch(Rectangle((X0 + i * STEP, y), W, H, facecolor=fill,
                               edgecolor=edge, lw=1.2, zorder=3))
        ax.text(cx(i), y + H / 2, lab, ha="center", va="center", fontsize=11,
                color=DARK, zorder=4)


# linhas primeiro (por baixo das caixas)
for v in range(16):
    ch = HEX[v]
    ax.plot([cx(v), cx(PERM_A.index(ch))], [Y_IN, Y_A + H], color=BLUE_EDGE, lw=0.9, zorder=1)
    ax.plot([cx(v), cx(PERM_B.index(ch))], [Y_IN, Y_B + H], color=RED_EDGE, lw=0.9, zorder=1)

row(Y_IN, list(HEX), "white", DARK)
row(Y_A, PERM_A, BLUE_FILL, BLUE_EDGE)
row(Y_B, PERM_B, RED_FILL, RED_EDGE)

for y, txt in ((Y_IN, "Input"), (Y_A, "Permutation A"), (Y_B, "Permutation B")):
    ax.text(X0 - 0.3, y + H / 2, txt, ha="right", va="center", fontsize=12,
            fontweight="bold", color=DARK)

ax.text(cx(7.5), -0.5, "⋮", ha="center", va="center", fontsize=16, color=DARK)
ax.text(cx(7.5), -1.0,
        r"$16! \approx 2.09 \times 10^{13}$ possible permutations — only 2 are shown",
        ha="center", va="center", fontsize=12, fontweight="bold", color=DARK)

fig.savefig(out / "fig-02-permutacoes-16-en.png", bbox_inches="tight", pad_inches=0.1)
plt.close(fig)
