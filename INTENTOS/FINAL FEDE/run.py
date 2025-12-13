# https://flask.palletsprojects.com/en/2.3.x/
# https://pythonbasics.org/flask-http-methods/

from flask import Flask
from route import route 
def main():
    app = Flask(__name__,template_folder='templates')
    route(app)
    app.run('0.0.0.0', 5000, debug=True) 
main()