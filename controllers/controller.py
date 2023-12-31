from flask import request, jsonify,send_file
from controllers.services.clean_save import guardar_limpiar,reformular_data
from controllers.services.make_model import crear_modelos_cercania
from controllers.services.recive_data import recivir_archivo, recivir_archivoTxt, recivir_archivoKey
from controllers.services.predictor import verify_request
from controllers.services.generateResponse import core_gpt, generate_prompt
from controllers.services.results_questions import save_review
import json
from openpyxl import Workbook
import pandas as pd




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
    
    def send_files():
        nofile = FormRequest().get('Nofile')
        
        if nofile == 1:
            file = "../ChatBot/data/download_files/data_new.xlsx"
            df = pd.read_csv('../ChatBot/data/data.csv')
            df.to_excel(file, index=False)
        elif nofile == 2:
            file = '../ChatBot/data/download_files/preguntas_nuevas.xlsx'
            
        return send_file(file, as_attachment=True)
    

    def review():
        pregunta = FormRequest().get('pregunta')
        findQuestion = verify_request(pregunta)
        review = FormRequest().get('review')
        pregunta = FormRequest().get('respuesta')
        save_review(review,pregunta,findQuestion[3][0])
        return "",204

    
    def response():
        pregunta = FormRequest().get('pregunta')

        if pregunta is None or pregunta.strip() == "":
            respuesta_json = {"solucion":"La pregunta está vacía o no se ha proporcionado",
                              "similares":"",
                              "find":False,
                              "pregunta":""}
            # Si no se recibe la pregunta o está vacía, se devuelve un mensaje de error
            return respuesta_json
        
        text_solucion,comentario,context,similar_questions,find = verify_request(pregunta)
        prompt = generate_prompt(text_solucion,context,pregunta,comentario)
        solucion = core_gpt(prompt)
        respuesta_json = {"solucion":solucion,
                          "similares":similar_questions,
                          "find":find,
                          "pregunta":pregunta}
        return respuesta_json
    




    def dataRecive():
        confirm_file1 = ""
        confirm_file2 = ""
        confirm_file3 = ""

        # Obtener el archivo del formulario con el nombre 'archivo'
        file1 = request.files.get('archivo')
        file2 = request.files.get('txt')
        file3 = request.files.get('key')

        # Llamar a la función 'recivir_archivo' para procesar el archivo
        confirm_file1 = recivir_archivo(file1)
        confirm_file2 = recivir_archivoTxt(file2)
        confirm_file3 = recivir_archivoKey(file3)

        # Devolver la confirmación del archivo procesado
        response = [confirm_file1,confirm_file2,confirm_file3]
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

