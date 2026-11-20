---
title: "Cómo extraer y reordenar páginas de un PDF con Java y Apache PDFBox"
image: https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/extraer-paginas-pdf-java-pdfbox.webp
description: "Ejemplo reproducible con PDFBox 3 para extraer páginas en el orden solicitado, validar el rango y comprobar el archivo resultante."
author: Zen (PDF Fan)
date: 2026-11-21
label: Java
---

Supón que un informe de cuatro páginas trae la portada en la 1, los resultados en la 2, un borrador interno en la 3 y el método en la 4. Te piden un anexo que empiece con el método y termine con los resultados. La selección es `4,2`: el orden forma parte de la petición. Un programa que ordene esos números automáticamente entregaría dos páginas correctas en el orden equivocado.

La prueba de este artículo usa un informe ficticio. Sus páginas tienen títulos distintos para comprobar el contenido de la salida, y la página 4 está en formato Carta con una rotación de 90°. La página 2 está en A4 sin rotación.

## Crear un PDF nuevo en el orden solicitado

En [Apache PDFBox 3](https://pdfbox.apache.org/3.0/getting-started.html), `Loader` abre el original y `importPage` incorpora cada página a un documento nuevo. El lector cuenta las páginas desde 1; `getPage` empieza en 0. Por eso se resta uno al obtener la página. Los números del pie de página pueden ser distintos de los que muestra el visor, por ejemplo, si hay una portada sin numerar.

Guarda el siguiente ejemplo como `ExtraerPaginas.java`. Recibe tres argumentos: el PDF original, un nombre de archivo de salida que no exista y la lista de páginas separadas por comas.

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.pdmodel.PDDocument;

public class ExtraerPaginas {
    public static void main(String[] args) throws Exception {
        if (args.length != 3) {
            throw new IllegalArgumentException(
                "Uso: ExtraerPaginas original.pdf salida.pdf 4,2");
        }

        Path entrada = Path.of(args[0]);
        Path salida = Path.of(args[1]);
        if (Files.exists(salida)) {
            throw new IllegalArgumentException("La salida ya existe: " + salida);
        }

        int[] seleccion = Arrays.stream(args[2].split(",", -1))
            .map(String::trim)
            .mapToInt(Integer::parseInt)
            .toArray();

        try (PDDocument origen = Loader.loadPDF(entrada.toFile());
             PDDocument destino = new PDDocument()) {
            int total = origen.getNumberOfPages();
            for (int pagina : seleccion) {
                if (pagina < 1 || pagina > total) {
                    throw new IllegalArgumentException(
                        "Página fuera del rango 1-" + total + ": " + pagina);
                }
            }

            for (int pagina : seleccion) {
                destino.importPage(origen.getPage(pagina - 1));
            }
            destino.save(salida.toFile());
        }
    }
}
```

El código comprueba todos los índices antes de importar ninguna página. Conserva la secuencia que recibe y admite números repetidos si se quiere duplicar una página. `try` con recursos asegura que PDFBox cierre ambos documentos, incluso si el archivo no se puede leer o la selección es inválida. El comando está pensado para una ejecución local: la comprobación de que el destino no existe no sustituye un mecanismo de escritura exclusivo si varias ejecuciones comparten la misma ruta.

## Ejecutar y comprobar el anexo

Con JDK 11 o posterior, se puede ejecutar el archivo fuente directamente. En este ejemplo se usaron Java 22 y [PDFBox App 3.0.8](https://pdfbox.apache.org/download.html). Coloca el JAR, el archivo Java y tu PDF de prueba en el mismo directorio.

```sh
java -cp pdfbox-app-3.0.8.jar ExtraerPaginas.java informe.pdf anexos.pdf 4,2
```

El archivo de prueba resultante se volvió a abrir con PDFBox. Se leyó el texto de cada página con `PDFTextStripper` y se comprobó también su geometría:

| Página de salida | Página del original | Texto | Formato y rotación |
| --- | --- | --- | --- |
| 1 | 4 | METODO | Carta, 90° |
| 2 | 2 | RESULTADOS | A4, 0° |

También se verificaron dos casos de error: `4,0` no generó ningún PDF y un intento de usar `informe.pdf` como salida se rechazó. La suma SHA-256 del original siguió siendo la misma. Si repites la prueba, usa un nombre nuevo para la salida o guarda el resultado anterior en otro lugar.

Para una comprobación puntual con un archivo de prueba, también puedes [extraer páginas de un PDF en el navegador](https://pdf.fan/es/extraer-paginas-pdf/) y revisar las miniaturas antes de descargar. En cualquiera de los dos casos, abre la copia y comprueba el texto o la imagen de la primera y la última página. Contar páginas por sí solo no detecta una inversión en el orden.

## Límites del ejemplo

La muestra contiene páginas estáticas sin formularios ni anotaciones. En archivos reales, comprueba por separado marcadores, anotaciones, enlaces internos, formularios y recursos heredados de las páginas. Algunas referencias pueden llevar a páginas omitidas. Extraer páginas crea una copia que no conserva la validez de una firma digital del informe original. Si el documento requiere un proceso de firma o archivado, conserva el original y valida la copia con ese proceso antes de distribuirla.

*Nota de autoría: Zen trabaja en PDF Fan, la herramienta web citada. Se utilizó asistencia de IA en la preparación del borrador y el ejemplo de Java se ejecutó con archivos ficticios.*
