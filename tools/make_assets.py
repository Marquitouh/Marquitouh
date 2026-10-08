# -*- coding: utf-8 -*-
"""
Prepara los assets del README para que se vean bien en tema claro y oscuro.

Salidas (nunca pisa los originales):
  assets/pixelfox-icon-clear.png -> el logo de PixelFox sin fondo blanco,
                                   recortado al contenido
  assets/rule.png               -> regla horizontal fina y monocroma

Uso:  python tools/make_assets.py

Se leen los PNG con fondo blanco y se escriben las versiones "-clear".
"""

import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

RULE = os.path.join(ASSETS, "rule.png")

# nombre del original -> nombre de la version transparente
CLEAR = {
    "pixelfox-icon.png": "pixelfox-icon-clear.png",
}

# El fondo de los PNG originales es blanco puro (o casi). Se considera "fondo"
# cualquier pixel casi blanco.
NEAR_WHITE = 238
FEATHER = 2          # px de suavizado del borde


def strip_white(src, dst, crop=True):
    """Escribe en dst una copia sin el fondo blanco, recortada al contenido."""
    if not os.path.isfile(src):
        return None
    im = Image.open(src).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= NEAR_WHITE and g >= NEAR_WHITE and b >= NEAR_WHITE:
                px[x, y] = (r, g, b, 0)
            elif a > 0:
                # suavizado del borde: cuanto mas cerca del blanco, mas alpha
                lum = (r + g + b) / 3.0
                if lum > NEAR_WHITE - 40:
                    px[x, y] = (r, g, b, int(max(0, (lum - (NEAR_WHITE - 40)) / 40.0 * a)))

    if crop:
        bbox = im.getbbox()
        if bbox:
            im = im.crop(bbox)

    im.save(dst)
    return im.size


def make_rule():
    """Regla horizontal fina y monocroma, para separar secciones."""
    w, h = 720, 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    mid = h // 2
    for x in range(w):
        t = abs(x / float(w - 1) - 0.5) * 2      # 1 en los bordes, 0 en el centro
        a = int(38 + 150 * t ** 1.6)            # se desvanece hacia el centro
        d.point((x, mid), fill=(140, 148, 160, a))
    im.save(RULE)
    return im.size


DIVIDER = (
    "                                        "
    "                    ˙ · ·  · · ˙         "
)


def main():
    for src_name, dst_name in CLEAR.items():
        src = os.path.join(ASSETS, src_name)
        dst = os.path.join(ASSETS, dst_name)
        size = strip_white(src, dst)
        print("transparente: {} -> {}{}".format(
            src_name, dst_name,
            "" if not size else "  {}x{}".format(*size)))

    print("regla:   rule.png -> {}x{}".format(*make_rule()))


if __name__ == "__main__":
    main()