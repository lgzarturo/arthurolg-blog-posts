# Pase de Editor SEO Experto

Aplica este pase después de redactar y antes de validar. El editor protege la
calidad periodística y la voz de Arturo: SEO significa responder mejor a una
necesidad real, no repetir palabras clave.

## Diagnóstico editorial

1. Define una sola intención de búsqueda principal: informacional, comparativa,
   transaccional o navegación. Si el borrador mezcla intenciones, elige una y
   convierte las demás en contexto secundario.
2. Formula una keyword principal como la escribiría el lector y 3–6 términos
   relacionados. Incorpóralos solo donde aporten precisión.
3. Comprueba que el título prometa exactamente lo que el artículo entrega, que
   el slug sea corto y legible, y que la descripción tenga entre 120 y 160
   caracteres cuando sea posible.

## Edición en el documento

- El primer párrafo debe confirmar rápidamente el problema y para quién es útil.
- Cada `##` debe responder una pregunta o avanzar la tesis; los `###` deben
  ordenar detalles, no fragmentar artificialmente el texto.
- Incluye sinónimos y entidades del tema en el texto, encabezados, alt text de
  imágenes y enlaces, pero evita la densidad mecánica de keywords.
- Enlaza a artículos del blog que existan, tomados de `index_articles.py` (ver
  [internal-linking.md](internal-linking.md)): dentro de la prosa, con texto
  descriptivo, sin forzarlos y respetando los mínimos del arquetipo.
- Cita las fuentes del dossier (ver [research.md](research.md)) con enlace
  contextual en la frase que afirma el dato; `## Referencias` solo las lista.
- Escribe el alt text describiendo la escena y su relación con el artículo; no
  uses frases genéricas como “imagen de tecnología”.
- Elimina introducciones vagas, repeticiones, promesas exageradas y párrafos que
  solo existen para alcanzar una duración.

## Control final

- [ ] La intención de búsqueda se entiende desde el título y la introducción.
- [ ] El título, slug y descripción son coherentes entre sí.
- [ ] La keyword principal aparece de forma natural y no domina el texto.
- [ ] La estructura permite escanear el artículo con encabezados, listas, código
      y Mermaid solo donde mejoran la comprensión.
- [ ] Las referencias y enlaces respaldan el contenido sin sustituir la voz
      propia del artículo.
- [ ] Los enlaces internos existen (el validador rompe con un enlace roto) y las
      fuentes están citadas en la prosa, no solo en `## Referencias`.
- [ ] El ángulo no repite un artículo ya publicado (revisado con el índice).
