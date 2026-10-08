# -*- coding: utf-8 -*-
"""
Inyecta el arte ASCII del encabezado en el README.

Uso:
    python tools/build_readme.py                  # usa assets/ascii/ansi_shadow.txt
    python tools/build_readme.py --font doom      # cambia la fuente del hero
    python tools/build_readme.py --list           # muestra las fuentes disponibles

El bloque <!--HERO_ASCII--> del README.md se reemplaza por el arte, asi el
encabezado nunca queda desalineado por culpa de un caracter pegado a mano.
"""

import argparse
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
ASCII_DIR = os.path.join(ROOT, "assets", "ascii")
PLACEHOLDER = "<!--HERO_ASCII-->"
DEFAULT_FONT = "ansi_shadow"


def available():
    if not os.path.isdir(ASCII_DIR):
        return []
    return sorted(
        os.path.splitext(f)[0] for f in os.listdir(ASCII_DIR) if f.endswith(".txt")
    )


def art_for(font):
    path = os.path.join(ASCII_DIR, font + ".txt")
    if not os.path.isfile(path):
        raise SystemExit(
            "No existe {}. Fuentes disponibles: {}".format(path, ", ".join(available()))
        )
    with io.open(path, encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


def inject(font):
    with io.open(README, encoding="utf-8") as fh:
        content = fh.read()

    art = art_for(font)

    if PLACEHOLDER in content:
        # primera vez: el README todavia tiene el marcador
        content = content.replace(PLACEHOLDER, art)
    else:
        # ya inyectado: se reemplaza el contenido del <pre> ... </pre>
        if "<pre>" not in content or "</pre>" not in content:
            raise SystemExit("No se encontro un bloque <pre> ... </pre> en el README.")
        start = content.index("<pre>") + len("<pre>")
        end = content.index("</pre>")
        content = content[:start] + "\n" + art + "\n" + content[end:]

    with io.open(README, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)

    width = max(len(l) for l in art.split("\n"))
    print("Hero inyectado: fuente={} ancho={} columnas lineas={}".format(
        font, width, len(art.split("\n"))))


def main():
    ap = argparse.ArgumentParser(description="Inyecta el arte ASCII en el README")
    ap.add_argument("--font", default=DEFAULT_FONT, help="fuente figlet a usar")
    ap.add_argument("--list", action="store_true", help="lista fuentes disponibles")
    args = ap.parse_args()

    if args.list:
        print("\n".join(available()))
        return

    inject(args.font)


if __name__ == "__main__":
    main()