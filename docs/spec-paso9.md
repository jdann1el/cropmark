# Spec — Paso 9: especificidad y transferencia entre formatos

Mejorar la especificidad visual y el ritmo de Taller Barro sin perder la lectura conseguida en B2; observar además una miniatura y un flyer en dos condiciones. Es un ensayo de tres piezas de trabajo, no una validación de Cropmark ni una prueba causal. Criterios congelados antes de generar: no se relajan después para obtener PASS.

## Alcance y condiciones

- **P1 — B3:** carrusel Taller Barro, tres finales de 1080 × 1350. Reutiliza el copy de B2; compara exactamente tres filas: A directo de Paso 7, B2 de Paso 8 y B3, a 360 × 450 por lámina. Los artefactos anteriores permanecen sin alterar.
- **P2 — thumbnail A/B:** vídeo `I let 3 AI agents redesign my portfolio`; dos finales de 1280 × 720. Overlay común exacto `3 AIs. 1 Portfolio.` (cuatro palabras); el título completo identifica el vídeo, no es copy adicional obligatorio en la imagen. No se inventa un resultado de los agentes.
- **P3 — flyer A/B:** evento ficticio de Barcelona; dos finales de 1080 × 1350. Copy exacto `Noche de vinilos · Sala Taller · 14 nov · 21:00`. No añadir dirección, precio, año, disponibilidad ni otras afirmaciones.
- En P2/P3, **A** es image_gen directo, prompt sin instrucciones del skill y salida raster final; **B** usa Cropmark, base generada limpia sin texto/logos y tipografía exacta en capas controlables. Se conservan prompts y salidas reales, incluidas letras deformadas de A. Una A defectuosa sigue siendo evidencia del ensayo, con FAIL de entrega donde corresponda; no se repara silenciosamente ni se degrada adrede.
- Cambios del skill solo derivados del diagnóstico de Paso 8 y del estudio: especificidad del gesto/objeto, ritmo de serie, jerarquía y tratamiento de marca/CTA, transferencia a thumbnail/post. Se mantiene el estado candidato sin validar.

Copy B3, por orden; `/` indica corte de línea, no carácter que añadir:

| Lámina | Descriptor | Titular | Apoyo | CTA |
|---|---|---|---|---|
| 1 | CERÁMICA | La forma / toma cuerpo. | Una pieza empieza con un gesto. | EXPLORA EL TALLER |
| 2 | CERÁMICA | Del giro / nace el borde. | El torno acompaña cada movimiento. | SIGUE EL PROCESO |
| 3 | CERÁMICA | Cada huella / deja memoria. | Un rastro queda en la superficie. | MIRA LAS PIEZAS |

Marca en las tres láminas: `TALLER BARRO`; descriptor exacto confirmado en B2: `CERÁMICA`. Se conserva todo el copy exacto de Paso 8, incluidas las tres cadenas de la columna CTA; solo `MIRA LAS PIEZAS` recibe tratamiento visual de CTA. `EXPLORA EL TALLER` y `SIGUE EL PROCESO` permanecen como texto llano integrado, sin botón ni pastilla. Se usan fuentes OFL locales y se registra el archivo real.

## Estudio previo y dirección inicial

Leídos: spec/diagnóstico/candidato de Paso 8, ruta Cropmark, módulos carousel/thumbnail/post, carousel-system, story-in-frame, typography, imagery, composition-study y checklist. Inspeccionadas solo como estudio las imágenes locales 05-02, 08-04 y las hojas 02, 04, 07, 11 y 19: expansión de frase, masas de titular alrededor de imagen, silueta de miniatura, agrupación de copy y protagonismo material. Ni la apariencia ni el contraste de una muestra convierten su solución en regla universal; los flyers de evento requieren declarar la comparabilidad parcial de esas referencias.

Una comparación inicial `jev.compare_options` recomendó **gesto de arcilla como ancla**: contorno de vasija, arco del torno y huella protagonista; copy sin oclusión y zonas tranquilas comprobadas. Ranking: gesto 87,3 (confianza 0,759), póster/collage 24,5 (0,796), columna repetida 17,4 (0,711). Criterios: especificidad 40 %, lectura 35 %, secuencia 25 %; gesto recibió 3,86 / 3,13 / 3,41. Es orientación, no verificación visual ni una escala de calidad calibrada. No repetir la comparación para buscar otro resultado.

Antes de generar B, cada pieza registra dirección, inventario, conceptos/bocetos conforme a la ruta aplicable y zonas para todo el copy. B3 resuelve portada + interior exigente antes del cierre; el diagnóstico de B2 permite una evolución acotada. La comparación con referencias usa vistas temporales fuera del repo, IDs y observaciones; no importa sus píxeles al artefacto.

## Criterios congelados por artefacto

| Artefacto | Evidencia y condición verificable |
|---|---|
| B3 (3 PNG + fuentes/capas/sidecars) | Dimensiones exactas y cadenas anteriores completas; cero oclusión de copy obligatorio; marca y las tres cadenas de acción legibles a 360 px. Solo el cierre `MIRA LAS PIEZAS` recibe tratamiento de CTA; `EXPLORA EL TALLER` y `SIGUE EL PROCESO` se integran como texto llano sin botón ni pastilla. Un gesto cerámico identificable por lámina. Al menos dos relaciones imagen–titular distintas en la serie, nombradas y visibles, además del mero cambio de motivo fotográfico. Portada introduce forma, interior movimiento, cierre huella; el juicio comprueba si la relación supera la simple vecindad temática de B2. |
| Thumbnail A/B (2 PNG) | 1280 × 720; overlay común exacto y ≤4 palabras. Inspección completa y previews por condición a 360, 320 × 180 y 168 × 95: a 360 y 320 se lee cada palabra; a 168 sobreviven sujeto/premisa y silueta del titular. Tres agentes y un portfolio deben quedar sugeridos sin prometer éxito ni mostrar métricas falsas. Ninguna información esencial en los 40 px de borde ni en la zona de duración inferior derecha (18 % × 15 %). A registra cualquier incumplimiento; B conserva copy editable. |
| Flyer A/B (2 PNG) | 1080 × 1350; las cuatro unidades del copy exacto se leen a 360 × 450 y no hay hechos añadidos. Jerarquía distingue evento de sala/fecha/hora; un elemento reconocible de vinilo/escucha participa en la composición. Copy esencial dentro de 64 px de margen. A registra cualquier incumplimiento; B conserva copy editable. |
| Contraste de B3 y B singles | Por cada grupo real de texto: caja, tinta, fuente, luminancia sRGB linealizada bajo núcleo de glifos, P05, mediana y porcentaje bajo umbral. P05 ≥4,5:1 para secundarios y ≥3:1 para titular grande; todas las palabras legibles en feed aunque la estadística pase. Medir fondo antes de efectos; sombras/contornos desactivados por defecto y ninguna excepción sustituye corregir soporte. |
| Comparativas | Salidas exactas: `S9/carousel-AB3-feed.png` (nueve celdas de 360 × 450: filas A de Paso 7 directo, B2 de Paso 8, B3; columnas láminas 1–3); `S9/thumb-AB.png` y `S9/flyer-AB.png` (parejas A/B); `S9/thumb-AB-360.png` y `S9/flyer-AB-360.png` (lado a lado con cada condición a 360 px de ancho). Añadir vistas de thumbnail a 320 y 168 px. Celdas derivadas de los finales reales sin retocarlos. Registrar por separado lectura, especificidad, jerarquía, acabado y límites de comparación; no presuponer que B gane. |
| QA y paquete | QA estricto por formato: `carousel --expected-count 3`, `thumb --expected-count 2`, `post --expected-count 2`; conservar comandos, salidas y fallos. Contrato y design_check cuando haya paneles ajustados o ejes/huecos prometidos; metas previas, no ajustadas al resultado. Fuentes/licencias, bases, capas y render reproducible para B; prueba de paquete fuera de la carpeta original y edición localizada de texto. A se declara raster sin capas originales editables. |
| Juicio final | Revisor distinto del ejecutor abre todos los finales y comparativas; coteja referencias a la misma escala cuando sean comparables. Por pieza: PASS/FAIL/pendiente técnico y juicio visual separado con al menos tres observaciones concretas y brechas residuales. Un pase de QA no establece nivel de referencia. |

**T-6:** no justificar forzosamente ni estirar espacios en líneas cortas por defecto. Registrar cortes y avances reales; cualquier excepción exige función compositiva visible y lectura comprobada. No usar el referente 05-02 como permiso general para dispersar palabras.

## Presupuesto y correcciones

Tope global absoluto: **12 llamadas integradas a image_gen**, incluidos fallos y reintentos. Plan inicial: tres bases B3 + A/B thumbnail + A/B flyer = **7**; reserva máxima de **5**, repartida según defectos observados. Registrar cada llamada antes/de inmediato después: pieza, prompt exacto, número global, estado y ruta. **Cualquier fallo o indisponibilidad de la herramienta detiene toda generación**; registrar bloqueo y pendientes, sin CLI, API key, otro generador ni proveedor. No consumir reserva por rutina.

Cada pieza P1/P2/P3 dispone de R0 más **hasta tres rondas correctivas**; P1 consume rondas por el conjunto de tres láminas y P2/P3 por su pareja A/B. No son tres rondas por archivo ni por condición. Cada ronda registra imagen/región, defecto, variable principal, predicción, acción y efecto observado; un cambio de concepto cuenta. A conserva su condición directa, cualquier nueva generación cuenta contra el tope y se conserva la versión anterior. Al límite, parar y entregar fallos/pendientes honestos.

## Tareas, dependencias y archivos permitidos

`S9` = `evals/art-direction/diagnostic-2026-10-22/renders/step9/`. Los nombres internos se registran en un manifiesto, sin ampliar permisos fuera de esos árboles. Ningún rol cambia de modelo/esfuerzo silenciosamente; no usar Astra.

| ID / depende de | Rol exacto | Entrega y archivos permitidos |
|---|---|---|
| T0 / — | **gpt-6.1-sol / high**, spec/plan y posterior juez independiente de diseño | Este `docs/spec-paso9.md`; juicio final comunicado al principal tras T4. No ejecuta skill, generación, render, QA, commits ni push. |
| T1 / T0 | **gpt-6-luna / high**, ejecutor | Dirección/briefs en `S9/`; dos briefs según TEMPLATE, marcados explícitamente como ficticios de prueba: `skills/cropmark/briefs/example-portfolio-agents-thumbnail-test.md` y `skills/cropmark/briefs/example-noche-vinilos-flyer-test.md`. Reglas candidatas solo en `skills/cropmark/SKILL.md`, `formats/{carousel,thumbnail,post}.md`, `techniques/{carousel-system,story-in-frame,typography,imagery}.md`, `references/visual-rules.md`, `qa/checklist.md`; registro en `docs/candidate-update-2026-10-23.md`. No tocar umbrales/código QA. |
| T2 / T1 | **gpt-6-luna / high**, prompts y generación | Prompts exactos, manifiesto y `S9/imagegen-log.json`; imágenes solo en `S9/{B3,thumbnail,flyer}/`. Mantiene A sin skill/B con skill y presupuesto global. |
| T2b / T2, por activo | **gpt-6-luna / low**, mecánico | Copias byte a byte de activos generados al árbol de su pieza; dimensiones/hash registrados. No altera originales. |
| T3 / bases revisadas de T2b | **gpt-6-luna / high**, compositor, render y documentación | Scripts, capas, contratos, fuentes/licencias, rondas y finales en `S9/`; diagnóstico `docs/diagnostic-2026-10-24-paso9.md`. Respeta revisión de representativos antes de extender B3 y conserva las tres cadenas de acción: las dos primeras como texto llano integrado, solo `MIRA LAS PIEZAS` con tratamiento de CTA. |
| T3b / T3, por final | **gpt-6-luna / low**, mecánico | Contact sheets y previews dentro de `S9/`, derivados de finales sin alterarlos. |
| T4 / T3 y T3b | QA/registro: **gpt-6-luna / high**; juicio: **gpt-6.1-sol / high** | Ejecutor guarda QA/contraste en `S9/qa/` y diagnóstico. Juez solo lectura; devuelve juicio para que el ejecutor lo registre fielmente. |
| T5 / T4 y entregables completos | **gpt-6-luna / high**, verificador nuevo distinto del ejecutor | Solo lectura; informes propios en `/tmp`. Recalcula comprobaciones, hashes, cuentas, exclusiones y criterios sin depender del relato del ejecutor. |
| T6 / T5 | **gpt-6-luna / low**, integración mecánica si está autorizada por el principal | Solo paths anteriores y metadatos Git: stage por paths, commits e intento de push a `cropmark-reference-library` bajo la autorización existente. Verifica diff y resultado; sin merge/publicación. |

## Límites intactos

No benchmark de 18 corridas, instalación, merge, publicación, nueva aprobación humana, cambio de gate/ledger ni conclusión causal. No modificar `docs/recalibration-v3-human-feedback.json`: SHA-256 esperado `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38`; hash y estado **0/17** al nivel de referencia permanecen sin cambios. Refs locales son solo estudio: no copiar imágenes, capas, texturas, rutas de importación ni URLs CDN al paquete/repo; citar IDs y observaciones basta. No stagear QA ajeno de Step3 ni `__pycache__`. Antes de integrar, verificar hash, diff, archivos stageados y ausencia de referencias. Este spec no declara completadas las tareas posteriores.
