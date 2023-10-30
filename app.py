from flask import Flask
from api.index import blueprint
#importar blueprint

def create_app():
    """
    Crea y configura la aplicación Flask.
    """
    app = Flask(__name__)

    # Configuración de la aplicación (opcional, si se requiere configuración)
    # app.config['DEBUG'] = True
    # app.config['SECRET_KEY'] = 'my_secret_key'

    # Registrar las rutas de la API bajo la URL '/chatbot'
    app.register_blueprint(blueprint, url_prefix='/chatbot')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5051)
