# _mysql_db.py
# Conexión y helpers para MySQL (usa mysql-connector-python)
import mysql.connector

################### FUNCIONES PRINCIPALES ####################################
def conectarBD(configDB=None):
    """
    Conecta usando un dict configDB con keys:
    host, user, pass, dbname
    Retorna la conexión o None.
    """
    if configDB is None:
        return None
    try:
        mydb = mysql.connector.connect(
            host=configDB.get('host'),
            user=configDB.get('user'),
            password=configDB.get('pass'),
            database=configDB.get('dbname')
        )
        return mydb
    except mysql.connector.Error as e:
        print("ERROR conectarBD ->", e)
        return None

def cerrarBD(mydb):
    if mydb:
        try:
            mydb.close()
        except:
            pass

def consultarDB(mydb, sQuery="", val=None, title=False):
    """
    Ejecuta SELECT y devuelve una lista de tuplas.
    Si falla devuelve [].
    """
    try:
        if mydb:
            mycursor = mydb.cursor()
            if val is None:
                mycursor.execute(sQuery)
            else:
                mycursor.execute(sQuery, val)
            res = mycursor.fetchall()
            if title:
                res.insert(0, mycursor.column_names)
            return res
    except mysql.connector.Error as e:
        print("ERROR consultarDB ->", e)
    return []

def ejecutarDB(mydb, sQuery="", val=None):
    """
    Ejecuta INSERT/UPDATE/DELETE.
    Devuelve rowcount (int). En error devuelve 0.
    """
    try:
        mycursor = mydb.cursor()
        if val is None:
            mycursor.execute(sQuery)
        else:
            mycursor.execute(sQuery, val)
        mydb.commit()
        return mycursor.rowcount
    except mysql.connector.Error as e:
        try:
            mydb.rollback()
        except:
            pass
        print("ERROR ejecutarDB ->", e)
        return 0

# Wrappers que usan configDB (dict)
def selectDB(configDB=None, sql="", val=None, title=False):
    if configDB is None:
        return []
    mydb = conectarBD(configDB)
    res = consultarDB(mydb, sQuery=sql, val=val, title=title)
    cerrarBD(mydb)
    return res

def insertDB(configDB=None, sql="", val=None):
    if configDB is None:
        return 0
    mydb = conectarBD(configDB)
    res = ejecutarDB(mydb, sQuery=sql, val=val)
    cerrarBD(mydb)
    return res

def updateDB(configDB=None, sql="", val=None):
    return insertDB(configDB, sql, val)  # reuse (returns rowcount)

def deleteDB(configDB=None, sql="", val=None):
    return insertDB(configDB, sql, val)  # reuse (returns rowcount)

# CONFIG BASE por compatibilidad con tu proyecto
BASE = { "host":"localhost",
        "user":"root",
        "pass":"",
        "dbname":"base_le_totette"}
