# Spec — Paso 8: contraste de referencias y prueba B2

Corregir la jerarquía y la lectura secundaria de B mediante zonas de texto previstas antes de generar la fotografía. La propuesta se contrasta con referencias de diseño y se prueba con el mismo brief de Taller Barro. B2 es una candidata sin validar; este ensayo no modifica la puerta de aceptación.

## Alcance

- Diagnosticar B del Paso 7 y estudiar las referencias 05-02, 07-02, 07-03, 08-04, 13-03, 19-03 y 20-03, sin reutilizar sus píxeles.
- Documentar reglas candidatas y ajustar únicamente instrucciones de Cropmark relacionadas con fondo, jerarquía, contraste local y lectura en feed.
- Generar hasta tres bases B2 sin texto/logos y componer tres láminas de 1080 × 1350 con el copy exacto del mismo brief y fuentes OFL locales.
- Comparar A y B existentes con B2 a 360 × 450 por lámina; revisar también cada B2 a resolución completa y ejecutar QA estricto.
- Verificar de forma independiente, integrar solo archivos permitidos y hacer el push autorizado a `cropmark-reference-library`.

## Fuera de alcance y límites duros

No hay nuevo brief, regeneración de A/B, benchmark de 18 corridas, cambio de gate/ledger, aprobación humana inferida, instalación, merge ni publicación. No se modifica `docs/recalibration-v3-human-feedback.json`: SHA-256 esperado `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38`. No se incorporan referencias, rutas a sus assets ni URLs CDN; solo identificadores de estudio y observaciones. Quedan excluidos Step3 QA y `__pycache__`.

**Máximo seis llamadas integradas a image_gen en total, incluidos reintentos. Ante cualquier fallo de la herramienta, detener la generación y registrar el bloqueo; ningún generador, API key o CLI alternativo.** Máximo tres rondas de corrección tras el primer render; cada ronda registra causa, variable principal, predicción y resultado. No ocultar fallos ni seguir corrigiendo al agotar el límite.

## Criterios medibles

1. El diagnóstico contiene la tabla de cuatro columnas pedida, siete referencias identificadas, medidas y límites de interpretación; separa observación de regla candidata.
2. Cada prompt B2 registra zonas para **todos** los bloques de copy; las tres bases carecen de texto y logos. Las zonas se validan sobre la imagen obtenida antes de componer. No basta lo solicitado en el prompt.
3. Tres finales B2 miden 1080 × 1350, mantienen las cadenas del brief y tienen cajas de texto registradas. Ningún objeto tapa copy obligatorio. Sombras y contornos están desactivados por defecto; cualquier excepción requiere justificación visual y medida, sin sustituir la corrección del fondo.
4. Para cada caja se registra contraste local sobre la base sin efectos, bajo el núcleo de los glifos: luminancia sRGB linealizada, P05, mediana y porcentaje bajo umbral. Objetivo provisional: P05 ≥ 4,5:1 para marca, descriptor, apoyo y CTA; ≥ 3:1 para titular grande. No se usa el promedio de una región como garantía. Toda palabra obligatoria debe leerse completa a 360 px aunque la estadística pase.
5. Se exporta un feed A/B/B2 con nueve láminas de 360 × 450 y se registra juicio de lectura, jerarquía, acabado y relación objeto–titular. La comparación no atribuye causalidad ni presupone que B2 gane.
6. QA estricto se ejecuta en las tres B2; se conservan comandos, códigos de salida y fallos residuales en el diagnóstico. Los objetivos locales anteriores complementan el QA existente y no cambian sus umbrales.
7. Un verificador distinto del ejecutor coteja artefactos y criterios. El informe distingue PASS, FAIL y pendiente; una entrega puede documentar un experimento fallido sin afirmar aceptación visual.
8. Antes de integrar se verifica el hash del feedback, el diff y la exclusión de assets de referencia. Solo archivos autorizados entran al commit y al push. Base de partida: rama `cropmark-reference-library`, HEAD/origin `4c87db5`.

## Tareas por dependencia y permisos

`S8` significa `evals/art-direction/diagnostic-2026-10-22/renders/step8/`. Todos los roles conservan los modelos y esfuerzos indicados; no se sustituyen de forma silenciosa.

| ID / depende de | Entrega | Archivos permitidos | Rol exacto / cierre |
|---|---|---|---|
| T0 / — | Spec y juicio de diseño con evidencia verificada | `docs/spec-paso8.md`, `docs/diagnostic-2026-10-24-behance-contrast.md` | **gpt-6.1-sol / high**, spec-plan y juicio. Alcance y diagnóstico escritos antes de aplicar reglas. La comparación JEV ya se realizó una vez; no repetirla. |
| T1 / T0 | Reglas candidatas y estado sin validar | `docs/candidate-update-2026-10-23.md`; `skills/cropmark/SKILL.md`, `techniques/imagery.md`, `techniques/typography.md`, `techniques/carousel-system.md`, `references/visual-rules.md`, `qa/checklist.md` | **gpt-6-luna / high**, ejecutor. Solo cambios derivados del diagnóstico; no tocar gate ni umbrales de QA. |
| T2 / T1 | Prompts exactos, registro de llamadas y bases B2 | `S8/B2/`, `S8/imagegen-log.json` | **gpt-6-luna / high**, ejecutor de prompts/generación. Zonas completas verificadas; respetar seis llamadas y parada por fallo. |
| T2b / T2 | Copiar sin alterar las tres bases desde las rutas locales del generador | `S8/B2/base-{1,2,3}.png` | **gpt-6-luna / low**, mecánico. Comprobar dimensiones y byte-match; no borrar originales ni tocar otros assets. |
| T3 / T2b | Compositor, cajas, tres finales y feed A/B/B2 | `S8/`, diagnóstico del T0 | **gpt-6-luna / high**, ejecutor de composición/renders/docs. Reutiliza A/B sin alterarlos; documenta hasta tres correcciones. |
| T4 / T3 | Juicio visual y resultados de contraste/QA | Diagnóstico del T0; informes y vistas en `/tmp` | Juicio: **gpt-6.1-sol / high**. Ejecución y registro de QA: **gpt-6-luna / high**. Evaluación a 360 px y tamaño completo con fallos visibles. |
| T5 / T4 | Verificación independiente contra repo | Solo lectura; informes en `/tmp` | **gpt-6-luna / high**, verificador distinto del ejecutor. Adjunta evidencia propia de criterios, hash y exclusiones. |
| T6 / T5 | Archivos integrados, commits y push autorizado | Solo archivos anteriores y metadatos Git | **gpt-6-luna / low**, movimientos mecánicos/commits. Verifica stage por paths, identidad indicada por el principal y resultado del push; sin merge. |

T0 escribe únicamente estos dos documentos. Las tareas posteriores pertenecen a sus ejecutores; este spec no declara que ya se hayan completado.
