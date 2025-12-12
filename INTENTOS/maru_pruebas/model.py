
'''### info:
    ACCESO A LOS DATOS
    Gestiona todos los accesos a la información que necesita la aplicación, tanto 
    consultas como actualizaciones.

    Las peticiones de acceso o manipulación de información llegan al 'model' a 
    través del 'controller'.

    Nota: Utiliza un módulo específico para acceder a la base de datos. En este
    caso usamos mySql; por tanto utilizamos el módulo desarrollado '_mysql_db' 
    para la ocasión.

'''
from maru_pruebas._mysql_db import *


def crearUsuario(di):
    '''### Información:
        Agrega un nuevo usuario (un registro) en la tabla usuario de la DB
        Recibe 'di' un diccionario con los datos del usuario a agegar en la tabla.
        Retorna True si realiza con existo el insert, False caso contrario.
    '''
    sQuery=""" 
        INSERT INTO usuario
        (id, nombre, apellido, email, pass)
        VALUES
        (%s,%s, %s, %s, %s);
    """
    val=(None,di.get('nombre'), di.get('apellido'), di.get('email'), di.get('password'))
    resul_insert=insertDB(BASE,sQuery,val)
    return resul_insert==1

def obtenerUsuarioXEmail(param,email,clave='usuario'):
    '''### Información:
       Obtiene todos los campos de la tabla usuario a partir de la clave 'email'.
       Carga la información obtenida de la BD en el dict 'param'
       Recibe 'param' in diccionario
       Recibe 'email' que es el mail si se utiliza como clave en la búsqueda
       Recibe 'clave' que es a clave que se le colocará al dict 'param'
       
    '''
    sSql="""SELECT id, nombre,apellido,email,pass 
    FROM  usuario WHERE  email=%s;""" 
    val=(email,)

    fila=selectDB(BASE,sSql,val)
    param[clave]={}
    param[clave]['id']=fila[0][0]
    param[clave]['nombre']=fila[0][1]
    param[clave]['apellido']=fila[0][2]
    param[clave]['email']=fila[0][3]
    param[clave]['password']=fila[0][4]

def obtenerUsuarioXEmailPass(result,email,password):
    '''### Información:
       Obtiene todos los campos de la tabla usuario a partir de la clave 'email'
         y del 'password'.
       Carga la información obtenida de la BD en el dict 'result'
       Recibe 'result' in diccionario donde se almacena la respuesta de la consulta
       Recibe 'email' que es el mail si se utiliza como clave en la búsqueda
       Recibe 'password' que se utiliza en la consulta. (Para validadar al usuario)
       Retorna:
        True cuando se obtiene un registro de u usuario a partir del 'email' y el 'pass.
        False caso contrario.
    '''
    res=False
    sSql="""SELECT id, nombre,apellido,email,pass 
    FROM  usuario WHERE  email=%s and pass=%s;"""
    val=(email,password)
    fila=selectDB(BASE,sSql,val)
    if fila!=[]:
        res=True
        result['id']=fila[0][0]
        result['nombre']=fila[0][1]
        result['apellido']=fila[0][2]
        result['username']=fila[0][3] # es el mail
        result['password']=fila[0][4]
        result['imagen']=''
        result['rol']=''
    return res    
        

def actualizarUsuario(di,email):
    '''### Información:
        Actualiza el registro de la tabla usuario para la clave 'email'
        Recibe 'di' un dict con los campos que se requiere modificar.
        Recibe 'email' que es la clave para identificar el regsitro a actualizar.
        Retorna True si realiza la actualización correctamente.
                False caso contrario.

    '''
    sQuery="""update usuario 
        SET nombre=%s, 
        apellido=%s,
        pass=%s 
        WHERE email=%s;
        """
    val=(di.get('nombre'), 
         di.get('apellido'), 
         di.get('password'), 
         email )
    
    resul_update=updateDB(BASE,sQuery,val=val)
    return resul_update==1

# def validarUsuario(email,password):
#     '''### Información:
#           Se consulta a la BD un usuario 'email' y un 'password'
#           retorna True si 'email' y  'password' son válido
#           retorna False caso contrario
#     '''
#     sSql='''
#         SELECT * FROM  usuario
#             WHERE 
#             email=%s
#             AND 
#             pass=%s;
#     '''
#     val=(email,password)
#     fila=selectDB(BASE,sSql,val=val)
#     return fila!=[]
