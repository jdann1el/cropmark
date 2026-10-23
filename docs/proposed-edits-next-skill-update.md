# Propuesta para la próxima actualización de Cropmark

**Estado:** candidato integrado en los módulos de la skill de esta rama; sigue **sin validar hasta que pase la puerta**. No cambia el benchmark ni la puerta de publicación. El feedback humano continúa en 0/17 valoraciones al nivel de referencia, 9 lejos y 8 cerca; no se añadieron respuestas y se conservan los campos que ya estaban vacíos. No equivale a aprobación.

## Capas candidatas: mecanismo de composición, ejecución y selección de rondas

Antes de añadir reglas generales, probar un registro breve por dirección elegida: qué elemento concreto del inventario se usa, qué acción física conecta el objeto con el copy, qué palabras lleva/ocluye y cómo se reconoce esa relación en feed. Añadir al registro qué defecto central se prioriza en cada ronda y por qué, para no gastar iteraciones en acabado secundario mientras falla el mecanismo principal.

- **Paso 1:** las relaciones geométricas de la reconstrucción se aproximaron, pero persistieron diferencias de forma y ocupación de fuente. La medición de cajas no bastó para resolver el carácter tipográfico.
- **Paso 2:** la revisión externa encontró descriptor fuera del eje, palabra de fondo sin sangrado y escala de titular desigual. Son fallos de transferencia y lectura del grupo que las comprobaciones de cajas no anticiparon.
- **Paso 3:** A/B movían la misma libreta/lista; los contactos con puntuación parecían tangencias. Además, varias rondas se gastaron en contraste técnico.
- **Paso 4:** la selección «blind-lowering-over-the-light» produjo una idea distinta del Paso 3 y el sol que se reduce da continuidad; es una señal positiva para la selección de dirección con biblioteca en esta prueba, no evidencia causal general. Sin embargo, el titular sigue impreso en un rectángulo crema plano, sin interacción texto–objeto; el semicírculo no se lee como luz detrás de una ventana sin depender del caption. La portada deja cerca del 60 % del panel vacío y el corte «Baja el / día.» es torpe; el tracking amplio del CTA, el descriptor ilegible en feed y la tangencia del gancho siguen visibles. Las tres rondas fueron a cordón, textura y líneas, no al panel vacío, la lectura del sol ni el vínculo texto–objeto. Esto señala fallos de mecanismo de composición/ejecución y de selección de qué corregir primero.
- **Paso 5:** el riel de la persiana se dibujó por delante y cubrió 12 px de la tinta; el feed confirmó un cruce explícito y legible, aunque la revisión externa aún señaló baja materialidad y dudas sobre la relación. No basta para declarar validado el mecanismo.
- **Paso 6:** la corrección dejó 5 px (~0,06 de la caja de línea) cubiertos; las frases completas y la escena de ventana se leen a 360 px. Un pliegue diagonal simple mejora la señal de tela sin rondas de textura. Es una prueba limitada en la misma dirección, no una medida de fiabilidad.
- **Prueba nueva (Taller Barro):** sin reutilizar briefs de NOCHE LENTA, la vasija lleva el titular y una cinta frontal cruza su borde bajo; las frases se leen en el feed final R2. Dos correcciones se centraron en espacio de capas/objeto: legibilidad del cruce y despeje de contornos. Las fuentes fueron formas dibujadas y fuentes OFL empaquetadas; el resultado es más plano que los comparadores fotográficos. Un brief valida que el texto agregado se puede seguir y probar; no valida su eficacia general.

La revisión externa de Paso 4 corrige el juicio de la primera ejecución: la dirección sí fue distinta, pero entonces el titular seguía dentro de una tarjeta plana. Paso 5/6 y Taller Barro respaldan probar una mecánica de superficie, gesto y capas; ninguna prueba demuestra causalidad, preferencia ni fiabilidad general. La copia candidata se limita a registrar esa relación y a comprobar su lectura.

## Ediciones candidatas en el branch (no validadas)

El módulo de composición ahora propone un campo de **relación titular–objeto** cuando una dirección dependa de ella. El registro indica:

1. La palabra o palabras exactas que el objeto lleva, envuelve u ocluye.
2. La superficie/gesto físico y el orden de capas que hacen visible esa acción (por ejemplo: titular en tela, riel delantero por encima).
3. La franja o parte de tinta que se cubre y el límite de legibilidad acordado a tamaño feed.
4. Una comprobación a 360 px de la frase completa y del objeto sin depender del caption.

La adición a `techniques/carousel-system.md` pide palabras afectadas, superficie/gesto, orden de capas, tinta cubierta y límite de legibilidad a tamaño feed; requiere comprobar objeto y frase completa a 360 px. `qa/checklist.md` registra esos datos; `SKILL.md` enruta el caso a ese mecanismo y a R15. La prioridad candidata es corregir la relación central, escala y posición de capas antes de extender; textura y acabado siguen después de que la relación lea.

También se incorporan cuatro comprobaciones observables del estudio de 21 piezas cuando sean pertinentes: no justificar ni estirar titulares cortos (T-6); usar como punto de partida huecos verticales de 0,3–1 altura de mayúscula dentro del grupo y al menos el doble entre grupos; revisar cortes que terminen en palabras funcionales y rag menor de 0,4; limitar como objetivo a tres tipos decorativos por lámina y comparar retirando uno si hay más. Son señales de diagnóstico, no leyes de gusto ni plantillas. No se copian imágenes, píxeles ni nombres de diseñadores.

## Pruebas pendientes antes de considerar cualquier cambio

1. Probar briefs congelados nuevos con y sin biblioteca, bajo el mismo proceso y revisión ciega, sin reutilizar Pasos 1–4 como held-out.
2. Comprobar si el registro de inventario/acción produce ideas distintas de una variación de colocación y si estas siguen claras en feed, en varios tipos de brief; separar el resultado observado de cualquier atribución causal a la biblioteca.
3. Revisar si el objeto lleva u ocluye palabras de forma legible, si su contexto visual permite reconocerlo sin depender del caption y si el titular usa el espacio del objeto. Registrar defectos observables y rondas por causa, dando prioridad al mecanismo central antes de los acabados secundarios.
4. Cumplir la puerta existente sin alterarla: seis briefs nuevos, 18 ejecuciones comparables, al menos 5/6 preferencias humanas frente a cada condición, al menos 5/6 valoraciones al nivel de referencia, ninguna familia sin un aprobado, y entrega editable técnicamente correcta.

La puerta permanece intacta. No se ejecutó el benchmark de 18 corridas ni se editaron sus archivos. No se añadió feedback nuevo; el resultado sigue en 0/17 al nivel de referencia y se conservan los campos vacíos existentes. Mantener las adiciones como candidato hasta reunir seis briefs nuevos, dieciocho ejecuciones comparables, las preferencias/ratings mínimos, aprobación en cada familia y entrega editable correcta; después hace falta revisión de John. Este candidato no afirma aprobación ni causalidad.
