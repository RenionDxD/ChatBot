import pandas as pd
import io
from controllers.services.generateResponse import core_gpt
import json
from openai import OpenAI

def recivir_archivo(file):
    """
    Recibe un archivo y lo guarda en una ubicación específica.

    Args:
        file (FileStorage): El archivo a recibir y guardar.

    Returns:
        str: Mensaje de confirmación o error.
    """
    if not file:
        return "No se recibió ningún archivo XLSX"

    if not file.filename.endswith(('.xlsx')):
        return "Error: El archivo proporcionado no tiene el formato correcto (XLSX)"
    
    file.save('../ChatBot/data/data.xlsx')  # Guarda el archivo en una ubicación específica
    respuesta = validation_data()
    print(respuesta)

    return "Archivo XLSX guardado con éxito"

    


def recivir_archivoTxt(file):
    if file:
        if file.filename.endswith(('.txt')):
            # Guardar el archivo en una ubicación específica
            file.save('../ChatBot/data/Prompts.txt')
            
            # Verificar el formato y las líneas del archivo
            with open('../ChatBot/data/Prompts.txt', 'r') as archivo:
                lineas = archivo.readlines()
                
            if len(lineas) != 4:
                return "Error: El archivo no contiene exactamente cuatro líneas."
            
            for linea in lineas:
                if '=' not in linea:
                    return f"Error en el prompt: {linea.strip()}. No contiene un signo igual (=)."
            
            # Si el archivo cumple con los requisitos, devolver un mensaje de éxito
            respuesta = validation_data()
            print(respuesta)
            return "Archivo txt guardado y validado con éxito"
        
        else:
            return "Error: El archivo que se proporcionó no es del formato correcto (.txt)"
    
    return "No se recibió ningún archivo txt"




def validation_data():   
    """
    Valida la consistencia de las columnas en el archivo XLSX con las especificadas en el archivo Prompts.txt.

    Returns:
        bool: True si las columnas son iguales, False en caso contrario.
    """
    columnas_de_interes = []

    # Leer el archivo 'Prompts.txt' para obtener las columnas de interés
    with open('../ChatBot/data/Prompts.txt', 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variable, _ = linea.strip().split('=')
            # Almacenar el nombre de la columna
            columnas_de_interes.append(variable.strip())

    # Leer el archivo XLSX
    df = pd.read_excel('../ChatBot/data/data.xlsx')

    # Verificar si las columnas del XLSX son iguales a las del Prompt.txt
    return list(df.columns) == columnas_de_interes



def recivir_archivoKey(file):
    try:
        contenido_archivo = file.getvalue().decode('utf-8')
    
        # Buscar la línea que contiene la clave de GPT
        lineas = contenido_archivo.split('\n')
        
        clave_gpt = lineas[0].strip()
        
        with open('../ChatBot/config/history.json', 'r') as file:
                config = json.load(file)
        config['keyGPT'] = clave_gpt
        
        with open('../ChatBot/config/history.json', 'w') as file:
                json.dump(config, file, indent=2)

        try:
            with open('../ChatBot/config/history.json', 'r') as file:
                    config = json.load(file)
            key = config['keyGPT']
            client = OpenAI(api_key=key,)    
            #reformula para entendimiento de usuario
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "lore"},])
            response = response.choices[0].message.content
        except Exception as e:
            return f"La llave contiene fallas"
    
        return "La llave funciona perfectmante"
    except:
        return "No se recivio ningun archivo de llave"
