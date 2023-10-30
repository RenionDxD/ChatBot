from flask import request
from controllers.services.clean_save import guardar_limpiar,reformular_data
from controllers.services.make_model import crear_modelosCercania
from controllers.services.recive_data import recivir_archivo, recivir_archivoTxt
from controllers.services.predictor import verify_request
from controllers.services.generateResponse import core_gpt
import random

class clientController:
    
    def response():
        redireccion = "usuario"
        pregunta = FormRequest().get('pregunta')
        text_solucion,similares = verify_request(pregunta)
        solucion = core_gpt(text_solucion,redireccion,pregunta)
        respuesta_json = {
            "solucion":solucion
        }
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
        confirmacion_reformular = reformular_data()
        confirmacion_guardado = guardar_limpiar()
        confirmacion_modelo = crear_modelosCercania()
        
        if confirmacion_guardado and confirmacion_modelo and confirmacion_reformular:
            resultado = "Proceso exitoso: El modelo se ha creado con éxito."
        elif not confirmacion_guardado and not confirmacion_modelo and not confirmacion_reformular:
            resultado = "Error: El modelo no ha sido creado/actualizado."
        elif not confirmacion_guardado:
            resultado = "Error: Hubo un problema al guardar y limpiar los datos. Verifica la ubicación del archivo o la estructura de este."
        else:
            resultado = "Error: El modelo no ha sido creado/actualizado, pero la limpieza de datos fue exitosa."

        return resultado
        

        
def FormRequest():
    # Define una función llamada FormRequest para obtener los datos del formulario en formato JSON
    request_form = request.get_json() # Obtener los datos del formulario en formato JSON
    return request_form