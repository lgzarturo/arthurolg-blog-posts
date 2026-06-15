---
title: Configurar Claude Code para trabajo serio: velocidad, control de tokens y un arnés de seguridad
image: https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/configurar-claude-code-para-trabajo-serio.webp
description: Claude Code es potente desde el primer arranque, pero su configuración por defecto está pensada para empezar rápido, no para un equipo que lo usa todos los días sobre código real. Aprende a configurarlo para optimizar tokens, velocidad y seguridad.
author: Arturo López
date: 2026-06-14
label: Guía
---

Claude Code es potente desde el primer arranque, pero su configuración por defecto está pensada para empezar rápido, no para un equipo que lo usa todos los días sobre código real. Sin afinarlo, terminas aprobando los mismos comandos una y otra vez, gastando tokens en razonamiento que no pediste, y dejando abiertas operaciones que nunca deberían ejecutarse sin supervisión.

Este artículo resume cómo configurar Claude Code en dos frentes: **optimizar el trabajo** (tokens, velocidad, multiagente) y **definir un arnés de seguridad** que ponga límites firmes a lo que el agente puede hacer. Todo está verificado contra la documentación oficial y probado en una configuración real.

---

## Primero, el mapa: dos archivos que no se deben mezclar

Casi toda la fricción al configurar Claude Code nace de confundir dos archivos que cumplen papeles distintos.

**`~/.claude/settings.json`** es tu configuración declarativa. Aquí controlas permisos, variables de entorno, hooks, atribución de commits, sandbox y preferencias. Es el archivo que editas, versionas (a nivel de proyecto) y endureces.

**`~/.claude.json`** es estado vivo que gestiona Claude Code: tu sesión OAuth, caches, métricas por proyecto, estado de *trust* de cada repositorio. No es para editar a mano. Solo contiene cuatro opciones de configuración que sí te pertenecen: `autoConnectIde`, `autoInstallIdeExtension`, `externalEditorContext` y `teammateDefaultModel`.

La regla de oro: **cada clave vive en un solo archivo, y equivocarse tiene consecuencias.** Los archivos de usuario, proyecto y local se validan de forma estricta: si una clave no pertenece al esquema, Claude Code **rechaza el archivo completo**, no solo esa línea. Es decir, poner `autoConnectIde` (que pertenece a `~/.claude.json`) dentro de `settings.json` no se ignora silenciosamente: anula todo tu archivo, incluido cada regla de seguridad que hayas escrito. Solo los *managed settings* de una organización se parsean de forma tolerante.

> **Cómo verificar que tu archivo carga.** Ejecuta `/status` y revisa la línea *Setting sources*: lista cada capa de configuración que Claude Code leyó. Si falta una, ese archivo no se cargó o tiene un error. Para el detalle de cualquier error de validación, usa `/doctor`.

---

## Parte 1 — Optimizar el trabajo

### Controlar el gasto de tokens

El consumo invisible más grande es el *extended thinking*. Razona antes de responder, no ves esa salida, pero **se factura como tokens de salida** y, sin tope, una sola petición compleja puede consumir decenas de miles de tokens. Si activaste el pensamiento extendido por defecto (`alwaysThinkingEnabled: true`) y un nivel de esfuerzo alto (`effortLevel: "xhigh"`), estás maximizando ese gasto en cada turno.

La palanca es un techo explícito:

```json
"env": {
  "MAX_THINKING_TOKENS": "24000"
}
```

Hay una tensión real que conviene decidir conscientemente: si elegiste `xhigh` para tareas de arquitectura, no lo capes de forma agresiva (a 10000, por ejemplo), porque cortarías el razonamiento que pediste. Un tope alto como 24000 funciona como red de seguridad contra consumos descontrolados sin degradar el trabajo complejo. Si quieres apagar el pensamiento por completo para tareas triviales, `MAX_THINKING_TOKENS: "0"` lo desactiva.

El resto de palancas de tokens trabajan en conjunto:

```json
"env": {
  "CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT": "1",
  "ENABLE_TOOL_SEARCH": "auto",
  "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "80",
  "CLAUDE_CODE_DISABLE_1M_CONTEXT": "1",
  "CLAUDE_CODE_SUBAGENT_MODEL": "haiku"
}
```

`CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT` reduce el prompt base que cargas en cada turno. `ENABLE_TOOL_SEARCH: "auto"` carga las definiciones de herramientas solo cuando se necesitan, en lugar de mantenerlas todas en contexto. `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: "80"` compacta la conversación antes de llegar al umbral por defecto, manteniendo las sesiones más sanas. `CLAUDE_CODE_DISABLE_1M_CONTEXT` evita la ventana de un millón de tokens cuando no la necesitas. Y `CLAUDE_CODE_SUBAGENT_MODEL: "haiku"` enruta los subagentes a un modelo más barato.

Para gestionar el contexto a ojo, agrega un medidor a la barra de estado:

```json
"statusLine": {
  "type": "command",
  "command": "npx -y @this-dot/claude-code-context-status-line"
}
```

Te muestra el porcentaje de contexto usado en cada turno, para que ejecutes `/compact` manualmente antes de que dispare la compactación automática.

### Multiagente: delegar para ir más rápido y gastar menos

La idea más rentable en Claude Code es **sacar el ruido de tu conversación principal**. Correr la suite de tests, traer documentación o procesar logs llena tu contexto con salida que no vas a volver a leer. Si delegas esas tareas a un subagente, la salida verbosa se queda en el contexto del subagente y solo el resumen relevante vuelve a tu hilo.

Claude Code ya trae subagentes integrados que usa automáticamente: **Explore** (solo lectura, corre en Haiku, para buscar y entender código), **Plan** (investigación en modo plan) y **general-purpose** (tareas complejas de varios pasos). No requieren configuración. Basta con pedir cosas como *"usa un subagente para correr los tests y reportar solo los que fallan"*.

Para tareas recurrentes, define subagentes propios. **Importante: viven en archivos Markdown (`.claude/agents/*.md`), no en `settings.json`.** Un revisor de solo lectura, alineado con un flujo de revisión por PR:

```markdown
---
name: code-reviewer
description: Revisa cambios de código para calidad y seguridad. Usar proactivamente tras escribir o modificar código.
tools: Read, Grep, Glob, Bash
model: sonnet
---

Eres un revisor senior. Corre git diff, enfócate en los archivos modificados
y reporta por prioridad: críticos, advertencias y sugerencias.
```

La frase *"usar proactivamente"* en la descripción es deliberada: es lo que le indica a Claude que delegue por su cuenta sin que se lo pidas explícitamente.

Cuando necesitas paralelismo real, los *agent teams* dan a cada trabajador su propio contexto independiente:

```json
"env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }
```

Es una función experimental con un costo a tener en cuenta: **cada teammate consume tokens por separado.** Conviene para trabajo multi-módulo o revisiones en paralelo; para tareas secuenciales simples, un subagente normal es más eficiente. El modelo por defecto de los teammates se fija en `~/.claude.json`:

```json
"teammateDefaultModel": "sonnet"
```

Una combinación que funciona bien: Haiku para la exploración barata (`CLAUDE_CODE_SUBAGENT_MODEL`), Sonnet para los teammates que producen trabajo sustancial.

---

## Parte 2 — El arnés de seguridad

Un arnés es el conjunto de límites que hacen que dejar a Claude trabajar con cierta autonomía sea seguro. La meta no es desconfiar del agente, sino acotar el daño posible: que jamás lea un secreto, ejecute algo destructivo, ni salte una confirmación crítica.

### Permisos en capas

El corazón del arnés es `permissions`, con tres listas que se evalúan **en orden: `deny` primero, luego `ask`, luego `allow`**, y gana la primera coincidencia. El principio rector es el de mínimo privilegio: permite explícitamente lo seguro y frecuente, pide confirmación para lo sensible, y bloquea lo peligroso de forma terminante.

```json
"permissions": {
  "allow": [
    "Bash(git status*)", "Bash(git diff*)", "Bash(npm test*)",
    "Bash(npm run lint*)", "Bash(pytest*)", "Read(**)", "Edit(**)"
  ],
  "ask": [
    "Bash(git push*)", "Bash(git rebase*)", "Bash(npm install*)",
    "Bash(docker run*)", "Bash(./gradlew build*)", "Bash(vercel*)"
  ],
  "deny": [
    "Agent(bypass-runner)",
    "Bash(rm -rf *)", "Bash(sudo *)", "Bash(curl * | sh)",
    "Bash(git push --force*)", "Bash(git reset --hard *)",
    "Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)",
    "Read(./**/*.pem)", "Read(./**/*.key)", "Read(~/.ssh/**)", "Read(~/.aws/**)"
  ],
  "defaultMode": "acceptEdits",
  "disableBypassPermissionsMode": "disable"
}
```

Dos detalles importan. Primero, las reglas de lectura en `deny` son tu primera línea contra la fuga de secretos: bloquean que el agente siquiera abra archivos `.env`, llaves privadas o credenciales. Segundo, `disableBypassPermissionsMode: "disable"` cierra el atajo más peligroso del CLI: desactiva el modo *bypass* y la bandera `--dangerously-skip-permissions`, de modo que ninguna sesión pueda saltarse las confirmaciones por completo.

### Hooks: automatización defensiva

Los hooks ejecutan comandos en eventos del ciclo de vida. Reciben su entrada como **JSON por `stdin`** —no como variables de entorno— así que la extracción correcta es con `jq`. Esto significa que `jq` debe estar instalado en cada máquina (`brew install jq` / `apt install jq`); de lo contrario los hooks no corren.

Un hook `PreToolUse` que bloquea (con código de salida 2) cualquier intento de leer archivos sensibles vía bash, reforzando las reglas `deny`:

```json
"hooks": {
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "json=$(cat); cmd=$(printf '%s' \"$json\" | jq -r '.tool_input.command // empty'); if printf '%s' \"$cmd\" | grep -qE '(\\.env|secrets/|id_rsa|\\.pem|\\.key)' && printf '%s' \"$cmd\" | grep -qE '(cat|less|more|head|tail|cp |mv |scp )'; then echo 'Bloqueado: lectura de archivos sensibles' >&2; exit 2; fi"
    }]
  }]
}
```

Un hook `PostToolUse` puede formatear automáticamente cada archivo tras editarlo (Prettier, ESLint, Ruff), eliminando la mayor fuente de fricción por aprobaciones. Y un hook `SubagentStop` puede registrar cuándo termina cada subagente, dándote trazabilidad del trabajo delegado.

### Aislamiento de procesos y red

Dos capas más completan el arnés. La limpieza de entorno evita filtrar credenciales a los subprocesos que Claude ejecuta:

```json
"env": { "CLAUDE_CODE_SUBPROCESS_ENV_SCRUB": "1" }
```

Y el sandbox aísla los comandos bash del sistema de archivos y la red (macOS, Linux y WSL2). Se puede dejar preparado pero inactivo, y activarlo cuando hayas validado que los dominios permitidos cubren tu flujo:

```json
"sandbox": {
  "enabled": false,
  "filesystem": { "denyRead": ["~/.ssh", "~/.aws", "~/.gnupg", "./.env", "./.env.*"] },
  "network": {
    "allowedDomains": ["github.com", "*.npmjs.org", "pypi.org", "*.gradle.org", "api.anthropic.com"],
    "allowLocalBinding": true
  }
}
```

### La atribución de commits no es lo que parece

Un punto que confunde a todos: **el autor de un commit lo fija `git`, no Claude Code.** La configuración `attribution` solo controla el *trailer* que Claude añade:

```json
"attribution": { "commit": "", "pr": "" }
```

Con `commit` y `pr` en cadena vacía, eliminas el `Co-Authored-By: Claude` de commits y PRs. Pero para que el commit aparezca a tu nombre, la identidad la define git:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@correo.com"
```

---

## Las trampas que cuestan una tarde

Estos son los errores reales que aparecen al endurecer la configuración, y que conviene conocer de antemano.

**Mezclar los dos archivos rompe todo.** `autoConnectIde` y `autoInstallIdeExtension` pertenecen a `~/.claude.json`. Si los pones en `settings.json`, disparan un error de esquema que rechaza el archivo entero. La forma segura de configurarlos es con `/config`.

**`includeCoAuthoredBy` está deprecada.** Fue reemplazada by `attribution`. Si dejas ambas, la primera es ruido; usa solo `attribution`.

**`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` apaga el actualizador.** Ese interruptor agrupa varias cosas, entre ellas `DISABLE_AUTOUPDATER`, lo que entra en conflicto con `autoUpdatesChannel: "stable"`. Si quieres privacidad sin tocar las actualizaciones, usa los flags granulares (`DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING`, `DISABLE_FEEDBACK_COMMAND`) en lugar del agrupador.

**`skipDangerousModePermissionPrompt` contradice la postura de seguridad.** Ya que busca saltar la confirmación del modo peligroso, va directo en contra de `disableBypassPermissionsMode: "disable"`. Si desactivas el modo *bypass*, esta clave no es necesaria.

**Cuidado con las redundancias.** `CLAUDE_CODE_DISABLE_AUTO_MEMORY` es el equivalente por variable de entorno de `autoMemoryEnabled: false`; con una basta. Y `CLAUDE_CODE_ATTRIBUTION_HEADER` no afecta la atribución de los commits (controla un header de caché del *system prompt*): no aporta al objetivo y es inocua en la API directa.

**Los hooks no usan variables `$CLAUDE_TOOL_*`.** Reciben JSON por `stdin`; si copias hooks viejos que esperan variables de entorno, no se ejecutarán nunca. Extrae con `jq`.

---

## Checklist final

1. Separa los archivos: configuración en `settings.json`, las cuatro globales (`autoConnectIde`, `autoInstallIdeExtension`, `externalEditorContext`, `teammateDefaultModel`) en `~/.claude.json` vía `/config`.
2. Pon un techo al razonamiento con `MAX_THINKING_TOKENS` y decide conscientemente tu `effortLevel`.
3. Activa las palancas de tokens: system prompt simple, búsqueda de herramientas, auto-compactación temprana, subagentes en Haiku.
4. Delega el ruido a subagentes; usa *agent teams* solo donde el paralelismo justifique el costo.
5. Monta el arnés: permisos en capas, `disableBypassPermissionsMode`, hooks defensivos, *env scrub* y, cuando estés listo, el sandbox.
6. Instala `jq` en cada máquina donde uses hooks.
7. Fija tu identidad de git y limpia la atribución con `attribution`.
8. Verifica con `/status` y `/doctor` antes de confiar en la configuración.

La configuración por defecto de Claude Code te deja empezar; esta te deja trabajar en serio. La diferencia está en dos cosas: gastar tokens donde aportan valor, y poner límites firmes donde el costo de un error es alto. Una vez montado el arnés, puedes darle autonomía al agente con la tranquilidad de que las operaciones realmente peligrosas siguen requiriendo tu mano.
