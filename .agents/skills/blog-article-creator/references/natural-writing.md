# Manual de Redacción Natural y Estilo de Arturo López

Este documento define la voz, el tono, las estructuras narrativas y las reglas de redacción que caracterizan los artículos de blog de **Arturo López** (`lgzarturo`).

El objetivo fundamental es que **cada artículo suene 100% auténtico, personal, cercano y profesional**, transmitiendo la voz de un desarrollador experimentado, artesano del software y pensador pragmático, eliminando de raíz cualquier rastro o muletilla generada por modelos de inteligencia artificial.

---

## 1. La Voz y Tono de Arturo López

Arturo López es desarrollador de software, líder técnico y apasionado de la arquitectura de sistemas, la inteligencia artificial agéntica, los videojuegos de estrategia y rol, y la filosofía práctica (estoicismo, productividad consciente, desapego del resultado y aprendizaje continuo).

### Principios Fundamentales de la Voz:
1. **Primera Persona Cercana y Directa:** Escribe siempre en primera persona ("Yo", "en mi experiencia", "en mi día a día", "hoy quiero reflexionar contigo", "me gusta pensar que"). Habla de tú a tú al lector, tratándolo como a un colega de profesión o a un compañero de trinchera tecnológica.
2. **Pragmático pero Reflexivo:** Combina la solidez técnica (Spring Boot, Kotlin, Java, TypeScript, TDD, Clean Code, Git worktrees, arquitecturas agénticas) con reflexiones humanas profundas sobre el valor del tiempo, el desapego de los frutos de la acción y el crecimiento interior.
3. **El Artesano vs. El Gurú:** No escribe desde un pedestal de sabelotodo. Escribe desde el taller: experimenta, tropieza, analiza los *trade-offs*, realiza *post-mortems* honestos y comparte sus aprendizajes con humildad ("De novato a maestro", "Lecciones aprendidas en el camino").
4. **Analogías que salen del tema (no de una lista):** Las mejores metáforas nacen del propio asunto: su dominio, su historia, un caso real, un objeto cotidiano que se parezca al mecanismo. Primero busca ahí. Una analogía es opcional; un artículo sin ninguna es perfectamente válido.
   - **Paleta opcional** (solo si encaja de forma orgánica y aclara algo; nunca como requisito ni como adorno): *videojuegos* (Pokémon, Age of Mythology, Dark Souls), *cultura pop* (Spider-Man) y *estoicismo* (Epicteto, Marco Aurelio, dicotomía del control).
   - **Antirrepetición:** si una referencia de la paleta apareció en 3 de los últimos 5 artículos, no la uses; el validador avisa. Cuando uses una, que sea concreta y aporte una idea que el texto no daría igual de bien sin ella.
5. **Actuar sin Depender del Resultado:** El disfrute del proceso y la excelencia artesanal están por encima de la validación externa o las métricas superficiales. Escribir y programar bien es la recompensa en sí misma.
6. **Idioma y Registro Estándar: Español Neutro (Estricto):**
   - **Tuteo Estándar:** Trata al lector de *tú* con conjugaciones neutras estándar (*tú tienes, tú puedes, tú observas, revisa, lee, diseña, mantén*).
   - **Cero Voseo:** Prohibido rotundamente el voseo (*tenés, podés, mirá, leé, dejá, hacés, vos, para vos, te dices a vos mismo*).
   - **Cero Regionalismos:** Prohibidos chilenismos (*po, cachai, altiro*), rioplatismos (*che, laburo, recién + infinitivo*), o giros ibéricos peninsulares (*vosotros, habéis, chaval*).
   - **Identidad:** Arturo López escribe en un español neutro con naturalidad mexicana culta, técnica, cercana y universal para toda la comunidad hispanohablante.

---

## 2. Ritmo, Dinámica y Formato Visual

Una redacción humana se distingue por su cadencia respiratoria variada. Si todos los párrafos miden exactamente 4 líneas o todas las oraciones tienen la misma estructura sintáctica, el texto se sentirá rígido y artificial.

### Reglas de Ritmo:
* **Variaciones de Longitud de Frase:** Alterna explicaciones técnicas o analíticas con sentencias breves y contundentes.
  * *Ejemplo:* "Cuando un sistema de producción colapsa a las tres de la mañana por una consulta mal optimizada, la teoría universitaria se desvanece por completo. Ahí solo queda el temple de la ingeniería."
* **Variaciones de Párrafo:** Mezcla párrafos descriptivos de 3 a 5 oraciones con párrafos independientes de una sola línea que obliguen al lector a pausar y asimilar la idea.
* **Citas Destacadas (`>` Blockquotes):** La cantidad escala con el arquetipo: nota 0–1, guía 1–3, análisis y tutorial 2–4. Cada cita debe ser una sentencia filosófica o técnica memorable, no un adorno.
  * *Ejemplo:* `> "El verdadero valor del desarrollador no reside en cuántas líneas de código teclea por minuto, sino en su capacidad para modelar reglas de negocio complejas con simplicidad y elegancia."`
* **Apoyo Visual Limpio:** Emplea diagramas Mermaid para arquitecturas, secuencias, flujos o relaciones; usa tablas comparativas y bloques de código rigurosamente comentados en Kotlin, Java, TypeScript, Bash o SQL. Reserva ASCII para bocetos que no sean diagramas técnicos formales.

---

## 3. Estructura Narrativa del Artículo

### A. El Gancho Inicial (Introducción)
Comienza sin rodeos introductorios ni generalidades. Usa una de estas fórmulas:
* **Una anécdota o escena concreta:** Un bug que costó horas descubrir, una guardia tensa de fin de semana, una refactorización intimidante.
* **Una tensión o dilema real:** "Muchos celebran la velocidad de autocompletado de la IA, pero muy pocos se detienen a analizar la deuda arquitectónica que se acumula cuando nadie valida el diseño subyacente."
* **Una pregunta sincera:** "¿Cuántas veces has postergado la limpieza de un servicio crítico por miedo a que se rompan contratos que ni siquiera están testeados?"
* **Una cita de impacto:** Una sentencia reflexiva que dispare el debate central.

### B. El Cuerpo Principal (`##` y `###`)
* Organizado en secciones lógicas tituladas de manera atractiva. La cantidad de secciones `##` del cuerpo escala con el arquetipo (nota 1–2, guía 3–4, análisis 4–6, tutorial 5+), sin contar Conclusión ni Referencias. No uses una plantilla fija.
* Los datos verificables llevan su fuente como enlace contextual en la frase que los afirma (ver `references/research.md`). Los enlaces a otros artículos del blog van dentro de la prosa (ver `references/internal-linking.md`).
* Cada sección aborda un problema concreto, demuestra el *por qué* antes del *cómo*, y ofrece un ejemplo o caso de uso práctico.
* Equilibra la prosa con código y diagramas: no satures con listas de viñetas vacías; privilegia la narrativa técnica explicativa.

### C. La Conclusión y el Cierre
Nunca resumas mecánicamente lo ya dicho. La conclusión:
1. Cierra el arco narrativo con una reflexión que enlace con el gancho inicial. En una nota puede ser de 2 o 3 líneas.
2. Termina con una idea, un reto o una pregunta **propios del tema**, escritos para este artículo. No hay frase de despedida obligatoria y no se repite la de otro artículo; el validador avisa si una oración del cierre coincide con la de los últimos 3 artículos.
3. Añade, como última cosa antes de `## Referencias`, **una sola línea constante** con los enlaces de contacto:

   ```markdown
   Si quieres comentar o compartir tu experiencia, escríbeme en [X (@algforge)](https://x.com/algforge) o abre un issue en el [repositorio](https://github.com/lgzarturo/arthurolg-blog-posts/issues). Una estrella en [GitHub](https://github.com/lgzarturo) también ayuda.
   ```

Estructura final:

```markdown
## Conclusión

<Reflexión de cierre propia del tema y, si aplica, una pregunta o reto específico>

Si quieres comentar o compartir tu experiencia, escríbeme en [X (@algforge)](...) o abre un issue en el [repositorio](...). Una estrella en [GitHub](...) también ayuda.

## Referencias

- [Título de la fuente, Organización](https://...)
```

---

## 4. Lista Negra: Clichés de IA Prohibidos

El validador rechaza activamente las siguientes expresiones y patrones:

| Cliché de IA Prohibido                                    | Motivo                                      | Alternativa Natural                                                |
| :-------------------------------------------------------- | :------------------------------------------ | :----------------------------------------------------------------- |
| *"En el vertiginoso mundo de..."*                         | Relleno genérico de IA                      | Arrancar directo con la acción o el problema.                      |
| *"En la era digital actual..."*                           | Tópico sin valor informativo                | Contextualizar con el problema técnico real.                       |
| *"En el mundo del desarrollo moderno..."*                 | Frase comodín vacía                         | Mencionar la herramienta, framework o arquitectura concreta.       |
| *"Cabe destacar / mencionar / resaltar"*                  | Muletilla burocrática                       | Exponer el hecho directamente.                                     |
| *"Es importante / fundamental destacar"*                  | Adorno prescindible                         | Dejar que el dato hable por su propia relevancia.                  |
| *"En conclusión, / En resumen, / En definitiva,"*         | Transición robótica al inicio de conclusión | Iniciar la conclusión con la reflexión final de forma fluida.      |
| *"Sin lugar a dudas / Sin duda alguna"*                   | Absolutismo innecesario                     | Aportar argumentos o matices técnicos.                             |
| *"Un papel fundamental / Pieza clave en el rompecabezas"* | Metáfora desgastada                         | Explicar la función arquitectónica precisa.                        |
| *"El viaje apenas comienza"*                              | Cierre cliché inspiracional barato          | Cerrar con un reto técnico o una invitación sincera a la práctica. |
| *"No es una excepción"*                                   | Automatismo sintáctico                      | Describir el caso particular con naturalidad.                      |
| Tríos adjetivales (*"rápido, eficiente y escalable"*)     | Patrón rítmico robótico de LLMs             | Usar adjetivos precisos justificados con evidencia.                |
| Voseo (*"tenés, podés, mirá, hacés, vos"*)                | Prohibido. Rompe el registro neutro         | Usar tuteo neutro (*"tienes, puedes, mira, haces, tú"*).           |
| Modismos regionales marcados (*"cachai, po, che, laburo"*) | Prohibido. Provincializa el artículo        | Usar léxico neutro claro (*"entiendes, colega, trabajo"*).        |
| Peninsularismos (*"vosotros, habéis, tenéis"*)            | Prohibido. No coincide con el perfil        | Usar segunda persona neutra (*"ustedes tienen"*).                  |

---

## 5. Checklist de Verificación Humana antes de Aprobar

- [ ] **Idioma:** ¿Está redactado 100% en español neutro (tuteo estándar), sin voseo (*tenés, mirá*) ni regionalismos chilenos, rioplatenses o peninsulares?
- [ ] **Voz:** ¿Suena a Arturo López hablando desde la experiencia y no a un texto autogenerado?
- [ ] **Gancho:** ¿Inicia con una anécdota, dilema o escenario real sin clichés?
- [ ] **Originalidad:** ¿El ángulo se diferencia de lo que ya existe en el blog y las analogías salen del tema (no de la paleta por costumbre)?
- [ ] **Longitud:** ¿La extensión corresponde al arquetipo aprobado y no hay párrafos que solo existen para llegar a un número?
- [ ] **Ritmo:** ¿Hay alternancia de frases largas y cortas y las citas en bloque (`>`) corresponden al arquetipo?
- [ ] **Fuentes:** ¿Los datos verificables tienen fuente primaria citada en la prosa y lo no verificado se eliminó o se presentó como opinión?
- [ ] **Enlaces internos:** ¿Hay enlaces a artículos del blog dentro de la prosa, sin forzarlos?
- [ ] **Cierre:** ¿La conclusión termina con una idea propia del tema, distinta a la de los últimos artículos, seguida de la línea constante de contacto?
- [ ] **Referencias:** ¿Contiene la sección `## Referencias` con las fuentes realmente usadas y enlaces funcionales?
- [ ] **Validación:** ¿Pasa limpio `.agents/skills/blog-article-creator/scripts/validate_article.py --archetype <arquetipo>`?
