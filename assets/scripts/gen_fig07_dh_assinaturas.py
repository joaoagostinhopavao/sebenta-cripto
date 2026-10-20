"""Figuras da Aula 07 / Cap07 (Diffie-Hellman e assinaturas digitais).

Uso (a partir da raiz do projeto):
    python assets/scripts/gen_fig07_dh_assinaturas.py        -> assets/images/fig-07-*.png
    python assets/scripts/gen_fig07_dh_assinaturas.py --en   -> en/assets/images/fig-07-*-en.png

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
# 1. A analogia das tintas
# ---------------------------------------------------------------------------
YEL, REDP, BLUE = "#f2c230", "#c8323c", "#2f5fb3"
ORA, GRN, BRN = "#e8792a", "#4f9a3c", "#7a4a2a"


def lata(ax, cx, cy, cor, txt, r=0.9):
    ax.add_patch(plt.Circle((cx, cy), r, facecolor=cor, edgecolor=DARK,
                            lw=2.2, zorder=2))
    label(ax, cx, cy - r - 0.55, txt, fs=FS - 4)


fig, ax = new_ax(11, 8.4, 22, 16.8)
xa, xb, xm = 4.0, 18.0, 11.0
label(ax, xa, 16.0, "Alice", fs=FS, bold=True)
label(ax, xb, 16.0, "Bob", fs=FS, bold=True)
label(ax, xm, 16.0, t("O Darth vê", "Darth sees"), fs=FS - 2, bold=True, color=GREEN)
# 1. cor comum
lata(ax, xa - 1.3, 13.4, YEL, t("comum", "common"))
lata(ax, xb - 1.3, 13.4, YEL, t("comum", "common"))
lata(ax, xm, 13.4, YEL, t("comum", "common"))
# 2. cores secretas
lata(ax, xa + 1.3, 13.4, REDP, t("secreta", "secret"))
lata(ax, xb + 1.3, 13.4, BLUE, t("secreta", "secret"))
# 3. misturas enviadas
arrow(ax, xa, 11.9, xa, 10.4)
arrow(ax, xb, 11.9, xb, 10.4)
lata(ax, xa, 9.4, ORA, t("comum + secreta", "common + secret"))
lata(ax, xb, 9.4, GRN, t("comum + secreta", "common + secret"))
lata(ax, xm - 1.3, 9.4, ORA, "")
lata(ax, xm + 1.3, 9.4, GRN, "")
label(ax, xm, 7.95, t("as duas misturas", "both mixtures"), fs=FS - 4)
# 4. troca
arrow(ax, xa + 1.1, 8.9, xb - 1.6, 5.6, color=ORA, lw=2.6)
arrow(ax, xb - 1.1, 8.9, xa + 1.6, 5.6, color=GRN, lw=2.6)
label(ax, xm, 6.0, t("trocam as misturas", "they swap the mixtures"),
      fs=FS - 3, style="italic")
# 5. cada um junta a sua cor secreta
lata(ax, xa - 1.3, 4.6, GRN, t("do Bob", "Bob's"), r=0.75)
label(ax, xa, 4.6, "+", fs=FS)
lata(ax, xa + 1.1, 4.6, REDP, t("secreta", "secret"), r=0.75)
lata(ax, xb - 1.1, 4.6, ORA, t("da Alice", "Alice's"), r=0.75)
label(ax, xb, 4.6, "+", fs=FS)
lata(ax, xb + 1.3, 4.6, BLUE, t("secreta", "secret"), r=0.75)
arrow(ax, xa, 3.1, xa, 2.0)
arrow(ax, xb, 3.1, xb, 2.0)
lata(ax, xa, 1.0, BRN, "")
lata(ax, xb, 1.0, BRN, "")
label(ax, xm, 1.0, t("a mesma cor final:\namarelo + vermelho + azul",
                     "the same final colour:\nyellow + red + blue"),
      fs=FS - 3, bold=True, color=RED)
save(fig, "fig-07-tintas")


# ---------------------------------------------------------------------------
# 2. O algoritmo de Diffie-Hellman (genérico)
# ---------------------------------------------------------------------------
def dh_diagrama(nome, vals):
    """vals: dicionário com os textos de cada caixa.

    Se vals tiver "final", acrescenta por baixo um par de caixas iguais
    (a mesma chave dos dois lados).
    """
    final = vals.get("final")
    o = 2.6 if final else 0.0          # deslocamento vertical de tudo o que fica acima
    fig, ax = new_ax(12, (15.2 + o) / 2, 24, 15.2 + o)
    xa, xb, xm = 4.2, 19.8, 12.0
    W = 6.4
    label(ax, xa, 14.4 + o, "Alice", fs=FS, bold=True)
    label(ax, xb, 14.4 + o, "Bob", fs=FS, bold=True)
    label(ax, xm, 14.4 + o, t("Canal aberto (o Darth vê)", "Open channel (Darth sees)"),
          fs=FS - 3, bold=True, color=GREEN)
    ax.plot([xm, xm], [2.9, 13.6 + o], color=GREEN, lw=1.5, ls=(0, (4, 4)), zorder=0)
    # 1. parâmetros públicos
    box(ax, xm, 12.4 + o, 7.6, 1.5, vals["gp"], fill=GREY)
    arrow(ax, xm - 3.8, 12.4 + o, xa + W / 2, 12.4 + o)
    arrow(ax, xm + 3.8, 12.4 + o, xb - W / 2, 12.4 + o)
    # 2. segredos
    fill, edge = key_style("priv")
    box(ax, xa, 9.8 + o, W, 1.5, vals["x"], fill=fill, edge=edge, lw=2.6)
    box(ax, xb, 9.8 + o, W, 1.5, vals["y"], fill=fill, edge=edge, lw=2.6)
    # 3. valores públicos
    arrow(ax, xa, 9.05 + o, xa, 7.95 + o)
    arrow(ax, xb, 9.05 + o, xb, 7.95 + o)
    fill, edge = key_style("pub")
    box(ax, xa, 7.2 + o, W, 1.5, vals["A"], fill=fill, edge=edge, lw=2.6)
    box(ax, xb, 7.2 + o, W, 1.5, vals["B"], fill=fill, edge=edge, lw=2.6)
    # 4. troca em claro
    arrow(ax, xa + W / 2, 7.0 + o, xb - W / 2, 4.6 + o)
    arrow(ax, xb - W / 2, 7.0 + o, xa + W / 2, 4.6 + o)
    ax.text(xm, 8.5 + o, vals["envia"], ha="center", va="center", fontsize=FS - 3,
            color=DARK, fontstyle="italic", zorder=3,
            bbox=dict(facecolor="white", edgecolor="none", pad=3))
    # 5. cada um calcula a chave
    fill, edge = key_style("priv")
    box(ax, xa, 3.9 + o, W, 1.5, vals["Ka"], fill=fill, edge=edge, lw=2.6)
    box(ax, xb, 3.9 + o, W, 1.5, vals["Kb"], fill=fill, edge=edge, lw=2.6)
    # 6. a mesma chave dos dois lados
    if final:
        arrow(ax, xa, 3.15 + o, xa, 4.65)
        arrow(ax, xb, 3.15 + o, xb, 4.65)
        box(ax, xa, 3.9, W, 1.5, final, fill=fill, edge=edge, lw=3.4, bold=True)
        box(ax, xb, 3.9, W, 1.5, final, fill=fill, edge=edge, lw=3.4, bold=True)
    label(ax, xm, 2.1, vals["nota"], fs=FS - 2, bold=True, color=RED)
    # legenda
    for k, (kind, txt) in enumerate([("pub", t("público", "public")),
                                     ("priv", t("secreto", "secret"))]):
        fill, edge = key_style(kind)
        xx = 7.6 + k * 5.0
        ax.add_patch(Rectangle((xx, 0.2), 0.9, 0.6, facecolor=fill,
                               edgecolor=edge, lw=2.4))
        ax.text(xx + 1.2, 0.5, txt, ha="left", va="center", fontsize=FS - 3,
                color=DARK)
    save(fig, nome)


dh_diagrama("fig-07-dh", {
    "gp": t("$g$ e $p$ (públicos)", "$g$ and $p$ (public)"),
    "x": t("escolhe $x$ (secreto)", "chooses $x$ (secret)"),
    "y": t("escolhe $y$ (secreto)", "chooses $y$ (secret)"),
    "A": "$A = g^x \\ \\mathrm{mod}\\ p$",
    "B": "$B = g^y \\ \\mathrm{mod}\\ p$",
    "envia": t("trocam $A$ e $B$", "they swap $A$ and $B$"),
    "Ka": "$K = B^x \\ \\mathrm{mod}\\ p$",
    "Kb": "$K = A^y \\ \\mathrm{mod}\\ p$",
    "final": "$K = g^{xy} \\ \\mathrm{mod}\\ p$",
    "nota": t("Os dois ficam com a mesma chave, que nunca viajou",
              "Both end up with the same key, which never travelled"),
})

dh_diagrama("fig-07-dh-exemplo", {
    "gp": "$g = 5$, $p = 23$",
    "x": "$x = 6$",
    "y": "$y = 15$",
    "A": "$A = 5^{6} \\ \\mathrm{mod}\\ 23 = 8$",
    "B": "$B = 5^{15} \\ \\mathrm{mod}\\ 23 = 19$",
    "envia": t("trocam 8 e 19", "they swap 8 and 19"),
    "Ka": "$K = 5^{6 \\cdot 15} \\ \\mathrm{mod}\\ 23$",
    "Kb": "$K = 5^{6 \\cdot 15} \\ \\mathrm{mod}\\ 23$",
    "final": "2",
    "nota": t("Os dois ficam com a mesma chave, $K = 2$",
              "Both end up with the same key, $K = 2$"),
})


# ---------------------------------------------------------------------------
# 3. Ataque do intermediário (exemplo geral do deck, p. 118)
# ---------------------------------------------------------------------------
def seta_rotulo(ax, x0, x1, y, txt, cor=DARK):
    arrow(ax, x0, y, x1, y, color=cor, lw=3)
    label(ax, (x0 + x1) / 2, y + 0.75, txt, fs=FS + 6, color=cor)


fig, ax = new_ax(13, 6.7, 26, 13.4)
xa, xd, xb = 1.8, 13.0, 24.2
# linha de cima: sem ataque
label(ax, 13.0, 12.9, t("Sem ataque", "Without the attack"), fs=FS + 4, bold=True,
      color=GREEN)
label(ax, xa, 9.9, "Alice", fs=FS + 6, bold=True)
label(ax, xb, 9.9, "Bob", fs=FS + 6, bold=True)
seta_rotulo(ax, xa + 2.6, xb - 2.6, 10.6, "$PU_a$", cor=GREEN)
seta_rotulo(ax, xb - 2.6, xa + 2.6, 8.6, "$E(PU_a, k)$")
ax.plot([1, 25], [7.2, 7.2], color=GREY, lw=2)
# linha de baixo: com o Darth no meio
label(ax, 13.0, 6.3, t("Com o Darth no meio", "With Darth in the middle"),
      fs=FS + 4, bold=True, color=RED)
label(ax, xa, 3.4, "Alice", fs=FS + 6, bold=True)
label(ax, xd, 3.4, "Darth", fs=FS + 6, bold=True, color=RED)
label(ax, xb, 3.4, "Bob", fs=FS + 6, bold=True)
seta_rotulo(ax, xa + 2.6, xd - 2.6, 4.1, "$PU_a$", cor=GREEN)
seta_rotulo(ax, xd + 2.6, xb - 2.6, 4.1, "$PU_d$", cor=RED)
seta_rotulo(ax, xb - 2.6, xd + 2.6, 2.1, "$E(PU_d, k)$")
seta_rotulo(ax, xd - 2.6, xa + 2.6, 2.1, "$E(PU_a, k)$")
label(ax, xd, 0.6, t("o Darth decifra com $PR_d$ e fica com $k$",
                     "Darth decrypts with $PR_d$ and keeps $k$"),
      fs=FS + 3, style="italic", color=RED)
save(fig, "fig-07-mitm")


# ---------------------------------------------------------------------------
# 4. Assinar o hash da mensagem (esquema (a) do deck, Stallings)
# ---------------------------------------------------------------------------
HS = r"$\mathit{hash}$" if not EN else "hash"


def assinatura(nome, cifrar):
    fig, ax = new_ax(13, 7.0 if cifrar else 5.6, 26, 14.0 if cifrar else 11.2)
    top = 13.3 if cifrar else 10.5
    label(ax, 5.0, top, "Alice", fs=FS, bold=True)
    label(ax, 21.0, top, "Bob", fs=FS, bold=True)
    y1, y2 = top - 3.4, top - 6.6
    # Alice: M -> H -> cifra com PR_a -> assinatura
    box(ax, 1.6, y1, 2.4, 1.5, "M", fill=GREY)
    arrow(ax, 1.6, y1 - 0.75, 1.6, y2 + 0.75)
    box(ax, 1.6, y2, 2.4, 1.5, "M", fill=GREY)
    arrow(ax, 2.8, y1, 4.0, y1)
    box(ax, 5.0, y1, 2.0, 1.5, "H", fill="white")
    arrow(ax, 6.0, y1, 7.0, y1)
    fp, ep = key_style("priv")
    box(ax, 9.0, y1, 4.0, 1.5, t("cifra com\n$PR_a$", "encrypt with\n$PR_a$"),
        fill=fp, edge=ep, lw=2.6)
    arrow(ax, 9.0, y1 - 0.75, 9.0, y2 + 0.75)
    box(ax, 9.0, y2, 4.0, 1.5, t("assinatura", "signature"), fill=GREY, bold=True)
    label(ax, 5.3, y2, "+", fs=FS + 2, bold=True)
    x_send0 = 11.0
    if cifrar:
        y3 = y2 - 3.0
        ax.plot([5.3, 5.3], [y2 - 0.75, y3 + 0.75], color=DARK, lw=2.2)
        box(ax, 5.3, y3, 5.4, 1.5, t("AES: cifra\ncom $K$", "AES: encrypt\nwith $K$"),
            fill="white")
        arrow(ax, 8.0, y3, 17.0, y3)
        label(ax, 12.5, y3 + 0.55, t("envia", "sends"), style="italic")
        box(ax, 19.7, y3, 5.4, 1.5, t("AES: decifra\ncom $K$", "AES: decrypt\nwith $K$"),
            fill="white")
        arrow(ax, 19.7, y3 + 0.75, 19.7, y2 - 0.75)
        label(ax, 12.5, y3 - 1.4, t("Só quem tem $K$ lê M e a assinatura",
                                    "Only whoever holds $K$ can read M and the signature"),
              fs=FS - 3, color=RED, bold=True)
    else:
        arrow(ax, x_send0, y2, 17.4, y2)
        label(ax, 14.2, y2 + 0.55, t("envia M + assinatura", "sends M + signature"),
              style="italic", fs=FS - 3)
    # Bob: M -> H ; assinatura -> decifra com PU_a ; compara
    box(ax, 18.6, y2, 2.4, 1.5, "M", fill=GREY)
    box(ax, 22.6, y2, 4.0, 1.5, t("assinatura", "signature"), fill=GREY, bold=True)
    arrow(ax, 18.6, y2 + 0.75, 18.6, y1 - 0.75)
    box(ax, 18.6, y1, 2.0, 1.5, "H", fill="white")
    fu, eu = key_style("pub")
    arrow(ax, 22.6, y2 + 0.75, 22.6, y1 - 0.75)
    box(ax, 22.6, y1, 4.0, 1.5, t("decifra com\n$PU_a$", "decrypt with\n$PU_a$"),
        fill=fu, edge=eu, lw=2.6)
    arrow(ax, 18.6, y1 + 0.75, 19.9, y1 + 1.6)
    arrow(ax, 22.6, y1 + 0.75, 21.3, y1 + 1.6)
    label(ax, 20.6, y1 + 2.05, t("iguais?", "equal?"), fs=FS - 1, bold=True, color=RED)
    if not cifrar:
        label(ax, 13.0, 1.6, t("Qualquer pessoa verifica; só a Alice podia ter assinado",
                               "Anyone can verify; only Alice could have signed"),
              fs=FS - 2, bold=True, color=RED)
    save(fig, nome)


assinatura("fig-07-assinar", False)
assinatura("fig-07-assinar-cifrar", True)


# ---------------------------------------------------------------------------
# 5. DSA: assinar e verificar (adaptado de Stallings, Fig. 13.4)
# ---------------------------------------------------------------------------
MOD = "\\ \\mathrm{mod}\\ "


def linha(ax, xs, ys, color=DARK, lw=2.2):
    ax.plot(xs, ys, color=color, lw=lw, zorder=1, solid_capstyle="round")


def ponto(ax, x, y, color=DARK):
    ax.plot([x], [y], "o", color=color, ms=8, zorder=4)


def pilha(ax, x0, w, rotulos):
    """Mensagem com a assinatura (r, s) anexada, como na figura do Stallings."""
    (m, r, s) = rotulos
    box(ax, x0 + w / 2, 8.6, w, 6.0, m, fill=GREY, round_=False, fs=FS + 4, bold=True)
    box(ax, x0 + w / 2, 5.05, w, 1.1, r, fill="white", round_=False, bold=True)
    box(ax, x0 + w / 2, 3.95, w, 1.1, s, fill="white", round_=False, bold=True)


# --- (a) assinar ------------------------------------------------------------
fig, ax = new_ax(13, 6.2, 26, 12.4)
# entradas
label(ax, 0.6, 10.8, "$m$", fs=FS + 2, bold=True)
label(ax, 0.6, 7.0, "$k$", fs=FS + 2, bold=True, color=RED)
label(ax, 0.6, 1.6, "$x$", fs=FS + 2, bold=True, color=RED)
label(ax, 3.4, 0.7, t("chave privada", "private key"), fs=FS - 5, color=RED,
      style="italic")
label(ax, 3.6, 7.6, t("aleatório, só uma vez", "random, used once"), fs=FS - 5,
      color=RED, style="italic")
# M segue para a direita e desce para o hash
arrow(ax, 1.2, 10.8, 22.3, 10.8)
ponto(ax, 2.6, 10.8)
linha(ax, [2.6, 2.6], [10.8, 3.3])
arrow(ax, 2.6, 3.3, 4.0, 3.3)
box(ax, 5.0, 3.3, 2.0, 1.6, "$H$", fill="white", bold=True)
arrow(ax, 6.0, 3.3, 9.0, 3.3)
label(ax, 7.5, 2.7, "$H(m)$", fs=FS - 3)
# k para r, e um ramo para s
arrow(ax, 1.2, 7.0, 10.0, 7.0, color=RED)
ponto(ax, 8.0, 7.0, color=RED)
linha(ax, [8.0, 8.0], [7.0, 4.4], color=RED)
arrow(ax, 8.0, 4.4, 9.0, 4.4, color=RED)
# parâmetros públicos para r
for xx, nome in [(12.5, "$p$"), (14.5, "$q$"), (16.5, "$g$")]:
    label(ax, xx, 9.75, nome, fs=FS, bold=True, color=GREEN)
    arrow(ax, xx, 9.3, xx, 7.9, color=GREEN)
box(ax, 14.5, 7.0, 9.0, 1.8, f"$r = (g^{{k}}{MOD}p){MOD}q$", fill="white")
# r para s
arrow(ax, 14.5, 6.1, 14.5, 4.7)
box(ax, 14.5, 3.8, 11.0, 1.8, f"$s = k^{{-1}}\\,(H(m) + x\\,r){MOD}q$", fill="white")
# q para s
label(ax, 18.0, 0.9, "$q$", fs=FS, bold=True, color=GREEN)
arrow(ax, 18.0, 1.4, 18.0, 2.9, color=GREEN)
# x para s
linha(ax, [1.2, 14.5], [1.6, 1.6], color=RED)
arrow(ax, 14.5, 1.6, 14.5, 2.9, color=RED)
# r e s anexados à mensagem
linha(ax, [19.0, 20.6, 20.6], [7.0, 7.0, 5.05])
arrow(ax, 20.6, 5.05, 22.3, 5.05)
arrow(ax, 20.0, 3.95, 22.3, 3.95)
pilha(ax, 22.3, 3.0, ("$m$", "$r$", "$s$"))
label(ax, 21.8, -0.1, t("adaptado de Stallings (8.ª ed.), Fig. 13.4", "adapted from Stallings (8th ed.), Fig. 13.4"),
      fs=FS - 6, style="italic", color="#666666")
save(fig, "fig-07-dsa-assinar")


# --- (b) verificar ----------------------------------------------------------
fig, ax = new_ax(13, 6.2, 26, 12.4)
pilha(ax, 0.5, 3.0, ("$m$", "$r$", "$s$"))
label(ax, 2.0, 12.0, t("recebido", "received"), fs=FS - 4, style="italic")
# M -> H -> caixa grande
arrow(ax, 3.5, 8.6, 6.0, 8.6)
box(ax, 7.0, 8.6, 2.0, 1.6, "$H$", fill="white", bold=True)
arrow(ax, 8.0, 8.6, 11.0, 8.6)
label(ax, 9.5, 9.2, "$H(m)$", fs=FS - 3)
for xx, nome, cor in [(13.0, "$y$", GREEN), (15.5, "$p$", GREEN), (17.5, "$q$", GREEN),
                      (19.5, "$g$", GREEN)]:
    label(ax, xx, 12.0, nome, fs=FS, bold=True, color=cor)
    arrow(ax, xx, 11.55, xx, 10.3, color=cor)
label(ax, 10.6, 12.0, t("chave pública", "public key"), fs=FS - 5, color=GREEN,
      style="italic")
fill, edge = key_style("pub")
box(ax, 16.5, 8.6, 11.0, 3.4,
    f"$u_1 = H(m)\\,w{MOD}q$\n$u_2 = r\\,w{MOD}q$\n"
    f"$v = (g^{{u_1}}\\,y^{{u_2}}{MOD}p){MOD}q$",
    fill=fill, edge=edge, lw=2.6)
# s -> w -> caixa grande
linha(ax, [3.5, 4.8, 4.8], [3.95, 3.95, 2.0])
arrow(ax, 4.8, 2.0, 6.0, 2.0)
box(ax, 9.0, 2.0, 6.0, 1.6, f"$w = s^{{-1}}{MOD}q$", fill="white")
label(ax, 9.0, 4.35, "$q$", fs=FS, bold=True, color=GREEN)
arrow(ax, 9.0, 3.9, 9.0, 2.8, color=GREEN)
linha(ax, [12.0, 13.0], [2.0, 2.0])
arrow(ax, 13.0, 2.0, 13.0, 6.9)
label(ax, 12.5, 6.3, "$w$", fs=FS - 2)
# r -> caixa grande e -> comparação
linha(ax, [3.5, 22.0], [5.05, 5.05])
ponto(ax, 16.0, 5.05)
arrow(ax, 16.0, 5.05, 16.0, 6.9)
label(ax, 15.5, 6.3, "$r$", fs=FS - 2)
arrow(ax, 22.0, 5.05, 22.0, 3.9)
# v -> comparação
linha(ax, [22.0, 24.2, 24.2], [8.6, 8.6, 3.9])
arrow(ax, 24.2, 4.6, 24.2, 3.9)
label(ax, 24.7, 6.6, "$v$", fs=FS - 2)
box(ax, 23.1, 3.0, 4.4, 1.8, "$v = r$ ?", fill=PINK, edge=RED, color=RED, bold=True,
    lw=2.8)
label(ax, 23.1, 1.4, t("se sim, a assinatura\né válida", "if so, the signature\nis valid"),
      fs=FS - 5, color=RED, bold=True)
label(ax, 21.8, -0.1, t("adaptado de Stallings (8.ª ed.), Fig. 13.4", "adapted from Stallings (8th ed.), Fig. 13.4"),
      fs=FS - 6, style="italic", color="#666666")
save(fig, "fig-07-dsa-verificar")


# --- esquema simplificado (adaptado de Stallings, Fig. 13.2b) -------------
fig, ax = new_ax(14, 4.2, 28, 8.4)
y0 = 4.2
box(ax, 1.5, y0, 2.4, 1.8, "$m$", fill=GREY, fs=FS + 2, bold=True)
arrow(ax, 2.7, y0, 3.8, y0)
fill, edge = key_style("priv")
box(ax, 6.3, y0, 5.0, 2.2, t("Assina com\n$PR_a$ e $k$", "Signs with\n$PR_a$ and $k$"),
    fill=fill, edge=edge, lw=2.6)
label(ax, 6.3, 6.6, t("chave privada da Alice\n+ $k$ aleatório, só uma vez",
                      "Alice's private key\n+ random $k$, used once"),
      fs=FS - 4, color=RED)
arrow(ax, 8.8, y0, 9.9, y0)
box(ax, 11.4, y0, 3.0, 1.8, "$(r, s)$", fill="white", bold=True)
arrow(ax, 12.9, y0, 17.1, y0)
label(ax, 15.0, y0 + 0.6, t("envia $m$ e $(r, s)$", "sends $m$ and $(r, s)$"),
      fs=FS - 4, style="italic")
fill, edge = key_style("pub")
box(ax, 19.6, y0, 5.0, 2.2, t("Verifica com\n$PU_a$", "Verifies with\n$PU_a$"),
    fill=fill, edge=edge, lw=2.6)
label(ax, 19.6, 6.6, t("chave pública da Alice", "Alice's public key"),
      fs=FS - 4, color=GREEN)
arrow(ax, 22.1, y0, 23.4, y0)
box(ax, 25.4, y0, 4.0, 1.8, "$v = r$ ?", fill=PINK, edge=RED, color=RED, bold=True,
    lw=2.8)
label(ax, 25.4, 2.3, t("se sim, a assinatura\né válida", "if so, the signature\nis valid"),
      fs=FS - 5, color=RED, bold=True)
label(ax, 22.6, 0.6, t("adaptado de Stallings (8.ª ed.), Fig. 13.2",
                       "adapted from Stallings (8th ed.), Fig. 13.2"),
      fs=FS - 6, style="italic", color="#666666")
save(fig, "fig-07-dsa-simples")


# --- o DSA em blocos (adaptado de Stallings, Fig. 13.3) --------------------
def bloco(ax, x, ytop, w, titulo, linhas, kind, fs=FS - 3, lh=1.0, hh=1.2):
    """Bloco com faixa de título e linhas (símbolo, descrição) ou fórmulas."""
    fill, edge = {"pub": (GREENBG, GREEN), "priv": (PINK, RED),
                  "op": (GREY, DARK)}[kind]
    h = hh + lh * len(linhas) + 0.3
    ax.add_patch(Rectangle((x, ytop - h), w, h, facecolor="white", edgecolor=edge,
                           lw=2.0, zorder=1))
    ax.add_patch(Rectangle((x, ytop - hh), w, hh, facecolor=fill, edgecolor=edge,
                           lw=2.0, zorder=2))
    ax.text(x + 0.35, ytop - hh / 2, titulo, ha="left", va="center", fontsize=fs + 1,
            fontweight="bold", color=edge if kind != "op" else DARK, zorder=3)
    y = ytop - hh - 0.15 - lh / 2
    for ln in linhas:
        if isinstance(ln, tuple):
            sym, desc = ln
            ax.text(x + 0.45, y, sym, ha="left", va="center", fontsize=fs + 1,
                    color=DARK, zorder=3)
            tx = ax.text(x + 1.6, y, desc, ha="left", va="center", fontsize=fs,
                         color=DARK, zorder=3)
            fit(ax, tx, w - 1.9)
        else:
            tx = ax.text(x + 0.45, y, ln, ha="left", va="center", fontsize=fs + 1,
                         color=DARK, zorder=3)
            fit(ax, tx, w - 0.7)
        y -= lh
    return ytop - h


fig, ax = new_ax(14, 7.35, 28, 14.7)
xl, xr, wl, wr, gap = 0.0, 14.6, 13.8, 13.4, 0.45
y = 14.6
y = bloco(ax, xl, y, wl, t("Parâmetros públicos (partilhados)", "Public parameters (shared)"), [
    ("$p$", t("primo de 2048 ou 3072 bits", "prime of 2048 or 3072 bits")),
    ("$q$", t("primo de 224 ou 256 bits, divisor de $p - 1$",
              "prime of 224 or 256 bits, divides $p - 1$")),
    ("$g$", t(f"$= h^{{(p-1)/q}}{MOD}p$, com $1 < h < p - 1$ e $g > 1$",
              f"$= h^{{(p-1)/q}}{MOD}p$, with $1 < h < p - 1$ and $g > 1$")),
    ("$H$", t("função de $\\mathit{hash}$ (por exemplo, SHA-256)", "hash function (e.g. SHA-256)")),
], "pub") - gap
y = bloco(ax, xl, y, wl, t("Chave privada", "Private key"), [
    ("$x$", t("aleatório, $0 < x < q$", "random, $0 < x < q$")),
], "priv") - gap
y = bloco(ax, xl, y, wl, t("Chave pública", "Public key"), [
    ("$y$", f"$= g^{{x}}{MOD}p$"),
], "pub") - gap
y = bloco(ax, xl, y, wl, t("Número secreto de cada assinatura", "Per-signature secret number"), [
    ("$k$", t("aleatório, $0 < k < q$, usado uma única vez",
              "random, $0 < k < q$, used only once")),
], "priv")
y = 14.6
y = bloco(ax, xr, y, wr, t("Assinar", "Signing"), [
    f"$r = (g^{{k}}{MOD}p){MOD}q$",
    f"$s = k^{{-1}}\\,(H(m) + x\\,r){MOD}q$",
    t("assinatura $= (r, s)$", "signature $= (r, s)$"),
], "op") - gap
y = bloco(ax, xr, y, wr, t("Verificar", "Verifying"), [
    f"$w = s^{{-1}}{MOD}q$",
    f"$u_1 = H(m)\\,w{MOD}q$",
    f"$u_2 = r\\,w{MOD}q$",
    f"$v = (g^{{u_1}}\\,y^{{u_2}}{MOD}p){MOD}q$",
    t("válida se $v = r$", "valid if $v = r$"),
], "op")
label(ax, 21.3, y - 0.9, t("adaptado de Stallings (8.ª ed.), Fig. 13.3",
                           "adapted from Stallings (8th ed.), Fig. 13.3"),
      fs=FS - 6, style="italic", color="#666666")
save(fig, "fig-07-dsa-tabela")
