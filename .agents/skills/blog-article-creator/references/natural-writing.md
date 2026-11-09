# Manual de Redacción Natural y Estilo de Arturo López

Este documento define la voz, el tono, las estructuras narrativas y las reglas de redacción que caracterizan los artículos de blog de **Arturo López** (`lgzarturo`).

El objetivo fundamental es que **cada artículo suene 100% auténtico, personal, cercano y profesional**, transmitiendo la voz de un desarrollador experimentado, artesano del software y pensador pragmático, eliminando de raíz cualquier rastro o muletilla generada por modelos de inteligencia artificial.

---

## 1. La Voz y Tono de Arturo López

Arturo López es desarrollador de software, líder técnico y apasionado de la arquitectura de sistemas, la inteligencia artificial agéntica, los videojuegos de estrategia y rol, y la filosofía práctica (estoicismo, productividad consciente, desapego del resultado y aprendizaje continuo).

### Principios Fundamentales de la Voz:
1. **Primera Persona Cercana y Directa:** Escribe en primera persona y habla de tú a tú al lector, como a un colega de profesión. No hay fórmulas de entrada ni frases comodín: la voz sale de lo que cuentas, no de expresiones repetidas entre artículos.
2. **Pragmático pero Reflexivo:** Combina la solidez técnica (Spring Boot, Kotlin, Java, TypeScript, TDD, Clean Code, Git worktrees, arquitecturas agénticas) con reflexiones humanas profundas sobre el valor del tiempo, el desapego de los frutos de la acción y el crecimiento interior.
3. **El Artesano vs. El Gurú:** No escribe desde un pedestal de sabelotodo. Escribe desde el taller: experimenta, tropieza, analiza los *trade-offs*, realiza *post-mortems* honestos y comparte sus aprendizajes con humildad.
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
* **Variaciones de Párrafo:** Mezcla párrafos descriptivos de 3 a 5 oraciones con párrafos independientes de una sola línea que obliguen al lector a pausar y asimilar la idea.
* **Citas Destacadas (`>` Blockquotes):** Son opcionales y tienen solo un máximo por arquetipo (nota 1, guía 2, análisis y tutorial 3). Cada cita debe ser una sentencia memorable propia del tema, no un adorno.
* **Bloques Visuales (cero por defecto):** Mermaid y tablas solo si la Ficha los declara, cada uno con lo que explica que la prosa no puede. Si la Ficha no los declara, no se añaden. El código es obligatorio solo en `tutorial`; cuando aparece, va comentado. Reserva ASCII para bocetos que no sean diagramas técnicos formales.

### Registro por Objetivo
El objetivo de la Ficha fija el registro (ver `reading-time.md`): `reflexionar` → íntimo y narrativo; `estar-al-dia` → periodístico; `entender` → explicativo; `decidir` → evaluativo, con criterios; `hacer` → directo e imperativo. El registro cambia de un artículo a otro; la voz de Arturo se mantiene.

---

## 3. Estructura Narrativa del Artículo

### A. Arco Narrativo por Tipo
El tipo de la Ficha fija el orden de los movimientos (no los títulos de las secciones):

| Tipo | Arco |
| :--- | :--- |
| `tutorial` | problema → preparación → pasos → verificación → errores comunes |
| `lista` | escena → lecciones con hilo conductor → síntesis |
| `analisis` / `comparativa` | tesis → evidencia → contraargumento → postura |
| `postmortem` | incidente → diagnóstico → causa raíz → lección |
| `perfil` | mito → hechos → lo que enseña hoy |
| `ensayo` | tensión → exploración → giro → aprendizaje |
| `novedades` | qué cambió → por qué importa → qué hacer ahora |

### B. El Gancho Inicial (Introducción)
Entra al tema sin rodeos y respeta el tope de intro del arquetipo. El gancho sale de una lista cerrada: **escena, dilema, pregunta, cita, dato o contraintuición**. Antes de la Ficha, lee las aperturas recientes y elige un gancho distinto al de los últimos 5:

```bash
python3 .agents/skills/blog-article-creator/scripts/index_articles.py --recent 5 --openings
```

No hay frases de ejemplo para copiar: cada gancho se escribe desde el material del artículo.

### C. El Cuerpo Principal (`##` y `###`)
* Una sección `##` por parte del esquema, con el presupuesto que dio `plan_length.py`. No uses una plantilla fija.
* **Transiciones con enlace concreto:** cada `##` arranca retomando algo concreto de la sección anterior (un dato, una pregunta abierta, una consecuencia). El validador avisa si un párrafo empieza con una muletilla vetada: "Ahora bien", "Dicho esto", "Pasemos a", "Veamos ahora", "Llegados a este punto", "Antes de continuar", "Por otro lado,", "Con esto en mente".
* Los datos verificables llevan su fuente como enlace contextual en la frase que los afirma (ver `references/research.md`). Los enlaces a otros artículos del blog van dentro de la prosa (ver `references/internal-linking.md`).
* Cada sección aborda un problema concreto, demuestra el *por qué* antes del *cómo*, y ofrece un ejemplo o caso de uso práctico.
* No satures con listas de viñetas vacías; privilegia la narrativa técnica explicativa.

### D. La Conclusión y el Cierre
Nunca resumas mecánicamente lo ya dicho. La conclusión:
1. Cierra el arco narrativo con una reflexión que enlace con el gancho inicial, dentro del rango del arquetipo (sin contar la línea de contacto).
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
- [ ] **Gancho:** ¿Inicia con un gancho de la lista cerrada, distinto al de los últimos 5 artículos, y la intro respeta su tope?
- [ ] **Arco y registro:** ¿Sigue el arco de su tipo y el registro de su objetivo?
- [ ] **Transiciones:** ¿Cada `##` retoma algo concreto de la sección anterior, sin muletillas vetadas?
- [ ] **Visuales:** ¿Cada Mermaid o tabla está declarado en la Ficha?
- [ ] **Originalidad:** ¿El ángulo se diferencia de lo que ya existe en el blog y las analogías salen del tema (no de la paleta por costumbre)?
- [ ] **Longitud:** ¿Cada sección se acerca a su presupuesto y no hay párrafos que solo existen para llegar a un número?
- [ ] **Ritmo:** ¿Hay alternancia de frases largas y cortas y las citas en bloque (`>`) no superan el máximo del arquetipo?
- [ ] **Fuentes:** ¿Los datos verificables tienen fuente primaria citada en la prosa y lo no verificado se eliminó o se presentó como opinión?
- [ ] **Enlaces internos:** ¿Hay enlaces a artículos del blog dentro de la prosa, sin forzarlos?
- [ ] **Cierre:** ¿La conclusión termina con una idea propia del tema, distinta a la de los últimos artículos, seguida de la línea constante de contacto?
- [ ] **Referencias:** ¿Contiene la sección `## Referencias` con las fuentes realmente usadas y enlaces funcionales?
- [ ] **Validación:** ¿Pasa limpio `.agents/skills/blog-article-creator/scripts/validate_article.py --type <tipo> --objective <objetivo> --visuals <N>`?
