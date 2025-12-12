# controller.py
from flask import request, session, redirect, render_template, url_for, flash
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
from appConfig import config
import model 
from datetime import datetime
from _mysql_db import *

'''### info:
     CONTROL 
'''

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

# ---------------- LOGIN / SIGNUP ----------------
def login_get():
    # Renderiza form de login
    return render_template("login.html")

def login_post():
    mail = request.form.get('mail')
    contrasena = request.form.get('contrasena')
    cliente = model.validarCliente(mail, contrasena)
    if not cliente:
        flash("Usuario o contraseña incorrecta.", "error")
        return render_template("login.html")
    # cliente = (id, nombre, tipo, mail)
    session['cliente_id'] = cliente[0]
    session['nombre'] = cliente[1]
    session['tipo'] = cliente[2]
    session['mail'] = cliente[3]
    # Redirigir según rol
    if cliente[2] == "admin":
        return redirect(url_for("admin_estadisticas_route"))
    else:
        return redirect(url_for("home_route"))

def logout():
    session.clear()
    return redirect(url_for("login_get_route"))

def signup_get():
    return render_template("signup.html")

def signup_post():
    datos = {
        'nombre': request.form.get('nombre'),
        'mail': request.form.get('mail'),
        'contrasena': request.form.get('contrasena')
    }
    if model.crearCliente(datos):
        flash("Cuenta creada correctamente. Ingrese con sus credenciales.", "success")
        return redirect(url_for("login_get_route"))
    else:
        flash("Error al crear la cuenta.", "error")
        return render_template("signup.html")

# PARA VERIFICAR SI SE LOGGEÓ Y COMO QUÉ TIPO DE USUARIO
def necesita_login(func):
    def wrapper(*args, **kwargs):
        if not session.get('cliente_id'):
            return redirect(url_for("login_get_route"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def solo_admin(func):
    def wrapper(*args, **kwargs):
        if session.get('tipo') != "admin":
            return redirect(url_for("home_route"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def solo_cliente(func):
    def wrapper(*args, **kwargs):
        if session.get('tipo') != "cliente":
            return redirect(url_for("admin_estadisticas_route"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# ---------------- RUTAS CLIENTE ----------------
@necesita_login
@solo_cliente
def home():
    return render_template("index.html")

@necesita_login
@solo_cliente
def catalogo():
    productos = []
    for r in model.obtenerProductos():
        productos.append({
            'id': r[0],
            'nombre': r[1],
            'precio_unidad': r[2],
            'img': r[3],
            'descripcion': r[4],
            'ventas': r[5]
        })
    return render_template("catalogo.html", productos=productos)

@necesita_login
@solo_cliente
def ver_producto(pid):
    p = model.obtenerProductoPorId(pid)
    if not p:
        return "Producto no encontrado", 404
    producto = {
        'id': p[0],
        'nombre': p[1],
        'precio_unidad': p[2],
        'img': p[3],
        'descripcion': p[4],
        'ventas': p[5]
    }
    return render_template("producto.html", producto=producto)

@necesita_login
@solo_cliente
def mi_cuenta():
    # miCuenta.html debe usar {{ session['nombre'] }} y {{ session['mail'] }}
    return render_template("miCuenta.html")

# Wishlist
@necesita_login
@solo_cliente
def wishlist_get():
    cliente_id = session['cliente_id']
    rows = model.obtenerWishlistCliente(cliente_id)
    productos = [{'id': r[0], 'nombre': r[1], 'precio_unidad': r[2], 'img': r[3], 'descripcion': r[4]} for r in rows]
    return render_template("wishlist.html", productos=productos)

@necesita_login
@solo_cliente
def wishlist_add():
    model.agregarWishlist(session['cliente_id'], request.form.get("producto_id"))
    # redirigir a home:
    return redirect(url_for("home_route"))

@necesita_login
@solo_cliente
def wishlist_remove():
    model.quitarWishlist(session['cliente_id'], request.form.get("producto_id"))
    return redirect(url_for("wishlist_route"))

# Carrito
@necesita_login
@solo_cliente
def carrito_get():
    cliente_id = session['cliente_id']
    rows = model.obtenerCarritoCliente(cliente_id)
    productos = [{'id': r[0], 'nombre': r[1], 'precio_unidad': r[2], 'img': r[3], 'descripcion': r[4]} for r in rows]
    return render_template("carrito.html", productos=productos)

@necesita_login
@solo_cliente
def carrito_add():
    model.agregarCarrito(session['cliente_id'], request.form.get("producto_id"))
    # Se solicitó que al agregar al carrito redirija a home:
    return redirect(url_for("home_route"))

@necesita_login
@solo_cliente
def carrito_remove():
    model.quitarCarrito(session['cliente_id'], request.form.get("producto_id"))
    return redirect(url_for("carrito_route"))

# Pedidos cliente
@necesita_login
@solo_cliente
def mis_pedidos():
    cliente_id = session['cliente_id']
    pedidos = model.obtenerPedidosPorCliente(cliente_id)
    return render_template("pedidosusuario.html", pedidos=pedidos)

# Crear tote personalizado (GET muestra form; POST guarda imagen y registro)
@necesita_login
@solo_cliente
def crea_tote_route():
    if request.method == "GET":
        return render_template("creatote.html")
    # POST
    imagen = upload_file(request.files.get("imagen"))
    color = request.form.get("color")
    estampa = request.form.get("estampa")
    model.guardarTotePersonalizado(session['cliente_id'], imagen, color, estampa)
    flash("Tote personalizado creado y guardado.", "success")
    return redirect(url_for("home_route"))

# ---------------- RUTAS ADMIN ----------------
@necesita_login
@solo_admin
def admin_pedidos():
    pedidos = model.obtenerTodosPedidos()
    return render_template("pedidosadmin.html", pedidos=pedidos)

@necesita_login
@solo_admin
def admin_estadisticas():
    return render_template("estadisticas.html")

@necesita_login
@solo_admin
def add_product_get():
    return render_template("add_product.html")

@necesita_login
@solo_admin
def add_product_post():
    form = request.form.to_dict()
    imagen = upload_file(request.files.get("imagen"))
    form['img'] = imagen or ''
    if model.crearProducto(form):
        flash("Producto creado exitosamente.", "success")
        return redirect(url_for("admin_estadisticas_route"))
    else:
        flash("Error creando producto.", "error")
        return render_template("add_product.html")

########## ERROR NO ENCONTRADA ###########
def paginaNoEncontrada(name):
    ''' Info:
      Retorna una pagina generica indicando que la ruta 'name' no existe
    '''
    res='Pagina "{}" no encontrada<br>'.format(name)
    res+='<a href="{}">{}</a>'.format("/","Home")
    
    return res
