from flask import Flask, session
from route import route
import os

def main():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # C O N F I G
    # Para poder iniciar session, colocar un string aleatorio para inicializar la clave.
    app.config['SECRET_KEY'] = 'some random string'  

    # Opcional: máxima seguridad en uploads si se usan (no cambiamos nada)
    # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    route(app)
    # Solo para desarrollo. En producción usar WSGI.
    app.run('0.0.0.0', 5000, debug=True)

if __name__ == '__main__':
    main()
