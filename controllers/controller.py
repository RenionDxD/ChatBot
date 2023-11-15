from flask import request, jsonify
from controllers.services.clean_save import guardar_limpiar,reformular_data
from controllers.services.make_model import crear_modelos_cercania
from controllers.services.recive_data import recivir_archivo, recivir_archivoTxt
from controllers.services.predictor import verify_request
from controllers.services.generateResponse import core_gpt
import json




class clientController:

    def history():
        data = request.get_json()

        if not isinstance(data, dict) or 'boolean' not in data:
            config_info = ['Error: Datos de entrada no válidos']

        use_history = data.get('boolean')

        with open('../ChatBot/config/history.json', 'r') as file:
            config = json.load(file)

        config['history'] = use_history

        with open('../ChatBot/config/history.json', 'w') as file:
            json.dump(config, file, indent=2)

        config_info = ["Se cambio la configuracion del historial"]

        return config_info
    



    
    def response():
        pregunta = FormRequest().get('pregunta')

        if pregunta is None or pregunta.strip() == "":
            # Si no se recibe la pregunta o está vacía, se devuelve un mensaje de error
            return jsonify({"solucion": "La pregunta está vacía o no se ha proporcionado"})
        
        text_solucion,comentario,context = verify_request(pregunta)
        solucion = core_gpt(text_solucion,context,pregunta,comentario)
        respuesta_json = {"solucion":solucion}

        return respuesta_json
    




    def dataRecive():
        confirm_file1 = ""
        confirm_file2 = ""

        # Obtener el archivo del formulario con el nombre 'archivo'
        file1 = request.files.get('archivo')
        file2 = request.files.get('txt')

        # Llamar a la función 'recivir_archivo' para procesar el archivo
        confirm_file1 = recivir_archivo(file1)
        confirm_file2 = recivir_archivoTxt(file2)

        # Devolver la confirmación del archivo procesado
        response = [confirm_file1,confirm_file2]
        return response
        
    
    def nuevoModelo():
        resultado = ""
        array_informe = []

        confirmacion_reformular, informe, df = reformular_data()
        confirmacion_guardado, informe2 = guardar_limpiar()
        confirmacion_modelo, informe3 = crear_modelos_cercania()
        
        if confirmacion_guardado and confirmacion_modelo and confirmacion_reformular:
            resultado = "Proceso exitoso: El modelo se ha creado con éxito."
        elif not confirmacion_guardado and not confirmacion_modelo and not confirmacion_reformular:
            resultado = "Error: El modelo no ha sido creado/actualizado."
        elif not confirmacion_guardado:
            resultado = "Error: Hubo un problema al guardar y limpiar los datos. Verifica la ubicación del archivo o la estructura de este."
        else:
            resultado = "Error: El modelo no ha sido creado/actualizado, pero la limpieza de datos fue exitosa." 

        array_informe=[informe,informe2,informe3,resultado,str(df)]
        return array_informe
        

        
def FormRequest():
    """
    Obtiene los datos del formulario en formato JSON.

    Returns:
    - Datos del formulario en formato JSON.
    """
    # Define una función llamada FormRequest para obtener los datos del formulario en formato JSON
    request_form = request.get_json() # Obtener los datos del formulario en formato JSON

    return request_form

