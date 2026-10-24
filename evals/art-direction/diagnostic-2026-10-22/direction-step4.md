# Paso 4 — dirección y bocetos

Antes de renderizar: el encargo es una cuenta ficticia de descanso, con el copy y el inventario del brief [NOCHE LENTA](../../../skills/cropmark/briefs/example-noche-lenta.md). No hay activos fotográficos. La dirección repartida fue `artefact-in-scene`; la razón nombra la franja de luz atrapada por la persiana (inventario 3). El draw la relaciona con señales, recibos y tarjetas, pero el brief decide el objeto: una persiana dibujada en código que pertenece al tema, no una tarjeta que se haga pasar por objeto.

## Tres conceptos iniciales

1. **La persiana tipográfica.** El tejido de una persiana enrollable lleva el titular; el riel baja sobre la última franja de luz durante portada, paso y cierre.
2. **El interruptor de la palabra.** La palabra «DÍA» queda unida a un interruptor dibujado; al apagarlo, el titular cambia de estado.
3. **La nota que se enrolla.** Una nota única para mañana se enrolla en el tambor de la persiana y desaparece al cerrarse.

Los tres usan objetos del inventario. El primero da una acción de secuencia y lleva el texto en una superficie textil; el segundo no aprovecha la instrucción de dejar una cosa lista; el tercero se acerca demasiado al recurso de libreta/lista del Paso 3.

## Bocetos visuales previos al render desarrollado

- **A — tejido impreso:** el marco, tambor, cordón, lamas y riel hacen reconocible la persiana. El titular va directamente sobre el tejido con padding constante; la luz visible bajo el riel disminuye entre slides.
- **B — texto tras el riel:** el titular queda en la pared detrás de la persiana y el riel oculta parte de las palabras; una máscara mantiene la frase legible. La sombra sobre la tinta debe hacer explícita la oclusión.

**Revisión de los bocetos antes del R0.** En la hoja feed, A mantiene «Baja el día» legible en la tela y deja luz bajo el riel; a tamaño completo se reconocen tambor, guías y cordón, aunque la superficie todavía puede parecer una tarjeta plana. B corta «Baja el día» por el centro con el riel, pero no consigue que la oclusión parezca una acción física controlada; además oculta copy obligatorio. Elijo A y desarrollo la tela como persiana de ventana con textura/material y riel móvil. El riesgo de que parezca una tarjeta se juzgará otra vez en R0/feed.

## Plan de secuencia

| Slide | Papel | Copy | Acción de la persiana |
|---|---|---|---|
| 01 | Portada | «Baja el día.» + apoyo + CTA | Primera bajada; queda visible la última franja de luz. |
| 02 | Interior | Rutina sencilla + apoyo + CTA | El tejido lleva cuatro líneas del titular y la luz se reduce. |
| 03 | Cierre | «Suelta por hoy.» + apoyo + CTA | El riel cierra la luz; el cordón descansa junto a la tela. |

La familia de fuente, escala de titular, paleta y eje de texto son constantes. No se usa una palabra fantasma de fondo. Se juzga primero la hoja feed; después cada lámina a tamaño completo. Las correcciones se registran por una variable principal, con máximo tres rondas por slide.

## Idea y competidor

“En esta pieza, **la última franja de luz retenida por la persiana** se convierte en **la tela que lleva «Baja el día» y las frases de la secuencia mientras el riel desciende**; frente a la alternativa más cercana del Paso 3 —libreta/lista que solo completa o queda bajo el titular—, ¿seguiría funcionando?” No: la libreta/lista no retiene esa franja de luz ni se convierte en el soporte textil que baja sobre ella. La mecánica todavía podría servir a otra cuenta de descanso; el brief no aporta identidad de marca propia, así que no se afirmará exclusividad de marca.

El contenido sigue siendo creativo y no clínico. La revisión de referencias es de fichas de texto y URLs de páginas de proyecto; no se usan píxeles de referencia.
