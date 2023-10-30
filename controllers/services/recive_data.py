

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
            return "Archivo txt guardado y validado con éxito"
        
        else:
            return "Error: El archivo que se proporcionó no es del formato correcto (.txt)"
    
    return "No se recibió ningún archivo txt"