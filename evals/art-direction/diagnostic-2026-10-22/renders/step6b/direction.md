# Direction record — Taller Barro

## Antes del primer render

- Brief: marca ficticia de cerámica; carrusel de 3 láminas, 1080×1350, español. Copy literal: «La forma / toma cuerpo.»; «Del giro / nace el borde.»; «Cada huella / deja memoria.». Sin hechos ni activos reales. Formas dibujadas en código; fuentes OFL incluidas en Cropmark.
- Público/respuesta: quien disfruta el proceso material; mirar el gesto, reconocer la arcilla y explorar el taller. No se atribuyen técnica, origen ni resultados a un negocio real.
- Identidad/recursos: «TALLER BARRO» es un nombre de muestra. DM Serif Display y Outfit, ambas fuentes empaquetadas; arcilla clara, fondo verde carbón y acento terracota. Sin píxeles externos.
- Dirección sorteada: `artefact-in-scene`; estilo guardado: `text-in-scene`. Semilla 20261023; opciones asentadas en el brief: `artefact-in-scene`, `duel`, `type-is-the-image`. La cinta de arcilla puede formar un borde que lleve y cruce el titular. Competitor test: el torno, la huella y la pared de arcilla dan al gesto una lectura de taller; se evita dejarlo como una tarjeta genérica.
- Referencias comparables consultadas a tamaño feed: `bh11-estudio-mona/11-02.png`, afiche adherido a un soporte vertical, con capas de papel/pintura que cubren parte de la tipografía; `bh19-kings-cafe/19-06.png`, recibo central con producto y platos que atraviesan sus bordes. Observación: la primera usa una superficie física y una oclusión visible; la segunda da prioridad al recibo plano y a los productos superpuestos. Inferencia, no dato: la superficie/acción material puede hacer que el titular pertenezca a la escena. Diferencia de oficio: ambas son fotografías con textura, perspectiva e iluminación; este estudio usa formas vectoriales dibujadas.
- Inventario: cinta de arcilla; torno; borde de vasija; huella de pulgar; herramienta curva; anillo de pie; rastro de barbotina; línea incisa; virutas; mancha de esmalte.
- Ancla tipográfica común: x=140; dos líneas con misma familia/tamaño/paso y respiración regular; nombre, descriptor, titular, apoyo y CTA comparten eje. CTA con tracking normal.

## Tres conceptos previos

1. La forma se vuelve tangible → letras incisas sobre el vientre de una vasija y el borde de arcilla pasa por delante de la base de la última línea → reconocer titular y objeto como una sola pieza.
2. El giro produce un borde → una cinta de arcilla dibuja una espiral de torno alrededor del titular → seguir el movimiento del material hasta su forma.
3. Una marca guarda un gesto → el pulgar deja una depresión en una losa que lleva las palabras → asociar memoria con una huella hecha a mano.

## Secuencia planificada

| Lámina | Rol | Copy | Dispositivo y composición |
|---|---|---|---|
| 01 | Portada | La forma / toma cuerpo. | Vasija amplia; letras sobre la superficie de arcilla; el borde frontal cruza solo unos píxeles del tramo inferior de «toma cuerpo.». |
| 02 | Proceso | Del giro / nace el borde. | Torno y cinta ascendente; una sección del borde pasa sobre el renglón final sin romper la lectura. |
| 03 | Cierre | Cada huella / deja memoria. | Losa de arcilla y huella visible junto a un titular asentado sobre esa superficie. |

## Bocetos y selección

- Bocetos: `sketch-A.png`, `sketch-B.png`; comparación: `sketches-feed-2up.png` (360×450 por lámina). A se lee primero como titular marcado en el cuerpo de una vasija; B como torno, pero la espiral se mete en «borde.» y divide el titular.
- Elección: A, porque la vasija lleva las palabras y el borde delantero puede cruzar la última línea con una causa material clara. Ajuste previo al desarrollo: ampliar el cuerpo detrás del inicio del titular y alinear los renglones con el eje de marca; la primera silueta hacía tangencia con la «L».
- Descarte: B, por colisión de la espiral con la palabra final en feed. No se resuelve escalando la textura ni añadiendo detalles.

## Pieza representativa y comparador

- Representativos R0: `R0-representative-feed-2up.png`, `slide-cover-R0.png`, `slide-process-R0.png`. En feed se entendían ambas frases; a tamaño completo la cinta horizontal cortaba demasiado la base de «nace el borde.» y los círculos del torno pasaban detrás de varias letras. La relación estaba presente, pero competía con el copy.
- Comparador a 360 px: `/tmp/cropmark-step6b-comparator.png` (solo temporal; las referencias no se incorporan). Diferencias observadas: (1) nuestra vasija es una forma vectorial plana; las dos referencias muestran perspectiva, luz y contacto fotográfico, por lo que tienen más credibilidad material; (2) la referencia de Estudio Mona usa varias capas sobre un afiche y cubre palabras de forma expresiva, mientras nuestro borde cruza solo el extremo inferior de la última línea, con mayor lectura literal y menor complejidad de capas; (3) Kings Café arma un grupo de recibo y productos mucho más denso, mientras nuestra pieza concentra casi todo el peso en una vasija y deja más aire alrededor. El conjunto vectorial no alcanza el acabado fotográfico; la lectura de objeto/titular sí se puede juzgar.
- Ronda 1 — causa: marcas del torno y cinta frontal reducían la lectura de la última frase. Variable principal: posición/cantidad de marca de arcilla frente al bloque tipográfico. Predicción: que solo se tape la franja inferior de 5 px del último renglón y desaparezcan las líneas del torno detrás del texto, conservando el gesto físico. Resultado: a 360 px se leen «La forma / toma cuerpo.» y «Del giro / nace el borde.» completas; la cinta aún se ve por delante. Antes: `R0-representative-feed-2up.png`; después: `R1-representative-feed-2up.png`, `slide-cover-R1.png`, `slide-process-R1.png`.
- Ronda 2 — causa: la boca de la vasija dejaba dos salientes rectangulares, y la extensión mostró que la huella del cierre invadía «memoria.» y el contorno del torno quedaba demasiado cerca del apoyo. Variable principal: espacio/contorno del objeto respecto del bloque de copy. Predicción: conservar la escala y el cruce del titular, cerrar la silueta de la vasija, separar la huella del renglón y abrir el hueco hacia apoyo; así se mantienen la relación física y una lectura limpia en las tres láminas. Resultado: la vasija queda continua; la huella se desplazó a la derecha, la placa del torno y la losa se acortaron y el apoyo bajó 10 px. En el feed final no hay contacto de la huella con «memoria.» ni tangencia entre objetos y apoyo. Antes: `R1-representative-feed-2up.png`, `R2-before-round2-feed-3up.png`, `slide-close-R2-before-round2.png`; después: `R2-representative-feed-2up.png`, `R2-feed-3up.png`, `slide-cover-R2.png`, `slide-process-R2.png`, `slide-close-R2.png`.
- Extensión final tras la revisión representativa. Fuente, escala y eje izquierdo se conservan; cada titular va a 90 px. En las dos primeras láminas, el último renglón queda sobre arcilla y la cinta delantera cubre 5 px de tinta (cerca de 0,06 de su caja de tinta); el copy completo pasa la vista a 360 px sin caption. CTA con tracking 0 y descriptor «CERÁMICA» legibles en el feed. No se concluye que el acabado vectorial iguale las fotos comparadas.

## Revisión del conjunto

Revisión final: `R2-feed-3up.png` y las tres láminas R2 inspeccionadas; el último renglón completo es legible, el borde de arcilla cruza una fracción pequeña de tinta, y huella/torno no tocan copy ni apoyo. No queda el tercio inferior vacío: el apoyo y CTA ocupan su zona. Residuo: la ilustración vectorial tiene menos relieve y luz material que una fotografía; no se añadió textura para disimularlo. Dos rondas sobre el set representativo; el cierre reveló y permitió corregir el contacto accidental dentro de la segunda ronda.
