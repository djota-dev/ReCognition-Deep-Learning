# Traductor de Lenguaje de Señas en Tiempo Real

## Descripción
**reCognition** es un proyecto en desarrollo que utiliza redes neuronales y tecnologías de visión computacional para traducir gestos de manos a texto en tiempo real. Está basado en las bibliotecas MediaPipe y OpenCV, con el objetivo de crear una experiencia de traducción de lenguaje de señas mediante gestos capturados desde la cámara.

### Funcionalidades Actuales
- **Detección de gestos de la mano:** Utiliza un modelo de MediaPipe para detectar las manos y reconocer gestos comunes del lenguaje de señas.
- **Traducción a texto:** Los gestos detectados se traducen a texto correspondiente (ej., "Hola", "Gracias", "Sí", "No").
- **Subtítulos en tiempo real:** El texto traducido se muestra en la pantalla con un estilo profesional de subtítulos.
- **Cámara virtual:** El proyecto utiliza una cámara virtual para enviar la imagen procesada a aplicaciones de videollamadas, como Zoom o Skype.

### Estado del Proyecto
Este proyecto aún está **en desarrollo** y **no cumple con todas las funcionalidades** planeadas. Algunas de las limitaciones actuales son:
- **Reconocimiento limitado de gestos:** No todos los gestos de lenguaje de señas están soportados por el momento.
- **Precisión en la detección de gestos:** La precisión y la robustez de la detección aún pueden mejorar, especialmente en condiciones de iluminación subóptimas.
- **Red de gestos en evolución:** El sistema está en proceso de ampliarse para reconocer más gestos y mejorar el reconocimiento de los gestos complejos.

## Problemas que Resuelve

Este traductor tiene como objetivo abordar varios desafíos asociados con la barrera de comunicación entre personas que utilizan lenguaje de señas y aquellas que no lo hacen. Algunas de las principales problemáticas que propone resolver son:

- **Comunicación más accesible:** Facilitar la comunicación entre personas con dificultades auditivas o que utilizan el lenguaje de señas, permitiendo que los gestos sean entendidos por todos.
- **Interacción más fluida:** Mejorar las interacciones en videollamadas y plataformas de comunicación remota para que las personas que utilizan lenguaje de señas puedan comunicarse sin barreras.
- **Automatización de la traducción:** Automatizar el proceso de traducción de los gestos, eliminando la necesidad de traductores humanos en tiempo real.

## Explicación Técnica

### Tecnologías Usadas

El proyecto utiliza una combinación de herramientas avanzadas para lograr la detección y traducción en tiempo real:

- **MediaPipe:** Para la detección de manos y el seguimiento de los puntos clave en tiempo real. MediaPipe es una biblioteca de Google que ofrece soluciones preentrenadas para tareas como detección de manos, rostros, y poses.
- **PyVirtualCam:** Para crear una cámara virtual que permite transmitir la imagen procesada a plataformas de videollamadas.
- **OpenCV:** Para el procesamiento de imágenes y manipulación de los frames de la cámara.
- **PIL (Python Imaging Library):** Para agregar texto y subtítulos con estilo a las imágenes procesadas.
- **Redes Neuronales:** Si bien actualmente no se usa un modelo de red neuronal completamente entrenado, el proyecto está diseñado para integrar redes neuronales en el futuro, lo que permitiría mejorar la precisión de la detección y expandir el vocabulario de gestos.

### Cómo Funciona

1. **Captura de imágenes:** La cámara web captura un frame de video en tiempo real.
2. **Detección de manos:** MediaPipe procesa el frame para detectar las manos y obtener las posiciones de los puntos clave en las manos.
3. **Reconocimiento de gestos:** Los puntos clave de la mano se analizan para determinar el gesto que la persona está realizando. Actualmente, se detectan gestos básicos como "Hola", "Gracias", "Sí", entre otros.
4. **Traducción a texto:** El gesto reconocido se traduce a un texto predefinido usando un diccionario de gestos.
5. **Mostrar subtítulos:** El texto traducido se agrega como subtítulos en el frame procesado, con un fondo semitransparente y un estilo similar al de YouTube.
6. **Cámara virtual:** El frame con los subtítulos se envía a una cámara virtual para ser utilizado en aplicaciones de videollamadas.

### Limitaciones Actuales

- **Reconocimiento de gestos limitado:** Solo un número reducido de gestos está siendo reconocido actualmente. La base de datos de gestos debe expandirse y mejorarse para detectar más gestos.
- **Desafíos de precisión:** La detección de manos y la interpretación de gestos son sensibles a la iluminación y al ángulo de la cámara, lo que puede afectar la precisión.
- **No uso de redes neuronales para la clasificación:** Aunque el sistema es prometedor, la clasificación de gestos todavía no se realiza a través de redes neuronales profundas, lo que limitará su capacidad para generalizar a nuevos gestos en el futuro.


## Instalación

### 1. Crea un entorno virtual:
   
   Para asegurarte de que todas las dependencias estén aisladas y no interfieran con otros proyectos, es recomendable crear un entorno virtual. Para hacerlo, ejecuta:

   ```bash
   python -m venv venv
   ```

   Luego, activa el entorno virtual:

   - En Linux/Mac:

     ```bash
     source venv/bin/activate
     ```

   - En Windows:

     ```bash
     .env\Scripts\activate
     ```

### 2. Instala las dependencias:

   Una vez que tengas el entorno virtual activado, instala las dependencias necesarias con el siguiente comando:

   ```bash
   pip install -r requirements.txt
   ```

### 3. Ejecuta el proyecto:

   Después de instalar las dependencias, puedes ejecutar el proyecto con:

   ```bash
   python traductor.py
   ```

## Dependencias

- **mediapipe**: Biblioteca para la detección y el seguimiento de las manos.
- **opencv-python**: Biblioteca para el procesamiento de imágenes y video.
- **pyvirtualcam**: Permite crear una cámara virtual para videollamadas.
- **Pillow**: Biblioteca para agregar texto y dibujar en las imágenes.
- **numpy**: Para operaciones numéricas y manipulaciones de matrices.

## Contribución

Este proyecto está en constante desarrollo y se aceptan contribuciones. Si tienes alguna sugerencia o quieres ayudar a mejorar el proyecto, no dudes en hacer un pull request o abrir un issue.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

**Nota**: Este proyecto aún está en una etapa temprana de desarrollo. Algunas funcionalidades pueden no estar completamente implementadas o ser inexactas en ciertos casos. Se están realizando esfuerzos continuos para mejorar la precisión de la detección y expandir la base de gestos soportados.
