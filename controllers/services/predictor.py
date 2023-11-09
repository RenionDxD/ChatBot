import pandas as pd
import joblib
from controllers.services.check_history import rectificar_historial


# Función para verificar una pregunta y encontrar soluciones similares
def verify_request(pregunta):
    """
    Esta función toma una pregunta como entrada y busca respuestas similares en un conjunto de datos previamente cargado.
    
    Args:
        pregunta (str): La pregunta de entrada que se desea comparar con preguntas en el conjunto de datos.
        
    Returns:
        solucion (str): La solución correspondiente a la pregunta más similar encontrada.
        similares (list): Una lista de preguntas similares excluyendo la pregunta principal.
        """
    rute = rectificar_historial()
    data_search = pd.read_csv(f'{rute[0]}/data.csv')
    
    # Cargar el vectorizador TF-IDF y el modelo NBRs previamente entrenados
    tfidf_vectorizer = joblib.load(f"{rute[1]}/vectorizador.pkl")
    nbrs = joblib.load(f"{rute[1]}/modelo_nbrs.pkl")
    
    
    texto_vectorizado = tfidf_vectorizer.transform([pregunta])
    
    distances, indices = nbrs.kneighbors(texto_vectorizado)
    similar_questions = [data_search.iloc[i]['detalle']  for i in indices[0]]
    respuesta = similar_questions[0]
    fila = data_search[data_search['detalle'] == respuesta]
    solucion = fila['solucion'].values[0]
    context = search_context(fila.index[0])
    print(context)
    
    return solucion,context


def search_context(index):
    rute = rectificar_historial()
    
    columnas_de_interes = []
    with open(f'{rute[0]}/Prompts.txt', 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variable, valor = linea.strip().split('=')
            columnas_de_interes.append((variable.strip()))
    numero_fila = index

    df = pd.read_csv(f'{rute[0]}/data.csv', usecols=columnas_de_interes)


    if 0 <= numero_fila < len(df):
        fila = df.iloc[numero_fila]
        # Verificar si hay una 'x' en las columnas de interés para la fila dada
        columnas_con_x = [col for col in columnas_de_interes if fila[col] == 'x']
        if columnas_con_x:
            return columnas_con_x[0]
        else: 
            return "usuario"
    else:
        return "usuario"
