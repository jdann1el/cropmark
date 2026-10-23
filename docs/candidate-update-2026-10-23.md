# Candidato de actualización de Cropmark — 2026-10-23

> **Estado: CANDIDATO, sin validar hasta que pase la puerta.** Los cambios de skill están en esta rama para revisión; no se han publicado ni fusionado. La puerta y el benchmark no se modifican. No hay aprobación ni prueba causal.

## Qué se añade

Se prueba un campo opcional de relación titular–objeto para composiciones que dependan de ese vínculo: palabras concretas, superficie/gesto, orden de capas, fracción de tinta cubierta y límite de lectura. Requiere revisar a 360 px que el objeto y la frase completa sobrevivan sin caption. Las rondas priorizan el mecanismo central y la medida/posición antes de textura o acabado. Se suman cuatro comprobaciones concretas del estudio de 21 piezas: rag sin justificar/estirar (T-6), separación vertical por grupos, cortes y proporción de rag, y presupuesto orientativo de tipos decorativos. No son leyes estéticas ni plantillas.

## Inventario de archivos cambiados

### Documentación y módulos de skill

- `docs/diagnostic-2026-10-22-typographic-carousel.md` — registra Paso 6, las dos correcciones, rutas y veredicto visual limitado.
- `docs/proposed-edits-next-skill-update.md` — convierte la propuesta en candidato integrado, incorpora Pasos 6 y 6b y mantiene abiertas las pruebas de puerta.
- `docs/candidate-update-2026-10-23.md` — este changelog y el estado del candidato.
- `skills/cropmark/SKILL.md` — una línea de routing hacia el mecanismo y R15.
- `skills/cropmark/techniques/carousel-system.md` — datos de relación titular–objeto, comprobación a 360 px y prioridad de rondas.
- `skills/cropmark/references/visual-rules.md` — R15 y cuatro comprobaciones de composición/type derivadas del estudio, redactadas como diagnósticos checkables.
- `skills/cropmark/qa/checklist.md` — evidencia de capas/fracción de tinta y lectura de la frase a 360 px.
- `skills/cropmark/briefs/example-taller-barro.md` — brief ficticio de cerámica para comprobar la redacción con otro sector.

### Código de render y contratos

- `evals/art-direction/diagnostic-2026-10-22/render_step6.py` — renderer reproducible de la reparación Paso 6.
- `evals/art-direction/diagnostic-2026-10-22/renders/step6/layout-contract.json` — alineaciones, margen y cruce intencional declarados para la serie final.
- `evals/art-direction/diagnostic-2026-10-22/render_step6b.py` — renderer de bocetos, representativos y entrega de tres láminas para el brief nuevo.
- `evals/art-direction/diagnostic-2026-10-22/renders/step6b/direction.md` — dirección previa, conceptos, comparador, ronda y revisión final.
- `evals/art-direction/diagnostic-2026-10-22/renders/step6b/layout-contract.json` — alineaciones, márgenes, separaciones y solapes deliberados del set.

### Renders Paso 6

- `evals/art-direction/diagnostic-2026-10-22/renders/step6/R{0,1,2}-feed-3up.png` — hojas comparables de las tres rondas.
- `evals/art-direction/diagnostic-2026-10-22/renders/step6/slide-{cover,inner,close}-R{0,1,2}.png` y cada `.png.boxes.json` — nueve láminas y sidecars.

### Renders de validación Paso 6b

- `evals/art-direction/diagnostic-2026-10-22/renders/step6b/sketch-A.png`, `sketch-A.png.boxes.json`, `sketch-B.png`, `sketch-B.png.boxes.json`, `sketches-feed-2up.png` — dos composiciones previas y su comparativa.
- `evals/art-direction/diagnostic-2026-10-22/renders/step6b/R{0,1,2}-representative-feed-2up.png` — lectura a feed de portada + proceso por ronda.
- `evals/art-direction/diagnostic-2026-10-22/renders/step6b/slide-{cover,process}-R{0,1,2}.png` y cada `.png.boxes.json` — seis láminas representativas y sidecars.
- `evals/art-direction/diagnostic-2026-10-22/renders/step6b/R2-before-round2-feed-3up.png`, `slide-close-R2-before-round2.png` — antes de corregir el contacto accidental descubierto al extender.
- `evals/art-direction/diagnostic-2026-10-22/renders/step6b/R2-feed-3up.png`, `slide-{cover,process,close}-R2.png` y cada `.png.boxes.json` — hoja final y tres láminas revisadas.

Todos los renders comprometidos son arte vectorial trazado por código y tipografía de fuentes OFL empaquetadas. No se incluyen imágenes de `refs-cache/` ni del repositorio de referencias. El comparador temporal de Paso 6b está en `/tmp/cropmark-step6b-comparator.png`, fuera del cambio.

## Evidencia y límites

- **Paso 1:** las cajas ayudan a medir transferencia, pero no sustituyen el juicio sobre forma, peso y ocupación de fuente.
- **Paso 2:** el descriptor, los cortes y la escala común mostraron fallos que las cajas por sí solas no anticiparon.
- **Paso 3:** variaciones del mismo objeto no daban ideas distintas; varias rondas se gastaron en detalles técnicos.
- **Paso 4:** la biblioteca sugirió otra dirección y una ventana reconocible, pero el titular seguía en una tarjeta plana; la revisión externa identificó el fallo de texto–objeto y prioridades.
- **Paso 5:** el riel llegó a cubrir tinta de verdad, pero persistieron dudas de lectura y materialidad.
- **Paso 6:** 5 px (~0,06 de la caja de tinta) cubiertos; los titulares y la ventana se leen a 360 px. Un pliegue diagonal, simple y tenue, da una señal vectorial de tela.
- **Paso 6b:** en un brief ficticio nuevo, la vasija lleva el titular y la cinta frontal cruza una franja baja; dos rondas reparan la legibilidad y el espacio de formas respecto del copy. El feed R2 conserva las frases y no presenta contactos accidentales entre impresión y titular/apoyos.

Son pruebas pequeñas de ejecución en dos briefs; Paso 5 y Paso 6 reutilizan el mismo contenido/dirección y Paso 6b es un solo brief nuevo. El acabado es vectorial y menos táctil que las referencias fotográficas; el comparador solo guía observación. No se midieron preferencias humanas, no se demuestra causalidad/fiabilidad y no hay aprobación. El feedback no se modificó ni recibió respuestas nuevas; se conservan sus campos vacíos y el estado de 0/17 valoraciones al nivel de referencia. SHA-256 de `docs/recalibration-v3-human-feedback.json`: `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38`.

## Comprobaciones técnicas

`qa.py --strict --expected-count 3` y `design_check.py` pasan en Paso 6 R2 y Paso 6b R2. Pasan `evals/test_library_draw.py` (8), `test_design_check.py` (28), `test_validate_skill.py` (7), `test_regressions.py` (25) y `test_blind_gate.py` (7); también `draw.py --check` verifica 21 referencias y 12 direcciones. `evals/validate_skill.py` conserva dos errores preexistentes en briefs fuera de este cambio (`example-noche-lenta.md` y `example-biblioteca-nacional.md`, ambos apuntan a `.cropmark/direction.json` inexistente); el nuevo brief no añade un error. Los tests HTML/contratos de navegador no se ejecutaron porque este entorno no tiene `node_modules` ni navegador Playwright disponibles; no se instaló nada. Ninguna comprobación técnica es evaluación estética ni aprobación de puerta.

## Antes de validar o considerar publicación

La puerta existente queda intacta: seis briefs nuevos, 18 ejecuciones comparables, al menos 5/6 preferencias humanas contra cada condición, al menos 5/6 valoraciones al nivel de referencia, ninguna familia sin un aprobado y entrega editable técnicamente correcta. Faltan el conjunto de corridas, revisión humana, aprobación por familia y la validación técnica de entrega editable; los campos vacíos originales permanecen y no se añadió feedback. John debe revisar este candidato y la evidencia antes de cualquier paso posterior. No se ejecutó el benchmark.
