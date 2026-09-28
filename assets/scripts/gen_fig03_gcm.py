"""Figuras do modo GCM (Cap03 / Aula 03), segundo NIST SP 800-38D.

Gera:
  assets/images/fig-03-modo-gcm.png         esquema CTR + GHASH -> tag
  assets/images/fig-03-gcm-pacote.png       o que segue no canal (AAD | C | tag)
Com --en: rótulos em inglês, em en/assets/images/*-en.png (versão inglesa do livro).

Nonce de 96 bits: J0 = nonce || 0^31 || 1 (contador 1, só para mascarar a tag);
a cifragem dos dados começa no contador 2. H = AES_K(0^128).
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, FancyBboxPatch

DARK = "#1c0808"
CRIMSON = "#b0202a"
PINK = "#fae3e3"
GREEN = "#e3f1e3"; GREEN_E = "#3d7a3d"
GOLD = "#fdf0d5"; GOLD_E = "#b7791f"
GREY = "#6b5b5b"
EN = "--en" in sys.argv
OUT = "en/assets/images/" if EN else "assets/images/"
SUF = "-en" if EN else ""


def t(pt, en):
    return en if EN else pt


def box(ax, x, y, w, h, text, fc=PINK, ec=CRIMSON, tc=DARK, fs=15, bold=True):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=fc, ec=ec, lw=2.4, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", zorder=4, linespacing=1.2)


def dark(ax, x, y, w, h, text, fs=15):
    box(ax, x, y, w, h, text, fc=DARK, ec=DARK, tc="white", fs=fs)


def xor(ax, x, y, r=0.36):
    ax.add_patch(Circle((x, y), r, fc="white", ec=DARK, lw=2.6, zorder=3))
    ax.plot([x - r * 0.72, x + r * 0.72], [y, y], color=DARK, lw=2.6, zorder=4)
    ax.plot([x, x], [y - r * 0.72, y + r * 0.72], color=DARK, lw=2.6, zorder=4)


def arrow(ax, p, q, color=DARK, lw=2.4):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=20, lw=lw,
                                 color=color, shrinkA=0, shrinkB=0, zorder=2))


# ---------- esquema principal ----------
fig, ax = plt.subplots(figsize=(18, 9.2))
ax.set_xlim(-0.2, 25.2); ax.set_ylim(0.2, 12.6); ax.axis("off")

# faixas de fundo
ax.add_patch(FancyBboxPatch((0.0, 4.75), 16.0, 7.6, boxstyle="round,pad=0,rounding_size=0.25",
                            fc="#fdf6f6", ec="#e8c4c4", lw=1.5, zorder=0))
ax.text(0.3, 11.8, t("Cifragem (modo CTR)", "Encryption (CTR mode)"), fontsize=17, color=CRIMSON, fontweight="bold", style="italic")
ax.add_patch(FancyBboxPatch((0.0, 2.2), 25.0, 2.1, boxstyle="round,pad=0,rounding_size=0.25",
                            fc="#f6f3f3", ec="#d9cccc", lw=1.5, zorder=0))
ax.text(0.3, 3.8, t("Autenticação (GHASH)", "Authentication (GHASH)"), fontsize=17, color=CRIMSON, fontweight="bold", style="italic")

c1, c2, cj = 7.0, 13.0, 22.5
yc, ya, yx, yC, yg = 10.7, 8.85, 7.05, 5.55, 3.05

# contadores
box(ax, c1, yc, 3.4, 0.95, "nonce ‖ 2")
box(ax, c2, yc, 3.4, 0.95, "nonce ‖ 3")
arrow(ax, (c1 + 1.7, yc), (c2 - 1.7, yc), color=GREY, lw=2)
ax.text((c1 + c2) / 2, yc + 0.32, "+1", ha="center", fontsize=14, color=GREY)
box(ax, cj, yc, 3.4, 0.95, "nonce ‖ 1")
ax.text(cj, yc + 0.85, t("J₀ (contador inicial)", "J₀ (initial counter)"), ha="center", fontsize=14, color=CRIMSON, style="italic")

# AES
for x in (c1, c2, cj):
    arrow(ax, (x, yc - 0.475), (x, ya + 0.475))
    dark(ax, x, ya, 2.6, 0.95, "AES$_K$")

# XOR com texto claro -> texto cifrado
for x, i in ((c1, 1), (c2, 2)):
    arrow(ax, (x, ya - 0.475), (x, yx + 0.36))
    xor(ax, x, yx)
    box(ax, x - 3.0, yx, 2.4, 0.9, t(f"Texto\nclaro $P_{i}$", f"Plaintext\n$P_{i}$"), fs=14)
    arrow(ax, (x - 1.8, yx), (x - 0.36, yx))
    arrow(ax, (x, yx - 0.36), (x, yC + 0.45))
    box(ax, x, yC, 2.6, 0.9, t(f"Texto\ncifrado $C_{i}$", f"Ciphertext\n$C_{i}$"), fs=14)

# cadeia GHASH
box(ax, 1.5, yg, 2.2, 0.9, "AAD", fc=GREEN, ec=GREEN_E)
mults = [4.2, 10.0, 16.0, 20.6]
xors = [(c1, "C"), (c2, "C"), (18.4, "len"), (cj, "J0")]
arrow(ax, (2.6, yg), (mults[0] - 0.62, yg))
dark(ax, mults[0], yg, 1.24, 0.8, "× H", fs=14)
chain = [mults[0], c1, mults[1], c2, mults[2], 18.4, mults[3], cj]
for a, b in zip(chain, chain[1:]):
    ra = 0.62 if a in mults else 0.36
    rb = 0.62 if b in mults else 0.36
    arrow(ax, (a + ra, yg), (b - rb, yg))
for m in mults[1:]:
    dark(ax, m, yg, 1.24, 0.8, "× H", fs=14)
for x in (c1, c2, 18.4, cj):
    xor(ax, x, yg)
# C_i descem para o GHASH
for x in (c1, c2):
    arrow(ax, (x, yC - 0.45), (x, yg + 0.36))
# comprimentos entram por baixo
box(ax, 18.4, 1.05, 3.3, 0.8, "len(AAD) ‖ len(C)", fs=13)
arrow(ax, (18.4, 1.45), (18.4, yg - 0.36))
# AES_K(J0) desce até ao último XOR
arrow(ax, (cj, ya - 0.475), (cj, yg + 0.36), color=CRIMSON)
# tag
box(ax, 24.3, 1.05, 1.6, 0.8, "Tag", fc=GOLD, ec=GOLD_E, fs=15)
ax.plot([cj, cj], [yg - 0.36, 1.05], color=DARK, lw=2.4, zorder=2)
arrow(ax, (cj, 1.05), (24.3 - 0.8, 1.05))

ax.text(0.3, 1.05, t("H = AES$_K$(0¹²⁸)     × H: multiplicação em GF(2¹²⁸)", "H = AES$_K$(0¹²⁸)     × H: multiplication in GF(2¹²⁸)"),
        fontsize=14.5, color=DARK, va="center", style="italic")

plt.savefig(OUT + "fig-03-modo-gcm" + SUF + ".png", dpi=110, bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---------- pacote enviado ----------
fig, ax = plt.subplots(figsize=(15, 2.6))
ax.set_xlim(0, 15); ax.set_ylim(0, 2.6); ax.axis("off")
ax.add_patch(FancyBboxPatch((0.1, 0.15), 14.8, 2.1, boxstyle="round,pad=0,rounding_size=0.15",
                            fc="white", ec=GREY, lw=1.8, ls=(0, (5, 3))))
ax.text(0.35, 1.95, t("O que segue no canal", "What travels on the channel"), fontsize=15, color=DARK, fontweight="bold")
box(ax, 2.7, 0.95, 4.2, 0.95, t("AAD\n(visível, autenticado)", "AAD\n(visible, authenticated)"), fc=GREEN, ec=GREEN_E, fs=14)
box(ax, 8.1, 0.95, 5.6, 0.95, t("Texto cifrado $C_1 C_2 \\ldots$\n(cifrado, autenticado)", "Ciphertext $C_1 C_2 \\ldots$\n(encrypted, authenticated)"), fs=14)
box(ax, 13.0, 0.95, 3.0, 0.95, "Tag\n(128 bits)", fc=GOLD, ec=GOLD_E, fs=14)
plt.savefig(OUT + "fig-03-gcm-pacote" + SUF + ".png", dpi=110, bbox_inches="tight", facecolor="white")
