# Cropmark — estado de la implementación

Candidata `art-direction-preview.2`, pendiente de aceptación visual. Fecha: 19 de octubre de 2026. Se conserva rc5 como base técnica; PR #1 no queda aceptada por este trabajo.

## Implementado

- Router breve; módulos por encargo; tres conceptos, dos bocetos visuales y pieza representativa para originales. Ruta corta para copia fiel y ajustes concretos. Tres rondas máximas para todo el conjunto.
- Catorce reglas con diagnóstico, corrección, comprobación y excepciones. Manual ilustrado con ejemplos didácticos identificados; no son resultados de mejora medidos.
- Atlas de los 21 proyectos aportados, con mecanismos separados de tratamientos. La cobertura es una muestra visual representativa por proyecto, no auditoría completa.
- Catálogo de doce casos: seis resultados internos históricos con hashes/trazas, tres proyectos que declaran uso de IA y tres referencias de calidad. Las marcas señalan relaciones analizadas, incluidos contraejemplos válidos; no atribuyen automáticamente defectos ni autoría por apariencia.
- Tres estudios propios antes/después, conservando recursos y contenido. Son revisiones del coordinador y propuestas pendientes de preferencia humana; no ejecuciones autónomas ni victorias de la candidata.
- Diagrama editable Mermaid, SVG, HTML y PNG; documentación local. No se ha instalado la candidata sobre tu skill existente.
- Comprobador opcional de relaciones declaradas: márgenes, ejes, separaciones, padding, fuentes disponibles y tokens compartidos. No detecta intención, originalidad ni alineación óptica. Motores, fuentes y QA raster estricta conservados de rc5.

## Verificación realizada

- 61 pruebas heredadas: 24 contratos, 25 regresiones, 12 integración HTML.
- 23 pruebas nuevas: 19 geometría y entradas CLI, 4 validación de recursos portables. Se comprobó en copia de prueba que invertir el comparador de separación produce cinco fallos.
- Validador de skill, recursos, JSON, 21 referencias y comparación de hashes de motores/fuentes: pasan. Diagrama: self-check offline aprobado; SVG/PNG inspeccionados.
- Calibración: 3 briefs × 3 condiciones × 2 esfuerzos = 18 ejecuciones independientes; 48 PNG finales. Los registros de cada agente documentan render, revisión, paquete copiado reproducido byte a byte y cambio local de texto. Los hashes del inventario corresponden a los originales, sin repeticiones para buscar mejores resultados.
- Modelo solicitado en las 18 llamadas: GPT-6.1 Sol; esfuerzos bajo y alto. No hay introspección independiente de modelo servido, semillas, tokens o coste completo: se registran como no disponibles, no como cero.

## Límites que afectan a la interpretación

Las imágenes se generaron una vez y se suministraron por igual a todas las condiciones. No se ha probado todavía la búsqueda/generación autónoma de recursos. Dentro de la calibración no hubo red: los agentes pudieron leer el atlas, pero no inspeccionar en vivo las referencias externas. La cafetería y la furgoneta son escenas conceptuales ficticias, no pruebas de identidad de producto. Solo se ha comprobado portabilidad en el runtime local usado; otros motores/versiones de rasterizado pueden variar.

D2 y D3 de la candidata con esfuerzo bajo registran ejecución por lotes de las piezas representativas/conjunto: la secuencia por etapas no se cumplió plenamente. Se conservan estas desviaciones. La prueba de geometría no demuestra que esas composiciones sean buenas. Ninguna autoevaluación sustituye tu criterio.

La calibración usó la instantánea congelada `art-direction-rc1`. El paquete entregado añade dos reparaciones posteriores: rechazo de contratos geométricos mal formados y eliminación de una referencia fuera de la skill. El resto de instrucciones es idéntico. Manifiestos y diferencias están en evidence/. No se trasladan automáticamente conclusiones a otra revisión futura.

## Puerta pendiente del plan aprobado

1. Valorar la galería a ciegas: preferencia A/B/C, empate o ninguna; qué opciones alcanzan el nivel de referencia; defectos concretos. La ficha local exporta JSON y no envía datos.
2. Con esa calibración, ajustar si procede y congelar/hashar la candidata final.
3. Crear después seis briefs nuevos, dos por familia, y ejecutar una vez las tres condiciones: 18 ejecuciones de validación. Aún no se han creado ni consumido esos briefs.
4. Publicar solo con entregas editables técnicamente correctas, preferencia humana ciega ≥5/6 frente a cada comparador, calidad absoluta aprobada ≥5/6 y al menos un aprobado por familia. Empates y pérdidas se conservan; no se convierten en victorias.

No se ha publicado una versión, fusionado PR ni declarado un resultado de portfolio aprobado.
