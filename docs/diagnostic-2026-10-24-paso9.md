# Paso 9 — registro de composición y transferencia (R0/R1)

**Alcance T3:** registro de proceso, render, medición y QA. Este documento no sustituye el juicio visual de T4 ni declara validado Cropmark.

En este documento, **S9** significa `evals/art-direction/diagnostic-2026-10-22/renders/step9/`; las rutas con ese prefijo son relativas a esa carpeta.

## Pregunta y límites del ensayo

Paso 9 trabaja sobre tres piezas ficticias: carrusel de cerámica Taller Barro (B3, tres láminas), miniatura del video sobre tres agentes que rediseñan un portfolio, y flyer ficticio Noche de vinilos. El objetivo fue recomponer B3 con ritmo y relaciones imagen–titular variados, y comparar raster directo A con composición editable Cropmark B en miniatura y flyer. Se preservó el copy especificado y no se añadieron resultados, métricas ni datos del evento.

La prueba no aísla causalidad: las imágenes son generadas y diferentes entre piezas; además, el fondo B de miniatura cambió en R1. El QA comprueba condiciones técnicas; no equivale a juicio estético, preferencia humana medida, nivel de referencia ni aprobación.

## Estudio de referencias

Se leyeron el diagnóstico y candidato de Paso 8, el recorrido Cropmark, los módulos carousel/thumbnail/post, carousel-system, story-in-frame, typography, imagery, composition-study y checklist. Se inspeccionaron solo como estudio la imagen local 05-02, 08-04 y las hojas 02, 04, 07, 11 y 19. Las observaciones fueron expansión de frase, masas de titular alrededor de imagen, silueta de miniatura, agrupación de copy y protagonismo material. Las referencias de flyer de evento tienen comparabilidad parcial con el evento ficticio. No se copiaron sus píxeles, texturas, capas ni URLs a los renders o al paquete; sus soluciones no se trataron como reglas universales.

## Llamadas integradas a image_gen

El contador global queda en **8/12**: las llamadas 1–7 produjeron las tres bases B3, A/B de miniatura R0 y A/B de flyer R0. La llamada 8 produjo la base limpia de reemplazo para thumbnail B R1. La composición correctiva R1 de texto (B3, flyer y miniatura) consumió **0 llamadas adicionales**. El detalle de prompts y rutas está en S9/imagegen-log.json y S9/prompts.md, incluida la entrada “Global call 8 — Thumbnail B R1 replacement base”.

## R0 — primera composición

| Pieza | Causa | Variable principal | Predicción registrada | Efecto observado | Rutas antes / después |
|---|---|---|---|---|---|
| B3, tres láminas | Evitar el problema de Paso 8 de repetir una misma retícula y adaptar frame-system a las tres bases disponibles. | Posición/escala del titular, relación con gesto cerámico y tinta medida bajo glyph-core; las bases usan center-fit al master, sin reencuadre distinto por lámina. | Variar la relación rim → rueda → huella sin tapar el gesto; seleccionar tinta según contraste medido en cada grupo. | Hubo variación de posición y tamaño, pero apoyo y acciones de S1, CTA de S2 y tres grupos pequeños de S3 quedaron bajo P05 4.5:1. El titular de S1 se acercó al borde de la vasija; se señaló para inspección. | Bases: S9/B3/base-1.png, base-2.png y base-3.png. Salida: S9/B3/final-1.png, final-2.png y final-3.png. |
| Thumbnail A/B | Probar la misma premisa de tres entradas / un portfolio con salida directa raster A y texto controlable B. | Método de letra (raster A frente a overlay Cropmark B) con el overlay exacto de cuatro palabras. | Mantener agentes y portfolio distinguibles y una silueta de titular legible en tamaños reducidos. | QA técnico estricto pasó el par. B tuvo P05 16.887:1; A conserva letra raster incrustada, con tipografía desconocida. No es una preferencia ni una comparación causal. | Fuente A: S9/thumbnail/A-source.png. Base B R0: S9/thumbnail/B-base-source.png. R0: S9/thumbnail/A.png y B.png. |
| Flyer A/B | Comparar texto directo raster A con texto editable Cropmark B en una escena de vinilo, conservando el copy exacto. | Método de letra y jerarquía de evento frente a sala/fecha/hora. | Mantener el evento primero, todos los datos legibles y ningún dato inventado. | QA pasó el par y contraste B pasó, pero el cap visible de la metadata B fue 13.33 px a 360; además, la segunda línea empezaba con separador. | Fuentes: S9/flyer/A-source.png y B-base-source.png. R0: S9/flyer/A.png y B.png. |

R0 no consumió rondas correctivas. A permanece como raster directo normalizado al tamaño master; sus letras no se retocaron y la fuente se declara desconocida. B se renderizó con fuentes OFL locales y capas de texto controlables. Los finales, sidecars y datos completos están en S9/rounds/R0/render-log.json, contrast-R0.json y final-manifest.json.

### Medición completa de R0

Contraste: píxeles del núcleo de glifo sobre el crop final antes de superponer texto; RGB se linealizó a sRGB relativo. P05 y mediana son razones por píxel. El porcentaje indica núcleo bajo el objetivo del grupo. Las alturas de mayúscula son medidas del archivo de fuente, no salida de QA.

| Pieza / lámina | Grupo y copia | P05 | Mediana | Bajo objetivo | Objetivo | Cap visible |
|---|---|---:|---:|---:|---:|---:|
| B3 / 1 | brand: TALLER BARRO | 5.287:1 | 8.091:1 | 0.000% | 4.5:1 | 14.33 px @360 |
| B3 / 1 | descriptor: CERÁMICA | 7.337:1 | 9.984:1 | 0.000% | 4.5:1 | 14.33 px @360 |
| B3 / 1 | headline: La forma toma cuerpo. | 3.667:1 | 9.296:1 | 4.903% | 3.0:1 | 31.67 px @360 |
| B3 / 1 | support: Una pieza empieza con un gesto. | 1.204:1 | 2.485:1 | 73.908% | 4.5:1 | 14.00 px @360 |
| B3 / 1 | cta: EXPLORA EL TALLER | 1.559:1 | 2.952:1 | 73.302% | 4.5:1 | 14.00 px @360 |
| B3 / 2 | brand: TALLER BARRO | 4.894:1 | 5.285:1 | 0.000% | 4.5:1 | 14.33 px @360 |
| B3 / 2 | descriptor: CERÁMICA | 5.219:1 | 8.036:1 | 0.000% | 4.5:1 | 14.33 px @360 |
| B3 / 2 | headline: Del giro nace el borde. | 5.551:1 | 7.867:1 | 0.000% | 3.0:1 | 28.00 px @360 |
| B3 / 2 | support: El torno acompaña cada movimiento. | 4.841:1 | 8.729:1 | 0.000% | 4.5:1 | 14.00 px @360 |
| B3 / 2 | cta: SIGUE EL PROCESO | 2.255:1 | 4.518:1 | 49.765% | 4.5:1 | 14.00 px @360 |
| B3 / 3 | brand: TALLER BARRO | 4.375:1 | 4.922:1 | 13.307% | 4.5:1 | 14.33 px @360 |
| B3 / 3 | descriptor: CERÁMICA | 4.309:1 | 4.705:1 | 27.885% | 4.5:1 | 14.33 px @360 |
| B3 / 3 | headline: Cada huella deja memoria. | 4.329:1 | 5.246:1 | 0.000% | 3.0:1 | 29.67 px @360 |
| B3 / 3 | support: Un rastro queda en la superficie. | 4.267:1 | 4.868:1 | 21.929% | 4.5:1 | 14.00 px @360 |
| B3 / 3 | cta: MIRA LAS PIEZAS | 7.860:1 | 10.109:1 | 0.000% | 4.5:1 | 14.00 px @360 |
| thumbnail/B | headline: 3 AIs. 1 Portfolio. | 16.887:1 | 17.642:1 | 0.000% | 3.0:1 | 20.67 px @360 |
| flyer/B | event: Noche de vinilos | 7.287:1 | 8.041:1 | 0.000% | 3.0:1 | 18.00 px @360 |
| flyer/B | venue_date: Sala Taller · 14 nov · 21:00 | 6.806:1 | 7.427:1 | 0.000% | 4.5:1 | 13.33 px @360 |

R0 registra un fallo de contraste por glyph-core en 7 grupos: seis de B3 y metadata del flyer B. En miniatura R0 el cap del titular fue 20.67 px a 360; evento del flyer 18 px; metadata 13.33 px. En B3 el cap pequeño fue ≥14 px a 360 y el titular ≥2× ese mínimo.

### QA estricto R0

| Grupo | Archivos | Resultado | Informe |
|---|---|---|---|
| carousel | 3/3 | FAIL, exit 1 | carousel/qa-report.json |
| thumb | 2/2 | PASS, exit 0 | thumb/qa-report.json |
| post | 2/2 | PASS, exit 0 | post/qa-report.json |

El fallo de carrusel mostró, según el estimador de entorno de QA, “Una pieza empieza con un gesto.” a 2.5:1, “EXPLORA EL TALLER” a 3.4:1 y “SIGUE EL PROCESO” a 4.0:1. Los logs completos están en S9/qa/R0/carousel-console.txt, thumb-console.txt y post-console.txt; cada subcarpeta contiene el JSON.

Comandos ejecutados:

> python3 skills/cropmark/qa/qa.py carousel --strict --expected-count 3 evals/art-direction/diagnostic-2026-10-22/renders/step9/B3/final-1.png evals/art-direction/diagnostic-2026-10-22/renders/step9/B3/final-2.png evals/art-direction/diagnostic-2026-10-22/renders/step9/B3/final-3.png --out evals/art-direction/diagnostic-2026-10-22/renders/step9/qa/R0/carousel
>
> python3 skills/cropmark/qa/qa.py thumb --strict --expected-count 2 evals/art-direction/diagnostic-2026-10-22/renders/step9/thumbnail/A.png evals/art-direction/diagnostic-2026-10-22/renders/step9/thumbnail/B.png --out evals/art-direction/diagnostic-2026-10-22/renders/step9/qa/R0/thumb
>
> python3 skills/cropmark/qa/qa.py post --strict --expected-count 2 evals/art-direction/diagnostic-2026-10-22/renders/step9/flyer/A.png evals/art-direction/diagnostic-2026-10-22/renders/step9/flyer/B.png --out evals/art-direction/diagnostic-2026-10-22/renders/step9/qa/R0/post

## R1 — corrección posterior a la revisión del feed R0

| Pieza | Causa | Variable principal | Predicción registrada | Efecto observado | Rutas antes → después |
|---|---|---|---|---|---|
| B3 | Fallos P05 de apoyo/acciones en S1–S2 y marca/descriptor/apoyo en S3; contacto del glyph-core del titular S1 con la zona de vasija; jerarquía de S2 ponía apoyo/acción antes del titular. | Posición y color de bloques secundarios sobre zonas tranquilas medidas. | Obtener P05 ≥4.5:1 en todo copy pequeño, conservar titular ≥2× cap pequeño, eliminar contacto y restaurar titular antes de apoyo/CTA en S2. | Los 15 grupos pasan sus objetivos; todas las mayúsculas pequeñas son ≥14 px a 360, los titulares ≥2×; cero intersecciones de glyph-core con límites conservadores de objetos, cero cajas de texto cruzadas y ningún grupo fuera del lienzo. La caja de titular S1 se movió 20 px arriba tras medir 77 píxeles de glyph-core dentro de la zona aproximada de borde; en el final esa intersección es cero. | S9/B3/final-1.png, final-2.png y final-3.png → S9/rounds/R1/B3/final-1.png, final-2.png y final-3.png. |
| Flyer B | Metadata R0 por debajo de cap 14 px y con separador huérfano al inicio de línea. | Jerarquía/tamaño del bloque metadata. | Mantener string exacto en una unidad de lectura coherente, unir el separador a “Sala Taller”, subir cap a ≥14 px y conservar contraste. | “Sala Taller ·” / “14 nov · 21:00”; cap 14.33 px a 360, P05 6.773:1; sin glyph-core en la zona del vinilo. | S9/flyer/B.png → S9/rounds/R1/flyer-B.png; A sigue en S9/flyer/A.png. |
| Thumbnail B | Se autorizó una base B de reemplazo para representar agentes actuando sobre un portfolio; el primer borrador de overlay R1 cortó la segunda línea y no respetó 40 px al borde inferior. | Representación/posición del overlay en la nueva base limpia. | Conservar el texto exacto en dos líneas dentro de la banda inferior izquierda, completo en previews de 168/320/360 px, con siluetas y zona de duración libres. | “3 AIs. 1 Portfolio.” completa en los tres tamaños; P05 17.579:1, cap 8.79 px en preview 168, 43 px de despeje inferior. | Base original: S9/thumbnail/B-base-source.png; base nueva: S9/thumbnail/B-base-R1-source.png. R0 B: S9/thumbnail/B.png → R1 B: S9/thumbnail/B-R1.png; A sigue en S9/thumbnail/A.png. |

B3 conserva las tres cadenas de acción: EXPLORA EL TALLER y SIGUE EL PROCESO son texto llano; solo MIRA LAS PIEZAS conserva subrayado. El color blanco puro de marca/descriptor/apoyo de S3 sube sus medidas P05 sobre el objetivo. El flyer conserva la secuencia y puntuación exactas al unir el salto de línea. Las versiones R1 tienen render y fuentes editables. Las correcciones internas de posición del titular S1, orden de S2 y tamaño/posición de miniatura se documentaron como refinamientos del mismo pase R1, no como rondas adicionales. No se generó imagen para las correcciones de texto.

### Contraste y cap completos R1

| Pieza / lámina | Grupo y copia | P05 | Mediana | Bajo objetivo | Objetivo | Cap visible |
|---|---|---:|---:|---:|---:|---:|
| B3 / 1 | brand: TALLER BARRO | 5.287:1 | 8.091:1 | 0.000% | 4.5:1 | 14.33 px @360 |
| B3 / 1 | descriptor: CERÁMICA | 7.337:1 | 9.984:1 | 0.000% | 4.5:1 | 14.33 px @360 |
| B3 / 1 | headline: La forma toma cuerpo. | 5.500:1 | 9.277:1 | 0.000% | 3.0:1 | 31.67 px @360 |
| B3 / 1 | support: Una pieza empieza con un gesto. | 7.588:1 | 9.048:1 | 0.000% | 4.5:1 | 14.00 px @360 |
| B3 / 1 | cta: EXPLORA EL TALLER | 5.464:1 | 7.122:1 | 0.000% | 4.5:1 | 14.00 px @360 |
| B3 / 2 | brand: TALLER BARRO | 4.894:1 | 5.285:1 | 0.000% | 4.5:1 | 14.33 px @360 |
| B3 / 2 | descriptor: CERÁMICA | 5.219:1 | 8.036:1 | 0.000% | 4.5:1 | 14.33 px @360 |
| B3 / 2 | headline: Del giro nace el borde. | 6.816:1 | 8.659:1 | 0.000% | 3.0:1 | 28.00 px @360 |
| B3 / 2 | support: El torno acompaña cada movimiento. | 5.630:1 | 7.954:1 | 0.000% | 4.5:1 | 14.00 px @360 |
| B3 / 2 | cta: SIGUE EL PROCESO | 5.166:1 | 5.424:1 | 0.000% | 4.5:1 | 14.00 px @360 |
| B3 / 3 | brand: TALLER BARRO | 4.851:1 | 5.458:1 | 0.000% | 4.5:1 | 14.33 px @360 |
| B3 / 3 | descriptor: CERÁMICA | 4.778:1 | 5.217:1 | 0.000% | 4.5:1 | 14.33 px @360 |
| B3 / 3 | headline: Cada huella deja memoria. | 4.799:1 | 5.817:1 | 0.000% | 3.0:1 | 29.67 px @360 |
| B3 / 3 | support: Un rastro queda en la superficie. | 4.731:1 | 5.397:1 | 0.000% | 4.5:1 | 14.00 px @360 |
| B3 / 3 | cta: MIRA LAS PIEZAS | 7.860:1 | 10.109:1 | 0.000% | 4.5:1 | 14.00 px @360 |
| flyer_B | event: Noche de vinilos | 7.287:1 | 8.041:1 | 0.000% | 3.0:1 | 18.00 px @360 |
| flyer_B | venue_date: Sala Taller · 14 nov · 21:00 | 6.773:1 | 7.365:1 | 0.000% | 4.5:1 | 14.33 px @360 |
| thumbnail_B | headline: 3 AIs. 1 Portfolio. | 17.579:1 | 17.751:1 | 0.000% | 3.0:1 | 8.79 px @168 |

Mínimos R1: B3 pequeños P05 4.731:1 (mediana 5.217:1) y titulares P05 4.799:1 (mediana 5.817:1); el subcopy del flyer P05 6.773:1, 14.33 px de cap; thumbnail B P05 17.579:1. En todos los grupos el porcentaje bajo el objetivo fue 0.000%. La tabla y el detalle de sRGB lineal completo están en S9/rounds/R1/contrast-R1.json. S9/rounds/R1/placement-evidence.json registra cajas, márgenes, intersecciones de glifo y zonas de objeto; son rectángulos conservadores trazados tras inspección visual, no segmentación semántica automática. Los previews de miniatura están en S9/rounds/R1/thumbnail/B-R1-168.png, B-R1-320.png y B-R1-360.png.

### QA estricto R1

Checks de una condición sobre las salidas nuevas:

| Grupo | Archivos | Resultado | Informe |
|---|---|---|---|
| carousel | 3/3 | PASS, exit 0 | carousel/qa-report.json |
| thumb | 1/1 | PASS, exit 0 | thumb/qa-report.json |
| post | 1/1 | PASS, exit 0 | post/qa-report.json |

Checks de par final A/B (A se lee sin modificar y B usa la salida R1):

| Grupo | Archivos | Resultado | Informe |
|---|---|---|---|
| thumb-pair | 2/2 | PASS, exit 0 | thumb-pair/qa-report.json |
| post-pair | 2/2 | PASS, exit 0 | post-pair/qa-report.json |

Las órdenes completas y sus stdout están en S9/qa/R1/carousel-console.txt, thumb-console.txt, post-console.txt, thumb-pair-console.txt y post-pair-console.txt; informes machine-readable en las subcarpetas correspondientes. El pase QA no sustituye la lectura visual.

Comandos ejecutados:

> python3 skills/cropmark/qa/qa.py carousel --strict --expected-count 3 evals/art-direction/diagnostic-2026-10-22/renders/step9/rounds/R1/B3/final-1.png evals/art-direction/diagnostic-2026-10-22/renders/step9/rounds/R1/B3/final-2.png evals/art-direction/diagnostic-2026-10-22/renders/step9/rounds/R1/B3/final-3.png --out evals/art-direction/diagnostic-2026-10-22/renders/step9/qa/R1/carousel
>
> python3 skills/cropmark/qa/qa.py thumb --strict --expected-count 1 evals/art-direction/diagnostic-2026-10-22/renders/step9/thumbnail/B-R1.png --out evals/art-direction/diagnostic-2026-10-22/renders/step9/qa/R1/thumb
>
> python3 skills/cropmark/qa/qa.py post --strict --expected-count 1 evals/art-direction/diagnostic-2026-10-22/renders/step9/rounds/R1/flyer-B.png --out evals/art-direction/diagnostic-2026-10-22/renders/step9/qa/R1/post
>
> python3 skills/cropmark/qa/qa.py thumb --strict --expected-count 2 evals/art-direction/diagnostic-2026-10-22/renders/step9/thumbnail/A.png evals/art-direction/diagnostic-2026-10-22/renders/step9/thumbnail/B-R1.png --out evals/art-direction/diagnostic-2026-10-22/renders/step9/qa/R1/thumb-pair
>
> python3 skills/cropmark/qa/qa.py post --strict --expected-count 2 evals/art-direction/diagnostic-2026-10-22/renders/step9/flyer/A.png evals/art-direction/diagnostic-2026-10-22/renders/step9/rounds/R1/flyer-B.png --out evals/art-direction/diagnostic-2026-10-22/renders/step9/qa/R1/post-pair

## Referencias de salida y editabilidad

- Renderer R0: S9/render_s9.py. Renderer correctivo R1: S9/rounds/R1/render_r1.py.
- Fuentes OFL, sus licencias y manifiesto: S9/fonts/.
- Prueba de paquete y edición localizada fuera del proyecto: S9/package/editability-proof.json.
- Hojas/previews de thumbnail R1: S9/thumbnail/working-thumb-R1.png y S9/rounds/R1/thumbnail/.
- Llamadas/prompts: S9/imagegen-log.json y S9/prompts.md.

## Límites e interpretación

La muestra contiene un solo carrusel ficticio, una miniatura y un flyer ficticio. El fondo B de miniatura R1 difiere del fondo de miniatura A y de la base B R0; la llamada 8 cambió la escena para mostrar tres agentes activos alrededor de un portfolio. A conserva letra raster de fuente desconocida y B letra editable. En flyer, A también conserva lettering incrustado y B es editable. Por tanto, el ensayo no demuestra que Cropmark cause mejor legibilidad o calidad ni compara exactamente el método sobre la misma imagen. No se midieron preferencias de personas ni se hizo validación de referencia. QA es técnico y no confirma mérito visual.

No se modificaron el gate, umbrales de QA, benchmark ni el archivo de feedback; no se cambió su estado. El archivo docs/recalibration-v3-human-feedback.json mantiene el estado 0/17 y SHA-256 esperado 31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38.

## Juicio visual final de Sol / T4

Juicio de revisión visual del modelo, no una medición de preferencia humana ni evidencia causal. Resultado recibido:

- **Carrusel — preferencia: set B2.** B3 recupera la legibilidad de S1 y despeja el titular del borde de la vasija; S3 es la lámina más fuerte. Aun así, las columnas de texto de S1/S2 quedan muy junto a la imagen y la jerarquía general sigue densa frente a B2. Frente a 11-03 y 19-06, la relación entre masas tipográficas, escala y roles del texto es menos decisiva. B3 mejora R0, pero permanece por debajo de esas referencias.
- **Thumbnail — preferencia: B-R1.** Los tres agentes activos alrededor del portfolio comunican la acción con más claridad y el overlay es compacto; la frase se lee completa a 360 y 320 px, aunque a 168 px se entiende con menos inmediatez cuántas acciones ocurren. La escena se lee como un tablero físico, lo que limita la especificidad de un portfolio digital; además, los numerosos props laterales ocupan espacio sin ayudar. A 168 px, distinguir las tres acciones requiere atención. Frente a 02-10, sujeto y situación tendrían que sobrevivir con menos dependencia del detalle. B-R1 es la opción más cercana conceptualmente al encargo, pero aún es menos inmediata a 168 px.
- **Flyer — preferencia: A.** B-R1 agrupa mejor la metadata y mantiene reconocible el vinilo, pero el bloque de metadata pesa demasiado y la tipografía horizontal se integra menos que en A. Frente a la referencia 19-06 —comparación parcial— aún falta esa integración de la letra con la escena. Sol considera que A conserva mejor jerarquía que B-R1, aunque su lettering sea raster y de fuente desconocida.

El juicio no declara un nivel de referencia ni valida las reglas candidatas. No afirma preferencia humana, efecto causal ni aprobación del gate. Las brechas descritas continúan abiertas.

## Verificación técnica independiente T5

T5 repitió los comandos estrictos sobre los tres grupos congelados y obtuvo PASS (carrusel 3/3, miniatura 2/2 y flyer 2/2; exit 0 en los tres). La revisión manual independiente confirmó copy completo, sin clipping ni oclusiones; recalculó el contraste sobre núcleos de glifo y las alturas de cap, y derivó las hojas desde los PNG finales. También verificó la integridad del hash de feedback y el estado 0/17. La llamada 8 del registro quedó enlazada con `copied_to`, SHA-256 y `byte_identical: true`. Esto verifica ejecución e integridad de archivos; no constituye aprobación estética, preferencia humana, evidencia causal ni cambio de gate.
