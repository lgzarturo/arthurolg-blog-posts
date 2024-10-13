# ¿Como puedo contribuir?

Es muy sencillo, solo tienes que hacer un fork del repositorio donde se publican los artículos, clonarlo en tu máquina y seguir los siguientes pasos:

El repositorio de los artículos es [arthurolg-blog-posts](https://github.com/lgzarturo/arthurolg-blog-posts)

1. Crea una nueva rama con el nombre de tu artículo.
2. Escribe tu artículo siguiendo la estructura de los demás.
3. Guarda tu artículo en la carpeta `articles/`.
4. Añade una imagen en la carpeta `articles/images` y referencia la URL en tu artículo.
5. Además puedes publicar el artículo en una de las categorías principales `marketing`, `programming`, `technology` o `videogames`.
6. Haz un pull request a la rama principal del repositorio.
7. Espera a que tu artículo sea revisado y aprobado.
8. ¡Listo! Tu artículo será publicado en el blog.
9. Comparte tu artículo en redes sociales y con tus amigos.
10. ¡Gracias por contribuir!

Si tienes alguna duda, puedes abrir un issue en el repositorio.

> **Nota:** Si no tienes experiencia con Git, puedes seguir [esta guía](https://guides.github.com/activities/forking/).

## Instrucciones para escribir artículos

### Estructura de los artículos

Los artículos deben estar escritos en formato Markdown y seguir la siguiente estructura:

```markdown
---
title: Título del artículo
image: URL de la imagen
description: Descripción del artículo
author: Nombre del autor
date: Fecha de publicación
label: Etiqueta del artículo
---

Contenido del artículo
```

### Imagen

Las imágenes deben tener un tamaño de 1200x630 píxeles y se deben guardar en la carpeta `articles/images`. La URL de la imagen se debe referenciar en el artículo.

### Redimensionar imágenes

Para redimensionar imágenes, puedes utilizar la herramienta `magick` de ImageMagick. Por ejemplo, para redimensionar una imagen a 600 píxeles de ancho, puedes ejecutar el siguiente comando:

````bash
magick welcome-to-my-blog.webp -resize 600x welcome-to-my-blog-mobile.webp
magick welcome-to-my-blog.webp -resize 1024x welcome-to-my-blog-tablet.webp
magick welcome-to-my-blog.webp -resize 1920x welcome-to-my-blog-desktop.webp
````

## Clonar el repositorio

Para clonar el repositorio, puedes ejecutar el siguiente comando en tu terminal:

```bash
git clone git@github.com:lgzarturo/arthurolg-blog-posts.git
```
