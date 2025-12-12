"""
Punto de entrada principal del proyecto.
Inicializa la aplicación Flask, configura la SECRET_KEY
y registra todas las rutas definidas en route.py.
"""

from flask import Flask
from route import route

def main():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'clave-super-secreta-del-proyecto'
    route(app)
    app.run('0.0.0.0', 5000, debug=True)

main()

