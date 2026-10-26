# Estudio acotado de comparabilidad tipográfica — 20 de octubre de 2026

## Resultado

**Se verificó una serie comparable, con dos láminas útiles del mismo diseñador; no dos comparadores independientes.** La búsqueda acotada no permite presentar un conjunto de dos o tres autores como si estuviera resuelto. Las otras cuatro candidatas dependen demasiado de imágenes, maquetas o contenido adicional. Se documenta lo observado y se cierra la investigación en este punto.

Se hizo una sola consulta: `site.behance.net/gallery "carousel" "design tips" typography`. Se abrieron cinco candidatos de sus resultados y se inspeccionaron las imágenes reales. El caso más útil resultó ser una publicación de autor en Contra, también devuelta por esa consulta. Las capturas se hicieron con CUA nativo; no se descargaron medios remotos. No se leyeron diseños locales ni fichas humanas, ni se generaron piezas o modificaron skills/Git.

## Caso verificado: Raihan Chowdhory

Fuente primaria: [Strategic 6-Slide Carousel Design for Designer Education, publicación del autor](https://contra.com/community/nA1Rwrfh-strategic-6-slide-carousel-design-for-designer). [Perfil identificado de Raihan Chowdhory](https://contra.com/raihan_chowdhory_zw1olzuy). La procedencia y descripción están recogidas en captura de contexto (captura en el estudio privado).

**Por qué se aproxima:** la portada tiene una afirmación de seis palabras; la segunda lámina desarrolla un contraste en tres tiempos y termina en pregunta con apoyo breve. La expresión procede del cambio de peso, de las pausas y del desplazamiento del énfasis verbal. La segunda lámina permite estudiar ese mecanismo sin fotos, interfaz, ilustraciones ni etiquetas añadidas. La portada incluye una ilustración inferior: es una limitación real para comparar el conjunto, aunque el bloque de frase se puede analizar por separado.

**Lo que dice el autor frente a lo que se verificó:** describe una serie de seis láminas, identifica Poppins y declara formato 4:5. En la página se pudieron abrir cuatro adjuntos, marcados del 1/6 al 4/6. No se verificaron las láminas 5 y 6. La imagen de portada expone en su elemento `img` dimensiones naturales **2400 × 3200: proporción 3:4**, no 4:5. No se infiere la familia tipográfica desde sus píxeles: Poppins es una declaración del autor, no una comprobación del archivo fuente. Tampoco se verifican resultados de engagement o captación.

### Medidas y unidades

Los porcentajes se refieren al rectángulo de la lámina, no al visor ni a la página. W = anchura; H = altura. C = altura visible de una mayúscula, no cuerpo tipográfico ni `font-size`. «Paso/C» es la distancia vertical entre líneas dividida por C; no equivale al `line-height` del archivo editable.

Solo las dimensiones naturales de la portada son **exactas, leídas del DOM**. Los siguientes límites y relaciones son **estimaciones visuales** sobre capturas: incertidumbre aproximada de ±3 puntos porcentuales en masas/márgenes y ±0,1–0,15 en paso/C. Las cajas miden extensión, no superficie de tinta. No son parámetros recomendados.

| Lámina inspeccionada | Masas y bloque de frase, estimados | Espaciado, margen y firma, estimados |
|---|---|---|
| [**1/6, portada**](https://contra.com/community/nA1Rwrfh-strategic-6-slide-carousel-design-for-designer?mediaId=WyJDb250cmFJbWFnZSIsMjQ0Njg3MjMyXQ%3D%3D), afirmación breve. Captura completa (captura en el estudio privado) | Bloque verbal de cuatro líneas: ~56% W × 34% H, empieza a ~11% W y ~11% H. Dos líneas rojas y pesadas seguidas de dos negras más ligeras. Ilustración independiente inferior: ~62% W × 37% H. | Paso/C del bloque principal ~1,25–1,35. Entre última línea y cabeza ilustrada queda ~8% H: la pausa separa funciones. Margen izquierdo del texto ~11% W. No se observa firma nominal dentro de la lámina; número de página y flecha viven en el borde inferior, con altura de carácter ~2% H. |
| [**2/6, interior retórico**](https://contra.com/community/nA1Rwrfh-strategic-6-slide-carousel-design-for-designer?mediaId=WyJDb250cmFJbWFnZSIsMjQ0Njg3MjM1XQ%3D%3D), contraste + pregunta + apoyo. Captura completa (captura en el estudio privado) | Zona verbal total ~69% W × 61% H; arranca a ~10% W y ~19% H. Dos grupos repiten la misma estructura: encabezado pesado y conclusión ligera. El tercer grupo agranda la pregunta y cambia a rojo su palabra final. | Las pausas entre los primeros grupos son ~1,4 C de sus encabezados; se reconocen como tres unidades. Pregunta final: paso/C ~1,4–1,5. Apoyo inferior: ~1,3–1,4. La altura visible del apoyo es aproximadamente 0,6–0,7 de la del texto pesado. Mantiene margen izquierdo y pie de la portada; tampoco hay firma nominal. |
| [**4/6, pregunta y desarrollo**](https://contra.com/community/nA1Rwrfh-strategic-6-slide-carousel-design-for-designer?mediaId=WyJDb250cmFJbWFnZSIsMjQ0Njg3MjMzXQ%3D%3D), control secundario. Captura completa (captura en el estudio privado) | Pregunta a la izquierda: ~40% W × 41% H. Desarrollo a la derecha: ~34% W × 48% H. Un separador vertical y una conclusión inferior relacionan ambas zonas. | Márgenes laterales ~6–8% W. Paso/C de la pregunta ~1,25–1,35. El desarrollo enumera cuatro preguntas y usa casillas: requiere más contenido y más inventario gráfico que el encargo buscado. No se cuenta como segundo comparador independiente. |

### Relación entre portada e interior

**Observación:** conservan fondo crema, negro/rojo, peso alto para la proposición y peso menor para el desarrollo; el pie se mantiene apartado. La portada concentra una sola afirmación, mientras el interior usa tres pausas amplias. La continuidad no depende de colocar el mismo gran titular a la misma altura en todas las páginas.

**Interpretación:** la segunda lámina organiza la lectura como argumento. Primero establece dos unidades repetidas; después rompe la repetición con una pregunta más pesada y una palabra final marcada. Su expresividad es retórica y espacial, no una exhibición de efectos tipográficos. Esto sirve como referencia de jerarquía narrativa; es más limitado como benchmark de tipografía experimental o de deformación expresiva.

**Mecanismo transferible sin añadir contenido:** hacer que los cortes de línea y el cambio de peso coincidan con el giro ya presente en la frase; reservar una pausa mayor entre pregunta y apoyo que entre líneas de la misma pregunta. El bloque de explicación puede compartir el eje izquierdo sin competir por la misma escala. Ese mecanismo trabaja sobre las palabras existentes: no requiere importar la ilustración, las tres afirmaciones del ejemplo, su checklist, numeración, flechas, recuadros o nuevos microtextos.

**Límites:** la portada puede parecer más completa gracias a su ilustración y a la mayor altura 3:4. No constituye prueba de que su composición tipográfica aislada venza a otra solución. La lámina 4 tiene demasiado inventario para usarla como plantilla de una sola pregunta con explicación. Los errores gramaticales visibles en la copia publicada no se interpretan como decisiones de diseño. No se propone universalizar rojo, Poppins, tres grupos, alineación izquierda ni esos porcentajes.

## Candidatos inspeccionados que no se cuentan

| Autor y fuente primaria | Qué se observó y por qué no es un comparador justo |
|---|---|
| [Razaul Karim — 7 Carousel Design Tips](https://www.behance.net/gallery/220152785/Carousel-Series7-Carousel-Design-Tips-%28Free-Resources%29) | Presentación con personaje ilustrado, vegetación, hongos y animales; esos elementos construyen gran parte de las masas. Las palabras no sostienen por sí solas la composición expresiva. No se descarta por su posible técnica de generación, sino por dependencia de contenido visual adicional. |
| [Shamil Salimov — Design tips](https://www.behance.net/gallery/244688649/nstagram-Carousel-design) | Portada con abeja/fotografía e interiores con colibrí, jirafa y números enormes. Es una serie educativa real, pero su impacto no es comparable al de una frase breve con apoyo tipográfico. |
| [Gopi Krishna.G — 5 Rules for Composition](https://www.behance.net/gallery/238159913/Visual-Design-Tips-5-Rules-for-Composition) | Se inspeccionaron presentación y módulos [2](https://www.behance.net/gallery/238159913/Visual-Design-Tips-5-Rules-for-Composition/modules/1370356777) y [3](https://www.behance.net/gallery/238159913/Visual-Design-Tips-5-Rules-for-Composition/modules/1370356773): maquetas de Instagram/móvil, manos recortadas, títulos y varias líneas de consejos. No ofrece un par tipográfico expresivo breve/pregunta equivalente. Captura de comprobación (captura en el estudio privado). |
| [Mahian OLi — Designer’s 5 Golden Rules](https://www.behance.net/gallery/232466085/Designers-5-Golden-Rules-Carousel-Post-Design) | Serie con objetos 3D verde neón, cabeza/visor, esqueleto con auriculares, reloj de arena, contornos y asteriscos. Aunque el copy es corto en varias zonas, no se puede transferir su riqueza compositiva sin añadir objetos o decoración. |

## Alcance de la conclusión

La comparación más defendible aquí es **portada 1/6 + interior 2/6 de una sola serie**. Hay tres láminas inspeccionadas de ese autor y una captura de exclusión; no tres referentes independientes. Se entregan cinco capturas locales incluyendo la procedencia del proyecto. No se publicaron.

Una llamada JEV comparó únicamente resúmenes públicos de los cinco candidatos. Prefirió Raihan para este alcance (88,7/100; confianza 0,668); no verifica calidad ni reemplaza la inspección. Uso TypeSafe comunicado por la herramienta: 2.589 tokens de entrada / 304 de salida, separado del uso de Codex. La selección continúa limitada a **un** comparador útil, y la investigación se detuvo sin abrir nuevas rondas de búsqueda ni rebajar el criterio para completar dos.
