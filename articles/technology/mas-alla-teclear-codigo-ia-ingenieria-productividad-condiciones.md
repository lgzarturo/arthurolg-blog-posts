---
title: 'Más Allá de Teclear Código: Por Qué la IA Debe Mejorar Nuestro Trabajo y no Solo Multiplicarlo'
image: 'https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/mas-alla-teclear-codigo-ia-ingenieria-productividad-condiciones.webp'
description: 'La ingeniería de software son decisiones, no tecleo. Por qué abaratar el código con IA debe revivir sistemas legacy y mejorar el trabajo, no saturarlo.'
author: 'Arturo López'
date: '2026-11-07'
label: 'Tecnología'
---

Después de más de veinte años construyendo software en toda clase de trincheras, hay varios consensos ruidosos en el debate actual sobre la inteligencia artificial con los que discrepo profundamente.

El primero de ellos es la ilusión de que acabamos de descubrir el secreto de la velocidad. Aceptémoslo con humildad: las estimaciones de tiempo nunca han sido el punto fuerte del desarrollador. Pero los proyectos de software rara vez se retrasan porque a los ingenieros les falte destreza para mecanografiar caracteres en un editor. Lo habitual en dos décadas de profesión ha sido estrellarse contra la misma pared: requerimientos ambiguos que cambian a mitad de camino, negociaciones interminables sobre el alcance, dependencias no resueltas entre equipos y decisiones de negocio que se postergan durante semanas.

Confundir la velocidad de implementación con la velocidad real de entrega es un error de bulto que ya cometíamos mucho antes de que existieran los modelos de lenguaje.

Tampoco compro la narrativa derrotista que asegura que la inteligencia artificial nos ha degradado a simples operadores de control de calidad (*QA* de la máquina). Es verdad que hoy nos toca leer, comprender y auditar un volumen de código mucho mayor que hace tres años. Pero nuestro trabajo sigue siendo exactamente el mismo: entender problemas humanos complejos, modelar reglas de negocio y construir productos que funcionen bajo presión.

La ingeniería nunca se ha definido por la cantidad de líneas de código que dejamos registradas en un repositorio; se define por la calidad de las decisiones técnicas y arquitectónicas que tomamos para que un sistema sea sostenible en el tiempo.

## La vieja confusión entre teclear rápido y entregar a tiempo

Hace casi medio siglo, en su clásico ensayo [The Mythical Man-Month publicado en 1975](https://archive.org/details/mythicalmanmonth00broo), Frederick Brooks desarmó una falacia que la industria tecnológica parece empeñada en redescubrir cada diez años. Al analizar los calendarios reales de proyectos de software complejos, Brooks demostró que la codificación propiamente dicha —el acto físico de redactar sintaxis ejecutable— apenas representa **un sexto (16.7%) del tiempo total** de un proyecto. La planificación y el diseño consumen un tercio, mientras que las pruebas de componentes y la integración de sistemas absorben la mitad completa del esfuerzo.

Doce años más tarde, en su célebre artículo [No Silver Bullet: Essence and Accidents of Software Engineering en IEEE Computer](https://doi.org/10.1109/MC.1987.1663532), Brooks trazó una frontera epistemológica que sigue intacta: la diferencia entre la **dificultad accidental** (la sintaxis, los compiladores, la velocidad de escritura) y la **dificultad esencial** (conceptualizar entidades abstractas, delimitar contratos, gestionar estados inconsistentes y comunicarse con el usuario).

Reducir el tiempo de tecleo a cero mediante modelos generativos es un logro tecnológico impresionante, pero ataca casi exclusivamente la dificultad accidental. Si un equipo tarda seis semanas en acordar qué problema debe resolver una funcionalidad, si las dependencias entre servicios están acopladas, si te cambian la prioridad a mitad del camino, si tienes que resolver incidencias, debugging y si nadie sabe cómo validar los casos límite del dominio, generar trescientas líneas de código en diez segundos no acorta el plazo de entrega; únicamente adelanta el momento exacto en el que el sistema va a fallar.

> Generar sintaxis en segundos no resuelve la entrega de un proyecto; acelerar la escritura sin clarificar los requisitos solo consigue que choques contra el muro de la realidad a mayor velocidad.

De hecho, los datos empíricos más recientes respaldan esta advertencia con contundencia. En el informe [2024 State of DevOps Report elaborado por DORA y Google Cloud](https://dora.dev/research/2024/dora-report/), los investigadores encontraron un fenómeno revelador: a pesar de que el 76% de los profesionales encuestados ya utiliza asistentes de IA en sus labores diarias y un 75% reporta mejoras en su productividad individual, a nivel sistémico la adopción de estas herramientas se correlacionó con una **reducción estimada del 1.5% en el rendimiento de entrega (*throughput*)** y una **caída del 7.2% en la estabilidad del software**.

¿Por qué ocurre esta aparente contradicción? Porque el verdadero cuello de botella de la ingeniería no estaba en las manos del programador; estaba en su capacidad para validar, integrar y mantener la coherencia del sistema.

## La ingeniería son decisiones

Frente a este escenario, muchos profesionales sienten que han perdido el control de su oficio, convenciéndose de que su rol se ha reducido a ser inspectores cansados que limpian los errores de un modelo probabilístico. Me parece una lectura desenfocada.

Es innegable que la carga cognitiva que soportamos hoy es brutal. Tenemos más código que digerir, modelos que cambian cada trimestre, nuevas metodologías, herramientas agénticas y habilidades operativas que evolucionan a un ritmo implacable. Adaptarse a ese torbellino tiene un coste mental, energético y humano muy real que ninguna organización seria debería ignorar. Como han demostrado Nicole Forsgren y sus colaboradores al proponer el marco [The SPACE of Developer Productivity en ACM Queue](https://queue.acm.org/detail.cfm?id=3454124), la productividad del desarrollador es una ecuación multidimensional donde el bienestar, la satisfacción personal y la preservación del estado de flujo pesan tanto o más que cualquier métrica superficial de actividad.

Sin embargo, sentirse abrumado por el volumen no equivale a haber sido sustituido. Esto ya lo analicé al abordar la transición de [escribir código a hacer ingeniería de sistemas y reglas de negocio](https://www.arthurolg.com/article/programming_de-escribir-codigo-a-hacer-ingenieria-algoritmos-estructuras-de-datos-y-productos), teclear código siempre fue el medio, nunca el fin.

Cuando un arquitecto diseña un puente, no se mide su valía profesional por cuántos sacos de cemento carga sobre su espalda; se mide por su capacidad para calcular tensiones, elegir los materiales idóneos y garantizar que la estructura no colapse cuando el río crezca. Con el software sucede exactamente lo mismo: [el diferencial humano en el desarrollo con IA](https://www.arthurolg.com/article/technology_el-diferencial-humano-desarrollo-software-ia) reside en la intuición técnica, el criterio para decir «no» a una complejidad innecesaria y la responsabilidad de sostener el sistema en producción.

## La paradoja de Jevons y la resurrección del software olvidado

Hay otra perspectiva crucial que suele quedar enterrada bajo el ruido del marketing: durante décadas, escribir código artesanalmente fue una de las actividades que más tiempo consumía y, en muchos proyectos, **también una de las más profundamente aburridas**.

Pensemos con honestidad en el día a día previo a esta era: escribir por enésima vez convertidores de datos repetitivos, configurar esquemas de serialización idénticos a los del proyecto anterior, redactar controladores CRUD sin ninguna novedad conceptual o picar código pegamento (*glue code*) para conectar dos librerías incompatibles. Ese tedio mecánico no solo devoraba semanas de calendario, sino que generaba una parálisis económica devastadora en toda la industria.

Basta mirar la gigantesca montaña de sistemas heredados (*legacy*) que continúan operando en bancos, aerolíneas, hospitales y dependencias gubernamentales. Según el reporte sobre [The Cost of Poor Software Quality del Consortium for Information & Software Quality (CISQ)](https://www.it-cisq.org/the-cost-of-poor-quality-software-in-the-us-a-2022-report/), la deuda técnica acumulada en Estados Unidos supera los 1.5 billones de dólares, y el arrastre económico de sostener sistemas antiguos deficientes devora cientos de miles de millones al año. Las empresas gastan entre el 60% y el 80% de sus presupuestos de tecnología únicamente en «mantener las luces encendidas», porque intentar reescribir esos monolitos desde cero resultaba prohibitivo y ningún equipo quería asumir el calvario de descifrar código opaco sin pruebas.

La inteligencia artificial no ha sustituido la ingeniería; **ha reducido de forma drástica el coste marginal de implementar software**.

Y esa reducción económica abre una ventana extraordinaria que me parece infinitamente más prometedora que cualquier relato distópico sobre la sustitución laboral: **la posibilidad real de volver a construir, experimentar y renovar sistemas que antes no justificaban la inversión**.

Hoy podemos usar modelos avanzados para descifrar módulos antiguos, generar arneses de pruebas automáticas sobre código no documentado y refactorizar componentes zombis que llevaban una década acumulando polvo. En lugar de quemar meses de presupuesto en reescrituras suicidas, podemos aplicar una ingeniería iterativa y quirúrgica.

Pero aquí es donde acecha una trampa económica implacable: **la Paradoja de Jevons**.

En 1865, el economista William Stanley Jevons observó en su obra [The Coal Question](https://www.econlib.org/library/YPDBooks/Jevons/jvnCQ.html) que la introducción de máquinas de vapor más eficientes no redujo el consumo global de carbón en Inglaterra; al abaratar el coste por unidad de energía producida, multiplicó la demanda total del mineral en fábricas, ferrocarriles y barcos.

En la ingeniería de software actual estamos presenciando exactamente el mismo fenómeno rebote. Como generar código ahora es barato y accesible, muchas organizaciones no aprovechan esa ventaja para sanear su deuda técnica ni para dar un respiro a sus ingenieros. Caen en el error miope de exigir **producir indefinidamente más funcionalidades, con las mismas personas y en menos tiempo**.

Si generar código se vuelve diez veces más barato pero la cultura corporativa exige cien veces más volumen por trimestre, terminamos inundando los repositorios con código duplicado y rotación acelerada de parches temporales, elevando la fatiga cognitiva a niveles intolerables.

## Si automatizamos lo aburrido solo para hacer más trabajo, fallamos

No necesitamos atrincherarnos en la defensa romántica de la programación manual como si mecanografiar instrucciones fuera la esencia de nuestra identidad profesional. Pasar horas escribiendo código repetitivo nunca fue lo que nos hizo ingenieros; lo que nos hace ingenieros es el pensamiento abstracto, el diseño de soluciones y la capacidad de resolver problemas reales.

Tampoco tiene sentido convertir cada nueva herramienta en una amenaza existencial o en un motivo de pánico.

El verdadero desafío de nuestra generación es político, ético y metodológico: necesitamos adaptarnos a las nuevas herramientas, conservar un criterio técnico innegociable y, sobre todo, **exigir que la productividad tecnológica se traduzca en mejores condiciones de trabajo**.

Abaratar la implementación mecánica debe servir para reducir las horas extras absurdas, para dedicar tiempo de calidad a diseñar arquitecturas limpias, para reflexionar sobre los casos límite de seguridad y para devolverle a nuestra profesión el placer artesanal de crear sin el agobio de plazos asfixiantes.

Porque si automatizamos las partes más aburridas y repetitivas de nuestro oficio únicamente para terminar asumiendo el triple de carga mental y trabajando el doble de horas bajo la tiranía del volumen infinito, entonces no habremos avanzado un solo milímetro: habremos fracasado como industria.

## Conclusión

El futuro del desarrollo de software no le pertenece a quienes se resisten con nostalgia a soltar el teclado, pero tampoco a quienes aceptan dócilmente convertirse en fábricas de código inflado sin criterio de arquitectura ni respeto por su propio bienestar.

El futuro le pertenece a quienes utilizan la inteligencia artificial como una palanca económica para rescatar lo que estaba abandonado, diseñar sistemas robustos y liberar tiempo para lo verdaderamente importante: pensar, experimentar y vivir con dignidad.

Cuando mires las herramientas que hoy tienes en tu editor, hazte una pregunta honesta: ¿las estás utilizando para construir software más sólido y trabajar con mayor serenidad, o simplemente estás acelerando en la rueda de un molino que nunca deja de girar?

Si quieres comentar o compartir tu experiencia, escríbeme en [X (@algforge)](https://x.com/algforge) o abre un issue en el [repositorio](https://github.com/lgzarturo/arthurolg-blog-posts/issues). Una estrella en [GitHub](https://github.com/lgzarturo) también ayuda.

## Referencias

- [The Mythical Man-Month: Essays on Software Engineering, Frederick P. Brooks Jr. (Addison-Wesley)](https://archive.org/details/mythicalmanmonth00broo)
- [No Silver Bullet: Essence and Accidents of Software Engineering, Frederick P. Brooks Jr. (IEEE Computer)](https://doi.org/10.1109/MC.1987.1663532)
- [The Coal Question; An Inquiry Concerning the Progress of the Nation, William Stanley Jevons (Macmillan)](https://www.econlib.org/library/YPDBooks/Jevons/jvnCQ.html)
- [2024 State of DevOps Report, DORA & Google Cloud](https://dora.dev/research/2024/dora-report/)
- [The SPACE of Developer Productivity, Nicole Forsgren, Margaret-Anne Storey et al. (ACM Queue)](https://queue.acm.org/detail.cfm?id=3454124)
