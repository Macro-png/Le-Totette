# _mysql_db.py
# Conexión y helpers para MySQL (usa mysql-connector-python)
import mysql.connector

################### FUNCIONES PRINCIPALES ####################################

def conectarBD(configDB=None):
    # Establecer una conexión con el servidor MySQL
    # retorna la conexión
    mydb=None
    if configDB!=None:
        try:        
            mydb = mysql.connector.connect(
                    host=configDB.get("host"),
                    user=configDB.get("user"),
                    password=configDB.get("pass"),
                    database=configDB.get("dbname")
                   )
        except mysql.connector.Error as e:
            print("ERROR ->",e)        
    return mydb

def cerrarBD(mydb):
    # Realiza el cierra un conexión a una base de datos.
    # recibe 'mydb' una conexion a una base de datos
    if mydb!=None:
        mydb.close()

def consultarDB(mydb,sQuery="",val=None,title=False):
    # Realiza la consulta 'SELECT'
    # recibe 'mydb' una conexion a una base de datos
    # recibe 'sQuery' la cadena con la consulta sql.
    # recibe 'val' valores separados anti sql injection
    # recibe 'title' booleana
    # retorna una 'list' con el resultado de la consulta
    #     cada fila de la 'list' es una tupla
    #     Si 'title' es True, entonces agrega a la lista
    #     los títulos de las columnas.
    myresult=None
    try:
        if mydb!=None:
            mycursor = mydb.cursor()
            if val==None:
                mycursor.execute(sQuery)
            else:
                mycursor.execute(sQuery,val)
            myresult = mycursor.fetchall()
            # Para obtener los nombres de las columnas
            if title:
                myresult.insert(0,mycursor.column_names)
    except mysql.connector.Error as e:
        print("ERROR ->",e)   
    return myresult

def ejecutarDB(mydb,sQuery="",val=None):
    # Realiza las consultas 'INSERT' 'UPDATE' 'DELETE'
    # recibe 'mydb' una conexion a una base de datos
    # recibe 'sQuery' la cadena con la consulta (query) sql.
    # recibe 'val' valores separados anti sql injection
    # retorna la cantidad de filas afectadas con la query.
    res=None
    try:
        mycursor = mydb.cursor()
        if val==None:
            mycursor.execute(sQuery)
        else:
            mycursor.execute(sQuery,val)
        mydb.commit()   
        res=mycursor.rowcount        # filas afectadas
    except mysql.connector.Error as e:
        mydb.rollback()
        print("ERROR ->",e)    
    return res

## - - - FUNCIONES SECUNDARIAS - - - - - - - - - - - - - - - - - - - - - -
## UTILIZA LAS FUNCIONES PRINCIPALES PARA ACCEDER A LA BASE DE DATOS
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def selectDB(configDB=None,sql="",val=None,title=False):
    ########## SELECT
    # recibe 'configDB' un 'dict' con los parámetros de conexion
    # recibe 'sql' una cadena con la consulta sql
    # recibe 'val' valores separados anti sql injection
    # recibe 'title' booleana
    # retorna una 'list' con el resultado de la consulta
    #     cada fila de la 'list' es una 'tuple'
    #     Si 'title' es True, entonces agrega a la lista
    #     los títulos de las columnas.
    resQuery=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        resQuery=consultarDB(mydb,sQuery=sql,val=val,title=title)
        cerrarBD(mydb)
    return resQuery

def insertDB(configDB=None,sql="",val=None):
    ########## INSERT
    # recibe 'configDB' un 'dict' con los parámetros de conexion
    # recibe 'sql' una cadena con la consulta sql
    # recibe 'val' valores separados anti sql injection
    res=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        res=ejecutarDB(mydb,sQuery=sql,val=val)
        cerrarBD(mydb)
    return res

def updateDB(configDB=None,sql="",val=None):
    ########## UPDATE
    # recibe 'configDB' un 'dict' con los parámetros de conexion
    # recibe 'sql' una cadena con la consulta sql
    # recibe 'val' valores separados anti sql injection
    res=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        res=ejecutarDB(mydb,sQuery=sql,val=val)
        cerrarBD(mydb)
    return res

def deleteDB(configDB=None,sql="",val=None):
    ########## DELETE
    # recibe 'configDB' un 'dict' con los parámetros de conexion
    # recibe 'sql' una cadena con la consulta sql
    # recibe 'val' valores separados anti sql injection
    res=None
    if configDB!=None:
        mydb=conectarBD(configDB)
        res=ejecutarDB(mydb,sQuery=sql,val=val)
        cerrarBD(mydb)
    return res


# DICCIONARIO CON MI BASE DE DATOS
BASE = { "host":"localhost",
        "user":"root",
        "pass":"",
        "dbname":"base_le_totette"}

