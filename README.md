

# SprintSense

En entornos donde se llevan a cabo reuniones de equipo, clases o actividades colaborativas, es común depender de interfaces físicas (teclados, mouse, pantallas táctiles) para interactuar con contenidos digitales. Sin embargo, existen escenarios donde el uso de estas interfaces no es práctico, ya sea por razones de accesibilidad, higiene o conveniencia.

Este sistema se concibió pensando en su aplicación dentro de **metodologías ágiles**, donde la **rapidez**, la **adaptabilidad** y la **colaboración** son fundamentales. Al eliminar la necesidad de contacto físico con los dispositivos, facilitamos interacciones más fluidas y dinámicas en reuniones de equipo, sesiones de _brainstorming_ o presentaciones interactivas. La capacidad de controlar la interfaz con **gestos y comandos de voz** permite a los usuarios interactuar con el contenido de manera más natural y eficiente, reduciendo fricciones y optimizando el tiempo, elementos clave para mantener la agilidad en cualquier proyecto.

Este proyecto busca diseñar un sistema que permita controlar funciones básicas como cambiar de vista, dibujar, mover objetos o ejecutar acciones mediante **interacción visual sin contacto**, utilizando una cámara y comandos de voz.

#### Descripción General

El sistema está compuesto por cuatro módulos principales que trabajan de forma concurrente:

1.  **Captura de video** desde la webcam, gestionada por el módulo principal (`main.py`).
    
2.  **Detección de personas** con YOLOv8 para activar o desactivar la interfaz.
    
3.  **Reconocimiento de gestos** con MediaPipe para cambiar de modo, seleccionar objetos, dibujar.
    
4.  **Reconocimiento de voz** para escribir de forma alternativa sin necesidad de contacto.

----------

### Enlace al video

https://www.youtube.com/watch?v=NSueTlPPVJg

### Explicación técnica del funcionamiento

-   `main.py` administra la captura de video y coordina los módulos.
    
-   `detection.py` emplea YOLOv8 para identificar personas en la escena.
    
-   `gesture_control.py` gestiona el cambio de escenas y acciones visuales mediante gestos.
    
-   `voice_control.py` ejecuta reconocimiento de voz cada ciertos segundos y realiza retroalimentación hablada.
    
### Evidencia de funcionamiento

Crear nueva tarea y dictado por voz:
![GIF](informe/gifs/nueva.gif)

Marcar tarea como completada y eliminar:
![GIF](informe/gifs/completada.gif)

Modo dibujo:
![GIF](informe/gifs/dibujo.gif)

Editar tarea:
![GIF](informe/gifs/editar.gif)

Inactividad/Reactivar al detectar persona:
![GIF](informe/gifs/inactiva.gif)

