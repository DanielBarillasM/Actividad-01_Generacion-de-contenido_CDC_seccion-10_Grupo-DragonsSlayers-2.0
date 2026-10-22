# Plan de animación Manim · versión 02

## Propósito

El paquete Manim explica el compilador mediante transformaciones observables. No funciona como decoración de fondo: cada movimiento representa lectura, clasificación, jerarquía, validación, optimización o ejecución.

**Maestro:** `output/video/minilang-animaciones-v02.mp4`  
**Duración:** 3:13.46  
**Formato:** H.264, 1920×1080, 30 fps, audio AAC a 48 kHz  
**Fuente:** `audiovisual/scenes.py`  
**Storyboard:** `output/storyboard/manim-v02-contact-sheet.png`

## Principios de movimiento

- Una transformación conceptual importante por plano.
- Entradas entre 0.8 y 1.7 segundos; recorridos complejos hasta 2.3 segundos.
- Permanencia final de 3 a 4.2 segundos para que la narración respire.
- Movimiento con aceleración y desaceleración; sin saltos ni zooms ornamentales.
- El color identifica significado: azul fuente, amarillo tokens, violeta sintaxis, coral semántica y verde destino.
- La rejilla, marcas de registro y riel de fases permanecen discretos y constantes.
- Los efectos de audio confirman escaneo, error o éxito; nunca sustituyen la explicación.

## Manifiesto de escenas

| Orden | Escena | Duración | Inserción del guion | Acción principal |
|---:|---|---:|---:|---|
| 1 | `HookScene` | 16.50 s | Bloque 1 | La señal viaja del código al resultado 42. |
| 2 | `PipelineScene` | 24.90 s | Bloque 2 | Construcción secuencial de seis contratos y recorrido de la señal. |
| 3 | `LexerScene` | 22.23 s | Bloque 4 | Escáner, posición y transformación lexema→token. |
| 4 | `GrammarScene` | 17.47 s | Bloque 5 | Reglas, precedencia y agrupación `6 + (7 * 2)`. |
| 5 | `AstScene` | 22.00 s | Bloque 5 | Crecimiento del árbol, aislamiento del subárbol y evaluación ascendente. |
| 6 | `SemanticScene` | 14.47 s | Bloque 6 | Registro de una declaración y diagnóstico de nombre desconocido. |
| 7 | `OptimizationScene` | 15.90 s | Bloque 9 | Constant folding y reducción de tres instrucciones a una. |
| 8 | `StackScene` | 27.00 s | Bloque 7 | Seguimiento lento de seis instrucciones, pila y local 0. |
| 9 | `RuntimeScene` | 20.60 s | Bloque 8 | Validación, instanciación, ejecución e importación del host. |
| 10 | `CreditsScene` | 12.40 s | Bloque 13 | Créditos completos y licencia con tiempo de lectura. |

## Indicaciones de montaje

1. No colocar narración antes de que aparezca el título de cada escena.
2. Alinear cada oración con la transformación que describe; las pausas finales admiten extensiones mediante congelado limpio si una voz necesita hasta dos segundos más.
3. Alternar Manim con cámara, presentación o terminal. Evitar más de 55 segundos continuos de animación programática.
4. Usar cortes directos en momentos de reposo. No añadir transiciones de plantilla sobre las animaciones.
5. Conservar el audio de señales entre −18 y −12 dB respecto de la voz; el acorde de éxito puede llegar a −9 dB durante menos de un segundo.
6. Mantener `CreditsScene` íntegra y sin voz.

## Render reproducible

```powershell
python scripts/generate_audio.py
powershell -ExecutionPolicy Bypass -File scripts/render_animations.ps1 -Profile preview
powershell -ExecutionPolicy Bypass -File scripts/render_animations.ps1 -Profile final
```

El perfil `preview` produce 1280×720. El perfil `final` produce 1920×1080. Ambos conservan 30 fps y el mismo timing, por lo que un corte aprobado en preview puede sustituirse por el maestro sin desplazar la edición.

## Criterios de aprobación

- Ningún texto queda fuera del área segura ni por debajo de un tamaño legible en 1080p.
- La fase activa se reconoce por color sin depender únicamente del texto.
- Las acciones de pila coinciden con las instrucciones WAT visibles.
- El AST muestra multiplicación debajo de suma y recupera su composición sin superposiciones.
- El módulo solo produce `42` después de cruzar la importación `env.print_i32`.
- Los créditos contienen exclusivamente a Pablo Daniel Barillas Moreno, Hugo Daniel Barillas Ajín y Ernesto Ascencio.
