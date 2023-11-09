import pandas as pd


def recivir_archivo(file):
    """
    Recibe un archivo y lo guarda en una ubicación específica.

    Args:
        file (FileStorage): El archivo a recibir y guardar.

    Returns:
        str: Mensaje de confirmación o error.
    """
    if file:
        if file.filename.endswith(('.xlsx')):
            file.save('../ChatBot/data/data.xlsx')  # Guarda el archivo en una ubicación específica
            respuesta = validation_data()
            print(respuesta)
            return "Archivo xlsx guardado con éxito"
        else:
            return "Error: El archivo que se proporciono no es el formato correcto (XLSX)"
    else:
        return "No se recibió ningún archivo xlsx"
    


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
    columnas_de_interes = []

    # Leer el archivo 'Prompts.txt' para obtener las columnas de interés
    with open('../ChatBot/data/Prompts.txt', 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            variable, valor = linea.strip().split('=')
            # Almacenar el nombre de la columna
            columnas_de_interes.append(variable.strip())

    # Leer el archivo XLSX
    df = pd.read_excel('../ChatBot/data/data.xlsx')

    # Verificar si las columnas del XLSX son iguales a las del Prompt.txt
    if list(df.columns) == columnas_de_interes:
        return True
    else:
        return False