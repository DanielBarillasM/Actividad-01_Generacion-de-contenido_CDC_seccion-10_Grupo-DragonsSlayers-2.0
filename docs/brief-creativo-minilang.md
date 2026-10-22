# Brief creativo: De MiniLang a WebAssembly

**Tipo de proyecto:** Video educativo, animacion y demostracion interactiva  
**Canales:** YouTube, Canvas UVG y repositorio del equipo  
**Fecha del brief:** 2026-10-21  
**Produccion:** 2026-10-21 a 2026-11-03  
**Direccion y produccion:** DragonsSlayers 2.0  
**Presupuesto:** Produccion academica con herramientas de codigo abierto

## 1. Contexto

El proyecto responde a la Actividad 01 de Construccion de Compiladores. Debe explicar un tema tecnico con rigor, claridad y aprovechamiento audiovisual. La entrega formal es un video de al menos doce minutos publicado en YouTube bajo una licencia Creative Commons.

El resultado se considerara exitoso si una persona que conoce programacion puede explicar la diferencia entre lexer, parser y analisis semantico, seguir una expresion hasta WebAssembly y verificar una ejecucion que produce `42`.

## 2. Concepto

**Idea central:** un mismo programa cambia de forma en cada etapa del compilador sin cambiar de significado.

La narracion abre la caja negra del compilador. En lugar de enumerar definiciones, sigue la senal de `let resultado = 6 * 7;` a traves de tokens, AST, simbolos e instrucciones WebAssembly.

El concepto rechaza la clase grabada sin apoyo visual, las diapositivas saturadas, el estilo hacker/cyberpunk y las afirmaciones tecnicas que no puedan demostrarse con el compilador incluido.

## 3. Audiencia

Estudiantes universitarios de computacion que programan, pero aun perciben un compilador como una caja negra. Al terminar deben sentir que las fases son mecanismos concretos y observables, no terminologia abstracta.

## 4. Sujetos y objetos

- **Participantes:** Pablo Daniel Barillas Moreno, Hugo Daniel Barillas Ajín y Ernesto Ascencio.
- **Vestuario:** neutro, sin patrones finos; azul oscuro, gris o negro.
- **Expresion:** curiosidad al plantear la pregunta y precision al explicar.
- **Objetos requeridos:** computadora, editor limpio, terminal y microfono.
- **Objetos prohibidos:** logotipos de terceros sin permiso y pantallas con datos personales.

## 5. Composicion

| Canal | Relacion | Resolucion | Requisito |
|---|---:|---:|---|
| Video principal | 16:9 | 1920x1080 | Textos dentro del 90% central |
| Presentacion | 16:9 | Adaptable | Navegacion por teclado y foco visible |
| Miniatura | 16:9 | 1280x720 | Maximo cuatro palabras grandes |

Planos necesarios: introduccion a camara, lexer, construccion del AST, tabla de simbolos, pila WebAssembly, demostracion completa, cierre a camara y creditos.

## 6. Iluminacion

Para las apariciones a camara: luz principal suave a 45 grados, relleno tenue y fondo neutro. Temperatura consistente, sin mezclar luz natural azul con focos calidos. Las capturas digitales no simularan resplandores ni reflejos.

## 7. Color y tratamiento

Tema propio **Compiler Signal**:

- Tinta profunda: `#07131E`
- Superficie de plano: `#0D2130`
- Texto principal: `#EDF6F9`
- Codigo fuente: `#4DB7FF`
- Tokens: `#FFD166`
- Sintaxis/AST: `#B69CFF`
- Semantica/error: `#FF758F`
- Objetivo WebAssembly: `#57D68D`
- Texto secundario: `#91A9B8`

Contraste alto, saturacion controlada y lineas de registro delgadas. No se utilizaran gradientes decorativos.

## 8. Tono

- Riguroso, no solemne.
- Visual, no ornamental.
- Cercano, no informal.
- Preciso, no enciclopedico.

Ritmo deliberado con aceleraciones breves al transformar artefactos. Cada escena Manim mantiene sus estados finales entre 3 y 4 segundos para permitir una explicación sin prisa. Las transformaciones conceptuales duran entre 0.8 y 1.7 segundos; no se ralentiza el metraje después de renderizar. La voz domina la mezcla; la musica queda por debajo y los efectos solo confirman acciones.

## 9. Tablero de referencias

Las referencias son principios de composicion, no material para copiar:

1. Editores de codigo: alineacion y jerarquia monoespaciada.
2. Blueprints tecnicos: marcas de registro y rejilla tenue.
3. Depuradores: estado visible paso a paso.
4. Diagramas de compiladores: flujo direccional inequívoco.
5. Arboles sintacticos: jerarquia espacial limpia.
6. Trazas de pila: movimiento vertical de operandos.
7. Osciloscopios: una senal persistente que conecta escenas.
8. Especificaciones tecnicas: notas marginales discretas.
9. Terminales: respuesta inmediata y sin decoracion.
10. Animacion educativa: una transformacion importante por plano.

## 10. Evitar

- Lluvia de codigo, circuitos brillantes o fondos de hackers.
- Tarjetas redondeadas repetidas sin funcion informativa.
- Zooms, giros 3D o transiciones que no expliquen una transformacion.
- Texto pequeno, codigo cortado o mas de una idea central por plano.
- Musica con Content ID o recursos cuya licencia no sea verificable.

## 11. Entregables

| Activo | Formato | Especificacion |
|---|---|---|
| Compilador MiniLang | Python | Lexer, parser, semantica, optimizacion y WAT |
| Presentacion | HTML/CSS/JS | Interactiva, autocontenida y 16:9 |
| Guion tecnico | TEX y PDF | Narracion, visuales, tiempos y responsables |
| Animaciones | MP4 | Diez escenas Manim, 3:13, 1080p final; preview 720p |
| Video final | MP4 | 14-15 min, H.264, 1080p |
| Fuentes | Markdown/BibTeX | Referencias y licencias legibles |

Convencion: `minilang-[activo]-vNN.ext`.

El maestro audiovisual vigente es `output/video/minilang-animaciones-v02.mp4`. El desglose de duración, intención y montaje está en `docs/plan-animacion-manim.md`.

## 12. Cronograma

| Hito | Fecha | Responsable |
|---|---|---|
| Base tecnica y pruebas | 21-24 octubre | Pablo |
| Guion y storyboard | 25-27 octubre | Hugo |
| Animacion y primer corte | 28-31 octubre | Ernesto |
| Revision conjunta | 1-2 noviembre | Equipo completo |
| Publicacion | 3 noviembre | Equipo completo |

## 13. Aprobaciones

1. Pablo valida ejecucion y exactitud tecnica.
2. Hugo valida guion, fuentes y claridad.
3. Ernesto valida imagen, sonido y licencias.

Maximo dos rondas integrales. Cambios estructurales cierran el 31 de octubre.

## 14. Talento

Los tres integrantes participan en voz o camara. No se usaran voces clonadas. Las animaciones y la interfaz se producen con Manim y tecnologias web dentro del repositorio.

## 15. Acciones de producción humana

- [ ] Grabar las voces definitivas de los tres integrantes.
- [ ] Grabar las apariciones a camara.
- [ ] Elegir musica CC BY o CC0 y registrar su atribucion.
- [ ] Obtener aprobacion del titulo por parte del docente.
- [ ] Publicar en YouTube y entregar el enlace en Canvas.

