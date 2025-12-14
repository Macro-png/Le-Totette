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
#                       VER PAGINAS ("GET")
##########################################################################

def login_pagina(param):
    return render_template("login.html")
  
    
def signup_pagina(param):
    return render_template("signup.html")
  
         
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


def home_pagina(param):
    if not requiere_login():
        return redirect('/login')

    if es_admin():
        return redirect('/admin/estadisticas')

    return render_template("index.html")
    
    
def ver_carrito(param):
    if not requiere_login():
        return redirect('/login')
    if es_admin():
        return redirect('/admin/estadisticas')
    cliente_id = session['usuario']['id']
    productos = model.obtener_carrito(cliente_id)
    return render_template("carrito.html", productos=productos)   
    
    
def creatote_pagina(param):
    if not requiere_login():
        return redirect('/login')
    if es_admin():
        return redirect('/admin/estadisticas')
    return render_template("creatote.html")
    
    
def view_wishlist(param):
    if not requiere_login():
        return redirect('/login')
    if es_admin():
        return redirect('/admin/estadisticas')
    cliente_id = session['usuario']['id']
    productos = model.obtener_wishlist(cliente_id)
    return render_template("wishlist.html", productos=productos)


def pedidos_usuario(param):
    if not requiere_login():
        return redirect('/login')
    if es_admin():
        return redirect('/admin/estadisticas')
    cliente_id = session['usuario']['id']
    pedidos = model.obtener_pedidos_cliente(cliente_id)
    return render_template("pedidosusuario.html", pedidos=pedidos)


def pedidos_admin_pagina(param):
    if not requiere_login():
        return redirect('/login')
    if not es_admin():
        return redirect('/cliente')
    pedidos = model.obtener_pedidos_admin()
    return render_template("pedidosadmin.html", pedidos=pedidos)
 
 
#CHEQUEAR MI CUENTA 
def miCuenta_pagina(param):
    if not requiere_login():
        return redirect('/login')
    if es_admin():
        return redirect('/admin/estadisticas')
    cliente_id = session['usuario']['id']
    nombre = model.obtener_nombre_cliente(cliente_id)
    return render_template("miCuenta.html", nombre)  
     
   
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
    
    
def add_product_pagina(param):
    if not requiere_login():
        return redirect('/login')
    if not es_admin():
        return redirect('/cliente')
    return render_template("add_product.html")


#HAY QUE HACER QUE SE CARGUE LA DATA VIEJA (no se como... capaz que al escribir el nombre
# de la totebag automaticamente se complete todo el resto y de ahi lo podes modificar y guardar (?))
def mod_product_pagina(param):
    if not requiere_login():
        return redirect('/login')
    if not es_admin():
        return redirect('/cliente')
    return render_template("mod_product.html")
    

#CHEQUEAR SI SIRVE
def estadisticas_pagina(param):
    param = param or {}
    if not session.get('usuario') or session.get('usuario').get('tipo') != 'admin':
        return redirect('/login')
    # Usar la función del model que devuelve el producto más vendido
    totem = productoMasVendido()
    # productoMasVendido() en model devuelve filas; adaptamos
    if totem:
        # si devuelve listado de filas -> tomamos primer registro
        if isinstance(totem, (list,tuple)) and len(totem) > 0 and isinstance(totem[0], (list,tuple)):
            fila = totem[0]
            nombre = fila[1] if len(fila) > 1 else fila[0]
            cantidad = fila[2] if len(fila) > 2 else 0
        else:
            # si devuelve tupla (nombre, cantidad) o similar
            try:
                nombre = totem[0]
                cantidad = totem[1]
            except Exception:
                nombre = ''
                cantidad = 0
    else:
        nombre = ''
        cantidad = 0
    param['totemascomprado_nombre'] = nombre
    param['totemascomprado_cantidaddeventas'] = cantidad

    categorias = ventasPorCategoria()
    # convertir a lista de dicts {'nombre','ventas'} para coincidir con template
    lista_cat = []
    for c in categorias or []:
        if isinstance(c, (list,tuple)):
            lista_cat.append({'nombre': c[0], 'ventas': c[1]})
        elif isinstance(c, dict):
            lista_cat.append(c)
        else:
            lista_cat.append({'nombre': str(c), 'ventas': 0})
    param['categorias'] = lista_cat
    return render_template("estadisticas.html", param=param)


##########################################################################
#                      FORMULARIOS Y POST
##########################################################################

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

    
def signup(param): #PARA CREAR CUENTA
    '''Procesa registro (POST)'''
    param = param 
    nombre = request.form.get('nombre','').strip()
    mail = request.form.get('email','').strip()
    contrasena = request.form.get('contrasena','').strip()
    di = {'nombre': nombre, 'mail': mail, 'contrasena': contrasena, 'tipo': 'cliente'}
    exito = model.crearCliente(di)
    if exito:
        return redirect('/login')
    else:
        param['error'] = "No se pudo crear el usuario. Verifique los datos."
        return render_template("signup.html", param=param)
    

def creatote_formulario(param): #cliente crea su propia tote
    return

def agregar_producto_carrito(param, request, producto_id): #desde la pagina producto
    return

def agregar_producto_wishlist(param, request, producto_id): #desde la pagina producto
    return
 
def carrito_modificar_cantidad(param, request): #el cosito que hay para aumentar los numeritos
    return

def carrito_eliminar_producto(param, request): #el tacho
    return

def eliminar_wishlist(param): #el tacho
    return            

def pedidos_admin_modificarestado(param): #MODIFICAR ESTADO DEL PEDIDO
    return

def guardar_producto(param): #cuando admin agrega un producto con exito
    return


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


##########################################################################
# PAGINA NO ENCONTRADA DE MARIANO
##########################################################################
def paginaNoEncontrada(name):
    ''' Info:
      Retorna una pagina generica indicando que la ruta 'name' no existe
    '''
    res='Pagina "{}" no encontrada<br>'.format(name)
    if not requiere_login():
        return res + '<a href="{}">{}</a>'.format("/","login")
    if es_admin():
        return res +'<a href="{}">{}</a>'.format("/","admin")
    res+='<a href="{}">{}</a>'.format("/","cliente")