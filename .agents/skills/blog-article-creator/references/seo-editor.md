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
- **Respuesta directa:** en intención informacional, tras el gancho va un
  párrafo de 40–60 palabras que responde la consulta. Cuenta dentro del tope de
  intro del arquetipo.
- **Keyword principal** en el título, el primer párrafo, al menos un `##` y la
  descripción; en ningún otro lugar se fuerza.
- Formula los `##` como preguntas reales del lector cuando el tipo lo permite;
  si no, que cada `##` avance la tesis. Los `###` ordenan detalles, no
  fragmentan artificialmente el texto.
- **Pasajes citables (GEO):** escribe párrafos que se entiendan aislados, con
  sujeto explícito y un dato o afirmación completa, para que un buscador o un
  asistente pueda citarlos sin el resto del artículo.
- **FAQ opcional** solo en `novedades` y `tutorial`, y solo si la SERP muestra
  preguntas relacionadas. Nunca en artículos de reflexión.
- Incluye sinónimos y entidades del tema en el texto, encabezados, alt text de
  imágenes y enlaces, pero evita la densidad mecánica de keywords.
- Enlaza a artículos del blog que existan, tomados de `index_articles.py` (ver
  [internal-linking.md](internal-linking.md)): dentro de la prosa, con texto
  descriptivo, sin forzarlos y respetando los mínimos del arquetipo.
- Cita las fuentes del dossier (ver [research.md](research.md)) con enlace
  contextual en la frase que afirma el dato; `## Referencias` solo las lista.
- Escribe el alt text describiendo la escena y su relación con el artículo; no
  uses frases genéricas como “imagen de tecnología”.
- **Español mexicano culto, ortografía y acentuación:** revisa título,
  descripción, encabezados y cuerpo para asegurar tuteo estándar, tildes
  correctas (incluidas diacríticas), signos de apertura (`¿`, `¡`) y sintaxis
  natural en español mexicano neutro, sin calcos del inglés ni voseo.
- **Voz de autor único (sin «nosotros»):** verifica que las opiniones,
  investigaciones y referencias a artículos previos estén en primera persona del
  singular (*yo, mi, mis, investigué, expliqué*) y elimina cualquier plural
  editorial (*vimos, abordamos, nuestro, debemos*).
- **Tecnicismos claros y narrativa enfocada:** confirma que cada término técnico
  o anglicismo necesario quede explicado con sencillez la primera vez que
  aparece, y que ningún párrafo se desvíe de la tesis central.
- Elimina introducciones vagas, repeticiones, promesas exageradas y párrafos que
  solo existen para alcanzar una duración.

## Control final

- [ ] La intención de búsqueda se entiende desde el título y la introducción.
- [ ] El título, slug y descripción son coherentes entre sí.
- [ ] La keyword principal aparece de forma natural y no domina el texto.
- [ ] Hay respuesta directa tras el gancho (si la intención es informacional) y
      la keyword aparece en título, primer párrafo, un `##` y descripción.
- [ ] El texto está en español mexicano culto (español neutro), con ortografía,
      gramática y acentos correctos y signos `¿`/`¡` completos.
- [ ] La voz es de autor único en singular (*yo/mi*), sin «nosotros», «nuestro»
      ni plural editorial.
- [ ] Los tecnicismos están mediados con explicaciones claras y la narrativa se
      mantiene enfocada en la tesis.
- [ ] La estructura permite escanear el artículo con encabezados; Mermaid y
      tablas solo si la Ficha los declaró.
- [ ] Las referencias y enlaces respaldan el contenido sin sustituir la voz
      propia del artículo.
- [ ] Los enlaces internos existen (el validador rompe con un enlace roto) y las
      fuentes están citadas en la prosa, no solo en `## Referencias`.
- [ ] El ángulo no repite un artículo ya publicado (revisado con el índice).
