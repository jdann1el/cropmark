# Paso 8 — contraste de referencias y diagnóstico de B

**B necesita resolver el soporte del texto antes de componer.** En Paso 7, la interacción titular–objeto dio una idea propia, pero el copy secundario quedó pequeño y sobre zonas fotográficas variables. R3 añadió sombras y un contorno de 2 px; el QA estricto siguió fallando contraste secundario. Este documento registra el diagnóstico previo y el resultado B2; el skill sigue sin validar.

Base del estudio: `cropmark-reference-library`, HEAD/origin `4c87db5`. El feedback conserva como referencia el SHA-256 `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38`. Las referencias 05-02, 07-02, 07-03, 08-04, 13-03, 19-03 y 20-03 se consultaron solo para estudio; no son capas, texturas ni assets de entrega.

## Reglas observadas frente a B

“Regla del diseñador” describe una decisión visible en la muestra, no una intención confirmada de su autor. La última columna es una propuesta para probar, aún sin validar.

| regla del diseñador | qué hizo B | fallo | regla para el skill |
|---|---|---|---|
| 07-02 organiza titular y apoyo en bloques reconocibles: titular `(189,448,624,867)`, apoyo `(198,946,548,981)`. | Fijó apoyo en y=987 y CTA en y=1178 sobre fotografías distintas. | Repetir coordenadas no garantiza soporte legible; la textura cambia bajo cada bloque. | Planear zonas para todo el copy en el prompt y aceptar posiciones solo tras medir la base generada. |
| 08-04 alinea etiquetas superiores: caja `(53,56,1026,77)`, márgenes 53/54 px; titular de 150 px de alto frente a etiqueta de 21 px. | Dio prioridad al titular y dejó secundarios pequeños a 360 px. | La idea principal se sostiene, pero marca, descriptor, apoyo y CTA pierden lectura. | Comprobar jerarquía completa en feed; usar alineación y diferencias de escala deliberadas sin copiar esas medidas. |
| 13-03 separa titular de 88 px de alto y especificación de 24 px: razón 3,67. Una muestra oscura vecina da mediana 14,70:1. | Eligió color para superficies fotográficas variables y corrigió con efectos. | Una muestra vecina o el promedio del fondo no representa lo que hay bajo cada letra. | Medir contraste local bajo glifos en cada caja; documentar P05, mediana y proporción insuficiente. |
| 20-03 ofrece un tramo blanco sobre parche negro de 21:1; el titular también sigue sobre fotografía. | Añadió sombras y contorno tras encontrar problemas de contraste. | El recurso correctivo pesa visualmente y no garantiza la frase completa. | Resolver fondo/color/posición antes de añadir efectos; medir todo el copy, no solo el parche favorable. |
| 08-04 permite colisión de collage intencional; eso no autoriza a ocultar información necesaria. | En rondas anteriores, objetos recortaban texto; luego limitó las máscaras. | La interacción exigió rescatar letras para recuperar lectura. | Ningún objeto tapa copy obligatorio en B2; conservar relación con el objeto mediante posición, escala o forma. |
| 19-03 concentra un titular dominante de ocho líneas y un apoyo compacto. | Repartió varios bloques, incluidos apoyo y CTA, en zonas expuestas de la fotografía. | Los bloques dispersos añaden puntos de fallo y compiten con la imagen. | Agrupar secundarios en un campo tranquilo y justificar cada etiqueta/CTA con el brief. |
| 05-02 dispersa palabras sobre fotografía de forma deliberada; 07-03 usa textura, blanco y amarillo. | Buscó un sistema común de titular y secundarios. | Ni justificar/dispersar siempre ni adoptar una paleta de referencia resuelve la lectura. | Elegir organización por el contenido y verificar cada aplicación; no convertir una excepción estilística en receta universal. |

## Evidencia de contraste local de B

Mediciones recibidas del revisor sobre las bases crudas de B ajustadas a 1080 × 1350, sin sombras ni contornos. Se muestreó el fondo bajo el núcleo real de los glifos (umbral alfa/intensidad 250) y se calculó contraste píxel a píxel con luminancia sRGB linealizada. P05 es el percentil 5; los porcentajes corresponden a píxeles del núcleo por debajo de 4,5:1. No equivalen a una medición del acabado con efectos ni reemplazan su inspección visual.

| Lámina / bloque | P05 | Mediana | Píxeles < 4,5:1 |
|---|---:|---:|---:|
| S1 marca | 2,31:1 | 4,00:1 | 64,4 % |
| S1 descriptor | 1,49:1 | 3,56:1 | 73,0 % |
| S1 apoyo | 1,17:1 | 3,09:1 | 76,0 % |
| S2 apoyo | 1,13:1 | 3,42:1 | 76,1 % |
| S3 apoyo | 3,83:1 | 4,99:1 | 20,0 % |
| S1 CTA | 1,14:1 | 6,16:1 | 34,6 % |
| S2 CTA | 2,27:1 | 4,30:1 | 52,7 % |
| S3 CTA | 3,27:1 | 4,70:1 | 37,9 % |

S1 CTA muestra el límite del promedio: incluso una mediana de 6,16:1 convive con 34,6 % de píxeles bajo 4,5:1. Las cifras describen riesgo local del soporte; no permiten afirmar que toda palabra falle por igual. El QA estricto del Paso 7 sigue siendo una evidencia separada de fallo secundario en los finales.

También hay contraejemplos en las referencias: el parche oliva plano superior de 07-02 tiene luminancia 0,4185 y contraste con blanco de **2,24:1**. Su atractivo visual no garantiza contraste técnico. Los 14,70:1 de 13-03 son una muestra vecina, no el fondo exacto bajo las letras; los 21:1 de 20-03 describen el parche negro, no toda la frase sobre fotografía. No se extrapolan esos valores a las piezas completas.

## Objetivo provisional de B2

Mantener el brief, las tres láminas y el copy de A/B; planear antes de generar las zonas para titular, marca/descriptor, apoyo y CTA. Probar pared oscura con titular blanco y un campo inferior claro y despejado con secundarios oscuros, **si la escena realmente generada ofrece esas superficies**. Revisar las bases antes de fijar tinta y posición. No usar sombras ni contornos por defecto, ni oclusión de copy obligatorio.

Objetivos del ensayo: contraste local P05 ≥ 4,5:1 en secundarios y ≥ 3:1 en titular grande; registro de cada caja y de su porcentaje bajo umbral; todas las palabras legibles a 360 px; QA estricto con fallos explícitos; comparación de las nueve láminas A/B/B2. Estos objetivos operativos no alteran la puerta del proyecto ni demuestran calidad de referencia por sí solos. El juicio debe considerar acabado y relación titular–objeto además de lectura.

Se permiten seis llamadas integradas a image_gen en total y tres rondas de corrección; un fallo de herramienta detiene generación sin API/CLI alternativo. El [spec del Paso 8](spec-paso8.md) fija tareas, modelos y archivos autorizados. Al fijar este objetivo aún no se habían ejecutado generación, renders, QA ni cambios al skill; sus resultados se registran abajo. Ni las referencias ni este diagnóstico prueban causalidad. El estado humano 0/17 al nivel de referencia permanece sin cambios.

## Resultado de composición B2 — R0

Se inspeccionaron las tres bases generadas antes de componer: las zonas superiores izquierdas conservan pared oscura y las inferiores izquierdas, mesa clara; los objetos permanecen fuera de las cajas de copy. La composición usa el borde x=112, titular Instrument Serif de 108 px compartido y apoyos en dos líneas con cortes semánticos. Se usó Instrument Sans para marca, descriptor, apoyo y CTA; `jev.compare_options` la colocó primera con confianza baja (0,488), por lo que la elección se confirmó en los renders. No se aplicaron tracking, sombras, contornos ni placas.

R0 produjo tres PNG de 1080 × 1350 y sidecars con cajas y fuentes. La inspección de cada lámina y del feed de 360 × 450 encontró los bloques completos y legibles; no hay objetos sobre copy. La jerarquía empieza con el titular y mantiene una lectura clara de marca, descriptor, apoyo y CTA. En esta muestra, B2 ofrece campos de texto más calmados y lectura secundaria más clara que B; A conserva un acabado fotográfico más compacto con CTA en pastilla. Es un juicio de estas nueve láminas, no una atribución causal ni una preferencia humana. No se hizo ronda correctiva.

Contraste medido sobre los núcleos de glifos de cada caja, respecto a la base ajustada y sin efectos, con sRGB linealizado. P05 / mediana / porcentaje bajo el umbral: marca, P05 5,82–8,45 / mediana 9,07–10,83 / bajo 4,5:1 de 0–0,16 %; descriptor, P05 4,53–8,99 / mediana 7,36–10,00 / bajo 4,5:1 de 0–4,51 %; titular, P05 6,88–11,14 / mediana 9,53–12,52 / bajo 3:1 de 0 %; apoyo, P05 7,34–9,99 / mediana 9,19–10,90 / bajo 4,5:1 de 0 %; CTA, P05 7,82–8,26 / mediana 8,71–9,22 / bajo 4,5:1 de 0 %. Cada caja y el detalle por candidata de tinta están en `evals/art-direction/diagnostic-2026-10-22/renders/step8/rounds/R0/contrast-R0.json`. Marca y descriptor de la primera lámina conservan pequeñas fracciones de núcleo bajo 4,5:1, aunque sus P05 cumplen el objetivo provisional; no se omiten esos píxeles.

QA ejecutado: `python3 skills/cropmark/qa/qa.py carousel --strict --expected-count 3 --out evals/art-direction/diagnostic-2026-10-22/renders/step8/qa/R0 evals/art-direction/diagnostic-2026-10-22/renders/step8/B2/final-1.png evals/art-direction/diagnostic-2026-10-22/renders/step8/B2/final-2.png evals/art-direction/diagnostic-2026-10-22/renders/step8/B2/final-3.png` — código 0, tres de tres. El reporte está en `evals/art-direction/diagnostic-2026-10-22/renders/step8/qa/R0/qa-report.json`; la hoja A/B/B2 en `evals/art-direction/diagnostic-2026-10-22/renders/step8/AB2-feed.png`. La QA informa que su contraste es una estimación de fondo circundante; las métricas locales anteriores son la medición separada bajo los glifos. Resultado técnico PASS, candidato visual de esta revisión, no validación del skill ni de la puerta humana.

## Juicio final de diseño — revisión independiente de la composición

El rol de juicio **gpt-6.1-sol / high**, distinto del ejecutor B2, abrió directamente [el feed A/B/B2](../evals/art-direction/diagnostic-2026-10-22/renders/step8/AB2-feed.png), las tres finales [S1](../evals/art-direction/diagnostic-2026-10-22/renders/step8/B2/final-1.png), [S2](../evals/art-direction/diagnostic-2026-10-22/renders/step8/B2/final-2.png) y [S3](../evals/art-direction/diagnostic-2026-10-22/renders/step8/B2/final-3.png) a 1080 × 1350, y las siete referencias locales identificadas arriba. Este juicio se basa en esos píxeles, no en la nota visual provisional del compositor ni en un pase de QA.

**Prefiero B2 por un margen pequeño frente a A en este carrusel; mejora claramente B, pero aún no alcanza el oficio distintivo de las referencias estudiadas.** En la fila B2 a 360 px se leen completos «toma cuerpo.», «nace el borde.» y «deja memoria.» sobre pared oscura, y los tres apoyos se distinguen sobre mesa clara. En B, el apoyo de S1 cruza el cuerpo de la vasija y el CTA de S2 queda entre las estrías del torno; esa competencia desaparece en B2. También desaparece el borde pesado de marca/descriptor. El margen izquierdo común y los cortes de dos líneas dan una secuencia estable sin sacrificar la fotografía de manos y arcilla.

A mantiene ventajas visibles: su marca tiene más presencia, las pastillas hacen más reconocibles las acciones y la huella de S3 domina más el encuadre. B2 gana en calma, coherencia tipográfica entre láminas y lectura secundaria; su titular más estrecho y ligero deja respirar la escena. La preferencia es de esta revisión de diseño, no feedback humano de la puerta ni una conclusión general sobre los métodos.

Las brechas siguen siendo concretas. Las tres B2 repiten casi el mismo esquema de texto a la izquierda, objeto a la derecha y mesa abajo; la secuencia cambia el motivo pero poco el ritmo. Marca y descriptor se leen, aunque a 360 px forman un lockup pequeño y de carácter genérico; los CTA son líneas funcionales de poco énfasis. En S3, la huella queda como detalle inferior derecho y no organiza el titular. La relación texto–objeto es ahora de vecindad temática; B tenía una interacción física más propia, aunque sus problemas de lectura la debilitaban. Recuperar especificidad no exige volver a tapar letras.

Frente a 07-02, B2 se acerca al control de columna y al espacio para leer. Aún le falta una decisión gráfica tan reconocible como la palabra de fondo y el énfasis en cursiva de esa referencia, la expansión de palabras de 05-02, la composición del titular alrededor del collage de 08-04 o el bloque compacto con filetes de 19-03. El protagonismo del producto en 13-03 y la integración de las formas de marca en 20-03 también son más decididos. 07-03 confirma que una fotografía rica puede convivir con un mensaje central específico, aunque no garantiza contraste en cada tramo. Son diferencias observables de composición, no requisitos para copiar esos recursos ni una puntuación calibrada de equivalencia.

**Resultado acotado:** B2 corrige el problema de lectura y es una entrega más resuelta que B; supera ligeramente A para este juicio de serie. Se acerca a la disciplina de jerarquía de las referencias, pero conserva una dirección fotográfica y de marca demasiado intercambiable para declarar nivel de referencia. Una ejecución por condición, bases distintas y juicio de un modelo no prueban causalidad, aprobación humana ni validación del candidato. La puerta y el estado 0/17 permanecen intactos.

## Verificación independiente T5

El verificador **gpt-6-luna / high**, distinto del ejecutor, informó QA estricto con salida 0 en las tres B2 y un reporte nuevo idéntico byte a byte al de R0. Recalculó las quince ternas de contraste local y coincidieron con el registro; verificó que las nueve celdas del feed miden 360 × 450 y sus píxeles coinciden con los finales redimensionados, y que las bases coinciden byte a byte con los originales generados. El registro de generación declara tres llamadas exitosas de seis permitidas, sin fallos; R0 no necesitó rondas correctivas.

T5 confirmó ausencia de assets de referencia, URLs CDN o rutas de importación de referencias en la entrega, SHA-256 del feedback sin cambios y correspondencia de rama/HEAD/origin con la base del spec antes de integrar. En ese punto no había nada stageado ni `__pycache__`; los entregables nuevos de Paso 8 seguían sin seguimiento y el QA ajeno de Step3 seguía excluido. Esta verificación acredita artefactos y límites de ejecución; no convierte la preferencia de diseño en aprobación humana ni modifica el 0/17 al nivel de referencia.
