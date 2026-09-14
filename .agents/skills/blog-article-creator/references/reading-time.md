# Sistema de Control y Presupuesto de Tiempo de Lectura

Este documento detalla el estándar y la metodología para calcular, presupuestar y auditar la extensión de los artículos en función del **tiempo de lectura deseado por el usuario**.

---

## 1. Regla de Oro: Duración Explícita o Dinámica

* Si el usuario indica una duración (ej. *"artículo de 5 minutos"*, *"post extenso de 15 minutos"*), esa duración es el objetivo principal.
* Si no la indica, no asumir 10 minutos. Estimar la duración a partir de la profundidad, audiencia, número de conceptos, ejemplos, trade-offs, código y diagramas previstos.
* Proponer la duración calculada en la Ficha de Definición y detenerse para aprobación. La duración solo queda fijada cuando el usuario la acepta.
* Usar 3–5 minutos para una explicación breve, 6–9 para una guía normal, 10–15 para un análisis profundo y 16–20 para un tutorial o investigación extensa. No alargar con relleno.

---

## 2. Velocidad de Lectura Base (WPM)

Para prosa en español reflexiva y técnica (con términos de arquitectura, bloques de código e investigación), la velocidad base estimada es de:

$$\text{Velocidad Base} = 200 \text{ palabras por minuto (WPM)}$$

Esta velocidad garantiza que el tiempo asignado permita una lectura pausada y comprensiva del material técnico y de las reflexiones filosóficas.

---

## 3. Tabla de Presupuesto de Palabras por Tiempo de Lectura

$$\text{palabras\_prosa\_objetivo} = \text{minutos\_lectura} \times 200$$

| Tiempo Deseado | Objetivo Prosa | Rango Aceptable (Prosa) | Secciones (`##`) Recomendadas |
| :--- | :--- | :--- | :--- |
| **3 minutos** | ~600 palabras | 500 – 700 palabras | 2 – 3 secciones |
| **5 minutos** | ~1,000 palabras | 800 – 1,200 palabras | 3 – 4 secciones |
| **7 minutos** | ~1,400 palabras | 1,100 – 1,600 palabras | 4 – 5 secciones |
| **10 minutos** | **~2,000 palabras** | **1,600 – 2,400 palabras** | **5 – 6 secciones** |
| **15 minutos** | ~3,000 palabras | 2,400 – 3,500 palabras | 6 – 8 secciones |
| **20 minutos** | ~4,000 palabras | 3,200 – 4,500 palabras | 8 – 10 secciones |

---

## 4. Ajuste por Bloques de Código e Imágenes

Los bloques de código y las imágenes enriquecen el tiempo de lectura sin sumar recuento de palabras puras de prosa. Se aplican las siguientes equivalencias:

* **Bloque de código (moderado, 5-15 líneas):** $+0.33 \text{ min}$ (equivalente a ~65 palabras de prosa).
* **Bloque de código extenso (>15 líneas):** $+0.60 \text{ min}$ (equivalente a ~120 palabras de prosa).
* **Imagen / Diagrama ASCII:** $+0.20 \text{ min}$ (equivalente a ~40 palabras de prosa).
* **Diagrama Mermaid:** $+0.20 \text{ min}$ (equivalente a ~40 palabras de prosa).

### Fórmula del Tiempo Estimado Real:
$$\text{Tiempo Real (min)} = \left(\frac{\text{palabras\_prosa}}{200}\right) + (\text{bloques\_código} \times 0.33) + ((\text{imágenes} + \text{diagramas Mermaid}) \times 0.20)$$

---

## 5. Distribución de Palabras por Bloque

Para evitar desequilibrios donde la introducción sea enorme y el cuerpo quede raquítico, aplica el siguiente reparto porcentual:

```
┌──────────────────────────────────────────────────────────────┐
│             PRESUPUESTO DINÁMICO (N × 200 PALABRAS)          │
├──────────────────────────────┬───────────────┬───────────────┤
│ Bloque                       │ % del Total   │ Palabras       │
├──────────────────────────────┼───────────────┼───────────────┤
│ Gancho / Introducción        │ ~10%          │ N × 20         │
│ Cuerpo (según complejidad)   │ ~78%          │ N × 156        │
│ Reflexión final & CTA        │ ~12%          │ N × 24         │
└──────────────────────────────┴───────────────┴───────────────┘
```

---

## 6. Principio de Profundidad Técnica vs. "Paja" (Relleno)

> **Regla de Calidad de Arturo López:** Si al redactar falta volumen para alcanzar el tiempo objetivo, **NUNCA utilices paja, adjetivos huecos ni repeticiones**.

### Cómo aumentar la longitud de forma valiosa:
1. Agrega una **anécdota real** o un caso de uso concreto de producción.
2. Explica los **compromisos (*trade-offs*)** o las alternativas descartadas.
3. Incluye un **bloque de código o diagrama ASCII** explicando el problema interno.
4. Desarrolla los **casos bordes (*edge cases*)** y las lecciones aprendidas.

---

## 7. Ejecución de la Validación

Tras generar o modificar el artículo, audita el tiempo real con el script oficial del repositorio:

```bash
python3 .agents/skills/blog-article-creator/scripts/validate_article.py --file "<ruta-al-articulo.md>" --reading-time <minutos-o-auto> --ignore-date-today
```
