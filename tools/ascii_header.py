# -*- coding: utf-8 -*-
"""
Genera el bloque de arte ASCII del encabezado del README.

Salida:  assets/ascii/<fuente>.txt  +  imprime el arte en consola
Uso:     python tools/ascii_header.py

Requiere pyfiglet:  python -m pip install pyfiglet
"""

import io
import os

import pyfiglet

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "ascii")
TEXT = "MARQUITOUH"
FONTS = ["doom", "3d-ascii", "gothic", "ansi_shadow", "letters", "big", "block"]


def render(font):
    return pyfiglet.figlet_format(TEXT, font=font, width=400).rstrip("\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    for font in FONTS:
        art = render(font)
        path = os.path.join(OUT, font + ".txt")
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(art + "\n")
        width = max(len(line) for line in art.split("\n"))
        print("{:<12s} ancho={:<4d} lineas={:<3d} -> assets/ascii/{}.txt".format(
            font, width, len(art.split("\n")), font))


if __name__ == "__main__":
    main()