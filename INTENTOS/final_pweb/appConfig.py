# appConfig.py
from os import path, makedirs

config = {}
config['project_folder'] = path.dirname(path.realpath(__file__))
config['upload_folder'] = path.join(config['project_folder'], 'static', 'uploads')

# Crear carpeta uploads si no existe
if not path.exists(config['upload_folder']):
    makedirs(config['upload_folder'], exist_ok=True)

