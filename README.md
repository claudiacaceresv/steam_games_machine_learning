# Análisis de Datos, API y Predicción de Precios de Juegos de Steam

![Precios por fechas](./image/steam.png)

# Índice

1. [Análisis de Datos, API y Predicción de Precios de Juegos de Steam](#an%C3%A1lisis-de-datos-y-predicci%C3%B3n-de-precios-de-juegos-de-steam)
2. [Requisitos](#requisitos)
3. [Modo de uso](#modo-de-uso)
4. [Notas](#notas)
5. [Contacto](#contacto)
6. [Tecnologías utilizadas](#tecnolog%C3%ADas-utilizadas)

Este repositorio contiene un conjunto de funciones y un modelo de regresión lineal para analizar datos y predecir precios de juegos de la plataforma Steam. Además, incluye la creación de una API REST utilizando FastAPI para acceder a los resultados del análisis y a las predicciones del modelo. El análisis de datos, la construcción de la API y la implementación del modelo se llevan a cabo en un entorno Render.

## Requisitos

Asegúrate de tener Python 3.x instalado y las siguientes bibliotecas requeridas:

- pandas
- scikit-learn
- fastapi
- difflib

Puedes instalar las dependencias con el siguiente comando:

```
pip install pandas scikit-learn fastapi difflib
```

## Modo de uso

1. Clona este repositorio en tu sistema local.

2. Asegúrate de tener los siguientes archivos de datos disponibles en la carpeta `data/` en el directorio del proyecto:

3. Ejecuta el archivo `main.py` para iniciar el servidor FastAPI:

```
python main.py
```

4. Una vez que el servidor esté en funcionamiento, puedes acceder a las siguientes rutas en tu navegador o cliente de API (por ejemplo, Postman):

- `/genero`: Obtiene los 5 géneros más ofrecidos para un año específico.
- `/juegos`: Obtiene la lista de juegos lanzados en un año específico.
- `/specs`: Obtiene las 5 especificaciones más comunes para un año específico.
- `/earlyacces`: Obtiene la cantidad de juegos con early access para un año específico.
- `/sentiment`: Obtiene el conteo de sentimientos de los juegos para un año específico.
- `/metascore`: Obtiene los 5 juegos con mejor metascore para un año específico.
- `/prediccion`: Realiza una predicción del precio de un juego según las características proporcionadas.

## Notas

La predicción utiliza un modelo de regresión lineal previamente entrenado para estimar el precio de un juego en base a ciertas características proporcionadas por el usuario. Específicamente, estas características incluyen:

1. `acceso_anticipado`: Un valor binario (0 o 1) que indica si el juego tiene acceso anticipado (early access) o no.

2. `metascore`: La calificación de metacritic del juego, que es un indicador de la calidad y recepción del juego por parte de la crítica especializada.

3. `año`: El año de lanzamiento del juego.

4. `categoria`: La categoría del juego, que se refiere a su género o tipo de juego al que pertenece.

5. `sentimiento`: Un valor que describe el sentimiento general asociado con el juego.

El modelo de regresión lineal utiliza estas características para predecir el precio del juego. Para realizar la predicción, primero, se realiza un procesamiento de los valores de entrada para que sean compatibles con el modelo de entrenamiento.

- Para `categoria`, y `sentimiento`, se verifica si los valores proporcionados por el usuario existen en los datos de entrenamiento.
  Si la categoria no existe, se buscan categorías cercanas utilizando la función `difflib.get_close_matches`.
  Si el sentimiento no existe, devuelve los sentimientos disponibles.

Una vez que se han procesado y validado las características proporcionadas por el usuario, se crean las instancias de datos correspondientes y se escala la columna `metascore` utilizando el `StandardScaler` que se aplicó durante el entrenamiento del modelo.

Finalmente, el modelo de regresión lineal realiza la predicción del precio del juego basado en estas características procesadas y devuelve el valor estimado como resultado. Es importante tener en cuenta que la precisión de la predicción puede depender de la calidad y representatividad de los datos de entrenamiento y de la correlación de las características proporcionadas con los precios reales de los juegos en el conjunto de entrenamiento.

# Análisis de datos y predicción de precios de juegos de Steam

Este repositorio contiene un conjunto de funciones y un modelo de regresión lineal para analizar datos y predecir precios de juegos de la plataforma Steam. El análisis de datos se realiza a través de una API REST creada con FastAPI.

## Contacto

### Claudia Caceres

[![LinkedIn](./image/linkedin_logo.png)](https://www.linkedin.com/in/claudiacaceresv/) [![WhatsApp](./image/whatsapp_logo.png)](https://api.whatsapp.com/send?phone=541124831343)

## Tecnologías utilizadas

Python | Pandas | Matplotlib | Seaborn | Scikit-Learn | Difflib | FastAPI | Render

---

_Nota: Este documento es una representación simplificada del proyecto de análisis de datos de juegos de Steam y tiene fines ilustrativos. Las conclusiones y recomendaciones presentadas son hipotéticas y no constituyen asesoramiento financiero real._
