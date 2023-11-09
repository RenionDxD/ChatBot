import pandas as pd
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from unidecode import unidecode
import unicodedata
# instalar pip install openpyxl
# pip install unidecode
# pip install openpyxl

nltk.download('stopwords')
nltk.download('punkt')


def limpiar_texto(text):
    stop = stopwords.words('spanish')
    excluding = ['no', 'ni', 'pero', 'sino', 'sin', 'nada', 'nadie', 'ningún', 'ninguna', 'ningunos', 'ningunas']
    stopwords_espanol = [word for word in stop if word not in excluding]
    palabras_minusculas = nltk.word_tokenize(text.lower(),'spanish')  # Convertir a minúsculas
    # Eliminar stopwords
    palabras_filtradas = [palabra for palabra in palabras_minusculas if palabra not in stopwords_espanol]
    # Reconstruir el texto limpio
    texto_sin_espacio = ' '.join(palabras_filtradas)
    palabra_con_acentos = texto_sin_espacio
    texto_limpio = unidecode(palabra_con_acentos)
    return texto_limpio

def guardar_limpiar():
    try:
        data = pd.read_csv('../ChatBot/data/data.csv')
        data['modulo'] = data['modulo'].apply(limpiar_texto)
        data['detalle'] = data['detalle'].apply(limpiar_texto)
        data['comentario'] = data['comentario'].apply(limpiar_texto)
        data['solucion'] = data['solucion'].apply(limpiar_texto)
        data.to_csv('../ChatBot/data/files/texto_procesado.csv', index=False)
        return True,"Proceso de limpiado y guardado exitoso"
    except:
        return False,"Error: ha fallado la normalizacion de datos, verifique simbologia de celdas y palabras escritas correctamante"
    

def reformular_data():
    """
    Realiza la reformulación y limpieza de datos de un archivo XLSX, convirtiéndolo a un formato CSV y aplicando diversas transformaciones.

    Returns:
        bool: True si la reformulación y limpieza se completaron exitosamente, False en caso de error.
    """
    try:
        xlsx = pd.read_excel('../ChatBot/data/data.xlsx')
        xlsx.to_csv('../ChatBot/data/data.csv', index=False)
    except:
        return False,"Error: hubo una falla en convertir el formato a csv (compatible con el modelo)"
    
    
    try:
        df = pd.read_csv('../ChatBot/data/data.csv')
        #eliminar todas las filas que estén completamente vacías
        df = df.dropna(how='all')
        #eliminar columnas sin nombre (es decir, columnas que tienen NaN como nombre)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        #aplicar minusculas
        df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
        df.columns = [unicodedata.normalize('NFD', col).encode('ascii', 'ignore').decode('utf-8').lower() for col in df.columns]
        
        df = df.replace(r'^\s*$', 'vacio', regex=True) 
        
        df['modulo'] = df['modulo'].str.strip()
        df['detalle'] = df['detalle'].str.strip()
        df['comentario'] = df['comentario'].str.strip()
        df['solucion'] = df['solucion'].str.strip()

        # Rellena los campos vacíos en cada columna con los valores adecuados
        df['modulo'].fillna('vacio', inplace=True)
        df['detalle'].fillna('vacio', inplace=True)
        df['comentario'].fillna('vacio', inplace=True)
        df['solucion'].fillna('vacio')
        # Guarda el DataFrame modificado en un nuevo archivo CSV
        #df.dropna(inplace=True)
        
        id_mapping = {}
        # Recorre cada columna del DataFrame
        for column in df.columns:
            current_id = 1  # Reinicia el ID para cada columna
            column_values = df[column].tolist()  # Convierte la columna en una lista

            # Recorre los valores de la columna
            for value in column_values:
                if value not in id_mapping:
                    id_mapping[value] = str(current_id)
                    current_id += 1

        # Recorre nuevamente cada columna y agrega la columna "_id" correspondiente
        for column in df.columns:
            df[column + '_id'] = df[column].map(id_mapping)
            
        df.to_csv('../ChatBot/data/data.csv', index=False)
        print(df)
        return True,"Proceso de conversion de archivo exitoso",df
    except:
        return False,"Error: hay problema en el datos del archivo (tablas,columnas,simbologia, etc)","Informacion del XLSX defectuosa"
        

        
