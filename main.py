from difflib import get_close_matches
import pickle
from fastapi import FastAPI
import pandas as pd
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/readme", response_class=HTMLResponse)
def get_readme():
    with open("README.md", "r", encoding="utf-8") as readme_file:
        readme_content = readme_file.read()
    return readme_content

@app.get("/genero")
def genero(Año: str):
    # Transformar dato
    Año = int(Año)

    # Cargar la base de datos
    df_genero = pd.read_parquet('data/generos.parquet')

    # Filtrar el DataFrame por el año proporcionado
    df_año = df_genero[df_genero['año'] == Año]

    # Error: no hay registros para ese año
    if df_año.empty:
        error_msg = f"No hay registros para el año {Año}"
        return {'error': error_msg}

    # Ordenar el DataFrame por la cantidad de repeticiones en orden descendente
    df_año = df_año.sort_values(by='total', ascending=False)
    
    # Tomar los 5 géneros más ofrecidos
    top_generos = df_año.head(5)['genero'].tolist()
    
    del df_genero

    return {f'Top 5 generos mas ofrecidos en el año {Año}': top_generos}

@app.get("/juegos")
def juegos(Año: str):
    # Transformar dato
    Año = int(Año)

    # Cargar la base de datos
    df_titulos = pd.read_parquet('data/titulos.parquet')

    # Filtrar el DataFrame por el año proporcionado
    df_año = df_titulos[df_titulos['año'] == Año]

    # Error: no hay registros para ese año
    if df_año.empty:
        error_msg = f"No hay registros para el año {Año}"
        return {'error': error_msg}
    
    # Obtener la lista de títulos de juegos lanzados en ese año
    lista_juegos = df_año['titulo'].tolist()
    
    del df_titulos

    return {f'Juegos lanzados en el año {Año}': lista_juegos}

@app.get("/specs")
def specs(Año: str):
    # Transformar dato
    Año = int(Año)

    # Cargar la base de datos
    df_especificaciones = pd.read_parquet('data/especificaciones.parquet')

    # Filtrar el DataFrame por el año proporcionado
    df_año = df_especificaciones[df_especificaciones['año'] == Año]

    # Error: no hay registros para ese año
    if df_año.empty:
        error_msg = f"No hay registros para el año {Año}"
        return {'error': error_msg}

    # Obtener los 5 specs más repetidos
    top_specs = df_año['especificacion'].value_counts().head(5).index.tolist()

    del df_especificaciones

    return {f'Top 5 specs más repetidos en el año {Año}': top_specs}


def earlyacces(Año: str):
    # Transformar dato
    Año = int(Año)

    # Cargar la base de datos
    df_acceso_anticipado = pd.read_parquet('data/acceso_anticipado.parquet')

    # Filtrar el DataFrame por el año proporcionado y con acceso anticipado
    juegos_earlyacces = df_acceso_anticipado[(df_acceso_anticipado['año'] == Año) & (df_acceso_anticipado['acceso_anticipado'] == 'Si')]

    # Contar la cantidad de juegos lanzados con acceso anticipado en el año dado
    cantidad_juegos_earlyacces = juegos_earlyacces.shape[0]

    del df_acceso_anticipado

    return {f'Cantidad de juegos lanzados con acceso anticipado en el año {Año}': cantidad_juegos_earlyacces}

@app.get("/sentiment")
def sentiment(Año: str):
# Transformar dato
    Año = int(Año)

    # Cargar la base de datos
    df_sentimiento = pd.read_parquet('data/sentimiento.parquet')

    # Filtrar el DataFrame por el año proporcionado
    df_año = df_sentimiento[df_sentimiento['año'] == Año]

    # Error: no hay registros para ese año
    if df_año.empty:
        error_msg = f"No hay registros para el año {Año}"
        return {'error': error_msg}

    # Obtener los valores únicos de sentimiento y sus respectivos totales para el año dado
    sentimiento_totals = df_año.groupby('sentimiento')['total'].sum().to_dict()

    del df_sentimiento

    return {f"Analisis de sentimiento del año {Año}": sentimiento_totals}

@app.get("/metascore")
def metascore(Año: str):
    # Transformar dato
    Año = int(Año)

    # Cargar la base de datos
    df_metascore = pd.read_parquet('data/metascore.parquet')

    # Filtrar el DataFrame por el año proporcionado
    df_año = df_metascore[df_metascore['año'] == Año]

    # Error: no hay registros para ese año
    if df_año.empty:
        error_msg = f"No hay registros para el año {Año}"
        return {'error': error_msg}

    # Ordenar el DataFrame por el metascore en orden descendente y tomar los 5 juegos con mayor metascore
    top_juegos_metascore = df_año.sort_values(by='metascore', ascending=False).head(5)

   # Crear el diccionario de respuesta
    response_dict = {
        f"Analisis de metascore del año {Año}": {
            row['titulo']: row['metascore'] for _, row in top_juegos_metascore.iterrows()
        }
    }

    del df_metascore

    return response_dict

@app.get("/prediccion")    
def prediccion(acceso_anticipado:int, metascore:int, año:int, categoria:str, sentimiento:str):
    
    # Carga el dataset para las categorias
    df_funciones = pd.read_parquet('data/steam_games.parquet')

    # Carga el dataset para las categorias
    df_modelo_categoria = pd.read_parquet('data/modelo_categoria.parquet')

    # Carga el dataset para las sentimiento
    df_modelo_sentimiento = pd.read_parquet('data/modelo_sentimiento.parquet')

    # Cargar el modelo entrenado desde el archivo pickle
    with open('data/modelo_regresion_precio.pkl', 'rb') as file:
        modelo_regresion = pickle.load(file)
        
    # Cargar el StandardScaler desde el archivo pickle
    with open('data/modelo_scaler_metascore.pkl', 'rb') as file:
        scaler_metascore = pickle.load(file)
        
    # Cargar el valor RMSE desde el archivo pickle
    with open('data/modelo_rmse.pkl', 'rb') as file:
        rmse = pickle.load(file)
    
    # Categoría
    categoria = categoria.lower()
    fila_categoria = df_modelo_categoria[df_modelo_categoria['categoria'].str.lower() == categoria]
    if not fila_categoria.empty:
        numero_categoria = fila_categoria['categoria_n'].iloc[0]
    else:
        # Si la categoría no se encuentra, buscar categorías similares (máximo 10)
        categorias_disponibles = df_modelo_categoria['categoria'].str.lower().tolist()
        categorias_similares = get_close_matches(categoria, categorias_disponibles, n=10)
        if categorias_similares:
            return {"Error": f"Categoría '{categoria}' no encontrada. Categorías similares: {categorias_similares}"}
        else:
            # Usar melt para convertir las columnas 'genero' y 'especificacion' en filas bajo la columna 'categoria'
            df_melted = df_funciones.melt(value_vars=['genero', 'especificacion'], value_name='categoria')

            # Contar cuántas veces se repite cada valor en la columna 'categoria' y obtener las 5 categorías más repetidas
            top_5_categorias_valores = df_melted['categoria'].value_counts().nlargest(5).index.tolist()
            return {"Error": f"Categoría '{categoria}' no encontrada. Categorías similares no encontradas. Categorías más frecuentes: {top_5_categorias_valores}"}

    # Setimiento
    sentimiento = sentimiento.lower()
    sentimientos_disponibles = df_modelo_sentimiento['sentimiento'].str.lower().tolist()
    fila = df_modelo_sentimiento[df_modelo_sentimiento['sentimiento'] == sentimiento]
    if not fila.empty:
        numero_sentimiento = fila['sentimiento_n'].iloc[0]
    else:
        return {"Error": f"Sentimiento no encontrado. Sentimientos disponibles {sentimientos_disponibles}"}

    # Realizar la predicción usando el modelo de regresión lineal ya entrenado
    df_pred = pd.DataFrame({
        'acceso_anticipado': [acceso_anticipado],
        'metascore': [metascore],
        'año': [año],
        'categoria_n': [numero_categoria],
        'sentimiento_n': [numero_sentimiento]
    })

    # Utilizar el mismo objeto StandardScaler que se ajustó en la función de carga de datos
    df_pred[['metascore']] = scaler_metascore.transform(df_pred[['metascore']])

    # Realizar la predicción usando el modelo de regresión lineal ya entrenado
    precio_pred = modelo_regresion.predict(df_pred)[0]

    del df_funciones
    del df_modelo_categoria
    del df_modelo_sentimiento

    return {"precio_estimado": round(precio_pred, 2), "rmse": round(rmse, 2)}


