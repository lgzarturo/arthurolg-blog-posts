# Investigación y Fuentes

Un artículo de este blog no se escribe solo con lo que el modelo "sabe". Lo verificable se investiga, se liga a una fuente y se cita. La voz sigue siendo de Arturo; las fuentes la respaldan, no la sustituyen.

---

## 1. Cuándo Aplica

| Categoría (`label`) | Investigación |
| :--- | :--- |
| Programación, Spring Boot, Tecnología, Marketing, Videojuegos | **Obligatoria** en todos los arquetipos |
| Reflexión / General | Obligatoria **solo si** el texto cita datos, estudios, fechas, versiones o autores. Una reflexión personal sin afirmaciones externas no fuerza fuentes |

Mínimo de fuentes externas por arquetipo: `nota` 1–2 · `guia` 3–5 · `analisis` 5–8 · `tutorial` 8+. (Reflexión sin afirmaciones externas: 0.)

---

## 2. Dos Momentos de Investigación

### A. Investigación ligera (fase Definir, la hace la propia skill)

Antes de presentar la Ficha, con pocas búsquedas (`WebSearch`, `WebFetch`, y `Context7` para documentación de librerías o frameworks):

1. Confirma que la tesis no está contradicha por las fuentes primarias.
2. Detecta la versión o el estado actual del tema (fechas, releases, cambios recientes). El conocimiento del modelo puede estar desactualizado.
3. Propón el **plan de fuentes**: qué fuentes primarias se consultarán y qué afirmaciones respaldarán.

### B. Dossier completo (fase Investigar, lo hace un sub-agente)

Tras la aprobación de la Ficha, **siempre** se lanza un sub-agente en segundo plano (`Agent`, tipo `general-purpose`) para construir el dossier. La skill espera su informe y redacta sobre él. No se lanza antes de la aprobación.

El dossier **vive solo en la conversación**: no se guarda en el repositorio. La Hoja de Aprobación incluye su tabla resumida para que Arturo pueda auditar de dónde salió cada dato.

---

## 3. Contrato del Sub-agente de Investigación

Prompt mínimo (adaptar al tema; el sub-agente parte de cero y no ve la conversación):

```
Investiga para un artículo de blog técnico en español. No escribas el artículo.

Tema: <tema>
Tesis: <tesis de la Ficha>
Audiencia: <audiencia>
Arquetipo: <arquetipo> (necesito al menos <N> fuentes distintas)
Plan de fuentes aprobado: <lista del plan>

Reglas:
- Prioriza fuentes primarias: documentación oficial, JEPs/RFCs/specs, papers, repositorios
  oficiales, el texto original de un autor o entrevistas directas.
- Después, blogs de ingeniería de la organización responsable. Evita agregadores y
  resúmenes de segunda mano.
- Abre y lee cada fuente (WebFetch). No cites una URL que solo viste en un buscador.
- Verifica fechas, versiones y cifras en la fuente, no de memoria.
- Para librerías y frameworks usa Context7 antes que búsqueda web.

Devuelve SOLO una tabla Markdown con estas columnas y nada más de relleno:
| # | Afirmación verificable (con dato exacto) | Fuente (título, organización) | URL | Tipo (primaria/secundaria) | Confianza (alta/media/baja) | Nota |

Después de la tabla, lista aparte: (1) afirmaciones que NO pudiste verificar, (2) datos
que contradicen la tesis, (3) 2–3 ángulos o hechos poco obvios que valga la pena contar.
```

---

## 4. Jerarquía de Fuentes

1. **Primarias:** documentación oficial, especificaciones (JEP, RFC, JSR), papers, código fuente, textos originales de autores, estudios con metodología publicada.
2. **Primarias institucionales de segunda línea:** blog de ingeniería del proyecto o empresa responsable, charlas oficiales, changelogs.
3. **Secundarias confiables:** libros, artículos de referencia reconocidos, medios técnicos con autoría y fecha.
4. **Evitar:** agregadores, "top 10" sin autoría, contenido generado, páginas sin fecha, enlaces que solo repiten otro artículo.

Si solo existe una fuente secundaria para un dato, o se marca como tal en el texto ("según …") o se elimina el dato.

---

## 5. Cómo se Usan las Fuentes en el Artículo

* **Cita contextual en la prosa:** el enlace va en la frase que afirma el dato, con texto descriptivo. Evita "aquí" o "este enlace". Las fuentes que solo aparecen en `## Referencias` generan aviso.
* **`## Referencias`** enumera las fuentes realmente usadas, con título y organización. No es un lugar para enlaces genéricos propios (`github.com/lgzarturo`, `arthurolg.com`); el validador avisa si son los únicos.
* **Lo no verificado:** se elimina, o se presenta como opinión o experiencia propia ("en mi experiencia", "creo que"), nunca como hecho.
* **La voz manda:** las fuentes aportan hechos y precisión; la interpretación, los ejemplos y las metáforas siguen siendo de Arturo.
* **Actualidad:** para temas con versiones (frameworks, JDK, modelos de IA, precios), indica la versión o la fecha de la fuente en el texto.

---

## 6. Verificación Final

```bash
python3 .agents/skills/blog-article-creator/scripts/validate_article.py \
  --file "<ruta>.md" --archetype <arquetipo> --check-links
```

`--check-links` comprueba por HTTP las fuentes externas. Algunos sitios bloquean peticiones automáticas, por eso un fallo es un aviso: confírmalo a mano antes de descartar la fuente.

---

## 7. Checklist

- [ ] ¿Cada afirmación verificable tiene fuente en el dossier y enlace contextual en el texto?
- [ ] ¿Predominan fuentes primarias?
- [ ] ¿Se alcanza el mínimo del arquetipo (o la categoría lo exime)?
- [ ] ¿Las versiones, fechas y cifras coinciden con la fuente?
- [ ] ¿Lo no verificado se eliminó o se presentó como opinión?
- [ ] ¿La Hoja de Aprobación incluye la tabla resumida del dossier?
