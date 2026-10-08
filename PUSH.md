# Publicar el README en GitHub

Esto es el repo de perfil: <https://github.com/Marquitouh/Marquitouh>.
Los archivos de `README.md` ya están listos para copiar tal cual.

## Qué hay en esta carpeta

```
README.md                   -> el perfil (va a la raíz del repo del perfil)
assets/
  pixelfox-icon.png         -> logo del estudio, con fondo blanco (original)
  pixelfox-icon-clear.png   -> el logo sin fondo (este usa el README)
  web-banner.jpg            -> banner de marquitouh.github.io
  rule.png                  -> regla fina para separar secciones
  ascii/*.txt               -> arte ASCII del encabezado
tools/
  make_assets.py            -> genera la versión sin fondo y la regla
  ascii_header.py           -> genera las variantes de arte ASCII
  build_readme.py           -> inyecta el arte ASCII en el README
  preview.py                -> genera preview-light.html y preview-dark.html
.gitignore                  -> ignora los previews locales
```

## 1. Ver cómo queda (opcional)

```powershell
python tools\preview.py
```

Se generan `preview-light.html` y `preview-dark.html`. Abrilos con doble clic:
usan el mismo motor de Markdown que GitHub, así que lo que ves es lo que se ve
en el perfil. (Están en `.gitignore`, no se suben.)

## 2. Configurar git una sola vez

```powershell
git config --global user.name  "Marquitouh"
git config --global user.email "tu@email.com"
```

## 3. Subir

### Opción A - rápido (reemplaza el README viejo, el repo solo tiene un README)

```powershell
cd "D:\Carpetas y Cosas importantes\Codigos\Paginas\GitHub Marquitouh"
git init
git add .
git commit -m "Perfil: README nuevo, estilo ASCII monocromo"
git branch -M main
git remote add origin https://github.com/Marquitouh/Marquitouh.git
git push -u origin main --force
```

### Opción B - conserva el historial del repo (sin `--force`)

```powershell
cd "D:\Carpetas y Cosas importantes\Codigos"
git clone https://github.com/Marquitouh/Marquitouh.git _perfil-temporal
Copy-Item "GitHub Marquitouh\README.md" "_perfil-temporal\README.md" -Force
Copy-Item "GitHub Marquitouh\assets" "_perfil-temporal\assets" -Recurse -Force
cd _perfil-temporal
git add .
git commit -m "Perfil: README nuevo, estilo ASCII monocromo"
git push
```

> GitHub ya no acepta contraseña para subir por HTTPS: si pide usuario, usá tu
> usuario de GitHub y como contraseña un **personal access token**
> (<https://github.com/settings/tokens>, alcance `repo`).

## 4. Después de subir

- Recargá <https://github.com/Marquitouh> y el perfil ya está actualizado.
- Las tarjetas de stats tardan unos segundos la primera vez: se generan en
  vivo en los servidores de `github-readme-stats`.
- Revisá que las imágenes carguen: si alguna sale rota, es que la ruta
  `assets/...` no coincide con la carpeta del repo.

## Editar el contenido

- Textos, secciones y enlaces: editá `README.md` con cualquier editor.
- Cambiar la tipografía del arte ASCII del encabezado:

  ```powershell
  python tools\build_readme.py --font doom      # o: 3d-ascii, gothic, big, letters
  python tools\ascii_header.py                 # regenera las variantes
  ```

- Regenerar los logos sin fondo y la regla (después de cambiar los originales):

  ```powershell
  python tools\make_assets.py
  ```

- Requisitos: `python -m pip install pyfiglet pillow`

## Servicios externos del README

Estas imágenes se generan en servidores de terceros. Si uno se cae, la sección
queda vacía pero el resto del README sigue bien. Probados y funcionando:

| Qué | Dónde |
|---|---|
| Stats y top-langüajes | `github-readme-stats-fast.vercel.app` |
| Racha de contribuciones | `streak-stats.demolab.com` |
| Gráfico de actividad | `activity-graph.vercel.app` |
| Iconos del stack | `skillicons.dev` |
| Badges | `img.shields.io` |

El `github-readme-stats.vercel.app` original (sin `-fast`) estaba devolviendo
error 500 al momento de armar esto, por eso el README usa la variante `-fast`.
Si vuelve a funcionar, cambias las dos URLs de `/api` y de `/api/top-langs/`.

### Imágenes con dos temas

Las tarjetas de stats, racha y actividad están duplicadas: una con
`#gh-dark-mode-only` y otra con `#gh-light-mode-only`. GitHub muestra la que
corresponde al tema activo, así que en claro y en oscuro cada tarjeta se ve con
su fondo. El `preview.py` reproduce ese comportamiento para que el preview
local muestre lo mismo.

Si agregás una imagen con esos fragmentos y el preview muestra las dos, es que
falta regenerar: `python tools\preview.py`.