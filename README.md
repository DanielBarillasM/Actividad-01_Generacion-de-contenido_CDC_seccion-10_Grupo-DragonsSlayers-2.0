# De MiniLang a WebAssembly

Actividad 01 de **Construcción de Compiladores · Sección 10**. El proyecto explica visualmente cómo un programa pequeño atraviesa análisis léxico, sintáctico y semántico, optimización y generación de WebAssembly.

## Equipo · DragonsSlayers 2.0

- Pablo Daniel Barillas Moreno
- Hugo Daniel Barillas Ajín
- Ernesto Ascencio

## Entregables

| Recurso | Ubicación | Estado |
|---|---|---|
| Guion técnico y de exposición | `guion/guion.tex` y `output/pdf/guion.pdf` | Listo, 14:40 objetivo |
| Presentación interactiva | `presentacion/index.html` | Lista, 15 escenas |
| Compilador demostrativo | `minilang/` | Funcional y probado |
| Código de ejemplo | `examples/demo.mini` | Produce `42` |
| Animaciones Manim | `audiovisual/scenes.py` | Diez secuencias narrativas editables |
| Montaje de animaciones | `output/video/minilang-animaciones-v02.mp4` | Listo, 1920×1080, 30 fps, 3:13 |
| Plan de animación | `docs/plan-animacion-manim.md` | Ritmo, propósito y punto de inserción por escena |
| Storyboard de control | `output/storyboard/manim-v02-contact-sheet.png` | Fotograma representativo de las diez escenas |
| Brief y plan visual | `docs/brief-creativo-minilang.md` | Listo |
| Fuentes y licencias | `docs/fuentes-y-licencias.md` | Listo |
| Descripción de YouTube | `youtube/descripcion.md` | Lista para publicar |

El MP4 incluido es un paquete audiovisual de 3 minutos y 13 segundos, no el video final de doce minutos. El montaje final necesita las voces y apariciones de los tres integrantes, siguiendo el guion. No se incluyen integrantes provisionales ni voces sintéticas atribuidas a personas reales.

## Inicio rápido

Requiere Python 3.11 o posterior. Desde la raíz del proyecto:

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python -m minilang examples/demo.mini --tokens --ast --wat --run
```

La última orden muestra las representaciones intermedias, genera WAT y ejecuta el módulo con Wasmtime. El resultado final esperado es `42`.

Para abrir la presentación sin restricciones del navegador:

```powershell
python -m http.server 8000 --directory presentacion
```

Después, visitar `http://localhost:8000`. Se navega con las flechas, `Espacio`, `Inicio` y `Fin`. La diapositiva «Compilador en vivo» permite cambiar el código y observar tokens, AST, WAT y salida.

## Regenerar los recursos

Generar efectos de sonido y renderizar/ensamblar las diez escenas Manim en 1080p:

```powershell
python scripts/generate_audio.py
powershell -ExecutionPolicy Bypass -File scripts/render_animations.ps1 -Profile final
```

Para una revisión más rápida en 720p:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/render_animations.ps1 -Profile preview
```

Si los clips finales ya existen y solo se necesita volver a ensamblarlos:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/render_animations.ps1 -Profile final -SkipRender
```

Compilar el guion LaTeX:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error -output-directory output/pdf guion/guion.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory output/pdf guion/guion.tex
```

Ejecutar la validación automatizada del proyecto:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate.ps1
```

## Flujo para terminar el video

1. Ensayar con `output/pdf/guion.pdf` y cronometrar entre 14:00 y 15:00.
2. Grabar las voces en un lugar silencioso, a 48 kHz, dejando cinco segundos de ambiente.
3. Grabar introducción y cierre a cámara; el resto puede alternar presentación, terminal y animaciones.
4. Editar a 1920×1080, 30 fps. Insertar los clips Manim en los tiempos indicados por el guion.
5. Normalizar el diálogo alrededor de −16 LUFS, verificar que la música no compita con las voces y añadir subtítulos.
6. Exportar H.264, revisar de principio a fin y publicar en YouTube con licencia Creative Commons.
7. Copiar la descripción preparada en `youtube/descripcion.md` y entregar el enlace en Canvas.

## Diseño y licencia

La identidad «Compiler Signal» asigna un color estable a cada etapa: azul para código fuente, amarillo para tokens, violeta para sintaxis, coral para semántica y verde para salida. Los recursos propios se publican bajo CC BY 4.0; las fuentes técnicas y los créditos están documentados en `docs/fuentes-y-licencias.md`.
