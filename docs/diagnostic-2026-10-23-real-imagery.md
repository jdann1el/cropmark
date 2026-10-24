# Paso 7 — primera prueba real con imagen generada

**Estado:** exploración de un solo brief; no valida el skill ni cambia la puerta. La evaluación visual es juicio de diseño de la sesión principal, en modo de autorevisión; no hubo crítica visual independiente. No se pidió aprobación externa.

## Pregunta y método

¿Cropmark mejora una pieza con imagen generada, comparado con una petición directa sencilla a image_gen? Se usó únicamente `skills/cropmark/briefs/example-taller-barro.md`: carrusel ficticio 4:5 de tres láminas, mismo tema y copy. B reutiliza el brief y la dirección ya seleccionada en Paso 6b; es una prueba media de imagen generada, no un nuevo ensayo de selección de conceptos.

- **A — sin skill:** image_gen generó cada lámina completa con tipografía incluida a partir de un prompt breve. No se aplicó Cropmark ni se corrigió la composición después.
- **B — con skill:** image_gen generó una base fotográfica sin texto ni marcas para cada lámina. Cropmark compuso encima el copy exacto con Pillow, DM Serif Display y Outfit del bundle OFL. La boca de la vasija y el gesto de arcilla/mano pasan sobre una fracción baja de tinta del titular en cover e interior; el cierre deja la huella junto al titular.
- Los seis prompts exactos se guardan en `evals/art-direction/diagnostic-2026-10-22/renders/step7/A/prompts.txt` y `.../B/prompts.txt`. Los originales de imagen y los resultados finales también están en `.../step7/A/` y `.../step7/B/`.
- Se consumieron **6 llamadas integradas a image_gen**: 3 para A y 3 para B; todas tuvieron éxito, sin reintentos. No se usó API key ni CLI alternativo.

## Resultado y revisión visual

La hoja final `evals/art-direction/diagnostic-2026-10-22/renders/step7/AB-feed.png` muestra A arriba y B abajo, tres láminas por fila; cada baldosa es 360 × 450 px. A/final-1..3 y B/slide-1..3 son 1080 × 1350 px. Se revisó la hoja primero y después cada lámina final a tamaño completo.

**Veredicto de John (provisional): A queda ligeramente mejor como pieza completa en esta muestra.** El generador directo resolvió el copy con una exactitud poco habitual, contraste y CTA mayores, y una progresión fotográfica cálida coherente. A no muestra texto deformado ni gradientes genéricos. Sí recurre a una plantilla reconocible: composición centrada repetida, filetes decorativos y CTA en pastilla. Como carrusel de feed puede pasar por una pieza competente de diseñador, aunque no tiene una idea visual distintiva ni relación física entre el titular y la cerámica.

B es más específico y **gana claramente en la relación titular–objeto**: el borde de la vasija atraviesa la base de «toma cuerpo.» y el gesto de arcilla/mano cruza una parte pequeña de «nace el borde.». Tras los ajustes, las frases principales se leen a 360 px. Las máscaras reutilizan píxeles de las fotos generadas, con tinta cubierta registrada de 3,84 % en portada, 3,63 % en interior y 0 % en cierre. El titular de escala compartida y el borde izquierdo común forman un sistema menos genérico que A.

B aún **no supera a A en el conjunto ni pasa como entrega final de diseñador**: descriptor, apoyo y CTA se perciben pequeños en el feed y varios no alcanzan el contraste de la comprobación estricta. La superposición ya es legible, aunque exige atención para distinguir la interacción en la hoja reducida. No hay errores obvios de texto o gradientes, pero la mejora del mecanismo central no compensó por completo la jerarquía secundaria. En R3, la tinta oscura ayudó sobre la arcilla clara; el contorno de 2 px en marca/descriptor se ve pesado, como una pegatina, a tamaño completo y baja el acabado. A fue más limpio y cómodo de leer; B tuvo la idea más propia.

## Rondas de corrección de B

Se hicieron tres rondas de composición, sin más generaciones de imagen. Los feeds transitorios R0–R2 se sobrescribieron al renderizar; solo se conserva `AB-feed.png` final. No se atribuyen a esos estados rutas que ya no existen.

| Ronda | Causa observada | Variable principal | Efecto previsto | Efecto observado y evidencia conservada |
|---|---|---|---|---|
| R0 | El borde ocultaba demasiada tinta en cover; la mano ocultaba el final de «borde.» en interior. Apoyo y descriptor quedaban pequeños. | Render inicial de la relación y escala secundaria. | Hacer visible la interacción sin perder la frase. | El titular de cover y el final del interior quedaban comprometidos a 360 px. R0 no se conservó como archivo independiente. |
| R1 | El titular dominante y la jerarquía secundaria estaban desbalanceados. | Escala común del titular y posición vertical por lámina; tamaño de etiquetas, apoyo y CTA. | Conservar escala de titular compartida y margen común, dando más aire al último renglón. | Titular a 92 px; y=210/390/350; etiqueta/apoyo/CTA a 30/35/30 px. Cover se recuperó; la «e» final de «borde.» seguía poco clara. Estado intermedio sobrescrito. |
| R2 | La máscara de la mano seguía invadiendo el final de la palabra. | Solo la máscara del interior, ahora x=0,50–0,60 e y=0,418–0,445 normalizados. | Mantener un cruce físico pequeño sobre un carácter anterior y dejar «de.» libre. | «Nace el borde.» se lee completo en el feed y el registro marca 3,63 % de tinta cubierta. Ver `B/occlusion_masks.json`, `B/occlusion-log.json` y el feed final. El estado previo fue sobrescrito. |
| R3 | El QA estricto detectó bajo contraste en varias líneas secundarias. | Solo color de apoyo/CTA y contorno de etiquetas. | Aumentar contraste sobre arcilla clara sin cambiar posiciones ni relación. | Apoyo/CTA oscuros ayudaron sobre los materiales claros; el contorno de 2 px elevó contraste técnico, pero se ve pesado y reduce el acabado. QA sigue fallando en algunos campos. Ver láminas finales y resultados QA abajo. |

## QA y límites

Se ejecutó `python3 skills/cropmark/qa/qa.py carousel --strict --expected-count 3 --boxes evals/art-direction/diagnostic-2026-10-22/renders/step7/B/boxes --out /tmp/cropmark-step7-qa-final evals/art-direction/diagnostic-2026-10-22/renders/step7/B/slide-1.png evals/art-direction/diagnostic-2026-10-22/renders/step7/B/slide-2.png evals/art-direction/diagnostic-2026-10-22/renders/step7/B/slide-3.png`. **Salida 1:** las tres dimensiones pasan (1080 × 1350) y el contraste de los titulares pasa; quedan fallos de contraste estimado para marca 4,5:1, descriptor 4,1:1 y apoyo 2,6:1 en S1; apoyo 3,0:1 y CTA 4,5:1 en S2; CTA 4,1:1 en S3. El resultado es evidencia técnica, no sustituto de la revisión a tamaño real. Se alcanzaron las tres rondas; no se oculta el residuo.

La conclusión se limita a **un brief ficticio y una ejecución por condición**. No prueba causalidad, no demuestra que el skill mejore siempre imágenes generadas y no cuenta para la puerta. No afirma aprobación. La evaluación humana sigue en 0/17 al nivel de referencia; la puerta permanece sin cambios. `docs/recalibration-v3-human-feedback.json` conserva su hash y las respuestas vacías.

## Propuesta futura, no aplicada

Como B no fue mejor en conjunto, no se edita el skill a partir de esta prueba. La próxima propuesta podría pedir una comprobación explícita a 360 px de descriptor, apoyo y CTA —incluido contraste— además del titular, y comparar la jerarquía completa contra una generación directa sencilla. El contorno no se prescribe como solución universal. La propuesta debe seguir marcada como candidata sin validar hasta que la puerta existente se cumpla. Esta observación no altera reglas ni benchmark.
