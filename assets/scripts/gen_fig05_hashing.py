"""Figuras da Aula 05 / Cap05 (hashing, MAC, HMAC).

Uso (a partir da raiz do projeto):
    python assets/scripts/gen_fig05_hashing.py        -> assets/images/fig-05-*.png
    python assets/scripts/gen_fig05_hashing.py --en   -> en/assets/images/fig-05-*-en.png
"""
import hashlib
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

EN = "--en" in sys.argv
OUT = Path("en/assets/images" if EN else "assets/images")
SUF = "-en" if EN else ""

DARK = "#1c0707"
RED = "#b0202a"
PINK = "#f9e4e4"
GREEN = "#1f7a3a"
GREENBG = "#e3f3e7"
GREY = "#f2f2f2"
FS = 17

# "hash" em itálico nas figuras PT (estrangeirismo), via mathtext com a mesma fonte
matplotlib.rcParams.update({
    "mathtext.fontset": "custom",
    "mathtext.rm": "DejaVu Sans",
    "mathtext.it": "DejaVu Sans:italic",
    "mathtext.bf": "DejaVu Sans:bold",
    "mathtext.bfit": "DejaVu Sans:italic:bold",
})


def t(pt, en):
    return en if EN else pt


def it(word, bold=False):
    """Palavra estrangeira em itálico (só na versão PT)."""
    return (r"$\mathbfit{%s}$" if bold else r"$\mathit{%s}$") % word


def new_ax(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def box(ax, cx, cy, w, h, text, fill="white", edge=RED, color=DARK, fs=FS,
        bold=False, round_=False, lw=2.2):
    if round_:
        p = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                           boxstyle="round,pad=0,rounding_size=0.25",
                           facecolor=fill, edgecolor=edge, lw=lw, zorder=2)
    else:
        p = Rectangle((cx - w / 2, cy - h / 2), w, h, facecolor=fill,
                      edgecolor=edge, lw=lw, zorder=2)
    ax.add_patch(p)
    tx = ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=color,
                 fontweight="bold" if bold else "normal", zorder=3)
    fit(ax, tx, w - 0.3)
    return tx


def fit(ax, tx, width):
    """Reduz a letra até o texto caber em `width` (unidades dos dados)."""
    fig = ax.figure
    r = fig.canvas.get_renderer()
    x0 = ax.transData.transform((0, 0))[0]
    avail = ax.transData.transform((width, 0))[0] - x0
    while tx.get_window_extent(r).width > avail and tx.get_fontsize() > 8:
        tx.set_fontsize(tx.get_fontsize() - 0.5)


def hbox(ax, cx, cy, label="H", s=1.1, fs=FS + 2):
    box(ax, cx, cy, s, s, label, fill=DARK, edge=DARK, color="white", fs=fs,
        bold=True, round_=True)


def arrow(ax, x0, y0, x1, y1, color=DARK, lw=2.2, style="-|>"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                mutation_scale=20, shrinkA=0, shrinkB=0),
                zorder=1)


def poly(ax, pts, color=DARK, lw=2.2):
    """Linha poligonal com seta no último segmento."""
    for (x0, y0), (x1, y1) in zip(pts[:-2], pts[1:-1]):
        ax.plot([x0, x1], [y0, y1], color=color, lw=lw, zorder=1)
    arrow(ax, *pts[-2], *pts[-1], color=color, lw=lw)


def save(fig, name):
    fig.savefig(OUT / f"{name}{SUF}.png", bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# 1. Conceito: entradas de tamanhos diferentes -> saída de tamanho fixo
# ---------------------------------------------------------------------------
fig, ax = new_ax(12.4, 5.2, 24.4, 10.4)
ins = [
    ("A", "A", 1.4),
    (t("Olá Mundo!", "Hello World!"), t("Olá Mundo!", "Hello World!"), 4.2),
    (t("1 000 000 × «a»", "1,000,000 × 'a'"), "a" * 1_000_000, 7.4),
]
ys = (8.6, 5.2, 1.8)
hbox(ax, 11.6, 5.2, "H", s=1.6, fs=FS + 6)
for (lab, txt, w), y in zip(ins, ys):
    box(ax, 0.6 + w / 2, y, w, 1.2, lab, fill=PINK)
    arrow(ax, 0.6 + w, y, 10.8, 5.2 + (y - 5.2) * 0.25)
    hx = sha(txt)
    digest = hx[:16] + "…" + hx[-8:]
    arrow(ax, 12.4, 5.2 + (y - 5.2) * 0.25, 14.2, y)
    tx = box(ax, 18.9, y, 9.4, 1.2, digest, fill="white", fs=FS - 2)
    tx.set_family("monospace")
    fit(ax, tx, 9.1)
ax.text(18.9, 10.0, t("sempre 256 bits (SHA-256)", "always 256 bits (SHA-256)"),
        ha="center", va="center", fontsize=FS, color=RED, fontweight="bold")
ax.text(4.3, 10.0, t("qualquer tamanho", "any size"), ha="center", va="center",
        fontsize=FS, color=RED, fontweight="bold")
save(fig, "fig-05-hash-conceito")

# ---------------------------------------------------------------------------
# 2. Propriedades com chavetas fraco / forte
# ---------------------------------------------------------------------------
rows = [
    (t("Entrada de tamanho variável", "Variable input size"),
     t("H aplica-se a dados de qualquer tamanho", "H applies to data of any size")),
    (t("Saída de tamanho fixo", "Fixed output size"),
     t("H produz sempre o mesmo comprimento", "H always produces the same length")),
    (t("Eficiência", "Efficiency"),
     t("H(x) é fácil de calcular", "H(x) is easy to compute")),
    (t("Resistência a pré-imagem", "Preimage resistant"),
     t("dado h, inviável achar y com H(y) = h", "given h, infeasible to find y with H(y) = h")),
    (t("Resistência a 2.ª pré-imagem", "Second preimage resistant"),
     t("dado x, inviável achar y ≠ x com H(y) = H(x)",
       "given x, infeasible to find y ≠ x with H(y) = H(x)")),
    (t("Resistência a colisões", "Collision resistant"),
     t("inviável achar qualquer par x ≠ y com H(x) = H(y)",
       "infeasible to find any pair x ≠ y with H(x) = H(y)")),
    (t("Pseudoaleatoriedade", "Pseudorandomness"),
     t("a saída passa nos testes de aleatoriedade", "output passes randomness tests")),
]
rh = 1.0
fig, ax = new_ax(14.6, 5.6, 29.4, 9.0)
x0, c1, c2 = 3.2, 8.6, 14.6
top = 8.3
box(ax, x0 + c1 / 2, top, c1, rh, t("Requisito", "Requirement"), fill=DARK,
    edge=DARK, color="white", bold=True, fs=FS - 1)
box(ax, x0 + c1 + c2 / 2, top, c2, rh, t("Descrição", "Description"), fill=DARK,
    edge=DARK, color="white", bold=True, fs=FS - 1)
for i, (r, d) in enumerate(rows):
    y = top - (i + 1) * rh
    fill = PINK if i in (3, 4, 5) else "white"
    box(ax, x0 + c1 / 2, y, c1, rh, r, fill=fill, fs=FS - 2, lw=1.4)
    box(ax, x0 + c1 + c2 / 2, y, c2, rh, d, fill=fill, fs=FS - 2, lw=1.4)


def brace(ax, x, y_top, y_bot, side, label, color):
    d = -0.5 if side == "L" else 0.5
    ax.plot([x, x + d, x + d, x], [y_top, y_top, y_bot, y_bot], color=color,
            lw=3, zorder=3)
    ax.plot([x + d, x + 2 * d], [(y_top + y_bot) / 2] * 2, color=color, lw=3)
    ax.text(x + 2.4 * d, (y_top + y_bot) / 2, label, ha="right" if side == "L" else "left",
            va="center", fontsize=FS, color=color, fontweight="bold")


y_first_top = top - rh / 2
brace(ax, x0 - 0.15, y_first_top, y_first_top - 5 * rh, "L",
      t(it("Hash", True) + "\nfraco", "Weak\nhash"), DARK)
brace(ax, x0 + c1 + c2 + 0.15, y_first_top, y_first_top - 6 * rh, "R",
      t(it("Hash", True) + "\nforte", "Strong\nhash"), RED)
save(fig, "fig-05-propriedades")

# ---------------------------------------------------------------------------
# 3. Os três ataques: pré-imagem, segunda pré-imagem, colisão
# ---------------------------------------------------------------------------
fig, ax = new_ax(14, 4.6, 30, 9.6)
panels = [
    (1.0, t("Pré-imagem", "Preimage"), "?", "h", t("dado: h", "given: h")),
    (11.0, t("2.ª pré-imagem", "Second preimage"), "x", None,
     t("dado: x", "given: x")),
    (21.0, t("Colisão", "Collision"), None, None, t("dado: nada", "given: nothing")),
]
for x, title, a, b, given in panels:
    ax.add_patch(Rectangle((x - 0.4, 0.2), 8.8, 9.2, facecolor=GREY,
                           edgecolor="none", zorder=0))
    ax.text(x + 4, 8.6, title, ha="center", fontsize=FS + 2, color=RED,
            fontweight="bold")
    ax.text(x + 4, 7.6, given, ha="center", fontsize=FS - 1, color=DARK,
            style="italic")
# Pré-imagem
x = 1.0
box(ax, x + 1.2, 4.6, 1.8, 1.1, "y = ?", fill=PINK, edge=RED, color=RED, bold=True, fs=FS - 2)
arrow(ax, x + 2.1, 4.6, x + 3.6, 4.6)
hbox(ax, x + 4.2, 4.6)
arrow(ax, x + 4.8, 4.6, x + 6.2, 4.6)
box(ax, x + 7.0, 4.6, 1.4, 1.1, "h", fill="white", bold=True)
ax.text(x + 4, 1.4, t("inverter H", "invert H"), ha="center", fontsize=FS - 1)
# Segunda pré-imagem
x = 11.0
box(ax, x + 1.2, 5.8, 1.8, 1.1, "x", fill="white", bold=True)
box(ax, x + 1.2, 3.4, 1.8, 1.1, "y = ?", fill=PINK, color=RED, bold=True, fs=FS - 2)
for yy in (5.8, 3.4):
    arrow(ax, x + 2.1, yy, x + 3.6, yy)
    hbox(ax, x + 4.2, yy, s=0.9, fs=FS)
    arrow(ax, x + 4.7, yy, x + 6.1, 4.6)
box(ax, x + 7.1, 4.6, 2.0, 1.1, t("igual", "equal"), fill=GREENBG, edge=GREEN,
    color=GREEN, fs=FS - 2, bold=True)
ax.text(x + 4, 1.4, t("acertar num alvo fixo", "hit a fixed target"),
        ha="center", fontsize=FS - 1)
# Colisão
x = 21.0
box(ax, x + 1.2, 5.8, 1.8, 1.1, "x = ?", fill=PINK, color=RED, bold=True, fs=FS - 2)
box(ax, x + 1.2, 3.4, 1.8, 1.1, "y = ?", fill=PINK, color=RED, bold=True, fs=FS - 2)
for yy in (5.8, 3.4):
    arrow(ax, x + 2.1, yy, x + 3.6, yy)
    hbox(ax, x + 4.2, yy, s=0.9, fs=FS)
    arrow(ax, x + 4.7, yy, x + 6.1, 4.6)
box(ax, x + 7.1, 4.6, 2.0, 1.1, t("igual", "equal"), fill=GREENBG, edge=GREEN,
    color=GREEN, fs=FS - 2, bold=True)
ax.text(x + 4, 1.4, t("qualquer par serve", "any pair will do"), ha="center",
        fontsize=FS - 1)
save(fig, "fig-05-tres-ataques")

# ---------------------------------------------------------------------------
# 4. Paradoxo do aniversário: probabilidade de pelo menos uma coincidência
# ---------------------------------------------------------------------------
def p_coinc(n, N=365):
    q = 1.0
    for i in range(n):
        q *= (N - i) / N
    return 1 - q


ns = list(range(1, 71))
ps = [p_coinc(n) for n in ns]
fig, axp = plt.subplots(figsize=(10, 4.6), dpi=200)
axp.plot(ns, [p * 100 for p in ps], color=RED, lw=3.2)
p23 = p_coinc(23) * 100
p57 = p_coinc(57) * 100
axp.axhline(50, color="#999", lw=1.2, ls="--")
axp.plot([23], [p23], "o", color=DARK, ms=11, zorder=4)
axp.plot([57], [p57], "o", color=DARK, ms=11, zorder=4)
axp.annotate(t(f"23 pessoas: {p23:.1f} %".replace(".", ","), f"23 people: {p23:.1f} %"),
             (23, p23), xytext=(28, 30), fontsize=FS, color=DARK,
             arrowprops=dict(arrowstyle="-|>", color=DARK, lw=1.8))
axp.annotate(t(f"57 pessoas: {p57:.0f} %", f"57 people: {p57:.0f} %"),
             (57, p57), xytext=(45, 70), fontsize=FS, color=DARK,
             arrowprops=dict(arrowstyle="-|>", color=DARK, lw=1.8))
axp.set_xlabel(t("número de pessoas na sala", "number of people in the room"),
               fontsize=FS)
axp.set_ylabel(t("P(2 fazem anos no\nmesmo dia do ano) em %", "P(2 share\na birthday) in %"),
               fontsize=FS - 1)
axp.set_ylim(0, 102)
axp.set_xlim(0, 70)
axp.tick_params(labelsize=FS - 2)
for s in ("top", "right"):
    axp.spines[s].set_visible(False)
fig.savefig(OUT / f"fig-05-aniversario{SUF}.png", bbox_inches="tight", pad_inches=0.12)
plt.close(fig)

# ---------------------------------------------------------------------------
# 5. Cronologia MD5 / SHA
# ---------------------------------------------------------------------------
fig, ax = new_ax(14, 3.9, 30, 8.4)
ax.plot([0.8, 29.2], [4.2, 4.2], color=DARK, lw=3)
events = [
    (1990, "MD4", t("128 bits", "128 bits"), "up", DARK),
    (1992, "MD5", t("128 bits", "128 bits"), "up", DARK),
    (1995, "SHA-1", t("160 bits", "160 bits"), "up", DARK),
    (2002, "SHA-2", t("224 a 512 bits", "224 to 512 bits"), "up", GREEN),
    (2005, t("Colisões\nem MD5", "MD5\ncollisions"), "Wang & Yu", "down", RED),
    (2017, t("Colisão\nem SHA-1", "SHA-1\ncollision"), "SHAttered", "down", RED),
]
for i, (yr, lab, sub, side, col) in enumerate(events):
    x = 2.5 + i * 5.0
    ax.plot([x], [4.2], "o", color=col, ms=14, zorder=3)
    ax.text(x, 3.3 if side == "up" else 5.1, str(yr), ha="center",
            va="center", fontsize=FS - 2, color="#555")
    if side == "up":
        ax.text(x, 6.6, lab, ha="center", va="center", fontsize=FS + 1,
                color=col, fontweight="bold")
        ax.text(x, 5.5, sub, ha="center", va="center", fontsize=FS - 3, color=DARK)
    else:
        ax.text(x, 1.9, lab, ha="center", va="center", fontsize=FS - 1,
                color=col, fontweight="bold")
        ax.text(x, 0.4, sub, ha="center", va="center", fontsize=FS - 3,
                color=DARK, style="italic")
save(fig, "fig-05-cronologia")

# ---------------------------------------------------------------------------
# 6 e 7. Integridade com hash (Alice -> Bob) e o ataque do homem no meio
# ---------------------------------------------------------------------------
def sender(ax, x, label, data_lbl="M", fill=PINK):
    ax.text(x + 3, 9.1, label, ha="center", fontsize=FS + 2, color=RED,
            fontweight="bold")
    box(ax, x + 1.2, 7.4, 1.8, 1.0, data_lbl, fill=fill, bold=True)
    arrow(ax, x + 2.1, 7.4, x + 3.6, 7.4)
    hbox(ax, x + 4.2, 7.4, s=1.0, fs=FS)
    poly(ax, [(x + 1.2, 6.9), (x + 1.2, 4.6)])
    poly(ax, [(x + 4.2, 6.9), (x + 4.2, 5.1), (x + 3.0, 4.6)])
    box(ax, x + 1.6, 4.1, 2.6, 1.0, data_lbl, fill=fill, bold=True)
    box(ax, x + 3.7, 4.1, 1.6, 1.0, "h" if data_lbl == "M" else "h'", fill="white",
        bold=True)


def receiver(ax, x, data_lbl, h_lbl, verdict, ok):
    ax.text(x + 3, 9.1, "Bob", ha="center", fontsize=FS + 2, color=RED,
            fontweight="bold")
    box(ax, x + 1.3, 7.4, 2.6, 1.0, data_lbl, fill=PINK, bold=True)
    box(ax, x + 3.4, 7.4, 1.6, 1.0, h_lbl, fill="white", bold=True)
    arrow(ax, x + 1.3, 6.9, x + 1.3, 5.1)
    hbox(ax, x + 1.3, 4.5, s=1.0, fs=FS)
    arrow(ax, x + 1.8, 4.5, x + 2.8, 4.5)
    arrow(ax, x + 3.4, 6.9, x + 3.4, 5.0)
    ax.text(x + 3.4, 4.5, "=?", ha="center", va="center", fontsize=FS + 2,
            color=DARK, fontweight="bold")
    col, bg = (GREEN, GREENBG) if ok else (RED, PINK)
    box(ax, x + 3.0, 2.4, 7.6, 1.3, verdict, fill=bg, edge=col, color=col,
        fs=FS - 3, bold=True)
    arrow(ax, x + 3.4, 4.0, x + 3.4, 3.1)


fig, ax = new_ax(12.6, 4.8, 23.4, 10)
sender(ax, 0.8, "Alice")
poly(ax, [(5.4, 4.1), (9.0, 4.1), (9.0, 7.4), (12.6, 7.4)])
ax.text(9.0, 8.1, t("canal", "channel"), ha="center", fontsize=FS - 2, color="#555")
receiver(ax, 13.2, "M", "h", t("iguais: M chegou intacta", "equal: M arrived intact"), True)
save(fig, "fig-05-hash-integridade")

fig, ax = new_ax(14.6, 5.0, 32.6, 10.4)
sender(ax, 0.6, "Alice")
poly(ax, [(5.2, 4.1), (7.6, 4.1), (7.6, 7.4), (8.6, 7.4)])
# Darth
x = 8.8
ax.add_patch(Rectangle((x - 0.4, 0.9), 12.6, 9.2, facecolor=GREY, edgecolor="none", zorder=0))
ax.text(x + 5.8, 9.4, t("Darth (no meio do canal)", "Darth (in the middle)"),
        ha="center", fontsize=FS + 1, color=DARK, fontweight="bold")
box(ax, x + 1.3, 7.4, 2.6, 1.0, "M", fill=PINK, bold=True)
box(ax, x + 3.4, 7.4, 1.6, 1.0, "h", fill="white", bold=True)
ax.plot([x + 0.0, x + 4.2], [6.9, 7.9], color=RED, lw=3, zorder=4)
ax.plot([x + 0.0, x + 4.2], [7.9, 6.9], color=RED, lw=3, zorder=4)
ax.text(x + 7.9, 7.4, t("deita fora\nM e h", "discards\nM and h"), ha="center",
        va="center", fontsize=FS - 2, color=RED)
box(ax, x + 1.3, 4.1, 2.0, 1.0, "M'", fill=PINK, edge=RED, color=RED, bold=True)
arrow(ax, x + 2.3, 4.1, x + 3.6, 4.1)
hbox(ax, x + 4.2, 4.1, s=1.0, fs=FS)
arrow(ax, x + 4.7, 4.1, x + 6.0, 4.1)
box(ax, x + 6.8, 4.1, 1.6, 1.0, "h'", fill="white", edge=RED, color=RED, bold=True)
ax.text(x + 5.8, 2.0, t("H é pública: Darth calcula h' = H(M')",
                        "H is public: Darth computes h' = H(M')"),
        ha="center", fontsize=FS - 3, color=DARK, style="italic")
poly(ax, [(x + 7.6, 4.1), (x + 11.0, 4.1), (x + 11.0, 7.4), (x + 11.8, 7.4)])
receiver(ax, x + 12.0, "M'", "h'", t("iguais: Bob aceita M' falsa", "equal: Bob accepts fake M'"), False)
save(fig, "fig-05-hash-mitm")

# ---------------------------------------------------------------------------
# 8. Os quatro usos clássicos de um hash (Stallings), lado do emissor
# ---------------------------------------------------------------------------
def scheme(ax, y, tag, kind, sent, props):
    """kind: a, b, c, d."""
    ax.text(0.3, y + 0.9, f"({tag})", fontsize=FS + 1, color=RED, fontweight="bold")
    box(ax, 2.0, y, 1.3, 0.9, "M", fill=PINK, bold=True)
    if kind in ("c", "d"):
        box(ax, 2.0, y - 1.6, 1.3, 0.9, "S", fill=GREENBG, edge=GREEN, color=GREEN, bold=True)
        poly(ax, [(2.65, y - 1.6), (4.0, y - 1.6)])
        poly(ax, [(2.0, y - 0.45), (2.0, y - 0.8), (3.4, y - 0.8), (4.0, y - 1.3)])
        ax.text(4.6, y - 1.6, "‖", ha="center", va="center", fontsize=FS + 4, color=DARK)
        poly(ax, [(5.0, y - 1.6), (5.8, y - 1.6)])
        hbox(ax, 6.3, y - 1.6, s=0.9, fs=FS)
        hx = 6.75
    else:
        poly(ax, [(2.0, y - 0.45), (2.0, y - 1.6), (5.8, y - 1.6)])
        hbox(ax, 6.3, y - 1.6, s=0.9, fs=FS)
        hx = 6.75
    if kind == "b":
        poly(ax, [(hx, y - 1.6), (7.6, y - 1.6)])
        box(ax, 8.1, y - 1.6, 0.9, 0.9, "E", fill=DARK, edge=DARK, color="white",
            bold=True, round_=True)
        ax.text(8.1, y - 3.0, "K", ha="center", va="center", fontsize=FS - 1, color=RED, fontweight="bold")
        arrow(ax, 8.1, y - 2.65, 8.1, y - 2.05)
        hx = 8.55
    poly(ax, [(hx, y - 1.6), (9.6, y - 1.6), (9.6, y - 0.4)])
    poly(ax, [(2.65, y), (9.2, y)])
    ax.text(9.6, y, "‖", ha="center", va="center", fontsize=FS + 4, color=DARK)
    nx = 10.0
    if kind in ("a", "d"):
        poly(ax, [(10.0, y), (11.0, y)])
        box(ax, 11.5, y, 0.9, 0.9, "E", fill=DARK, edge=DARK, color="white",
            bold=True, round_=True)
        ax.text(11.5, y - 1.45, "K", ha="center", va="center", fontsize=FS - 1, color=RED, fontweight="bold")
        arrow(ax, 11.5, y - 1.1, 11.5, y - 0.45)
        nx = 11.95
    poly(ax, [(nx, y), (13.0, y)])
    ax.text(13.2, y, sent, ha="left", va="center", fontsize=FS - 1, color=DARK)
    ax.text(13.2, y - 1.2, props, ha="left", va="center", fontsize=FS - 3,
            color=GREEN, fontweight="bold")


fig, ax = new_ax(13, 5.4, 26, 10.6)
scheme(ax, 8.6, "a", "a", "E(K, M ‖ H(M))",
       t("integridade + autenticação + confidencialidade",
         "integrity + authentication + confidentiality"))
scheme(ax, 3.4, "b", "b", "M ‖ E(K, H(M))",
       t("integridade + autenticação (sem confidencialidade)",
         "integrity + authentication (no confidentiality)"))
save(fig, "fig-05-usos-ab")

fig, ax = new_ax(13, 5.4, 26, 10.6)
scheme(ax, 8.6, "c", "c", "M ‖ H(M ‖ S)",
       t("integridade + autenticação, sem cifra nenhuma",
         "integrity + authentication, no encryption at all"))
scheme(ax, 3.4, "d", "d", "E(K, M ‖ H(M ‖ S))",
       t("(c) + confidencialidade", "(c) + confidentiality"))
save(fig, "fig-05-usos-cd")

# ---------------------------------------------------------------------------
# 9. MAC: Darth já não consegue recalcular a marca
# ---------------------------------------------------------------------------
fig, ax = new_ax(14.4, 5.0, 32.4, 10.4)
# Alice
ax.text(3.6, 9.4, "Alice", ha="center", fontsize=FS + 2, color=RED, fontweight="bold")
box(ax, 1.6, 7.4, 1.8, 1.0, "M", fill=PINK, bold=True)
box(ax, 4.6, 8.9 - 0.3, 1.2, 0.9, "K", fill=GREENBG, edge=GREEN, color=GREEN, bold=True)
arrow(ax, 2.5, 7.4, 3.8, 7.4)
box(ax, 4.6, 7.4, 1.5, 1.0, "MAC", fill=DARK, edge=DARK, color="white", bold=True,
    round_=True, fs=FS - 2)
arrow(ax, 4.6, 8.15, 4.6, 7.9)
poly(ax, [(1.6, 6.9), (1.6, 4.6)])
poly(ax, [(4.6, 6.9), (4.6, 5.1), (3.6, 4.6)])
box(ax, 2.0, 4.1, 2.6, 1.0, "M", fill=PINK, bold=True)
box(ax, 4.1, 4.1, 1.6, 1.0, "T", fill="white", bold=True)
poly(ax, [(4.9, 4.1), (7.6, 4.1), (7.6, 7.4), (8.6, 7.4)])
x = 8.8
ax.add_patch(Rectangle((x - 0.2, 0.9), 12.0, 9.2, facecolor=GREY, edgecolor="none", zorder=0))
ax.text(x + 5.8, 9.4, t("Darth (no meio do canal)", "Darth (in the middle)"),
        ha="center", fontsize=FS + 1, color=DARK, fontweight="bold")
box(ax, x + 1.3, 7.4, 2.6, 1.0, "M", fill=PINK, bold=True)
box(ax, x + 3.4, 7.4, 1.6, 1.0, "T", fill="white", bold=True)
ax.text(x + 7.9, 7.4, t("troca M por M',\nmantém T", "swaps M for M',\nkeeps T"),
        ha="center", va="center", fontsize=FS - 2, color=RED)
box(ax, x + 1.3, 4.1, 2.6, 1.0, "M'", fill=PINK, edge=RED, color=RED, bold=True)
box(ax, x + 3.4, 4.1, 1.6, 1.0, "T", fill="white", bold=True)
ax.text(x + 5.8, 1.8, t("sem K, não consegue calcular\nT' = MAC(K, M')",
                        "without K, cannot compute\nT' = MAC(K, M')"),
        ha="center", fontsize=FS - 2, color=DARK, style="italic")
poly(ax, [(x + 4.2, 4.1), (x + 11.0, 4.1), (x + 11.0, 7.4), (x + 12.6, 7.4)])
x = 21.6
ax.text(x + 3, 9.4, "Bob", ha="center", fontsize=FS + 2, color=RED, fontweight="bold")
box(ax, x + 1.3, 7.4, 2.6, 1.0, "M'", fill=PINK, bold=True)
box(ax, x + 3.4, 7.4, 1.6, 1.0, "T", fill="white", bold=True)
arrow(ax, x + 1.3, 6.9, x + 1.3, 5.0)
box(ax, x + 1.3, 4.5, 1.5, 1.0, "MAC", fill=DARK, edge=DARK, color="white", bold=True,
    round_=True, fs=FS - 2)
box(ax, x - 0.6, 4.5, 1.0, 0.9, "K", fill=GREENBG, edge=GREEN, color=GREEN, bold=True)
arrow(ax, x - 0.1, 4.5, x + 0.55, 4.5)
arrow(ax, x + 2.05, 4.5, x + 2.9, 4.5)
arrow(ax, x + 3.4, 6.9, x + 3.4, 5.0)
ax.text(x + 3.4, 4.5, "=?", ha="center", va="center", fontsize=FS + 2, color=DARK,
        fontweight="bold")
arrow(ax, x + 3.4, 4.0, x + 3.4, 3.1)
box(ax, x + 3.0, 2.4, 7.6, 1.3, t("diferentes: Bob rejeita", "different: Bob rejects"),
    fill=GREENBG, edge=GREEN, color=GREEN, fs=FS - 2, bold=True)
save(fig, "fig-05-mac")

# ---------------------------------------------------------------------------
# 10. Extensão de comprimento com a função de hash simplificada
# ---------------------------------------------------------------------------
fig, ax = new_ax(14.6, 5.0, 31.4, 10.6)
ax.set_ylim(-0.6, 10.0)
ax.text(0.3, 9.3, t("Emissor:  H(K ‖ M)", "Sender:  H(K ‖ M)"), fontsize=FS + 1,
        color=DARK, fontweight="bold")
st = [(2.0, "0"), (8.0, "7"), (14.0, "49")]
blocks = [(t("chave\nK = 7", "key\nK = 7"), GREENBG, GREEN),
          (t("mensagem\nM = 42", "message\nM = 42"), PINK, RED)]
for i, (sx, sv) in enumerate(st):
    box(ax, sx, 6.0, 2.0, 1.2, sv, fill=GREY if i < 2 else DARK,
        color=DARK if i < 2 else "white", edge=DARK, bold=True, fs=FS + 2,
        round_=True)
    if i < 2:
        ax.text(sx, 4.95, (t("estado\ninicial", "initial\nstate") if i == 0
                           else t("estado", "state")),
                ha="center", va="top", fontsize=FS - 3, color="#555", style="italic")
    if i < 2:
        bl, bg, col = blocks[i]
        box(ax, sx + 3.0, 8.0, 3.6, 1.5, bl, fill=bg, edge=col, color=col, bold=True, fs=FS - 2)
        arrow(ax, sx + 1.0, 6.0, sx + 5.0, 6.0)
        arrow(ax, sx + 3.0, 7.25, sx + 3.0, 6.15)
        ax.text(sx + 3.0, 6.0, "+", ha="center", va="center", fontsize=FS + 4,
                color=DARK, fontweight="bold", bbox=dict(boxstyle="circle", fc="white", ec=DARK, lw=2))
ax.text(15.3, 6.0, t("estado final\n= marca enviada", "final state\n= tag sent"), va="center", ha="left", fontsize=FS - 2, color=DARK)
ax.text(0.3, 2.4, t("Atacante:", "Attacker:"), fontsize=FS + 1, color=RED, fontweight="bold")
ax.text(0.3, 1.5, t("não conhece K", "does not know K"), fontsize=FS - 2, color=RED)
poly(ax, [(14.0, 5.35), (14.0, 2.0), (15.0, 2.0)], color=RED)
box(ax, 16.0, 2.0, 2.0, 1.2, "49", fill=GREY, edge=RED, bold=True, fs=FS + 2, round_=True)
ax.text(16.0, 0.95, t("estado\nconhecido", "known\nstate"), ha="center", va="top",
        fontsize=FS - 3, color="#555", style="italic")
box(ax, 19.0, 4.2, 3.6, 1.5, t("acrescento\nM' = 13", "appended\nM' = 13"), fill=PINK, edge=RED, color=RED, bold=True, fs=FS - 2)
arrow(ax, 17.0, 2.0, 21.0, 2.0, color=RED)
arrow(ax, 19.0, 3.45, 19.0, 2.15, color=RED)
ax.text(19.0, 2.0, "+", ha="center", va="center", fontsize=FS + 4, color=RED,
        fontweight="bold", bbox=dict(boxstyle="circle", fc="white", ec=RED, lw=2))
box(ax, 22.0, 2.0, 2.0, 1.2, "62", fill=RED, edge=RED, color="white", bold=True, fs=FS + 2, round_=True)
ax.text(23.4, 2.0, t("= H(K ‖ M ‖ M')\nmarca válida para\nM ‖ M' = 42 ‖ 13",
                     "= H(K ‖ M ‖ M')\nvalid tag for\nM ‖ M' = 42 ‖ 13"),
        ha="left", va="center", fontsize=FS - 2, color=RED, fontweight="bold")
ax.text(22.0, 9.3, t("estado_atual ← (estado_anterior + valor) mod 100", "current_state ← (previous_state + value) mod 100"),
        ha="center", fontsize=FS - 1, color="#555", style="italic")
save(fig, "fig-05-extensao")

# ---------------------------------------------------------------------------
# 10b. H(M || K): duas mensagens com o mesmo estado antes de a chave entrar
# ---------------------------------------------------------------------------
fig, ax = new_ax(14.6, 6.2, 31.4, 13.4)
ax.set_ylim(-0.4, 13.0)
ax.text(31.0, 12.3, t("estado_atual ← (estado_anterior + valor) mod 100",
                      "current_state ← (previous_state + value) mod 100"),
        ha="right", fontsize=FS - 1, color="#555", style="italic")


def sufixo_row(y, label, vals, up):
    ax.text(0.3, y + (2.9 if up else -3.4), label, fontsize=FS, color=DARK,
            fontweight="bold")
    states = ["0", str(vals[0]), str(vals[0] + vals[1])]
    xs = (2.0, 8.0, 14.0)
    for i, (sx, sv) in enumerate(zip(xs, states)):
        box(ax, sx, y, 2.0, 1.2, sv, fill=GREY, edge=DARK, bold=True,
            fs=FS + 2, round_=True)
        cx = sx + 3.0
        ax.plot([sx + 1.0, cx - 0.45], [y, y], color=DARK, lw=2.2, zorder=1)
        arrow(ax, cx + 0.45, y, sx + 5.0, y)
        ax.text(cx, y, "+", ha="center", va="center", fontsize=FS + 4,
                color=DARK, fontweight="bold",
                bbox=dict(boxstyle="circle", fc="white", ec=DARK, lw=2))
        if i < 2:
            lab, bg, col = str(vals[i]), PINK, RED
        else:
            lab, bg, col = "K = 7", GREENBG, GREEN
        by = y + 1.9 if up else y - 1.9
        box(ax, cx, by, 2.4, 1.0, lab, fill=bg, edge=col, color=col, bold=True,
            fs=FS - 1)
        if up:
            arrow(ax, cx, by - 0.5, cx, y + 0.5)
        else:
            arrow(ax, cx, by + 0.5, cx, y - 0.5)
    box(ax, 20.0, y, 2.0, 1.2, str((vals[0] + vals[1] + 7) % 100), fill=DARK,
        edge=DARK, color="white", bold=True, fs=FS + 2, round_=True)


sufixo_row(9.0, t("M₁ = «pagar 10 € ao Darth»", "M₁ = 'pay Darth 10 €'"), (10, 20), True)
sufixo_row(4.0, t("M₂ = «pagar 10 000 € ao Darth»", "M₂ = 'pay Darth 10,000 €'"), (25, 5), False)
# o mesmo estado antes de K
ax.add_patch(Rectangle((12.2, 3.1), 3.6, 6.8, facecolor="none", edgecolor=RED,
                       lw=2.4, ls="--", zorder=4))
ax.text(14.0, 6.5, t("mesmo\nestado", "same\nstate"), ha="center",
        va="center", fontsize=FS - 2, color=RED, fontweight="bold")
ax.add_patch(Rectangle((18.2, 3.1), 3.6, 6.8, facecolor="none", edgecolor=RED,
                       lw=2.4, ls="--", zorder=4))
ax.text(20.0, 6.5, t("mesma\nmarca", "same\ntag"), ha="center",
        va="center", fontsize=FS - 2, color=RED, fontweight="bold")
ax.text(22.3, 9.0, t("= H(M₁ ‖ K)", "= H(M₁ ‖ K)"), ha="left", va="center",
        fontsize=FS, color=DARK, fontweight="bold")
ax.text(22.3, 4.0, t("= H(M₂ ‖ K)", "= H(M₂ ‖ K)"), ha="left", va="center",
        fontsize=FS, color=DARK, fontweight="bold")
save(fig, "fig-05-sufixo")

# ---------------------------------------------------------------------------
# 11. Construção do HMAC
# ---------------------------------------------------------------------------
fig, ax = new_ax(13, 4.0, 26, 8.0)
ax.set_ylim(2.4, 10.2)
ax.text(0.3, 9.4, t("1.º " + it("hash", True) + " (interior)", "1st hash (inner)"), fontsize=FS + 1,
        color=RED, fontweight="bold")
box(ax, 3.0, 7.6, 4.2, 1.2, "K' ⊕ ipad", fill=GREENBG, edge=GREEN, color=GREEN, bold=True)
ax.text(5.6, 7.6, "‖", ha="center", va="center", fontsize=FS + 6, color=DARK)
box(ax, 8.4, 7.6, 4.2, 1.2, t("mensagem M", "message M"), fill=PINK, bold=True)
arrow(ax, 10.5, 7.6, 12.2, 7.6)
hbox(ax, 12.9, 7.6, s=1.3, fs=FS + 3)
arrow(ax, 13.55, 7.6, 15.4, 7.6)
box(ax, 17.6, 7.6, 4.4, 1.2, t(it("hash", True) + " interior", "inner hash"), fill="white", bold=True)
poly(ax, [(17.6, 7.0), (17.6, 5.6), (9.0, 5.6), (9.0, 3.9)])
ax.text(0.3, 5.0, t("2.º " + it("hash", True) + " (exterior)", "2nd hash (outer)"), fontsize=FS + 1,
        color=RED, fontweight="bold")
box(ax, 3.0, 3.3, 4.2, 1.2, "K' ⊕ opad", fill=GREENBG, edge=GREEN, color=GREEN, bold=True)
ax.text(5.6, 3.3, "‖", ha="center", va="center", fontsize=FS + 6, color=DARK)
box(ax, 8.4, 3.3, 4.2, 1.2, t(it("hash", True) + " interior", "inner hash"), fill="white", bold=True)
arrow(ax, 10.5, 3.3, 12.2, 3.3)
hbox(ax, 12.9, 3.3, s=1.3, fs=FS + 3)
arrow(ax, 13.55, 3.3, 15.4, 3.3)
box(ax, 17.6, 3.3, 4.4, 1.2, "HMAC(K, M)", fill=DARK, edge=DARK, color="white", bold=True)
save(fig, "fig-05-hmac")
print("ok", OUT)
