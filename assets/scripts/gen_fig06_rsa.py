"""Figuras da Aula 06 / Cap06 (criptografia assimétrica e RSA).

Uso (a partir da raiz do projeto):
    python assets/scripts/gen_fig06_rsa.py        -> assets/images/fig-06-*.png
    python assets/scripts/gen_fig06_rsa.py --en   -> en/assets/images/fig-06-*-en.png

Convenção de cores: chave pública a verde, chave privada a carmesim.
"""
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
FS = 18
BH = 1.8  # altura das caixas

matplotlib.rcParams.update({
    "mathtext.fontset": "custom",
    "mathtext.rm": "DejaVu Sans",
    "mathtext.it": "DejaVu Sans:italic",
    "mathtext.bf": "DejaVu Sans:bold",
})


def t(pt, en):
    return en if EN else pt


def new_ax(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def fit(ax, tx, width):
    """Reduz a letra até o texto caber em `width` (unidades dos dados)."""
    r = ax.figure.canvas.get_renderer()
    x0 = ax.transData.transform((0, 0))[0]
    avail = ax.transData.transform((width, 0))[0] - x0
    while tx.get_window_extent(r).width > avail and tx.get_fontsize() > 8:
        tx.set_fontsize(tx.get_fontsize() - 0.5)


def box(ax, cx, cy, w, h, text, fill="white", edge=DARK, color=DARK, fs=FS,
        bold=False, round_=True, lw=2.2):
    if round_:
        p = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                           boxstyle="round,pad=0,rounding_size=0.25",
                           facecolor=fill, edgecolor=edge, lw=lw, zorder=2)
    else:
        p = Rectangle((cx - w / 2, cy - h / 2), w, h, facecolor=fill,
                      edgecolor=edge, lw=lw, zorder=2)
    ax.add_patch(p)
    if "\n" in text:
        fs = min(fs, FS - 2)
    tx = ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=color,
                 fontweight="bold" if bold else "normal", zorder=3,
                 multialignment="center")
    fit(ax, tx, w - 0.3)
    return tx


def arrow(ax, x0, y0, x1, y1, color=DARK, lw=2.2):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=20, shrinkA=0, shrinkB=0),
                zorder=1)


def label(ax, x, y, text, color=DARK, fs=FS - 2, bold=False, style="normal"):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color,
            fontweight="bold" if bold else "normal", fontstyle=style,
            multialignment="center")


def save(fig, name):
    fig.savefig(OUT / f"{name}{SUF}.png", bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


def key_style(kind):
    """kind = 'pub' | 'priv' -> (preenchimento, contorno)."""
    return (GREENBG, GREEN) if kind == "pub" else (PINK, RED)


def chain(ax, y, steps, x0=0.2, gap=0.9):
    """Desenha uma cadeia horizontal de caixas ligadas por setas.

    steps: lista de (largura, texto, kind) com kind em
    None (dado), 'pub' ou 'priv' (operação com essa chave),
    'net' (canal: só uma seta comprida com rótulo).
    Devolve a lista de centros x.
    """
    xs = []
    x = x0
    prev_right = None
    for w, text, kind in steps:
        if kind == "net":
            x_end = x + w
            arrow(ax, prev_right, y, x_end, y)
            label(ax, (prev_right + x_end) / 2, y + 0.55, text, style="italic")
            prev_right = None
            x = x_end
            xs.append(None)
            continue
        if prev_right is not None:
            arrow(ax, prev_right, y, x, y)
        cx = x + w / 2
        if kind is None:
            box(ax, cx, y, w, BH, text, fill=GREY, edge=DARK)
        else:
            fill, edge = key_style(kind)
            box(ax, cx, y, w, BH, text, fill=fill, edge=edge, lw=2.6)
        xs.append(cx)
        prev_right = x + w
        x = x + w + gap
    return xs


def legend(ax, x, y):
    for i, (kind, txt) in enumerate([("pub", t("chave pública", "public key")),
                                     ("priv", t("chave privada", "private key"))]):
        fill, edge = key_style(kind)
        xx = x + i * 5.2
        ax.add_patch(Rectangle((xx, y - 0.3), 0.9, 0.6, facecolor=fill,
                               edgecolor=edge, lw=2.4))
        ax.text(xx + 1.2, y, txt, ha="left", va="center", fontsize=FS - 3, color=DARK)


# ---------------------------------------------------------------------------
# 1. Confidencialidade: cifra-se com a chave pública do destinatário
# ---------------------------------------------------------------------------
def fig_um_esquema(nome, enc, dec, kind_enc, kind_dec, quem_enc, quem_dec, nota):
    fig, ax = new_ax(13, 3.8, 26, 7.6)
    xs = chain(ax, 3.2, [
        (3.6, t("X\n(mensagem)", "X\n(message)"), None),
        (3.8, enc, kind_enc),
        (1.4, "Y", None),
        (5.6, t("envia", "sends"), "net"),
        (3.8, dec, kind_dec),
        (3.6, t("X\n(mensagem)", "X\n(message)"), None),
    ])
    label(ax, xs[1], 5.0, quem_enc, color=key_style(kind_enc)[1], bold=True)
    label(ax, xs[4], 5.0, quem_dec, color=key_style(kind_dec)[1], bold=True)
    label(ax, 12.2, 1.1, nota, color=DARK, fs=FS - 1, bold=True)
    label(ax, xs[0], 6.6, "Alice", fs=FS, bold=True)
    label(ax, xs[5], 6.6, "Bob", fs=FS, bold=True)
    save(fig, nome)


fig_um_esquema(
    "fig-06-confidencialidade",
    t("cifra com\n$PU_b$", "encrypt with\n$PU_b$"),
    t("decifra com\n$PR_b$", "decrypt with\n$PR_b$"),
    "pub", "priv",
    t("chave pública do Bob", "Bob's public key"),
    t("chave privada do Bob", "Bob's private key"),
    t("Só o Bob consegue decifrar: só ele tem $PR_b$",
      "Only Bob can decrypt: only he holds $PR_b$"),
)

fig_um_esquema(
    "fig-06-autenticacao",
    t("cifra com\n$PR_a$", "encrypt with\n$PR_a$"),
    t("decifra com\n$PU_a$", "decrypt with\n$PU_a$"),
    "priv", "pub",
    t("chave privada da Alice", "Alice's private key"),
    t("chave pública da Alice", "Alice's public key"),
    t("Qualquer um decifra, mas só a Alice podia ter cifrado",
      "Anyone can decrypt, but only Alice could have encrypted"),
)

# ---------------------------------------------------------------------------
# 2. Os dois esquemas combinados
# ---------------------------------------------------------------------------
fig, ax = new_ax(12, 4.4, 24, 8.8)
y_top, y_bot = 6.0, 2.0
# Alice (linha de cima, da esquerda para a direita)
xs = chain(ax, y_top, [
    (1.6, "X", None),
    (3.6, t("cifra com\n$PR_a$", "encrypt with\n$PR_a$"), "priv"),
    (1.6, "Y", None),
    (3.6, t("cifra com\n$PU_b$", "encrypt with\n$PU_b$"), "pub"),
    (1.6, "Z", None),
], x0=0.6)
label(ax, (xs[0] + xs[4]) / 2, 7.9, t("Alice: 1.º assina, 2.º tranca para o Bob",
                                      "Alice: 1st signs, 2nd locks for Bob"), bold=True)
# canal
zx = xs[4]
ax.plot([zx + 0.8, 21.6], [y_top, y_top], color=DARK, lw=2.2)
label(ax, 17.6, y_top + 0.55, t("envia Z", "sends Z"), style="italic")
arrow(ax, 21.6, y_top, 21.6, y_bot + BH / 2)
# Bob (linha de baixo, da direita para a esquerda)
bob = [(1.6, "Z", None),
       (3.6, t("decifra com\n$PR_b$", "decrypt with\n$PR_b$"), "priv"),
       (1.6, "Y", None),
       (3.6, t("decifra com\n$PU_a$", "decrypt with\n$PU_a$"), "pub"),
       (1.6, "X", None)]
x = 22.4
cxs = []
for w, text, kind in bob:
    cx = x - w / 2
    if kind is None:
        box(ax, cx, y_bot, w, BH, text, fill=GREY)
    else:
        fill, edge = key_style(kind)
        box(ax, cx, y_bot, w, BH, text, fill=fill, edge=edge, lw=2.6)
    cxs.append(cx)
    x = x - w - 0.9
for (w0, _, _), c0, c1, (w1, _, _) in zip(bob[:-1], cxs[:-1], cxs[1:], bob[1:]):
    arrow(ax, c0 - w0 / 2, y_bot, c1 + w1 / 2, y_bot)
label(ax, 13.0, 0.35, t("Bob: 1.º destranca, 2.º confirma que veio da Alice",
                                        "Bob: 1st unlocks, 2nd checks it came from Alice"),
      bold=True)
legend(ax, 16.4, 7.9)
save(fig, "fig-06-combinado")

# ---------------------------------------------------------------------------
# 3. Exemplo numérico: M = 88, chaves (7, 187) e (23, 187)
# ---------------------------------------------------------------------------
fig, ax = new_ax(12.4, 3.4, 24.8, 6.8)
xs = chain(ax, 3.2, [
    (2.2, "M = 88", None),
    (4.6, r"$88^{7}$ mod 187", "pub"),
    (2.2, "C = 11", None),
    (3.4, t("envia", "sends"), "net"),
    (4.6, r"$11^{23}$ mod 187", "priv"),
    (2.2, "M = 88", None),
])
label(ax, xs[1], 4.75, t("chave pública (7, 187)", "public key (7, 187)"),
      color=GREEN, bold=True)
label(ax, xs[4], 4.75, t("chave privada (23, 187)", "private key (23, 187)"),
      color=RED, bold=True)
label(ax, xs[0], 1.6, t("Alice", "Alice"), bold=True)
label(ax, xs[5], 1.6, t("Bob", "Bob"), bold=True)
save(fig, "fig-06-exemplo-88")

# ---------------------------------------------------------------------------
# 4. Na prática: o RSA transporta a chave do AES (esquema híbrido)
# ---------------------------------------------------------------------------
fig, ax = new_ax(14.4, 5.0, 28.8, 10)
y1, y2 = 7.2, 2.6
# linha 1: a chave K vai cifrada com RSA
xs1 = chain(ax, y1, [
    (3.8, t("chave K\n(256 bits)", "key K\n(256 bits)"), None),
    (3.8, t("RSA: cifra\ncom $PU_b$", "RSA: encrypt\nwith $PU_b$"), "pub"),
    (2.6, "[K]", None),
    (4.2, t("envia", "sends"), "net"),
    (3.8, t("RSA: decifra\ncom $PR_b$", "RSA: decrypt\nwith $PR_b$"), "priv"),
    (2.8, "K", None),
], x0=0.4)
# linha 2: os dados vão cifrados com AES e a chave K
xs2 = chain(ax, y2, [
    (3.8, t("ficheiro\n(10 MB)", "file\n(10 MB)"), None),
    (3.8, t("AES: cifra\ncom K", "AES: encrypt\nwith K"), None),
    (2.6, t("cifrado", "encrypted"), None),
    (4.2, t("envia", "sends"), "net"),
    (3.8, t("AES: decifra\ncom K", "AES: decrypt\nwith K"), None),
    (2.8, t("ficheiro", "file"), None),
], x0=0.4)
# K alimenta as duas operações AES
for xa in (xs2[1], xs2[4]):
    src = xs1[0] if xa == xs2[1] else xs1[5]
    ax.plot([src, src], [y1 - BH / 2, (y1 + y2) / 2], color=RED, lw=2.0, ls="--")
    ax.plot([src, xa], [(y1 + y2) / 2, (y1 + y2) / 2], color=RED, lw=2.0, ls="--")
    arrow(ax, xa, (y1 + y2) / 2, xa, y2 + BH / 2, color=RED, lw=2.0)
label(ax, 2.2, 9.3, "Alice", bold=True, fs=FS)
label(ax, 27.0, 9.3, "Bob", bold=True, fs=FS)
label(ax, 14.4, 9.3, t("RSA: só 32 bytes, uma única vez", "RSA: only 32 bytes, once"),
      color=RED, bold=True)
label(ax, 14.4, 0.7, t("AES: os dados todos, depressa", "AES: all the data, fast"),
      color=DARK, bold=True)
save(fig, "fig-06-hibrido")


# ---------------------------------------------------------------------------
# 5. Estrutura do OAEP (PKCS#1 v2.2, RFC 8017), chave de 2048 bits, SHA-256
# ---------------------------------------------------------------------------
def xor(ax, cx, cy, r=0.45):
    ax.add_patch(plt.Circle((cx, cy), r, facecolor="white", edgecolor=DARK,
                            lw=2.2, zorder=3))
    ax.plot([cx - r, cx + r], [cy, cy], color=DARK, lw=2.2, zorder=4)
    ax.plot([cx, cx], [cy - r, cy + r], color=DARK, lw=2.2, zorder=4)


def mgf(ax, cx, cy):
    box(ax, cx, cy, 3.0, 1.5, t("MGF1\n(" + r"$\mathit{hash}$" + ")", "MGF1\n(hash)"),
        fill=DARK, edge=DARK, color="white", fs=FS - 2, bold=True)


fig, ax = new_ax(8.6, 6.2, 20, 14.4)
xs, xd = 4.4, 13.0          # colunas da semente e do bloco de dados
y_top, y_m1, y_m2, y_bot = 12.2, 9.2, 5.6, 2.4
# linha de cima: semente aleatória e bloco de dados DB
box(ax, xs, y_top, 4.6, 1.6, t("semente\n(aleatória)", "seed\n(random)"),
    fill="white")
box(ax, xd, y_top, 11.0, 1.6,
    t("DB = " + r"$\mathit{hash}$" + "(L) ‖ 00…00 ‖ 01 ‖ «S»",
      "DB = hash(L) ‖ 00…00 ‖ 01 ‖ 'Y'"), fill=GREY)
label(ax, xs, y_top + 1.25, "32 bytes", fs=FS - 4)
label(ax, xd, y_top + 1.25, "223 bytes", fs=FS - 4)
# 1.º XOR: DB ⊕ MGF1(semente)
ax.plot([xs, xs], [y_top - 0.8, y_m2 + 0.45], color=DARK, lw=2.2, zorder=1)
ax.plot([xs, 8.5 - 1.5], [y_m1, y_m1], color=DARK, lw=2.2, zorder=1)
mgf(ax, 8.5, y_m1)
arrow(ax, 8.5 + 1.5, y_m1, xd - 0.45, y_m1)
arrow(ax, xd, y_top - 0.8, xd, y_m1 + 0.45)
xor(ax, xd, y_m1)
# 2.º XOR: semente ⊕ MGF1(DB mascarado)
arrow(ax, xd, y_m1 - 0.45, xd, y_bot + 0.8)
ax.plot([xd, 8.5 + 1.5], [y_m2, y_m2], color=DARK, lw=2.2, zorder=1)
mgf(ax, 8.5, y_m2)
arrow(ax, 8.5 - 1.5, y_m2, xs + 0.45, y_m2)
xor(ax, xs, y_m2)
arrow(ax, xs, y_m2 - 0.45, xs, y_bot + 0.8)
# linha de baixo: X = 00 ‖ semente mascarada ‖ DB mascarado
box(ax, 1.5, y_bot, 1.2, 1.6, "00", fill=GREY, round_=False)
box(ax, xs, y_bot, 4.6, 1.6, t("semente\nmascarada", "masked\nseed"),
    fill="white", round_=False)
box(ax, 12.6, y_bot, 11.8, 1.6, t("DB mascarado", "masked DB"), fill=GREY,
    round_=False)
label(ax, 10.0, 0.6,
      t("X  (256 bytes, lido como um número)   →   C = $X^e$ mod n",
        "X  (256 bytes, read as one number)   →   C = $X^e$ mod n"),
      bold=True, fs=FS - 1)
label(ax, xd + 2.6, (y_m1 + y_m2) / 2, "⊕ = XOR", fs=FS - 2, color=RED, bold=True)
save(fig, "fig-06-oaep")
