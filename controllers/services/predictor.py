import pandas as pd
import joblib
from controllers.services.check_history import rectificar_historial
from controllers.services.save_new_questions import save_new_questions



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
    umbral = 0.99
    rute = rectificar_historial()
    data_search = pd.read_csv(f'{rute[0]}/data.csv')

    # Cargar el vectorizador TF-IDF y el modelo NBRs previamente entrenados
    tfidf_vectorizer = joblib.load(f"{rute[1]}/vectorizador.pkl")
    nbrs = joblib.load(f"{rute[1]}/modelo_nbrs.pkl")
    
    
    texto_vectorizado = tfidf_vectorizer.transform([pregunta])
    
    distances, indices = nbrs.kneighbors(texto_vectorizado)
    print(distances.min())
    
      
    try:
        similar_questions = [data_search.iloc[i]['detalle'] for i in indices[0]]
        respuesta = similar_questions[0]
        fila = data_search[data_search['detalle'] == respuesta]
       
        if distances.min() > umbral:
            solucion = "No entiendo lo que has dicho"
            comentario = "porfavor de proporcionar mas informacion o mejorar la respuesta"
            save_new_questions(pregunta)
            color_question = False
        else:
            solucion = fila['solucion'].values[0]
            comentario = fila['comentario'].values[0]
            color_question = True
       
        context = search_context(fila.index[0])
    except Exception as e:
        return "Error: Ha ocurrido un problema durante la verificación de la pregunta. si el error persiste comunícate con nuestras operadoras", "error en alguna parte", "usuario",False
    return solucion, comentario, context, similar_questions, color_question


def search_context(index):
    """
    Busca el contexto asociado a un índice específico en el conjunto de datos.
    
    Args:
        index (int): Índice de la fila en el conjunto de datos.
        
    Returns:
        context (str): El contexto asociado a la fila dada.
    """
    rute = rectificar_historial()
    
    columnas_de_interes = []
    with open(f'{rute[0]}/Prompts.txt', 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variable, _ = linea.strip().split('=')
            columnas_de_interes.append((variable.strip()))


    numero_fila = index
    df = pd.read_csv(f'{rute[0]}/data.csv', usecols=columnas_de_interes)


    if 0 <= numero_fila < len(df):
        fila = df.iloc[numero_fila]
        # Verificar si hay una 'x' en las columnas de interés para la fila dada
        columnas_con_x = [col for col in columnas_de_interes if fila[col] == 'x']
       
        return columnas_con_x[0] if columnas_con_x else "usuario"
    else:
        return "usuario"
