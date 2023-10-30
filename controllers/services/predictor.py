import pandas as pd
import joblib

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
    data_search = pd.read_csv('../ChatBot/data/data.csv')
    
    # Cargar el vectorizador TF-IDF y el modelo NBRs previamente entrenados
    tfidf_vectorizer = joblib.load("../ChatBot/data/files/vectorizador.pkl")
    nbrs = joblib.load("../ChatBot/data/files/modelo_nbrs.pkl")
    
    
    texto_vectorizado = tfidf_vectorizer.transform([pregunta])
    
    distances, indices = nbrs.kneighbors(texto_vectorizado)
    similar_questions = [data_search.iloc[i]['detalle']  for i in indices[0]]
    respuesta = similar_questions[0]
    
    fila = data_search[data_search['detalle'] == respuesta]
    
    solucion = fila['solucion'].values[0]
    similares = similar_questions[1:]
    
    return solucion,similares