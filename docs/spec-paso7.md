# Spec de trabajo — Paso 7: primera prueba con imagen generada

## Objetivo

Comparar, en un solo brief de Taller Barro y sin atribuir causalidad, un carrusel 4:5 de tres láminas generado directamente (A) con otro que use imágenes base generadas sin texto y la composición tipográfica de Cropmark (B).

## Entra

- Mismo copy, tema, formato y secuencia cover/interior/cierre en A y B.
- A conserva los prompts directos exactos y usa la imagen generada como lámina final.
- B usa bases generadas sin texto/logos, tipografía superpuesta con fuentes OFL del repo, relación titular–objeto, control a 360 px y QA.
- Hoja AB de seis láminas a 360 × 450; revisión visual humana del feed antes de las láminas individuales.
- Registro español con prompts, llamadas usadas, defectos observados, paths, veredicto A/B y límites.

## No entra

- Más briefs, benchmark de 18 corridas, cambios al gate, aprobación, prueba causal, instalación, publicación o merge.
- Imágenes de referencias, `refs-cache/` o URLs CDN; cambios al JSON de feedback; cambios de reglas no relacionados con este experimento.
- Más de 12 llamadas integradas a image_gen; ningún CLI, API key ni reintento con otro generador.

## Criterios de aceptación verificables

1. Hay tres slides A y tres slides B en `evals/art-direction/diagnostic-2026-10-22/renders/step7/`; las dimensiones finales son 1080 × 1350.
2. `A/prompts.txt` contiene el texto exacto de cada prompt A. `B/prompts.txt` contiene los prompts exactos de las bases B; estas no llevan copy ni marcas dentro de la imagen.
3. B usa las mismas cadenas del brief, fuentes OFL locales y un mecanismo objeto–titular visible; la frase completa se lee a 360 px. `AB-feed.png` muestra A y B, tres láminas por fila, cada una a 360 × 450.
4. Revisión propia del feed y láminas completas documentada; slop, lectura, relación objeto–titular y aptitud de diseñador se juzgan por separado y con honestidad.
5. Se ejecutan las comprobaciones de QA aplicables y se informa si pasan o fallan; no se ocultan fallos ni se presenta una corrida como prueba para la puerta.
6. Feedback JSON mantiene SHA-256 `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38` y respuestas vacías; no se tocan gate ni benchmark.
7. El diff no incorpora referencias ni CDN; no se stagea `renders/step3/qa-report.json/`; los cambios se comprometen con la identidad indicada y se intenta el push autorizado a la rama.

## Límites

Tope absoluto: 12 llamadas a image_gen integradas contando reintentos. Ante fallo o indisponibilidad, parar generación inmediatamente, no usar API key/CLI y registrar qué quedó pendiente. No ejecutar benchmark; no alterar gate, feedback, ledger ni benchmark. El resultado corresponde a un brief y no cuenta para la puerta. El estado 0/17 al nivel de referencia permanece honesto.

## Tareas

| ID | Entrada | Salida esperada | Archivos permitidos | Hecho cuando |
|---|---|---|---|---|
| T0 — Spec/plan | Brief, petición y reglas actuales | Este spec y tareas acotadas | `docs/spec-paso7.md` | Scope, exclusiones, límites y criterios están registrados antes de cerrar la ejecución. |
| T1 — Generar A/B | Brief Taller Barro, prompts aprobados por principal | 3 A finales y 3 bases B generadas | `.../renders/step7/A/`, `.../renders/step7/B/` | Todas son resultado de image_gen integrado; llamadas registradas; B text-free. |
| T2 — Componer B/feed | Assets T1 y copy fijo | Compositor, B compuestas y `AB-feed.png` | `.../renders/step7/render_step7.py`, `.../renders/step7/B/`, `.../renders/step7/AB-feed.png` | B tiene copy exacto, fuentes locales; feed seis-up exportado a escala fijada. |
| T3 — Diagnóstico | Imágenes finales, juicio visual del principal, salidas QA | Registro español Paso 7 | `docs/diagnostic-2026-10-23-real-imagery.md` | Cada condición y límite queda descrito sin inferir aprobación/causalidad. |
| T4 — QA | Láminas finales B y sidecars | Resultado QA estricto | Solo `/tmp` para informes/vistas | Ejecuta carousel QA en las tres láminas y registra tanto fallos como pases. |
| T5 — Verificación independiente | Spec y salidas terminadas | Lista de criterios verificada contra repo | Solo lectura; informes QA en `/tmp` | Un subagente distinto del ejecutor coteja criterios y adjunta comandos/salidas, sin basarse solo en su reporte. |
| T6 — Integración | Artefactos revisados, hallazgos QA y scans previos | Commits con identidad fijada y push a la rama | Paths permitidos del Paso 7 y Git | Solo archivos permitidos quedan en commits; el push termina en `origin/cropmark-reference-library`. |

El principal decide los prompts y realiza el juicio creativo; los subagentes ejecutan tareas delimitadas y devuelven evidencia de comandos y resultados.

## Estado y evidencia de cierre

| Tarea | Estado | Evidencia |
|---|---|---|
| T1 — Generar A/B | Entregada | 6 llamadas integradas exitosas y activos copiados a `evals/art-direction/diagnostic-2026-10-22/renders/step7/A/` y `B/`; no hubo reintentos. |
| T2 — Componer B/feed | Entregada | `render_step7.py` produjo las seis láminas finales 1080 × 1350, bases B y `AB-feed.png` con mosaicos de 360 × 450. |
| T3 — Diagnóstico | Entregada | `docs/diagnostic-2026-10-23-real-imagery.md`; autorevisión visual del principal, con límites expresos. |
| T4 — QA/finish | Completa; QA estricto falla contraste | QA estricto de carrusel verificó dimensiones y titulares, pero devolvió salida 1 por contraste en elementos secundarios. |
| T5 — Verificación independiente | Completa | El verificador confirma criterios 1–4 y 6–7; criterio 5 permanece FAIL por contraste secundario en QA estricto. |
| T6 — Integración | Completa | Commits `5cccdf0` y `9a48e68`; push exitoso a `origin/cropmark-reference-library`, cuyo ref local coincide con HEAD. |

La verificación independiente no sustituye el juicio visual del principal ni convierte esta prueba en evidencia de puerta o causalidad. El QA de contraste sigue fallando; no implica aprobación visual ni prueba para la puerta.
