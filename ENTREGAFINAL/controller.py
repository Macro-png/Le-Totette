from flask import render_template, redirect, request, session, url_for
import os
import model
from datetime import datetime
from werkzeug.utils import secure_filename
from uuid import uuid4
from appConfig import config

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def requiere_login():
    return 'usuario' in session


def es_admin():
    return requiere_login() and session['usuario']['tipo'] == 'admin'


def cerrar_sesion():
    session.clear()
    return redirect('/login')


# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------

def login_pagina(param):
    return render_template('login.html', param=param)


def signup_pagina(param):
    return render_template('signup.html', param=param)


def ingreso_usuario_valido(param):
    mail = request.form.get('email', '').strip()
    contrasena = request.form.get('contrasena', '').strip()

    result = {}
    if model.validarClientePorMailYContrasena(result, mail, contrasena):
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

    param['error'] = 'Mail o contraseña incorrectos'
    return render_template('login.html', param=param)



def signup(param):
    nombre = request.form.get("nombre")
    mail = request.form.get("mail")
    contrasena = request.form.get("contrasena")
    verificar = request.form.get("verificarcontrasena")

    # Validaciones básicas
    if not nombre or not mail or not contrasena:
        param["error"] = "Faltan datos"
        return render_template("signup.html", **param)

    if contrasena != verificar:
        param["error"] = "Las contraseñas no coinciden"
        return render_template("signup.html", **param)

    if len(contrasena) < 6:
        param["error"] = "Contraseña muy corta"
        return render_template("signup.html", **param)

    data = {
        "nombre": nombre,
        "mail": mail,
        "contrasena": contrasena
    }

    if model.crearCliente(data):
        return redirect(url_for("login"))

    param["error"] = "No se pudo crear la cuenta"
    return render_template("signup.html", **param)


# ---------------------------------------------------------------------------
# CLIENTE
# ---------------------------------------------------------------------------

def home_pagina(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    param['productos'] = model.obtenerTodosLosProductos()
    return render_template('index.html', param=param)


def catalogo_pagina(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    productos_db = model.obtenerTodosLosProductos()

    productos = []
    for p in productos_db:
        productos.append({
            'id': p[0],
            'nombre': p[1],
            'precio_unidad': p[2],
            'img': p[3],
            'descripcion': p[4],
        })

    param['productos'] = productos
    return render_template('catalogo.html', **param)



def producto_pagina(param, producto_id):
    if not requiere_login() or es_admin():
        return redirect('/login')

    producto = model.obtenerProductoPorId(producto_id)
    if not producto:
        return redirect('/cliente/home')

    param['producto'] = producto
    return render_template('producto.html', param=param)


# ---------------------------------------------------------------------------
# CREATOTE
# ---------------------------------------------------------------------------

def creatote_pagina(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    return render_template('creatote.html', param=param)


def creatote_formulario(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    # Acá después podés guardar archivo / diseño
    return redirect('/cliente/carrito')


# ---------------------------------------------------------------------------
# CARRITO
# ---------------------------------------------------------------------------

def ver_carrito(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    param['carrito'] = model.obtener_carrito(cliente_id)
    param['total'] = model.obtener_total_carrito(cliente_id)
    return render_template('carrito.html', param=param)


def agregar_producto_carrito(param, producto_id):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    model.agregar_producto_carrito(cliente_id, producto_id)
    return redirect('/cliente/carrito')


def eliminar_producto_carrito(param, producto_id):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    model.eliminar_producto_carrito(cliente_id, producto_id)
    return redirect('/cliente/carrito')


def vaciar_carrito(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    model.vaciar_carrito(cliente_id)
    return redirect('/cliente/carrito')


# ---------------------------------------------------------------------------
# WISHLIST
# ---------------------------------------------------------------------------

def view_wishlist(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    param['wishlist'] = model.obtener_wishlist(cliente_id)
    return render_template('wishlist.html', param=param)


def agregar_producto_wishlist(param, producto_id):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    model.agregar_wishlist(cliente_id, producto_id)
    return redirect('/cliente/wishlist')


def eliminar_wishlist(param, producto_id):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    model.eliminar_wishlist(cliente_id, producto_id)
    return redirect('/cliente/wishlist')


# ---------------------------------------------------------------------------
# PEDIDOS CLIENTE
# ---------------------------------------------------------------------------

def pedidos_usuario(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    param['pedidos'] = model.obtener_pedidos_cliente(cliente_id)
    return render_template('pedidosusuario.html', param=param)


def miCuenta_pagina(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    # datos desde la sesión
    param['nombre_usuario'] = session['usuario']['nombre']
    param['mail_usuario'] = session['usuario']['mail']

    return render_template('miCuenta.html', **param)



# ---------------------------------------------------------------------------
# ADMIN
# ---------------------------------------------------------------------------

def admin_estadisticas_pagina(param):
    if not es_admin():
        return redirect('/login')

    param['estadisticas'] = model.obtenerEstadisticas()
    return render_template('estadisticas.html', param=param)


def pedidos_admin_pagina(param):
    if not es_admin():
        return redirect('/login')

    param['pedidos'] = model.obtener_pedidos_admin()
    return render_template('pedidosadmin.html', param=param)


def pedidos_admin_modificar_estado(param, pedido_id):
    if not es_admin():
        return redirect('/login')

    estado = request.form.get('estado')
    model.actualizar_estado_pedido(pedido_id, estado)
    return redirect('/admin/pedidos')


def add_product_pagina(param):
    if not es_admin():
        return redirect('/login')

    return render_template('add_product.html', param=param)

def guardar_producto(param, diRequest):
    if not es_admin():
        return redirect('/login')

    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')

    # subir imagen
    #diResult = getRequest(diRequest)
    filename= upload_file(diRequest)

    # crear producto
    model.crear_producto(
        nombre=nombre,
        precio=precio,
        img=filename,
        descripcion=descripcion
    )


    return redirect('/admin/add_product')


##########################################################################
#                MANEJO DE  SUBIDA DE ARCHIVOS  
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
                    return filename_unique
 
                except:
                        pass
            else:
                diResult[key]={} # viene vacio el input del file upload
                
def getRequest(diResult):
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
 