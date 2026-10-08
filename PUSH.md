# Publicar el README en GitHub

Esto es el repo de perfil: <https://github.com/Marquitouh/Marquitouh>.
Los archivos de `README.md` ya están listos para copiar tal cual.

## Qué hay en esta carpeta

```
README.md              -> el perfil (va a la raíz del repo del perfil)
assets/
  pixelfox-icon.png    -> logo del estudio (ya estaba)
  logo-marquitouh.png  -> wordmark (ya estaba)
  web-banner.jpg       -> banner de marquitouh.github.io
  projects/*.png       -> portadas de los proyectos (generadas por código)
  ascii/*.txt          -> arte ASCII del encabezado
tools/
  generate_covers.py   -> genera las portadas de projects/
  ascii_header.py      -> genera las variantes de arte ASCII
  build_readme.py      -> inyecta el arte ASCII en el README
  preview.py           -> genera preview-light.html y preview-dark.html
.gitignore             -> ignora los previews locales
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
git commit -m "Perfil: README nuevo con arte ASCII, mini-cards y stats"
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
git commit -m "Perfil: README nuevo con arte ASCII, mini-cards y stats"
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
  python tools\ascii_header.py --help           # regenera las variantes
  ```

- Cambiar textos, colores o tamaños de las portadas de proyectos:
  editá la lista `PROJECTS` y las constantes de color de
  `tools/generate_covers.py`, y corré:

  ```powershell
  python tools\generate_covers.py
  ```

- Requisitos: `python -m pip install pyfiglet pillow`.