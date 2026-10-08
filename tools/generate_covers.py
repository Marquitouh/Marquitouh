# -*- coding: utf-8 -*-
"""
Genera las mini-cards (portadas) de la seccion "Proyectos" del README de perfil.

Salida:  assets/projects/<slug>.png   (960x540 -> se muestran a 400px de ancho)
Uso:     python tools/generate_covers.py

Todo se dibuja por codigo con Pillow: si cambias un titulo o un color y volves a
correr el script, las portadas se regeneran identicas.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(ASSETS, "projects")
FOX = os.path.join(ASSETS, "pixelfox-icon.png")

W, H = 960, 540          # se muestran a 400px de ancho (2x para que se vea nitido)
S = 2                    # factor de escala tipografico
RADIUS = 28

BG_TOP = (17, 21, 29)
BG_BOTTOM = (9, 11, 16)
BORDER = (44, 50, 61)
TITLE = (240, 244, 250)
SUB = (150, 160, 175)
MONO = (110, 120, 135)
ACCENT = (255, 107, 18)          # naranja PixelFox
ACCENT_SOFT = (255, 145, 60)

FONTS = r"C:\Windows\Fonts"
F_TITLE = os.path.join(FONTS, "ARIALNB.TTF")
F_SUB = os.path.join(FONTS, "segoeuib.ttf")
F_MONO = os.path.join(FONTS, "consola.ttf")

PROJECTS = [
    {
        "slug": "evangelion-loving-project",
        "title": "Evangelion",
        "title2": "Loving Project",
        "sub": "RPG DE RELACION · 30 DIAS · 9 PERSONAJES",
        "path": "~/Marquitouh/Evangelion-Loving-Project",
        "accent": (211, 18, 54),
    },
    {
        "slug": "memory-evangelion",
        "title": "Memory",
        "title2": "Evangelion",
        "sub": "JUEGO DE MEMORIA · CONSOLA",
        "path": "~/Marquitouh/Memory-Evangelion",
        "accent": (196, 60, 90),
    },
    {
        "slug": "tetris",
        "title": "Tetris",
        "title2": "",
        "sub": "CLASICO MULTIPLATAFORMA · CONSOLA",
        "path": "~/Marquitouh/Tetris",
        "accent": (90, 150, 240),
    },
    {
        "slug": "lunavow",
        "title": "Lunavow",
        "title2": "",
        "sub": "RPG MEDIEVAL · EN DESARROLLO",
        "path": "~/Marquitouh/Lunavow",
        "accent": ACCENT,
        "chip": "WIP",
    },
]


def gradient(size, top, bottom):
    """Gradiente vertical simple (sin numpy)."""
    img = Image.new("RGB", (1, size[1]))
    d = ImageDraw.Draw(img)
    for y in range(size[1]):
        t = y / max(1, size[1] - 1)
        d.point(
            (0, y),
            fill=(
                int(top[0] + (bottom[0] - top[0]) * t),
                int(top[1] + (bottom[1] - top[1]) * t),
                int(top[2] + (bottom[2] - top[2]) * t),
            ),
        )
    return img.resize(size, Image.BILINEAR)


def tracked_width(draw, text, font, spacing):
    return sum(draw.textlength(ch, font=font) for ch in text) + spacing * (len(text) - 1)


def letter_spaced(draw, xy, text, font, fill, spacing, anchor_center=True):
    """Texto con tracking manual (PIL no lo trae)."""
    total = tracked_width(draw, text, font, spacing)
    x, y = xy
    if anchor_center:
        x -= total / 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing
    return total


def fit_font(draw, text, path, max_size, min_size, max_width, tracking_ratio=0.12):
    """Elige el tamano de fuente mas grande que entre en max_width."""
    size = max_size
    while size > min_size:
        font = ImageFont.truetype(path, size)
        spacing = max(1, int(size * tracking_ratio))
        if tracked_width(draw, text, font, spacing) <= max_width:
            return font, spacing
        size -= 1
    font = ImageFont.truetype(path, min_size)
    return font, max(1, int(min_size * tracking_ratio))


def stripes(size, color, alpha=10, step=46, width=2):
    """Textura de diagonales, muy sutil."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x in range(-size[1], size[0] + size[1], step):
        d.line([(x, size[1]), (x + size[1], 0)], fill=color + (alpha,), width=width)
    return layer


def make_cover(cfg):
    accent = cfg["accent"]

    card = gradient((W, H), BG_TOP, BG_BOTTOM).convert("RGBA")
    card.alpha_composite(stripes((W, H), accent, alpha=12))

    # barra de acento superior
    bar = Image.new("RGBA", (W, 6), accent + (255,))
    card.alpha_composite(bar)

    # logo PixelFox en la esquina superior derecha
    fox = Image.open(FOX).convert("RGBA").resize((52 * S, 52 * S), Image.LANCZOS)
    card.alpha_composite(fox, (W - 52 * S - 36, 36))

    d = ImageDraw.Draw(card)

    # area util (deja aire para el logo y la ruta del repo)
    LEFT, RIGHT = 56, W - 56
    MAX_W = RIGHT - LEFT
    TOP_LIMIT, BOTTOM_LIMIT = 112, H - 96

    # titulo: una o dos lineas, ajustadas al ancho disponible
    lines = [l for l in (cfg["title"], cfg["title2"]) if l]
    title_fonts = [
        fit_font(d, l.upper(), F_TITLE, 74, 26, MAX_W) for l in lines
    ]
    line_h = [int(f.size * 1.18) for f, _ in title_fonts]

    f_sub, sub_spacing = fit_font(d, cfg["sub"], F_SUB, 22, 13, MAX_W, 0.16)
    sub_h = int(f_sub.size * 1.5)

    gap_title_sub = 26
    block_h = sum(line_h) + (gap_title_sub if lines else 0) + sub_h
    y = TOP_LIMIT + max(0, ((BOTTOM_LIMIT - TOP_LIMIT) - block_h) // 2)

    for line, (font, spacing) in zip(lines, title_fonts):
        letter_spaced(d, (W // 2, y), line.upper(), font, TITLE, spacing)
        y += int(font.size * 1.18)

    y += gap_title_sub - sub_h // 2
    letter_spaced(d, (W // 2, y), cfg["sub"], f_sub, SUB, sub_spacing)

    # chip opcional (WIP)
    if cfg.get("chip"):
        f_chip = ImageFont.truetype(F_SUB, 19 * S)
        tw = d.textlength(cfg["chip"], font=f_chip)
        x0, y0 = 52, 46
        d.rounded_rectangle(
            [x0, y0, x0 + tw + 34, y0 + 42], radius=21, outline=accent + (255,), width=2
        )
        d.text((x0 + 17, y0 + 21), cfg["chip"], font=f_chip, fill=accent + (255,), anchor="lm")

    # ruta del repo, estilo terminal
    f_mono = ImageFont.truetype(F_MONO, 19 * S)
    d.text((LEFT, H - 62), cfg["path"], font=f_mono, fill=MONO)

    # borde redondeado
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], radius=RADIUS, fill=255)
    card.putalpha(mask)
    border = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(border).rounded_rectangle(
        [1, 1, W - 2, H - 2], radius=RADIUS, outline=BORDER + (255,), width=2
    )
    card.alpha_composite(border)

    out = os.path.join(OUT, cfg["slug"] + ".png")
    card.convert("RGB").save(out, optimize=True)
    print("  ->", os.path.relpath(out, ROOT))


def main():
    os.makedirs(OUT, exist_ok=True)
    print("Generando portadas de proyectos...")
    for cfg in PROJECTS:
        make_cover(cfg)
    print("Listo.")


if __name__ == "__main__":
    main()