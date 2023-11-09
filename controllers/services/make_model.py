import joblib
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer





def crear_modelosCercania():
    try:
        df = pd.read_csv('../ChatBot/data/data.csv')
        tfidf_vectorizer = TfidfVectorizer(max_features=5000)
        tfidf_vectorizer.fit_transform(df['detalle'])
        joblib.dump(tfidf_vectorizer, "../ChatBot/data/files/vectorizador.pkl")
        
        X_train_tfidf = tfidf_vectorizer.fit_transform(df['detalle'])
        nbrs = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(X_train_tfidf)
        joblib.dump(nbrs, '../ChatBot/data/files/modelo_nbrs.pkl')
        
        return True,"El proceso de creacion de vectores de cercania ha sido exitoso"
    except:
        return False,"Error: El proceso de creacion de vectores de cercania ha fallado, verificar la columna detalle"