# Cropmark: relevo, diagnóstico y siguiente paso

Actualizado el 22 de octubre de 2026. Este documento permite continuar el trabajo desde otro agente sin reconstruir el historial del chat.

## Dónde está el proyecto

- Repositorio: [`jdann1el/cropmark`](https://github.com/jdann1el/cropmark).
- Rama de trabajo: `cropmark-art-direction`.
- Pull request: [#2 — Add art direction workflow and measurable visual craft rules](https://github.com/jdann1el/cropmark/pull/2), abierto como borrador y apilado sobre el PR #1, que tampoco está aceptado.
- La candidata actual es desarrollo. No se ha fusionado, publicado ni instalado como versión nueva. La versión publicada/instalada sigue siendo v0.4 en `main`; rc5 está en la base del PR #2 y continúa sin aceptar en el PR #1.
- La producción de recalibración v3 está congelada en `2077f231c765572163a7554a4a0a16f84f1b0533`; la documentación de la respuesta humana se añade en un commit posterior de la misma rama.

Para continuar en otro entorno, abre el PR #2 o cambia a `cropmark-art-direction`. Cada commit nuevo que se suba a esa rama aparecerá en el mismo PR. Un commit es un punto guardado del historial; `push` sube ese punto a GitHub; el PR mantiene el cambio revisable sin publicarlo ni fusionarlo. No hace falta abrir otro issue para guardar este relevo.

## Qué muestra la última valoración humana

La ficha original está en [`recalibration-v3-human-feedback.json`](recalibration-v3-human-feedback.json). Su SHA-256 es `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38`. Es una valoración parcial: cuatro de seis grupos tienen preferencia completa; hay notas en los seis. Se conservan los campos vacíos y no se deducen votos de la prosa.

De las 17 valoraciones de nivel que sí se marcaron, 9 dicen «lejos», 8 «cerca» y 0 «al nivel de referencia». No son 17 pruebas independientes: corresponden a opciones dentro de seis grupos. La candidata no gana ninguno de los cuatro grupos con preferencia completa.

| Caso | Esfuerzo bajo | Esfuerzo alto |
|---|---|---|
| Miniatura D1 | Empate entre sin skill y rc5; candidata lejos. La nota ve mejor la tipografía/flecha, pero critica el encuadre desigual de las furgonetas. | Preferencia por rc5; las tres opciones quedan cerca. La foto sigue sintiéndose mal encuadrada. |
| Carrusel tipográfico D2 | Ninguna preferida; las tres lejos. Se señalan distancias sin función y texto mal colocado en algunos recuadros. | Preferencia por la opción sin skill; sin skill y candidata quedan cerca, rc5 lejos. Siguen preocupando espacio innecesario, centrado óptico, escala y padding. |
| Campaña D3 | Preferencia sin responder. La candidata no tiene nivel marcado; la nota la llama la más limpia/profesional de las tres, pero dice que aún le falta algo. | Preferencia sin responder. Sin skill y rc5 quedan cerca; candidata lejos. La nota favorece cualitativamente A/C, pero ninguna llega al nivel buscado. |

La valoración no acepta la candidata como lista. Tampoco permite afirmar que high cause mejor calidad: varias opciones mejoran en high, incluso sin skill, y la muestra es pequeña. Los resultados detallados y límites de producción están en [`recalibration-v3-results.md`](recalibration-v3-results.md).

## Diagnóstico: ¿bucle o falta un criterio?

Hay riesgo claro de un bucle de ajustes con rendimiento decreciente, aunque los datos no demuestran un bucle histórico ni identifican una única causa. Se han corregido problemas técnicos y algunas piezas se ven más limpias, pero la calibración más reciente no demuestra mejora visual consistente de la candidata.

El criterio que parece faltar en la ejecución no es otra regla aislada: es juzgar y construir las relaciones de la pieza completa. Las comprobaciones de márgenes y cajas miden relaciones declaradas; pueden pasar aunque la idea sea débil o las distancias elegidas no funcionen. También se han tratado cambios de tamaño, fuente, color o recuadro como conceptos distintos cuando a menudo mantienen la misma idea y redistribuyen los mismos bloques.

La auditoría visual independiente coincide en que hay oficio gráfico y momentos aprovechables, pero observa poca diferencia conceptual entre alternativas. El fallo concreto más claro está en el carrusel D2: palabras altas dentro de algunos recuadros y una separación amplia que rompe una misma frase. La miniatura D1 arrastra un encuadre desequilibrado de la foto. En la campaña D3, la única foto limita la variedad; esa restricción no explica los problemas tipográficos del carrusel. En D3-high también existe una diferencia de gusto: la auditoría valoró la exploración asimétrica de la candidata y la persona la marcó lejos. Más novedad no equivale automáticamente a mejor ajuste.

Así que conviene separar cuatro preguntas antes de reescribir la skill: ¿puede el agente reproducir buenas relaciones tipográficas?, ¿puede transferirlas a otro mensaje?, ¿puede inventar una idea visual específica?, ¿elige el cliente esa dirección? Hasta ahora, proceso documentado, QA técnico y justificaciones no han probado esas capacidades de forma suficiente.

## Siguiente paso propuesto: diagnóstico acotado

No repetir ahora el benchmark completo de 18 ejecuciones ni añadir más prohibiciones generales. Empezar por el carrusel tipográfico, que permite estudiar oficio sin confundir el resultado con la selección de fotografía.

1. **Reconstruir una referencia social comparable.** Elegir una pieza aportada por el usuario con densidad y formato cercanos. Como estudio, reconstruir su escala y agrupación de texto, distribución del espacio, posición y tamaño visible del logo, recortes, máscaras y papel de líneas o recursos secundarios. Usar fuentes disponibles o licenciadas y anotar las diferencias. No presentar el ejercicio como trabajo propio publicado. Si no se conservan las relaciones al renderizar, investigar medición, métricas tipográficas, agrupación o motor antes de agregar reglas creativas.
2. **Transferir el sistema a contenido nuevo.** Cambiar mensaje y longitud; conservar solo las relaciones que sigan teniendo sentido. Esto distingue comprensión de composición de copia de coordenadas. Revisar primero la pieza completa y luego sus ajustes ópticos.
3. **Probar una dirección original.** Plantear dos ideas cuya diferencia esté en lo que el texto y la imagen hacen juntos, no solo en fuente, color o tamaño. Comparar atractivo, lectura, tono y coherencia como cliente. Cuando la causa de un problema sea la foto o el objeto, corregir la selección/encuadre si el brief lo permite.

Cada intervención debe registrar una causa, una sola variable principal, el efecto visual que se predice y lo observado al comparar los renders. Si una hipótesis no cambia el defecto, no se repite con otro nombre: se revisa la capa responsable. Se mantiene el máximo de tres rondas de corrección por pieza. Una excepción solo sirve si el resultado visible funciona, no por la explicación escrita.

Después del diagnóstico se decide qué editar: ejecución y agrupación, recursos e imagen, mecanismo de composición, o selección de dirección. Las miniaturas, carruseles y campañas siguen dentro del objetivo final; empezar por tipografía no reduce el alcance.

La puerta de publicación acordada no cambia: seis briefs realmente nuevos y congelados, 18 ejecuciones comparables, al menos 5/6 preferencias humanas frente a cada condición, al menos 5/6 aprobaciones de nivel de referencia y ninguna familia sin un aprobado, además de entrega editable técnicamente correcta. D1–D3 y los históricos ya expuestos cuentan como desarrollo, nunca como held-out nuevo.

## Instrucción breve para la siguiente IA

> Continúa el trabajo en `jdann1el/cropmark`, rama `cropmark-art-direction`, PR #2. Lee primero este relevo, `docs/recalibration-v3-results.md`, `docs/acceptance-ledger.json` y el protocolo v3. La última ficha humana es parcial y tiene 0/17 valoraciones al nivel de referencia; conserva los vacíos y no la describas como aprobación. No fusiones ni publiques la candidata. Analiza las referencias ya aportadas y prepara el diagnóstico acotado de reconstrucción tipográfica, transferencia y dirección original. Antes de cada prueba, fija causa, variable y efecto esperado; no repitas las 18 ejecuciones ni añadas reglas generales hasta que el diagnóstico indique qué capa falla. Mantén el umbral original de publicación.
