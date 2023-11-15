import pandas as pd
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from unidecode import unidecode
import unicodedata
from io import StringIO
# instalar pip install openpyxl
# pip install unidecode
# pip install openpyxl


try:
    nltk.download('stopwords')
    nltk.download('punkt')
except nltk.exceptions.HTTPError:
    # Manejar el error en caso de problemas de descarga
    print("No se ha podido descargar estos modulos")
    pass


def limpiar_texto(text):
    """
    Limpia el texto eliminando stopwords y acentos.

    Args:
        text (str): El texto a limpiar.

    Returns:
        str: El texto limpio.
    """
    stop = set(stopwords.words('spanish')) - set(['no', 'ni', 'pero', 'sino', 'sin', 'nada', 'nadie', 'ningún', 'ninguna', 'ningunos', 'ningunas'])

    palabras_minusculas = nltk.word_tokenize(text.lower(),'spanish')  # Convertir a minúsculas
   
    # Eliminar stopwords
    palabras_filtradas = [palabra for palabra in palabras_minusculas if palabra not in stop]
   
    # Reconstruir el texto limpio
    texto_limpio = unidecode(' '.join(palabras_filtradas))
    
    return texto_limpio

def guardar_limpiar():
    """
    Aplica la limpieza de texto a las columnas específicas de un DataFrame y guarda el resultado en un nuevo archivo CSV.

    Returns:
        tuple: Una tupla con un booleano indicando si el proceso fue exitoso y un mensaje informativo.
    """
    try:
        data = pd.read_csv('../ChatBot/data/data.csv')
        columnas_a_limpiar = ['modulo', 'detalle', 'comentario', 'solucion']
        
        for columna in columnas_a_limpiar:
            data[columna] = data[columna].apply(limpiar_texto)

        data.to_csv('../ChatBot/data/files/texto_procesado.csv', index=False)
        return True,"Proceso de limpiado y guardado exitoso"
    except Exception as e:
        return False, f"Error: Ha fallado la normalización de datos. Verifique simbología de celdas y palabras escritas correctamente. Detalle: {str(e)}"
    

def reformular_data():
    """
    Realiza la reformulación y limpieza de datos de un archivo XLSX, convirtiéndolo a un formato CSV y aplicando diversas transformaciones.

    Returns:
        bool: True si la reformulación y limpieza se completaron exitosamente, False en caso de error.
    """
    try:
        xlsx = pd.read_excel('../ChatBot/data/data.xlsx')
        xlsx.to_csv('../ChatBot/data/data.csv', index=False)
    except Exception as e:
        return False, f"Error: Hubo una falla en convertir el formato a CSV (compatible con el modelo). Detalle: {str(e)}"
    
    
    try:
        df = pd.read_csv('../ChatBot/data/data.csv')
        #eliminar todas las filas que estén completamente vacías
        df = df.dropna(how='all')
        #eliminar columnas sin nombre (es decir, columnas que tienen NaN como nombre)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        #aplicar minusculas
        df = df.apply(lambda x: x.apply(lambda y: y.lower() if isinstance(y, str) else y))
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
        info_buffer = StringIO()
        df.info(buf=info_buffer)

        # Recupera la información como una cadena
        df_info = info_buffer.getvalue()
        #print(df_info)
        return True,"Proceso de conversion de archivo exitoso",str(df_info)
    except Exception as e:
        return False, f"Error: Hay un problema en los datos del archivo (tablas, columnas, simbología, etc). Detalle: {str(e)}", "Información del XLSX defectuosa"
        

        
