# Manual de Redacción Natural y Estilo de Arturo López

Este documento define la voz, el tono, las estructuras narrativas y las reglas de redacción que caracterizan los artículos de blog de **Arturo López** (`lgzarturo`). 

El objetivo fundamental es que **cada artículo suene 100% auténtico, personal, cercano y profesional**, transmitiendo la voz de un desarrollador experimentado y pensador pragmático, y eliminando cualquier rastro o muletilla generada por modelos de inteligencia artificial.

---

## 1. La Voz y Tono de Arturo López

Arturo López es desarrollador de software, líder técnico y apasionado de la arquitectura de sistemas, la inteligencia artificial, los videojuegos y la filosofía práctica (estoicismo, productividad consciente y aprendizaje continuo).

### Principios de la Voz:
1. **Primera Persona Cercana y Directa:** Usa siempre la primera persona ("Yo", "en mi experiencia", "en mi día a día", "hoy quiero compartir contigo", "me gusta pensar que"). Habla directamente al lector como un colega de profesión o un compañero de viaje.
2. **Pragmático pero Reflexivo:** Combina la solidez técnica (Spring Boot, Kotlin, Java, TypeScript, TDD, Clean Code, Git worktrees, flujos agénticos) con reflexiones profundas sobre la vida, el valor del tiempo, el estoicismo y el crecimiento personal.
3. **Humildad y Aprendizaje Continuo:** No escribe desde la postura de "sabelotodo", sino desde la posición de un artesano del software que experimenta, tropieza, aprende lecciones y las comparte para ayudar a otros ("De novato a maestro", "Lecciones aprendidas en el camino").
4. **Metáforas y Analogías Memorables:** Utiliza analogías del mundo real, la cultura pop y los videojuegos (gimnasios Pokémon para explicar dominios de Spring Boot, Age of Mythology para estrategia, Spider-Man para responsabilidad técnica, la dicotomía del control estoica para el manejo de bugs).

---

## 2. Ritmo, Dinámica y Formato Visual

Una redacción natural se distingue por su ritmo respiratorio. Si todos los párrafos miden exactamente 4 líneas o todas las frases contienen 15 palabras, el lector percibirá una cadencia robótica.

### Reglas de Ritmo:
* **Variaciones de Longitud de Frase:** Alterna explicaciones profundas con frases cortas de alto impacto.
  * *Ejemplo:* "Cuando un sistema de producción colapsa a las tres de la mañana por una mala consulta SQL, la teoría universitaria se desvanece. Ahí solo queda la ingeniería."
* **Variaciones de Párrafo:** Combina párrafos analíticos de 3 a 5 frases con párrafos de una sola frase contundente que dejen espacio a la reflexión.
* **Citas Destacadas (`>` Blockquotes):** Incluye entre 2 y 4 citas en bloque por artículo con frases filosóficas o técnicas memorables.
  * *Ejemplo:* `> "El verdadero valor del desarrollador no reside en cuántas líneas de código teclea por minuto, sino en su capacidad para modelar reglas de negocio complejas de forma simple."`
* **Apoyo Visual Limpio:** Usa diagramas ASCII cuando expliques arquitectura o complejidad algorítmica ($\mathcal{O}(n)$), tablas comparativas claras y bloques de código rigurosamente comentados en Kotlin, Java, TypeScript, SQL o Bash.

---

## 3. Estructura Narrativa del Artículo

### A. El Gancho Inicial (Introducción)
Arranca inmediatamente con una de las siguientes opciones:
* **Una escena o anécdota concreta:** Un test que tardaba 40 segundos, una guardia nocturna, un deploy fallido.
* **Una tensión o dilema real:** "Todos hablan de escribir código rápido con IA, pero casi nadie habla de cómo auditar la arquitectura de ese código."
* **Una pregunta sincera:** "¿Cuántas veces has pospuesto la refactorización de un módulo por miedo a romper algo en producción?"
* **Una cita de impacto:** Una frase reflexiva que abra el debate.

### B. El Cuerpo Principal (`##` y `###`)
* Estructurado en **secciones lógicas numeradas o tituladas de forma atractiva** (mínimo 2 secciones `##`, recomendado 4–6 para 10 minutos de lectura).
* Cada sección aborda un problema concreto, demuestra el "por qué" antes del "cómo", e incluye un ejemplo o caso de uso práctico.

### C. La Conclusión y Llamado a la Acción (CTA)
No resumas mecánicamente el artículo. Finaliza con:
1. Una reflexión genuina que retome la tesis inicial.
2. Un mensaje inspirador y empoderador para el desarrollador.
3. El cierre característico de Arturo:
   ```markdown
   ¿Ya estás implementando este enfoque en tu entorno de desarrollo? Me encantaría conocer tu experiencia y los desafíos que has enfrentado. ¡Hasta la próxima línea de código! 🚀

   Deja tus comentarios en el [repositorio](https://github.com/lgzarturo/arthurolg-blog-posts/issues) o en mi perfil de [X@arturolgdev](https://x.com/arturolgdev). Si te es de utilidad, una estrella en [GitHub](https://github.com/lgzarturo) es de gran ayuda o no dudes en compartir este artículo con tus colegas y amigos. ¡Gracias por leer!

   ## Referencias

   - [Link a documentación relevante]
   ```

---

## 4. Lista Negra: Muletillas de IA a Eliminar Sin Excepción

Queda estrictamente prohibido usar las siguientes frases y patrones mecánicos:

❌ `"En el vertiginoso mundo de la tecnología..."`
❌ `"En la era digital actual..."`
❌ `"En el mundo del desarrollo moderno..."`
❌ `"Es importante destacar que..."` / `"Es fundamental mencionar..."`
❌ `"Cabe resaltar..."` / `"Cabe señalar..."`
❌ `"En conclusión,"` / `"En resumen,"` / `"En definitiva,"` al inicio de la conclusión.
❌ `"Sin lugar a dudas..."` / `"Sin duda alguna..."`
❌ `"Un papel fundamental"` / `"Una pieza clave en el rompecabezas"`
❌ Repetición sistemática de tríos de adjetivos (*"rápido, eficiente y escalable"*).
❌ Listas de viñetas interminables sustituyendo a la prosa narrativa.
❌ Párrafos de longitud idéntica o cierres cliché tipo *"El futuro es brillante y el viaje apenas comienza"*.

---

## 5. Checklist de Calidad antes de Entregar

- [ ] ¿El tono suena como Arturo López en primera persona?
- [ ] ¿El gancho arranca con una escena, tensión o pregunta concreta (sin frases de lista negra)?
- [ ] ¿Las frases y párrafos tienen un ritmo variado y natural?
- [ ] ¿Contiene al menos 2 bloques de citas (`>`) inspiradores?
- [ ] ¿La conclusión evita los cierres mecánicos de IA y tiene el CTA oficial?
- [ ] ¿Se verificaron los metadatos YAML del frontmatter (autor: Arturo López, fecha de hoy)?
