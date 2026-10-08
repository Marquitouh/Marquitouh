# -*- coding: utf-8 -*-
"""
Genera preview.html y preview-dark.html: el README renderizado por la API de
GitHub (GFM) con el CSS de GitHub, para ver como va a quedar antes de subirlo.

Uso:
    python tools/preview.py

Abri preview.html o preview-dark.html en el navegador. El render usa el mismo
motor de Markdown que GitHub, asi que lo que ves aca es (casi) lo que se ve en
el perfil.
"""

import io
import json
import os
import re
import urllib.request

# La API de GitHub pasa las imagenes externas por su proxy "camo", que rompe los
# fragmentos #gh-dark-mode-only / #gh-light-mode-only. En el perfil real esos
# fragmentos se respetan, asi que los recuperamos antes de escribir el preview.
CAMO = re.compile(
    r"https://camo\.githubusercontent\.com/[0-9a-f]{64}/([0-9a-fA-F]+)")


def unproxy(html):
    def repl(m):
        hexpart = m.group(1)
        url = bytes.fromhex(hexpart).decode("utf-8", "replace")
        return url

    return CAMO.sub(repl, html)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
API = "https://api.github.com/markdown"

TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Preview {mode} · README de Marquitouh</title>
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/github-markdown-css@5.5.1/github-markdown-{variant}.min.css">
<style>
  body {{ margin: 0; background: {page}; }}
  .markdown-body {{ max-width: 900px; margin: 0 auto; padding: 32px 24px 80px; }}
  .markdown-body pre {{ font-size: 12px; }}
  .markdown-body table {{ width: 100%; }}
  .markdown-body img {{ max-width: 100%; }}

  /* GitHub resuelve estos fragmentos con su propio CSS: lo replicamos aca para
     que el preview muestre la variante que corresponde al tema. */
  body.dark  img[src$="#gh-light-mode-only"] {{ display: none; }}
  body.light img[src$="#gh-dark-mode-only"] {{ display: none; }}
</style>
</head>
<body class="{variant}">
<article class="markdown-body">
{html}
</article>
</body>
</html>
"""

VARIANTS = {
    "light": ("light", "#ffffff"),
    "dark": ("dark", "#0d1117"),
}


def render(markdown, context):
    payload = json.dumps({"text": markdown, "mode": "gfm", "context": context}).encode("utf-8")
    req = urllib.request.Request(
        API,
        data=payload,
        headers={
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "marquitouh-readme-preview",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return unproxy(resp.read().decode("utf-8"))


def main():
    with io.open(README, encoding="utf-8") as fh:
        markdown = fh.read()
    html = render(markdown, "Marquitouh/Marquitouh")

    for name, (variant, page) in VARIANTS.items():
        out = os.path.join(ROOT, "preview-{0}.html".format(name))
        with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(TEMPLATE.format(html=html, variant=variant, page=page, mode=name))
        print("Preview generado: {}".format(out))


if __name__ == "__main__":
    main()