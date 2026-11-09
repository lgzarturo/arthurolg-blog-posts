---
title: 'Tu agente de código guarda tus secretos en texto plano: 1,379 ya están en GitHub'
image: 'https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/agente-codigo-secretos-texto-plano-settings-local-json.webp'
description: 'Apiiro halló 1,379 secretos en settings.local.json y Socket detectó el gusano strutil-core: por qué tu agente filtra credenciales y cómo blindar tu flujo.'
author: 'Arturo López'
date: '2026-11-08'
label: 'Tecnología'
---

Un clic. «Yes, and don't ask again». Eso es todo lo que hace falta para que un agente de código empiece a guardar contraseñas en texto plano dentro del repositorio, listo para subir a GitHub. No ocurre por una vulnerabilidad fortuita en el modelo: surge del diseño mismo de la persistencia de permisos.

Cuando le pides a una herramienta como Claude Code ejecutar una migración, consultar una base de datos o probar una API, el comando que propone suele contener credenciales reales. Si apruebas con la opción de no volver a preguntar para ahorrar fricción, el comando exacto queda registrado en `.claude/settings.local.json`. Y esta semana conocimos la magnitud de cuántos proyectos ya sufrieron este descuido.

## Qué encontró Apiiro y qué más pasó esta semana

El 5 de noviembre, la firma de seguridad [Apiiro publicó una investigación](https://apiiro.com/blog/coding-agents-leaking-secrets-github-dont-ask-again) que encendió las alertas en la comunidad técnica. Tras escanear 104,185 copias públicas de `.claude/settings.local.json` en GitHub, identificaron 1,122 archivos con credenciales reales (un 1.1% del total analizado). En conjunto, esos archivos contenían 1,379 secretos activos en ramas principales: 379 contraseñas de bases de datos directas, 122 claves service-role de Supabase, 103 tokens de administración de cuentas de Supabase, 149 claves de modelos de inteligencia artificial, 110 claves de API de Google, 43 credenciales SSH para servidores públicos, 42 tokens de GitHub, GitLab y npm, 23 claves de AWS y 6 llaves privadas.

Al extender el análisis al historial de git, repositorios con archivos de configuración compartidos (`settings.json`) y transcripciones de sesiones de agentes, la cifra creció hasta 2,539 secretos reales distribuidos en 1,994 repositorios. La filtración afectó a 63 organizaciones distintas, incluyendo empresas emergentes, agencias de software, aplicaciones de expedientes médicos y proveedores consolidados de bases de datos.

> Esta puede parecer una pequeña muestra, pero representa una superficie de riesgo considerable, especialmente considerando que estos secretos podrían estar presentes en repositorios privados y no ser detectados por herramientas de escaneo tradicionales. Es un llamado a la acción para que las empresas implementen medidas de seguridad adicionales para proteger sus repositorios.

El aspecto más revelador radica en el desempeño de los escáneres tradicionales. Apiiro ejecutó Gitleaks y TruffleHog sobre las 104,185 copias. Gitleaks detectó secretos en 564 de los 1,122 archivos comprometidos, mientras que TruffleHog señaló 643. Un total de 215 archivos (cerca del 19.2%) no fueron señalados por ninguna de las dos herramientas. Estas utilidades están calibradas para buscar cadenas aleatorias de alta entropía o patrones estructurados con prefijos definidos (como los identificadores clásicos de proveedores cloud). Cuando una contraseña ordinaria viaja dentro de un comando como `PGPASSWORD="password"` o `mysql -p`, el analizador estático la interpreta como texto convencional de consola.

En paralelo, el 1 de noviembre, la empresa de seguridad [Socket reportó una gema maliciosa en RubyGems llamada strutil-core](https://socket.dev/blog/shai-hulud-descendant-malicious-ruby-gem) (versión 1.0.1, retirada cinco horas después). La gema descargaba un gusano en JavaScript que recolectaba credenciales de 51 almacenes distintos, incluidos `.claude/.credentials.json` y `.codex/auth.json`, e inyectaba servidores MCP maliciosos en la configuración local para persistir. Este ataque incorporaba un mecanismo destructivo: un servicio de monitoreo eliminaba el directorio raíz del usuario si el token robado de GitHub era revocado. Sumado a incidentes previos como el ataque [Nx s1ngularity analizado por GitGuardian](https://blog.gitguardian.com/the-nx-s1ngularity-attack-inside-the-credential-leak/), el patrón resulta innegable: la configuración del agente ya no es solo susceptible a errores de publicación, sino que se ha convertido en un objetivo prioritario de robo.

## Por qué un archivo "local" termina en GitHub

La convergencia entre archivos omitidos por escáneres y amenazas dirigidas a carpetas de agentes evidencia tres suposiciones frágiles que la industria ha normalizado en el desarrollo asistido.

El primer supuesto es creer que la palabra «local» garantiza aislamiento en el control de versiones. De acuerdo con la [documentación oficial de Claude Code sobre configuración](https://code.claude.com/docs/en/settings), la herramienta añade automáticamente `.claude/settings.local.json` al archivo global de exclusiones de git (`~/.config/git/ignore`) la primera vez que genera el archivo. Este mecanismo opera adecuadamente en la estación de trabajo original, pero no se traslada al repositorio del proyecto. Si clonas el repositorio en otra computadora, lo abres en un contenedor, transfieres el directorio de trabajo o inicializas el repositorio posteriormente, esa exclusión global no existe. Git no interpreta la semántica del nombre: si el archivo no figura en el `.gitignore` del proyecto, pasa a formar parte del árbol de cambios.

El segundo supuesto es asumir que el desarrollador siempre revisa manualmente cada commit. En el debate de [Hacker News sobre el informe de Apiiro](https://news.ycombinator.com/item?id=50407882), Boris Cherny, responsable de Claude Code en Anthropic, señaló que el archivo está pensado para permanecer en local y recomendó utilizar el modo automático («Auto Mode») junto con los escáneres de seguridad del repositorio. No obstante, los datos recopilados demuestran que en 539 de los repositorios comprometidos el archivo fue introducido o modificado mediante un commit realizado en coautoría con el propio agente. Las reglas internas del asistente le prohíben versionar archivos `.env` o credenciales explícitas, pero su propia configuración de permisos locales no estaba incluida en esa lista de bloqueo.

El tercer supuesto es confiar en que la atención humana detectará credenciales incrustadas en comandos complejos. Ya he señalado en [¿Sigues leyendo todo el código de la IA?](https://www.arthurolg.com/article/technology_sigues-leyendo-todo-codigo-ia-diffs-tdd-validacion-determinista) que la revisión ocular colapsa rápidamente cuando los asistentes generan cadenas extensas de comandos encadenados. Tras diez interrupciones consecutivas aprobando tareas en la terminal, la fatiga de decisión empuja a pulsar «Yes, and don't ask again». Cuando llega el momento de consolidar cambios, un comando rutinario como `git add .` incluye silenciosamente la lista de permisos en el commit.

## Qué hacen CodeConductor y MicroSDD, y qué les falta

Frente a la fatiga humana y las fallas del ignore global, la solución exige controles estructurales en el arnés de ejecución. En mis propios proyectos abordo este desafío mediante dos estrategias complementarias: gobierno estricto y delimitación de alcance.

En [CodeConductor abordamos los flujos multiagente mediante arneses de ingeniería](https://www.arthurolg.com/article/technology_mas-ingenieria-menos-prompting-codeconductor), tratando la fuga de secretos como un riesgo que requiere supervisión arquitectónica:

- El consejo evaluador incluye un agente especializado `security-reviewer` con facultad de veto. Si este revisor detecta una posible exposición de credenciales o un patrón inseguro, la propuesta queda rechazada de forma inapelable, incluso si la mayoría de los demás agentes vota a favor.
- Las directivas en `AGENTS.md` y la configuración del entorno niegan por defecto el acceso a rutas sensibles (`.env*`, directorios de secretos y claves criptográficas). Tal como expliqué al [configurar Claude Code para trabajo serio](https://www.arthurolg.com/article/programming_configurar-claude-code-para-trabajo-serio), definir listas `deny` y ganchos `PreToolUse` bloquea intentos de lectura indebida en la terminal.
- El agente opera bajo un usuario de sistema operativo dedicado (`cc-agent`), acotando el acceso a variables y directorios protegidos de la máquina anfitriona.

Por su parte, en [MicroSDD, que utilicé para construir Agent Zero con validación determinista](https://www.arthurolg.com/article/technology_agent-zero-microsdd-arnes-agentes), el enfoque se centra en reducir el radio de acción:

- La instalación se realiza exclusivamente por proyecto en la raíz del repositorio, evitando configuraciones globales opacas.
- El gancho `PreToolUse` valida cada modificación contra un recibo RDD aprobado, rechazando cualquier escritura fuera de las rutas estrictamente autorizadas para la tarea.
- El flujo de trabajo exige adiciones explícitas en git (`git add <archivo>`), prohibiendo el uso indiscriminado de comandos que agreguen directorios completos.

Conviene ser transparentes respecto a las limitaciones actuales de ambas herramientas. En CodeConductor, el componente `output-scanner` encargado de inspeccionar diffs en busca de credenciales antes de confirmar cambios se encuentra definido en el diseño de arquitectura, pero aún no está integrado en la versión publicada. En MicroSDD, su instalador automatizado sincroniza opciones en `.claude/settings.local.json` y añade métricas a `.gitignore`, pero todavía no agrega automáticamente `settings.local.json` al `.gitignore` del proyecto cliente (a pesar de que nuestro repositorio de desarrollo sí lo incluye). Estoy en proceso de corregir este detalle en el scaffold inicial porque es indispensable para no depender de la memoria del usuario.

## Qué hacer hoy en cualquier repo

A la espera de que los entornos de desarrollo integren mejores defensas predeterminadas, existen medidas prácticas y verificables que conviene aplicar de inmediato en cualquier proyecto asistido por agentes:

1. **Inspecciona y limpia `.claude/settings.local.json`:** Abre el archivo en tus proyectos y revisa cada entrada de la lista `allow`. Si encuentras contraseñas, tokens de conexión o llaves de API incrustadas en comandos previamente aprobados, asume que esos valores ya no son privados y procede a rotarlos de inmediato en sus respectivos proveedores.
2. **Actualiza el `.gitignore` del repositorio:** No delegues la protección en archivos de exclusión globales del sistema. Añade de forma explícita las rutas críticas directamente en el `.gitignore` de la raíz del proyecto para que la regla viaje con el código fuente en cualquier clon o contenedor:
   - `.claude/settings.local.json`
   - `.claude/.credentials.json`
   - `.codex/auth.json`
   - `.env*`
3. **Desvincula archivos ya rastreados en el índice:** Si el archivo de configuración ya fue registrado previamente por git, incluirlo en `.gitignore` no impedirá que siga recibiendo seguimiento ni que futuras modificaciones se publiquen. Es indispensable ejecutar `git rm --cached .claude/settings.local.json` para retirarlo del árbol de trabajo sin eliminar la copia física de tu disco.
4. **Purga el historial completo si el archivo fue publicado:** Borrar un archivo en un commit nuevo no elimina el secreto de las confirmaciones previas, de las ramas remotas ni de las bifurcaciones públicas que otros usuarios hayan realizado. Siguiendo las recomendaciones de [GitHub Docs sobre remoción de datos sensibles](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository), la limpieza requiere herramientas deterministas como `git-filter-repo` aplicadas sobre un clon limpio:
   ```bash
   git filter-repo --path .claude/settings.local.json --invert-paths
   ```
   Tras reescribir el historial y forzar el envío a tus ramas remotas, recuerda que GitHub mantiene referencias en caché durante cierto tiempo. La rotación de las credenciales sigue siendo el único mecanismo que neutraliza el riesgo real.
5. **Comprueba la persistencia antes de revocar si sospechas malware:** En escenarios donde se sospeche la presencia de dependencias comprometidas (como el vector documentado con `strutil-core`), revocar inmediatamente un token de GitHub puede ser contraproducente. Si el malware instaló monitores en segundo plano como `net-health-checker`, la invalidación del token desencadenará la eliminación del directorio personal. El protocolo de respuesta exige aislar la estación de trabajo, verificar y detener los servicios registrados en systemd o LaunchAgents, eliminar los binarios sospechosos y únicamente entonces revocar las credenciales desde un equipo limpio.
6. **Sustituye comandos literales por variables y patrones de comodín:** Para evitar que las aprobaciones capturen datos sensibles, nunca escribas secretos directos en las solicitudes del asistente ni en los parámetros de ejecución. Utiliza variables de entorno del sistema operativo (`$DB_PASSWORD`) o recurre a reglas basadas en comodines como `Bash(npm run:*)` o `Bash(pytest *)`. De este modo, la regla registrada en la configuración almacena la estructura abstracta de la orden y no los valores confidenciales que viajan en su interior.
7. **Calibra escáneres locales con reglas para comandos:** Dado que las expresiones regulares estándar de Gitleaks y TruffleHog pasan por alto asignaciones de consola, añade patrones personalizados a tus ganchos de pre-commit para interceptar asignaciones como `PGPASSWORD=`, `sshpass -p` o cabeceras de autorización en peticiones de curl antes de que lleguen al repositorio.

## Conclusión

Un agente de código posee un acceso privilegiado a nuestro entorno de desarrollo: inspecciona archivos, ejecuta órdenes en el sistema operativo y registra autorizaciones en segundo plano. El error no radica en aprovechar sus capacidades de automatización, sino en suponer que la comodidad operativa puede prescindir de límites arquitectónicos deterministas.

Separar los secretos de la memoria del asistente y tratar los archivos de configuración local como superficies de ataque no constituye un exceso de celo, sino un requisito básico de ingeniería. La próxima ocasión en que la consola te ofrezca aprobar un comando de forma permanente, conviene dedicar un par de segundos a verificar qué información viaja en esa línea.

¿Cuántas credenciales sensibles residen en este momento en los archivos de configuración de tus agentes?

Si quieres comentar o compartir tu experiencia, escríbeme en [X (@algforge)](https://x.com/algforge) o abre un issue en el [repositorio](https://github.com/lgzarturo/arthurolg-blog-posts/issues). Una estrella en [GitHub](https://github.com/lgzarturo) también ayuda.

## Referencias

- [Coding Agents Are Leaking Your Secrets to GitHub, Apiiro](https://apiiro.com/blog/coding-agents-leaking-secrets-github-dont-ask-again)
- [Shai-Hulud Descendant Surfaces in Malicious Ruby Gem That Steals Credentials and Poisons AI Tools, Socket](https://socket.dev/blog/shai-hulud-descendant-malicious-ruby-gem)
- [Claude Code Settings Documentation, Anthropic](https://code.claude.com/docs/en/settings)
- [Discussion on Claude Code's "Don't Ask Again", Hacker News](https://news.ycombinator.com/item?id=50407882)
- [The Nx "s1ngularity" Attack: Inside the Credential Leak, GitGuardian](https://blog.gitguardian.com/the-nx-s1ngularity-attack-inside-the-credential-leak/)
- [Removing sensitive data from a repository, GitHub Docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
