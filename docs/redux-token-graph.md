# redux-token-graph

Guía de instalación, configuración y uso de **`code-review-graph`** y
**`token-savior-recall`** como herramientas globales con `uv`, compatibles con
los agentes Claude Code, Codex, OpenCode, Gemini CLI y AGY.

> **Fecha de la instalación:** 2026-06-28
> **Plataforma:** Windows 11 Pro (PowerShell 7+)
> **Gestor de paquetes:** `uv` 0.10.10
> **Usuario:** `R2D2`

---

## 1. Qué son estas herramientas

### `code-review-graph` (`crg`)

Grafo de conocimiento persistente e incremental para revisiones de código.
Indexa el repositorio con `tree-sitter`, calcula comunidades, flujos y
embeddings, y expone un servidor **MCP** para que los agentes de IA naveguen
símbolos sin tener que abrir archivos completos.

- **Beneficio clave:** reduce el coste en tokens al evitar releer archivos.
- **Ejecutables instalados:** `code-review-graph`, `crg-daemon`.

### `token-savior-recall` (`ts`)

CLI + servidor MCP que mantiene memoria persistente del proyecto y permite
navegar símbolos, dependencias y *callers* mediante un daemon en segundo plano.

- **Beneficio clave:** "Token Savior" — entrega contexto quirúrgico al agente
  (sólo el símbolo o función pedidos) en vez de archivos enteros.
- **Ejecutables instalados:** `token-savior`, `token-savior-bench`,
  `token-savior-dashboard`, `ts`.

---

## 2. Proceso de instalación realizado

Ambas herramientas se instalaron como **tools globales** de `uv` para que cada
una viva en su propio entorno aislado y permanezcan disponibles en el `PATH` de
usuario, independientemente del proyecto activo.

### 2.1. Comandos ejecutados

```powershell
# Verificación del entorno
uv --version          # uv 0.10.10
uv tool list          # estado inicial

# Instalación de code-review-graph
uv tool install code-review-graph

# Instalación de token-savior-recall con extras necesarios
uv tool install --reinstall "token-savior-recall[memory-vector]" --with mcp
```

### 2.2. Por qué `[memory-vector]` y `--with mcp`

El primer intento de instalación sin extras produjo estos avisos al ejecutar
`token-savior`:

```
[token-savior:memory] sqlite-vec not installed; vector search disabled.
[token-savior:memory] fastembed not installed; embedding disabled.
ModuleNotFoundError: No module named 'mcp'
```

Para resolverlos:

| Extra / dependencia | Habilita |
| ------------------- | -------- |
| `[memory-vector]`   | `sqlite-vec` (búsqueda vectorial) y `fastembed` (embeddings locales). |
| `--with mcp`        | Paquete `mcp` para el servidor MCP por *stdio*. |

### 2.3. Resultado final

```text
uv tool list
─────────────────────────────────────────────────────
code-review-graph v2.3.6
  - code-review-graph
  - crg-daemon
token-savior-recall v4.4.1
  - token-savior
  - token-savior-bench
  - token-savior-dashboard
  - ts
```

Ubicaciones físicas:

- **Entornos virtuales aislados:**
  `C:\Users\R2D2\AppData\Roaming\uv\tools\<tool-name>\`
- **Ejecutables en el PATH:**
  `C:\Users\R2D2\.local\bin\*.exe`

El directorio `C:\Users\R2D2\.local\bin` ya está en el **PATH de usuario**
(persistente, no de sesión), por lo que **cualquier agente** que herede el
entorno del usuario (Claude Code, Codex, OpenCode, Gemini CLI, AGY) los detecta
automáticamente.

---

## 3. Configuración por agente

Cada agente necesita registrar los servidores MCP de estas herramientas. Las
propias CLIs ofrecen subcomandos `install` / `init` que escriben la
configuración en los archivos nativos de cada plataforma.

### 3.1. `code-review-graph install`

Soporta de forma nativa varias plataformas con el flag `--platform`:

```
codex | claude | claude-code | cursor | windsurf | zed | continue |
opencode | antigravity | gemini-cli | qwen | kiro | qoder | copilot |
copilot-cli | all
```

Por defecto detecta automáticamente los agentes presentes y registra el MCP en
todos. Opciones útiles:

| Flag | Efecto |
| ---- | ------ |
| `--platform all` | Registra el MCP en todos los agentes detectados. |
| `--platform claude-code` | Sólo Claude Code. |
| `--platform codex` | Sólo Codex. |
| `--platform opencode` | Sólo OpenCode. |
| `--platform gemini-cli` | Sólo Gemini CLI. |
| `--no-skills` | No genera *skill files* nativos por plataforma. |
| `--no-hooks` | No instala hooks. |
| `--no-instructions` | No inyecta instrucciones en `CLAUDE.md` / `AGENTS.md`. |
| `--dry-run` | Vista previa sin escribir nada. |
| `-y` / `--yes` | Auto-confirma sin prompt interactivo. |

**Recomendación inicial:**

```powershell
# Desde la raíz del proyecto que quieres indexar:
code-review-graph install --platform all -y
```

### 3.2. `ts init` (Token Savior)

Soporta agentes: `claude`, `cursor`, `gemini`, `codex`. Para OpenCode/AGY se
configura manualmente como MCP server externo (ver §3.3).

```powershell
# Configuración global (por defecto, escribe en ~/)
ts init --agent claude -y
ts init --agent codex  -y
ts init --agent gemini -y

# Configuración local del proyecto (por defecto escribe a global)
ts init --agent claude --local -y
```

Opciones:

| Flag | Efecto |
| ---- | ------ |
| `--agent {claude,cursor,gemini,codex}` | Agente destino (auto-detect si se omite). |
| `--global` / `-g` | Escribe a settings globales (default). |
| `--local` / `-l` | Escribe a settings locales del proyecto. |
| `--yes` / `-y` | Sin prompt. |
| `--dry-run` | Sólo muestra el diff. |

### 3.3. Registro manual (OpenCode y AGY)

Si tu agente no aparece en los flags anteriores, registra los MCP servers a
mano. Comandos de invocación:

| Servidor MCP | Comando |
| ------------ | ------- |
| `code-review-graph` | `code-review-graph mcp` |
| `token-savior`      | `token-savior` (lee `stdin`, profile vía `TOKEN_SAVIOR_PROFILE`) |

**OpenCode** (`~/.config/opencode/config.json` o equivalente):

```json
{
  "mcpServers": {
    "code-review-graph": {
      "command": "code-review-graph",
      "args": ["mcp"]
    },
    "token-savior": {
      "command": "token-savior",
      "env": { "TOKEN_SAVIOR_PROFILE": "lean" }
    }
  }
}
```

**AGY** (`~/.agy/config.yaml` o el archivo de MCP del agente):

```yaml
mcp_servers:
  code-review-graph:
    command: code-review-graph
    args: [mcp]
  token-savior:
    command: token-savior
    env:
      TOKEN_SAVIOR_PROFILE: lean
```

> Ajusta el campo `command` al ejecutable `.exe` con ruta absoluta si tu agente
> no hereda el `PATH` del usuario:
> `C:\Users\R2D2\.local\bin\code-review-graph.exe` y
> `C:\Users\R2D2\.local\bin\token-savior.exe`.

### 3.4. Variable `TOKEN_SAVIOR_PROFILE`

Controla cuántas tools expone el MCP de `token-savior`:

| Valor   | Tools expuestas | Cuándo usar |
| ------- | --------------- | ----------- |
| `full`  | 69 (default)    | Sesiones largas, exploración intensa. |
| `lean`  | ~40             | Uso diario equilibrado **(recomendado)**. |
| `ultra` | ~15             | Proyectos pequeños, agentes con ventana limitada. |

Configuración global persistente en PowerShell:

```powershell
[Environment]::SetEnvironmentVariable('TOKEN_SAVIOR_PROFILE', 'lean', 'User')
```

---

## 4. Uso típico en proyectos

### 4.1. Inicializar `code-review-graph` en un proyecto

```powershell
# 1. Posicionarse en la raíz del repo
Set-Location C:\ruta\al\proyecto

# 2. Construir el grafo inicial (parsea todo el código)
code-review-graph build

# 3. Post-procesar (calcula flujos, comunidades, índice FTS)
code-review-graph postprocess

# 4. (Opcional) embeddings vectoriales para búsqueda semántica
code-review-graph embed

# 5. Modo watch: actualiza el grafo en cada cambio
code-review-graph watch
```

Subcomandos clave:

| Comando | Acción |
| ------- | ------ |
| `build` | Reconstruye el grafo entero. |
| `update` | Incremental, sólo archivos cambiados. |
| `status` | Estadísticas del grafo (nodos, aristas, migrations). |
| `visualize` | Genera visualización del grafo. |
| `wiki` | Documentación auto-generada del repo. |
| `serve` / `mcp` | Servidor HTTP / MCP. |
| `daemon` | Daemon en segundo plano. |
| `eval` | Métricas de calidad del grafo. |
| `detect-changes` | Detecta cambios desde el último build. |

### 4.2. Inicializar `token-savior` en un proyecto

```powershell
# 1. Listar proyectos registrados
ts projects

# 2. Registrar y seleccionar el proyecto activo
ts use C:\ruta\al\proyecto

# 3. Arrancar el daemon (acelera consultas posteriores)
ts daemon start
```

Subcomandos clave:

| Comando | Acción |
| ------- | ------ |
| `get <símbolo>` | Devuelve el código fuente de una función / clase. |
| `search <regex>` | Búsqueda regex sobre el código. |
| `ctx <símbolo>` | Contexto completo: fuente + dependencias + callers. |
| `structure <archivo>` | Estructura (clases, funciones, imports) de un archivo. |
| `files` | Lista de archivos del proyecto. |
| `find-dead-code` | Funciones nunca llamadas. |
| `breaking <git-ref>` | Breaking changes frente a una referencia git. |
| `git-status` | Estado git con estructura. |
| `replace <símbolo>` | Reemplaza la fuente de un símbolo desde stdin. |
| `move <símbolo> <archivo>` | Mueve un símbolo a otro archivo. |
| `add-field <modelo>` | Añade un campo a un modelo. |

Flags globales útiles:

```powershell
ts --text get MyClass.method     # salida raw (no JSON)
ts --verbose ctx some_function   # logs del motor
ts --no-daemon search "TODO"     # fuerza fork mode sin daemon
```

### 4.3. Flujo recomendado para un proyecto nuevo

```powershell
# Posicionarse en el proyecto
Set-Location C:\ruta\al\proyecto

# 1. Registrar MCPs en los agentes presentes
code-review-graph install --platform all -y
ts init --agent claude -y     # ajustar al agente que uses

# 2. Construir grafo y registrar proyecto
code-review-graph build
code-review-graph postprocess
ts use $PWD
ts daemon start

# 3. Abrir el agente — ya tiene contexto y memoria
claude            # o: codex / opencode / gemini / agy
```

---

## 5. Referencia rápida por agente

| Agente | Cómo registrar `code-review-graph` | Cómo registrar `token-savior` | Archivo afectado |
| ------ | ---------------------------------- | ----------------------------- | ---------------- |
| **Claude Code** | `code-review-graph install --platform claude-code -y` | `ts init --agent claude -y` | `~/.claude/settings.json`, `CLAUDE.md` |
| **Codex** | `code-review-graph install --platform codex -y` | `ts init --agent codex -y` | `~/.codex/config.toml`, `AGENTS.md` |
| **OpenCode** | `code-review-graph install --platform opencode -y` | Manual (ver §3.3) | `~/.config/opencode/config.json` |
| **Gemini CLI** | `code-review-graph install --platform gemini-cli -y` | `ts init --agent gemini -y` | `~/.gemini/settings.json` |
| **AGY** | Manual (ver §3.3) — usar `code-review-graph mcp` | Manual (ver §3.3) | `~/.agy/config.yaml` |

---

## 6. Comandos de mantenimiento

```powershell
# Listar tools globales instaladas
uv tool list

# Actualizar a la última versión
uv tool upgrade code-review-graph
uv tool upgrade token-savior-recall

# Reinstalar (limpio) con extras
uv tool install --reinstall "token-savior-recall[memory-vector]" --with mcp

# Desinstalar
uv tool uninstall code-review-graph
uv tool uninstall token-savior-recall

# Inspeccionar el directorio de tools
uv tool dir
# => C:\Users\R2D2\AppData\Roaming\uv\tools
```

---

## 7. Troubleshooting

| Síntoma | Causa probable | Solución |
| ------- | -------------- | -------- |
| `ModuleNotFoundError: No module named 'mcp'` al lanzar `token-savior` | Instalado sin el extra MCP. | `uv tool install --reinstall "token-savior-recall[memory-vector]" --with mcp` |
| `sqlite-vec not installed; vector search disabled` | Falta el extra `[memory-vector]`. | Reinstalar con `[memory-vector]`. |
| `token-savior` "se cuelga" en la terminal | Es el comportamiento correcto: espera *stdin* del cliente MCP. | Lánzalo a través del agente, no a mano. |
| El agente no encuentra `code-review-graph` ni `token-savior` | El proceso del agente no hereda el PATH de usuario. | Usar rutas absolutas en la config MCP: `C:\Users\R2D2\.local\bin\<exe>`. |
| `code-review-graph status` muestra muchas migraciones | Primera ejecución sobre una BD nueva. | Normal: corre migraciones v1 → v9 una sola vez. |
| El manifest de tools es demasiado grande | `TOKEN_SAVIOR_PROFILE=full` carga 69 tools. | `setx TOKEN_SAVIOR_PROFILE lean` (o `ultra`). |
| Búsquedas semánticas vacías | No se ejecutaron embeddings. | `code-review-graph embed` y reiniciar el daemon. |

---

## 8. Anexo — instalación reproducible (one-liner)

```powershell
# Instalación completa desde cero
uv tool install code-review-graph
uv tool install --reinstall "token-savior-recall[memory-vector]" --with mcp

# Verificación
uv tool list
(Get-Command code-review-graph).Source
(Get-Command ts).Source
[Environment]::SetEnvironmentVariable('TOKEN_SAVIOR_PROFILE', 'lean', 'User')
```

---

**Fin del documento.** Mantén este archivo cerca de tu raíz de configuración
(`~/`) o en la documentación interna del equipo. Cualquier proyecto nuevo sólo
necesita los pasos de §4.3 para quedar listo.
