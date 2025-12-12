'''### info:
     CONTROL 

    Dependencias:
        pip install uuid

    Referencias:
        https://pypi.org/project/uuid/
        https://docs.python.org/3/library/uuid.html
    
'''
from flask import request, session,redirect,render_template
from datetime import datetime
from model import *
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
from appConfig import config

def obtenerTabla(param):
    '''info:
        Se carga el dict 'param' con los datos de una tabla
        que será utilizado para cargar un html
        En esta función los datos son fijos (no busca en la BD), solo a
        efectos de realizar pruebas.
    '''
    param["page-title"]="Table"
    param["page-header"]= "Table"        
    param['table']={
        "title_table":"El titulo principal tabla",
        "description_table":"Esto es una prueba con una tabla",

        "colIni":1, # Sirve para mostrar desde col 0 (incluye id), desde 1 no lo incluye al id
                    # siempre color el id en la primer posición (la 0) de la lista
                    # poner a izquierda columnas que no quiere visualizar
                    
        "titles":{"id":"tbl_row_tit","cols":["ID","NOMBRE","APELLIDO","DNI","EDAD"]},
        "data":{"tbl_row_6":    ["6","Juan","Perez",1234,23],
                 "tbl_row_71":  ["71","Laura","Lopez",9632,55],
                 "tbl_row_12":  ["12","Lucia","Marano",8775,28],
                 "tbl_row_9832":["9832","Laura","Lopez",9632,55],
                 "tbl_row_131": ["131","Lucia","Marano",8775,28]
                },
               
        "pagination":{ # Si no desea paginacion, entonces dejar el diccionario vacio
                      "prev_pag":  {"href":"#","content":'"_"',"class":" "},
                      "pag_1":   {"href":"#","content":"1","class":" "},
                      "pag_2":   {"href":"#","content":"2","class":"active"},
                      "pag_3":   {"href":"#","content":"3","class":" "},
                      "pag_4":   {"href":"#","content":"4","class":" "},
                      "next_pag":{"href":"#","content":"_","class":" "}
                     }
    }
    
def obtenerMenuBottom(param,idActivo="mnub01"):
    '''info:
    Carga el dict 'param' con las datos de un menu
    que será utilizado para cargar un html
    recibe  'idActivo' Es el id del diccionario de aquel item del menu que estará 
               marcado en el html como activo
    recibe 'param' el diccionario de parámetros. 
    '''

    param["page-title"]=""
    param["page-header"]= ""
    
    param["menubottom"]= {
            "mnub01":{"href":"casita","content":"Home","class":" dfsdf"},
            "mnub02":{"href":"/login","content":"Log In","class":" "},
            "mnub03":{"href":"/logout","content":"Log Out","class":" "},
            "mnub04":{"href":"/pagina01","content":"Pagina 01","class":" "},
            "mnub05":{"href":"/pagina02","content":"Pagina 02","class":" "},
            "mnub06":{"href":"/register","content":"Register","class":" "},
            "mnub07":{"href":"/edit_user","content":"Editar Usuario","class":" "},
            "mnub08":{"href":"/about","content":"About","class":" "}
        }
    # Activar el id 
    param["menubottom"].get(idActivo)["class"]="active"


##########################################################################
# + + I N I C I O + + MANEJO DE  REQUEST + + + + + + + + + + + + + + + + +
##########################################################################

def getRequet(diResult):
    if request.method=='POST':
        for name in request.form.to_dict().keys():
            li=request.form.getlist(name)
            if len(li)>1:
                diResult[name]=request.form.getlist(name)
            elif len(li)==1:
                diResult[name]=li[0]
            else:
                diResult[name]=""
    elif request.method=='GET':  
        for name in request.args.to_dict().keys():
            li=request.args.getlist(name)
            if len(li)>1:
                diResult[name]=request.args.getlist(name)
            elif len(li)==1:
                diResult[name]=li[0]
            else:
                diResult[name]=""     
 
"""
def getRequet(request):
    '''info:
        Lee un solicitud 'request' y hace tratamiento de lectura diferenciado
        dependiendo del metodo (post o get). Luego unifica  el contenido del
        request en un diccionario 'myrequest'.
        Retorna 'myrequest' un diccionario con los datos 
               recibidos en la solicitud 'request'
    '''
    try: 
        if request.method =="POST":                           # Solicitud x POST, creación de una session
            myrequest=request.form          
        elif request.method =="GET" and len(request.args)!=0: # Solicitud x GET, creación de una session
            myrequest=request.args
        else:
            myrequest={}
    except ValueError:                              
        myrequest={}
    return myrequest
"""
##########################################################################
# - - F I N - - MANEJO DE  REQUEST - - - - - - - - - - - - - - - - - - - -
##########################################################################

##########################################################################
# + + I N I C I O + + MANEJO DE  SUBIDA DE ARCHIVOS  + + + + + + + + + + +
##########################################################################

def upload_file (diResult) :
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
    MAX_CONTENT_LENGTH = 1024 * 1024     
    if request.method == 'POST' :         
        for key in request.files.keys():  
            diResult[key]={} 
            diResult[key]['file_error']=False            
            
            f = request.files[key] 
            if f.filename!="":     
                #filename_secure = secure_filename(f.filename)
                file_extension=str(os.path.splitext(f.filename)[1])
                filename_unique = uuid4().__str__() + file_extension
                path_filename=os.path.join( config['upload_folder'] , filename_unique)
                # Validaciones
                if file_extension not in UPLOAD_EXTENSIONS:
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: No se admite subir archivos con extension '+file_extension
                if os.path.exists(path_filename):
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: el archivo ya existe.'
                    diResult[key]['file_name']=f.filename
                try:
                    if not diResult[key]['file_error']:
                        diResult[key]['file_error']=True
                        diResult[key]['file_msg']='Se ha producido un error.'

                        f.save(path_filename)   
                        diResult[key]['file_error']=False
                        diResult[key]['file_name_new']=filename_unique
                        diResult[key]['file_name']=f.filename
                        diResult[key]['file_msg']='OK. Archivo cargado exitosamente'
 
                except:
                        pass
            else:
                diResult[key]={} # viene vacio el input del file upload

    # si existe el archivo devuelve True
    # os.path.exists(os.path.join('G:\\directorio\\....\\uploads',"agua.png"))

    # borrar un archivo
    # os.remove(os.path.join('G:\\directorio\\.....\\uploads',"agua.png"))
            
##########################################################################
# - - F I N - - MANEJO DE  SUBIDA DE ARCHIVOS  - - - - - - - - - - - - - - 
##########################################################################


##########################################################################
# + + I N I C I O + + MANEJO DE  SESSION + + + + + + + + + + + + + + + + +
##########################################################################

def cargarSesion(dicUsuario):
    '''info:
        Realiza la carga de datos del usuario
        en la variable global dict 'session'.
        recibe 'dicUsuario' que es un diccionario con datos
               de un usuario.
        Comentario: Usted puede agregar en 'session' las claves que necesite
    '''

    session['id_usuario'] = dicUsuario['id']
    session['nombre']     = dicUsuario['nombre']
    session['apellido']   = dicUsuario['apellido']
    session['username']   = dicUsuario['username'] # es el mail
    session['imagen']     = ""
    session['rol']        = ""
    session["time"]       = datetime.now()  

def crearSesion(request):
    '''info:
        Crea una sesion. Consulta si los datos recibidos son validos.
        Si son validos carga una sesion con los datos del usuario
        recibe 'request' una solicitud htpp con los datos 'email' y 'pass' de 
        un usuario.
        retorna True si se logra un session, False caso contrario
    '''
    sesionValida=False
    mirequest={}
    try: 
        #Carga los datos recibidos del form cliente en el dict 'mirequest'.          
        getRequet(mirequest)
        # CONSULTA A LA BASE DE DATOS. Si usuario es valido => crea session
        dicUsuario={}
        if obtenerUsuarioXEmailPass(dicUsuario,mirequest.get("username"),mirequest.get("password")):
            # Carga sesion (Usuario validado)
            cargarSesion(dicUsuario)
            sesionValida = True
    except ValueError:                              
        pass
    return sesionValida

def haySesion():  
    '''info:
        Determina si hay una sesion activa observando si en el dict
        session se encuentra la clave 'username'
        retorna True si hay sesión y False si no la hay.
    '''
    return session.get("username")!=None

def cerrarSesion():
    '''info:
        Borra el contenido del dict 'session'
    '''
    try:    
        session.clear()
    except:
        pass

##########################################################################
# - - F I N - - MANEJO DE  SESSION - - - - - - - - - - - - - - - - - - - -
##########################################################################


##########################################################################
# + + I N I C I O + + PAGINA login, home y/o principal    + + + + + + + + 
##########################################################################

def home_pagina(param): 
    ''' Info:
      Carga la pagina home.
      Recibe 'param' el diccionario de parametros
      Retorna la pagina 'home' renderizada.
    '''
    obtenerMenuBottom(param)
    return render_template('home.html',param=param)

def login_pagina(param):
    ''' Info:
      Carga la pagina login.
      Recibe 'param' el diccionario de parametros
      Retorna la pagina 'login' renderizada.
    '''
    obtenerMenuBottom(param)
    return render_template('login.html',param=param)

##########################################################################
# - - F I N - - PAGINA login, home y/o principal   - - - - - - - - - - - -
##########################################################################


##########################################################################
# + + I N I C I O + + USUARIO: registro, edicion, actualizacion  + + + + + 
##########################################################################

def ingresoUsuarioValido(param,request):
    '''info:
        Valida el usuario y el pass contra la BD.
        recibe 'param' dict de parámetros
        recibe 'request' una solicitud http con los datos usuario y pass
        retorna: 
            Si es valido el usuario y pass => crea una session y retorna 
            la pagina home.
            Si NO es valido el usuario y pass => retorna la pagina login
            y agrega en el diccionario de parámetros una clave con un mensaje 
            de error para ser mostrada en la pagina login.
    '''
    if crearSesion(request):
        obtenerMenuBottom(param)  
        res=render_template('home.html',param=param)
    else:
        param['error_msg_login']="Error: Usuario y/o password inválidos"
        res= login_pagina(param)        
    return res  

def registro_pagina(param):
    '''info:
        Carga la pagina 'register'
    '''
    obtenerMenuBottom(param)       
    return render_template('register.html',param=param)

def ValidarFormularioRegistro(di):
    res=True
    res= res and di.get('nombre')!=""
    res= res and di.get('apellido')!=""
    res= res and di.get('email')!=""
    res= res and di.get('password')!=""
    return res
    
def registrarUsuario(param,request):
    '''info:
      Realiza el registro de un usuario en el sistema, es decir crea un nuevo usuario
      y lo registra en la base de datos.
      recibe 'param' el diccionario de parámetros.
      recibe request es la solicitud (post o get) proveniente del cliente
      retorna la pagina del login, para forzar a que el usuario realice el login con
      el usuario creado.
    '''
    mirequest={}
    getRequet(mirequest)
    
    if ValidarFormularioRegistro(mirequest):
        # CONSULTA A LA BASE DE DATOS: Realiza el insert en la tabla usuario
        if crearUsuario(mirequest):
            param['succes_msg_login']="Se ha creado el usuario con exito"
            cerrarSesion()           # Cierra sesion existente(si la hubiere)
            res=login_pagina(param)  # Envia al login para que vuelva a loguearse el usuario
        else:
            param['error_msg_register']="Error: No se ha podido crear el usuario"
            res=registro_pagina(param)
    else:
        param['error_msg_register']="Error: Problema en la validacion de los campos"
        res=registro_pagina(param)

    obtenerMenuBottom(param)
    return res 

def editarUsuario_pagina(param):
    '''info:
        Carga la pagina edit_user
        Retorna la pagina edit_user, si hay sesion; sino retorna la home.
    '''
    res= redirect('/') # redirigir al home o a la pagina del login

    if haySesion():    # hay session?
        # Confecciona la pagina en cuestion
        obtenerMenuBottom(param)
        obtenerUsuarioXEmail(param,session.get('username'), 'edit_user')
        res= render_template('edit_user.html',param=param)
           
    return res  


def actualizarDatosDeUsuarios(param,request):
    '''info:
            Recepciona la solicitud request que es enviada
            desde el formulario de edit_user 
          Retorna 
            si hay sesion: retorna la edit_user con los datos actualizados
               y un mensaje de exito o fracaso sobre el mismo form ; 
            si no hay sesion: retorna la home.
    '''
    res=False
    msj=""
    mirequest={}
    try:     
        getRequet(mirequest)      
        # *** ACTUALIZAR USUARIO ***
        
        if actualizarUsuario(mirequest,session.get("username")):
            res=True
            param['succes_msg_updateuser']="Se ha ACTUALIZADO el usuario con exito"
        else:
            #error
            res=False
            param['error_msg_updateuser']="Error: No se ha podido ACTUALIZAR el usuario"

        editarUsuario_pagina(param)
        res= render_template('edit_user.html',param=param)  
    except ValueError as e :                   
        pass
    return res 

##########################################################################
# - - F I N - - USUARIO: registro, edicion, actualizacion  - - - - - - - -
##########################################################################
 

##########################################################################
# + + I N I C I O + +  OTRAS PAGINAS     + + + + + + + + + + + + + + + + +
##########################################################################

def pagina01(param):  
    ''' Info:
        Carga la pagina 01
        Retorna la pagina 01, si hay sesion; sino retorna la home.
    '''
    if haySesion():       # hay session?            
        # Confecciona la pagina en cuestion
        obtenerMenuBottom(param)  
        param['page-header']="Pagina 01, Acceso con logeo"
        obtenerTablaProducto(param)
        res= render_template('pagina01.html',param=param)
    else:
        res= redirect('/')   # redirigir al home o a la pagina del login
    return res  
    

def pagina02(param):  
    ''' Info:
        Carga la pagina 02
        Retorna la pagina 02, si hay sesion; sino retorna la home.
    '''
    if haySesion():   # hay session?
        # Confecciona la pagina en cuestion
        obtenerMenuBottom(param)  
        param['page-header']="Pagina 02, Acceso con logeo"
        res= render_template('home.html',param=param)
    else:
        res= redirect('/') # redirigir al home o a la pagina del login
    return res 


def acercaDe_pagina(param): 
    ''' Info:
        Carga la pagina about
    ''' 
    obtenerMenuBottom(param)  
    param['page-header']="ABOUT, Acceso SIN LOGEO"
    return render_template('home.html',param=param) 

def obtenerTablaProducto(param):
    '''info:
        Obtiene la información completa de toda la tabla de producto desde la DB.
        Carga el dict 'param' con el contenido de la tabla
    '''
    #consultar la

    datos=[]
    datos=selectDB(BASE,"select * from producto;",title=True)
    tu_titulos=datos[0]
    li_datos=datos[1:]
    di_datos={}
    for fila in datos[1:]:                    # armo dict don los datos para colocarlo en los parámetroa
        di_datos["tbl_row_"+str(fila[0])]=fila



    param["page-title"]="Productos"
    param["page-header"]= "Productos"        
    param['table']={
        "title_table":"Productos",
        "description_table":"",

        "colIni":1, # Sirve para mostrar desde col 0 (incluye id), desde 1 no lo incluye al id
                    # siempre color el id en la primer posición (la 0) de la lista
                    # poner a izquierda columnas que no quiere visualizar
                    
        "titles":{"id":"tbl_row_tit","cols":tu_titulos},
        "data":li_datos,
               
    }        


def paginaNoEncontrada(name):
    ''' Info:
      Retorna una pagina generica indicando que la ruta 'name' no existe
    '''
    res='Pagina "{}" no encontrada<br>'.format(name)
    res+='<a href="{}">{}</a>'.format("/","Home")
    
    return res


##########################################################################
# - - F I N - -   OTRAS PAGINAS    - - - - - - - - - - - - - - - - - - - -
##########################################################################
