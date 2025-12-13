'''
from flask import request, session, redirect, render_template
import model

##########################################################################
# SESIÓN
##########################################################################

def requiere_login():
    return session.get('usuario') is not None

def es_admin():
    return session.get('usuario', {}).get('tipo') == 'admin'

def cerrarSesion():
    session.clear()
    return redirect('/login')

##########################################################################
# PÁGINAS CLIENTE
##########################################################################

def home_pagina(param):
    if not requiere_login():
        return redirect('/login')
    if es_admin():
        return redirect('/admin/estadisticas')
    return render_template("index.html")

def catalogo_pagina(param):
    if not requiere_login():
        return redirect('/login')
    if es_admin():
        return redirect('/admin/estadisticas')
    return render_template("catalogo.html", productos=[])

def producto_pagina(param, pid):
    if not requiere_login():
        return redirect('/login')
    if es_admin():
        return redirect('/admin/estadisticas')
    return render_template("producto.html", producto={})

##########################################################################
# LOGIN / SIGNUP
##########################################################################

def login_pagina(param):
    param = param or {}
    return render_template("login.html", param=param)

def signup_pagina(param):
    param = param or {}
    return render_template("signup.html", param=param)

def signup(param):
    di = {
        'nombre': request.form.get('nombre'),
        'mail': request.form.get('email'),
        'contrasena': request.form.get('contrasena'),
        'tipo': 'cliente'
    }
    if crearCliente(di):
        return redirect('/login')

    param['error'] = "No se pudo crear el usuario"
    return render_template("signup.html", param=param)

def ingresoUsuarioValido(param):
    email = request.form.get('email')
    contrasena = request.form.get('contrasena')

    result = {}
    if validarClientePorMailYContrasena(result, email, contrasena):
        session['usuario'] = {
            'id': result['id'],
            'nombre': result['nombre'],
            'tipo': result['tipo'],
            'mail': result['mail']
        }

        if result['tipo'] == 'admin':
            return redirect('/admin/estadisticas')
        return redirect('/cliente/home')

    param['error'] = "Mail o contraseña incorrectos"
    return render_template("login.html", param=param)

##########################################################################
# ADMIN
##########################################################################

def estadisticas_pagina(param):
    if not requiere_login() or not es_admin():
        return redirect('/login')
    return render_template("estadisticas.html")

##########################################################################
# CREATOTE
##########################################################################

def creatote_pagina(param):
    if not requiere_login():
        return redirect('/login')
    return render_template("creatote.html")

def creatote_formulario(param):
    return redirect('/cliente/carrito')


##########################################################################
# CARRITO
##########################################################################

def agregar_producto_carrito(param, request, producto_id):
    if not requiere_login():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    # función del MODEL
    agregar_producto_carrito(cliente_id, producto_id)
    return redirect('/cliente/carrito')

def view_carrito(param):
    if not requiere_login():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    productos = obtener_carrito(cliente_id)
    return render_template("carrito.html", productos=productos)

def carrito_modificar_cantidad(param, request):
    # La tabla carrito no tiene cantidad
    return redirect('/cliente/carrito')

def carrito_eliminar_producto(param, request):
    if not requiere_login():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    producto_id = request.form.get('producto_id')
    eliminar_producto_carrito(cliente_id, producto_id)
    return redirect('/cliente/carrito')

def carrito_vaciar(param):
    if not requiere_login():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    vaciar_carrito(cliente_id)
    return redirect('/cliente/carrito')


##########################################################################
# WISHLIST
##########################################################################

def agregar_producto_wishlist(param, request, producto_id):
    if not requiere_login():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    agregar_wishlist(cliente_id, producto_id)
    return redirect('/cliente/wishlist')

def view_wishlist(param):
    if not requiere_login():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    productos = obtener_wishlist(cliente_id)
    return render_template("wishlist.html", productos=productos)

def eliminar_wishlist(param):
    if not requiere_login():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    producto_id = request.form.get('producto_id')
    eliminar_wishlist(cliente_id, producto_id)
    return redirect('/cliente/wishlist')


##########################################################################
# PEDIDOS
##########################################################################

def pedidos_usuario(param):
    if not requiere_login():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    pedidos = obtener_pedidos_cliente(cliente_id)
    return render_template("pedidosusuario.html", pedidos=pedidos)

def pedidos_admin_pagina(param):
    if not es_admin():
        return redirect('/login')

    pedidos = obtener_pedidos_admin()
    return render_template("pedidosadmin.html", pedidos=pedidos)

def pedidos_admin_modificarestado(param):
    if not es_admin():
        return redirect('/login')

    pedido_id = request.form.get('pedido_id')
    estado = request.form.get('estado')
    actualizar_estado_pedido(pedido_id, estado)
    return redirect('/admin/pedidosadmin')


##########################################################################
# ADMIN - PRODUCTOS
##########################################################################

def add_product_pagina(param):
    if not es_admin():
        return redirect('/login')
    return render_template("add_product.html")

def guardar_producto(param):
    return redirect('/admin/estadisticas')


##########################################################################
# MI CUENTA
##########################################################################

def miCuenta_pagina(param):
    if not requiere_login():
        return redirect('/login')
    return render_template("miCuenta.html")

##########################################################################
# FUNCIONES EXTRA 
##########################################################################

def view_carrito(param):
    return render_template("carrito.html")

def carrito_modificar_cantidad(param):
    return redirect('/cliente/carrito')

def carrito_eliminar_producto(param):
    return redirect('/cliente/carrito')

def carrito_vaciar(param):
    return redirect('/cliente/carrito')

def view_wishlist(param):
    return render_template("wishlist.html")

def pedidos_usuario(param):
    return render_template("pedidosusuario.html")

def pedidos_admin_pagina(param):
    return render_template("pedidosadmin.html")

def pedidos_admin_modificarestado(param):
    return redirect('/admin/pedidosadmin')

def add_product_pagina(param):
    return render_template("add_product.html")

def guardar_producto(param):
    return redirect('/admin/add_product')

def paginaNoEncontrada(name):
    
    res='Pagina "{}" no encontrada<br>'.format(name)
    if not requiere_login():
        res+='<a href="{}">{}</a>'.format("/login","Login")
    elif es_admin():
        res+='<a href="{}">{}</a>'.format("/admin","Home")
    else:
        res+='<a href="{}">{}</a>'.format("/cliente","Home")
    return res
'''

from flask import request, session, redirect, render_template, url_for
import model
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
from appConfig import config

##########################################################################
# CONTROL DE SESIÓN Y ROLES
##########################################################################

def requiere_login():
    return session.get('usuario') is not None

def es_admin():
    usuario = session.get('usuario')
    if not usuario:
        return False
    return usuario.get('tipo') == 'admin'

def cerrarSesion():
    session.clear()
    return redirect('/login')

##########################################################################
# PÁGINAS PRINCIPALES
##########################################################################

def home_pagina(param):
    if not requiere_login():
        return redirect('/login')

    if es_admin():
        return redirect('/admin/estadisticas')

    return render_template("index.html")

def catalogo_pagina(param):
    if not requiere_login():
        return redirect('/login')

    if es_admin():
        return redirect('/admin/estadisticas')

    productos = model.obtenerTodosLosProductos()
    lista_productos = []

    for p in productos:
        lista_productos.append({
            'id': p[0],
            'nombre': p[1],
            'precio_unidad': p[2],
            'img': p[3],
            'descripcion': p[4],
            'ventas': p[5]
        })

    return render_template("catalogo.html", productos=lista_productos)

def producto_pagina(param, pid):
    if not requiere_login():
        return redirect('/login')

    if es_admin():
        return redirect('/admin/estadisticas')

    fila = model.obtenerProductoPorId(pid)
    producto = None

    if fila:
        producto = {
            'id': fila[0],
            'nombre': fila[1],
            'precio_unidad': fila[2],
            'img': fila[3],
            'descripcion': fila[4]
        }

    return render_template("producto.html", producto=producto)

##########################################################################
# LOGIN / SIGNUP
##########################################################################

def login_pagina(param):
    return render_template("login.html")

def signup_pagina(param):
    return render_template("signup.html")

def signup(param):
    nombre = request.form.get('nombre', '').strip()
    mail = request.form.get('email', '').strip()
    contrasena = request.form.get('contrasena', '').strip()

    di = {
        'nombre': nombre,
        'mail': mail,
        'contrasena': contrasena,
        'tipo': 'cliente'
    }

    if model.crearCliente(di):
        return redirect('/login')

    param['error'] = "No se pudo crear el usuario"
    return render_template("signup.html", param=param)

# ================= INICIO NUEVO (alineación con route.py) =================
def ingresoUsuarioValido(param):
    email = request.form.get('email', '').strip()
    contrasena = request.form.get('contrasena', '').strip()

    result = {}
    if model.validarClientePorMailYContrasena(result, email, contrasena):
        session.clear()
        session['usuario'] = {
            'id': result['id'],
            'nombre': result['nombre'],
            'tipo': result['tipo'],
            'mail': result['mail']
        }

        if result['tipo'] == 'admin':
            return redirect('/admin/estadisticas')

        return redirect('/cliente/home')

    param['error'] = "Mail o contraseña incorrectos"
    return render_template("login.html", param=param)
# ================== FIN NUEVO =============================================

##########################################################################
# CREATOTE
##########################################################################

def creatote_pagina(param):
    if not requiere_login():
        return redirect('/login')
    return render_template("creatote.html")

def creatote_formulario(param):
    return redirect('/cliente/carrito')

##########################################################################
# CARRITO
##########################################################################

def agregar_producto_carrito(param, request, producto_id):
    cliente_id = session['usuario']['id']
    model.agregar_producto_carrito(cliente_id, producto_id)
    return redirect('/cliente/carrito')

def view_carrito(param):
    cliente_id = session['usuario']['id']
    productos = model.obtener_carrito(cliente_id)
    return render_template("carrito.html", productos=productos)

def carrito_modificar_cantidad(param, request):
    return redirect('/cliente/carrito')

def carrito_eliminar_producto(param, request):
    cliente_id = session['usuario']['id']
    producto_id = request.form.get('producto_id')
    model.eliminar_producto_carrito(cliente_id, producto_id)
    return redirect('/cliente/carrito')

def carrito_vaciar(param):
    cliente_id = session['usuario']['id']
    model.vaciar_carrito(cliente_id)
    return redirect('/cliente/carrito')

##########################################################################
# WISHLIST
##########################################################################

def agregar_producto_wishlist(param, request, producto_id):
    cliente_id = session['usuario']['id']
    model.agregar_wishlist(cliente_id, producto_id)
    return redirect('/cliente/wishlist')

def view_wishlist(param):
    cliente_id = session['usuario']['id']
    productos = model.obtener_wishlist(cliente_id)
    return render_template("wishlist.html", productos=productos)

def eliminar_wishlist(param):
    cliente_id = session['usuario']['id']
    producto_id = request.form.get('producto_id')
    model.eliminar_wishlist(cliente_id, producto_id)
    return redirect('/cliente/wishlist')

##########################################################################
# PEDIDOS
##########################################################################

def pedidos_usuario(param):
    cliente_id = session['usuario']['id']
    pedidos = model.obtener_pedidos_cliente(cliente_id)
    return render_template("pedidosusuario.html", pedidos=pedidos)

def pedidos_admin_pagina(param):
    pedidos = model.obtener_pedidos_admin()
    return render_template("pedidosadmin.html", pedidos=pedidos)

def pedidos_admin_modificarestado(param):
    pedido_id = request.form.get('pedido_id')
    estado = request.form.get('estado')
    model.actualizar_estado_pedido(pedido_id, estado)
    return redirect('/admin/pedidosadmin')

##########################################################################
# ADMIN - PRODUCTOS
##########################################################################

def add_product_pagina(param):
    if not es_admin():
        return redirect('/login')
    return render_template("add_product.html")

def guardar_producto(param):
    return redirect('/admin/estadisticas')

##########################################################################
# MI CUENTA
##########################################################################

def miCuenta_pagina(param):
    return render_template("miCuenta.html")

##########################################################################
#UPLOAD (EL DE MARIANO)
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