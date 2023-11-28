from flask import Blueprint,jsonify
from controllers.controller import clientController

blueprint = Blueprint('api', __name__)

# Endopint verificador de estatus
@blueprint.route('/Online', methods=['GET'])
def check_status():
    return jsonify({'status': 'online'})

# Ruta a la que se le puede descargar archivos actualizados
@blueprint.route('/download', methods=['POST'])
def endpoint_download():
    return clientController.send_files()

# Ruta que recive la review de las preguntas
@blueprint.route('/send_review', methods=['POST'])
def endpoint_check_review():
    return clientController.review()

# Ruta para comprobar la lectura de datos viejos o nuevos
@blueprint.route('/historial', methods=['POST'])
def endpoint_use_history():
    return clientController.history()

# Definir rutas y asociarlas a funciones del controlador
@blueprint.route('/preguntas', methods=['POST'])
def endpoint_preguntas():
    return clientController.response()

# Ruta para crear o actualizar el modelo NBRS y vectorizador 
@blueprint.route('/modelar', methods=['POST'])
def endpoint_modelar():
    return clientController.nuevoModelo()

# ruta para recivir XLSX para entrenamiento
@blueprint.route('/post_data', methods=['POST'])
def endpoint_post_data():
    return clientController.dataRecive()
