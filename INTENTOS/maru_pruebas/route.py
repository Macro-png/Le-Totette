'''### info:
     CONTROL 
'''
import os
from flask import Flask, render_template, request
from controller import *

def route(app):
      
    @app.route("/")
    def login():
        param={}    
        return render_template("login.html")
      
    @app.route("/home")
    def home():
        ''' Info:
          Carga la pagina del home
        '''
        param={} 
        #return home_pagina(param)   
        return render_template("index.html")
              
    @app.route("/signin")
    def signin():
        param={}    
        return render_template("signin.html")
      
    @app.route('/recibir_datos',methods = ['POST', 'GET'])
    def formrecibe():
        diRequest={}
        getRequet(diRequest)
        upload_file (diRequest)
        return  diRequest

    @app.route('/<name>',methods = ['POST', 'GET'])
    def noEncontrada(name):
        ''' Info:
          Entra en esta ruta todo direccionamiento recibido que 
          no machea con ningun otro route. Es decir no es un pagina (dirección)
            válida en el sistema.
          Retorna una pagina indicando el error. 
        '''  
        return paginaNoEncontrada(name)
    
