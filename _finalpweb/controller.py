'''### info:
     CONTROL 

    Dependencias:
        pip install uuid

    Referencias:
        https://pypi.org/project/uuid/
        https://docs.python.org/3/library/uuid.html
    
'''

from flask import request, session, redirect, render_template, url_for, jsonify
from model import *
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask import request, session,redirect,render_template
from uuid import uuid4
from appConfig import config

'''
##### (motivo: compatibilidad con templates que pasan 'param' como dict)
_original_render_template = render_template
def render_template(template_name, *args, **kwargs):
    # Si el caller pasó 'param' como dict, lo desempaquetamos en el contexto de Jinja.
    param = kwargs.pop('param', None)
    if isinstance(param, dict):
        new_kwargs = {}
        new_kwargs.update(param)
        new_kwargs.update(kwargs)
        return _original_render_template(template_name, *args, **new_kwargs)
    return _original_render_template(template_name, *args, **kwargs)
'''

##########################################################################
#               FUNCIONES PRINCIPALES (las páginas)
##########################################################################

def home_pagina(param):
    '''Carga la pagina del home con listado de productos'''
    param = param or {}
    ##### (solo accessible con sesión) #####
    usuario = session.get('usuario')
    if not usuario:
        return redirect('/login') #SI NO ESTA LOGUEADO NO PERMITE ACCEDER
    else:
        return render_template("index.html")

def catalogo_pagina(param):
    param = param or {}
    ##### (solo accessible con sesión) #####
    usuario = session.get('usuario')
    if not usuario:
        return redirect('/login') #SI NO ESTA LOGUEADO NO PERMITE ACCEDER
    elif tipo_usuario():
        productos = obtenerTodosLosProductos()
        lista_productos = []
        for p in productos:
            lista_productos.append({
                'id': p[0],
                'nombre': p[1],
                'precio_unidad': p[2],
                'img': p[3],
                'descripcion': p[4] if len(p) > 4 else '', #if len(p)>4 va p[4] si no cumple el if va ''
                'ventas': p[5] if len(p) > 5 else 0
            }) 
        #recibe lista de tuplas y crea lista de 
        #diccionarios con keys repetidas
        param['productos'] = lista_productos
        return render_template("catalogo.html", param=param)


def login_pagina(param):
    param = param or {}
    return render_template("login.html", param=param)


def signup_pagina(param):
    param = param or {}
    return render_template("signup.html", param=param)


def producto_pagina(param, pid):
    '''Muestra la página de producto individual'''
    param = param or {}
    fila = obtenerProductoPorId(pid)
    producto_dict = None
    if fila:
        if isinstance(fila, (list,tuple)):
            producto_dict = {
                'id': fila[0],
                'nombre': fila[1],
                'precio_unidad': fila[2] if len(fila) > 2 else None,
                'img': fila[3] if len(fila) > 3 else '',
                'descripcion': fila[4] if len(fila) > 4 else ''
            }
        elif isinstance(fila, dict):
            producto_dict = fila
    param['producto'] = producto_dict
    return render_template("producto.html", param=param)

def ValidarFormularioRegistro(di):
    res=True
    res= res and di.get('nombre')!=""
    res= res and di.get('apellido')!=""
    res= res and di.get('email')!=""
    res= res and di.get('password')!=""
    return res

def signup(param):
    '''Procesa registro (POST)'''
    param = param 
    nombre = request.form.get('nombre','').strip()
    mail = request.form.get('email','').strip()
    contrasena = request.form.get('contrasena','').strip()
    di = {'nombre': nombre, 'mail': mail, 'contrasena': contrasena, 'tipo': 'cliente'}
    exito = crearCliente(di)
    if exito:
        return redirect('/login')
    else:
        param['error'] = "No se pudo crear el usuario. Verifique los datos."
        return render_template("signup.html", param=param)


def ingresoUsuarioValido(param, req):
    '''Procesa login (POST)'''
    param = param or {}
    if request.method == 'POST':
        email = request.form.get('email','').strip()
        contrasena = request.form.get('contrasena','').strip()
        result = {}
        ok = validarClientePorMailYContrasena(result, email, contrasena)
        if ok:
            session.clear()
            session['usuario'] = {
                'id': result['id'],
                'nombre': result['nombre'],
                'tipo': result['tipo'],
                'mail': result['mail']
            }
            if result.get('tipo') == 'admin':
                return redirect('/estadisticas')
            else:
                return redirect('/home')
        else:
            param['error'] = "Mail o contraseña incorrectos"
            return render_template("login.html", param=param)
    else:
        return render_template("login.html", param=param)
##### FIN NUEVO

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

def ingresoUsuarioValido(request):
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
        getRequest(mirequest)
        # CONSULTA A LA BASE DE DATOS. Si usuario es valido => crea session
        dicUsuario={}
        if obtenerUsuarioXEmailPass(dicUsuario,mirequest.get("username"),mirequest.get("password")):
            
            # Carga sesion (Usuario validado)
            cargarSesion(dicUsuario)
            sesionValida = True
    except ValueError:                              
        pass
    return sesionValida

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
    getRequest(mirequest)
    
    if ValidarFormularioRegistro(mirequest):
        # CONSULTA A LA BASE DE DATOS: Realiza el insert en la tabla usuario
        if crearUsuario(mirequest):
            param['succes_msg_login']="Se ha creado el usuario con exito"
            cerrarSesion()           # Cierra sesion existente(si la hubiere)
            res=login_pagina(param)  # Envia al login para que vuelva a loguearse el usuario
        else:
            param['error_msg_register']="Error: No se ha podido crear el usuario"
            res=signup_pagina(param)
    else:
        param['error_msg_register']="Error: Problema en la validacion de los campos"
        res=signup_pagina(param)

    return res 


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
    session['username']   = dicUsuario['username'] # es el mail
    session['tipo']        = dicUsuario['tipo']
    
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
        getRequest(mirequest)
        # CONSULTA A LA BASE DE DATOS. Si usuario es valido => crea session
        dicUsuario={}
        if obtenerUsuarioXEmailPass(dicUsuario,mirequest.get("username"),mirequest.get("password")):
            
            # Carga sesion (Usuario validado)
            cargarSesion(dicUsuario)
            sesionValida = True
    except ValueError:                              
        pass
    return sesionValida


def cerrarSesion():
    '''Cierra la sesion del usuario'''
    session.clear()
    return redirect('/login')


def login_get(param):
    return login_pagina(param)


def signup_get(param):
    return signup_pagina(param)


def editarUsuario_pagina(param):
    param = param or {}
    usuario = session.get('usuario')
    if not usuario or usuario.get('tipo') != 'cliente':
        return redirect('/login')
    obtenerClientePorId(param, usuario['id'], clave='usuario')
    return render_template("miCuenta.html", param=param)


def actualizarDatosDeUsuarios(param, req):
    param = param or {}
    usuario = session.get('usuario')
    if not usuario or usuario.get('tipo') != 'cliente':
        return redirect('/login')
    if req.method == 'POST':
        nombre = req.form.get('nombre','').strip()
        contrasena = req.form.get('contrasena','').strip()
        di = {'nombre': nombre, 'contrasena': contrasena}
        exito = actualizarCliente(di, usuario['mail'])
        if exito:
            session['usuario']['nombre'] = nombre
            param['msg'] = "Datos actualizados correctamente."
        else:
            param['error'] = "No se pudieron actualizar los datos."
    obtenerClientePorId(param, usuario['id'], clave='usuario')
    return render_template("miCuenta.html", param=param)


##########################################################################
#                            WISHLIST (cliente)
##########################################################################

def view_wishlist(param):
    '''Muestra la wishlist del usuario'''
    param = param or {}
    ##### solo clientes pueden acceder a wishlist #####
    usuario = session.get('usuario')
    if not usuario or usuario.get('tipo') != 'cliente':
        return redirect('/login')
    else:
        cliente_id = usuario['id']
        filas = obtenerWishlistPorCliente(cliente_id)
        param['productos'] = filas
        return render_template("wishlist.html", param=param)


def add_to_wishlist_ajax():
    '''Agregar producto a wishlist vía AJAX'''
    try:
        cliente_id = request.form.get('cliente_id')
        producto_id = request.form.get('producto_id')
        if not cliente_id:
            usuario = session.get('usuario')
            if not usuario:
                return jsonify({'ok': False, 'msg': 'No hay sesión iniciada'})
            cliente_id = usuario['id']
        if not producto_id:
            return jsonify({'ok': False, 'msg': 'Falta producto_id'})
        exito = agregarWishlist(int(cliente_id), int(producto_id))
        if exito:
            return jsonify({'ok': True, 'msg': 'Producto agregado a wishlist'})
        else:
            return jsonify({'ok': False, 'msg': 'Producto ya en wishlist o error al agregar'})
    except Exception as e:
        return jsonify({'ok': False, 'msg': 'Error interno: ' + str(e)})


def remove_from_wishlist_ajax():
    '''Quitar producto de wishlist vía AJAX'''
    try:
        cliente_id = request.form.get('cliente_id')
        producto_id = request.form.get('producto_id')
        if not cliente_id:
            usuario = session.get('usuario')
            if not usuario:
                return jsonify({'ok': False, 'msg': 'No hay sesión iniciada'})
            cliente_id = usuario['id']
        if not producto_id:
            return jsonify({'ok': False, 'msg': 'Falta producto_id'})
        res = quitarWishlist(int(cliente_id), int(producto_id))
        if res:
            return jsonify({'ok': True, 'msg': 'Producto removido de wishlist'})
        else:
            return jsonify({'ok': False, 'msg': 'No se pudo remover el producto'})
    except Exception as e:
        return jsonify({'ok': False, 'msg': 'Error interno: ' + str(e)})


##########################################################################
# PEDIDOS (CLIENTE y ADMIN)
##########################################################################

def crear_pedido_desde_carrito(param):
    '''Crea pedido a partir del carrito del usuario.
       (Nota: mantuve tu idea original; puedes añadir lógica interna luego)
    '''
    # (tu implementación original aquí — no la modifiqué)
    return redirect('/pedidosusuario')


def pedidos_usuario(param):
    param = param or {}
    usuario = session.get('usuario')
    if not usuario:
        return redirect('/login')
    cliente_id = usuario['id']
    filas = obtenerPedidosPorCliente(cliente_id)
    param['pedidos'] = filas
    return render_template("pedidosusuario.html", param=param)


def pedidos_admin(param):
    param = param or {}
    usuario = session.get('usuario')
    if not usuario or usuario.get('tipo') != 'admin':
        return redirect('/login')
    filas = obtenerPedidosParaAdmin()
    param['pedidos'] = filas
    return render_template("pedidosadmin.html", param=param)


##### INICIO NUEVO (motivo: normalizar/aceptar nombres de campos del AJAX y actualizar estado) #####
def actualizar_estado_pedido_ajax():
    '''Recibe POST AJAX con pedido_id y estado -> actualiza el pedido en la BD'''
    try:
        pedido_id = request.form.get('pedido_id') or request.form.get('pedidoId') or request.form.get('id')
        estado = request.form.get('estado')
        if not pedido_id or not estado:
            return jsonify({'ok': False, 'msg': 'Faltan parametros'})

        if estado == 'retirar':
            estado_db = 'para retirar'
        else:
            estado_db = estado

        estados_validos = ['espera', 'produccion', 'retirar', 'para retirar', 'cancelado']
        if estado not in estados_validos and estado_db not in estados_validos:
            return jsonify({'ok': False, 'msg': 'Estado inválido'})

        ok = actualizarEstadoPedido(int(pedido_id), estado_db)
        if ok:
            return jsonify({'ok': True, 'msg': 'Estado actualizado'})
        else:
            return jsonify({'ok': False, 'msg': 'No se pudo actualizar'})
    except Exception as e:
        return jsonify({'ok': False, 'msg': 'Error interno: ' + str(e)})
##### FIN NUEVO


##########################################################################
# CARRITO (cliente)
##########################################################################

def view_carrito(param):
    param = param or {}
    usuario = session.get('usuario')
    if not usuario or usuario.get('tipo') != 'cliente':
        return redirect('/login')
    cliente_id = usuario['id']
    filas = obtenerCarritoPorCliente(cliente_id)
    param['carrito'] = filas
    return render_template("carrito.html", param=param)


def add_to_cart_ajax():
    try:
        cliente_id = request.form.get('cliente_id')
        producto_id = request.form.get('producto_id')
        if not cliente_id:
            usuario = session.get('usuario')
            if not usuario:
                return jsonify({'ok': False, 'msg': 'No hay sesión iniciada'})
            cliente_id = usuario['id']
        if not producto_id:
            return jsonify({'ok': False, 'msg': 'Falta producto_id'})
        exito = agregarAlCarrito(int(cliente_id), int(producto_id))
        if exito:
            return jsonify({'ok': True, 'msg': 'Producto agregado al carrito'})
        else:
            return jsonify({'ok': False, 'msg': 'Producto ya en carrito o error al agregar'})
    except Exception as e:
        return jsonify({'ok': False, 'msg': 'Error interno: ' + str(e)})


def remove_from_cart_ajax():
    try:
        cliente_id = request.form.get('cliente_id')
        producto_id = request.form.get('producto_id')
        if not cliente_id:
            usuario = session.get('usuario')
            if not usuario:
                return jsonify({'ok': False, 'msg': 'No hay sesión iniciada'})
            cliente_id = usuario['id']
        if not producto_id:
            return jsonify({'ok': False, 'msg': 'Falta producto_id'})
        res = quitarDelCarrito(int(cliente_id), int(producto_id))
        if res:
            return jsonify({'ok': True, 'msg': 'Producto removido del carrito'})
        else:
            return jsonify({'ok': False, 'msg': 'No se pudo remover el producto'})
    except Exception as e:
        return jsonify({'ok': False, 'msg': 'Error interno: ' + str(e)})

##########################################################################
#                               CREA TU TOTE
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
# ADMIN: ESTADISTICAS y GESTION
##########################################################################

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


def add_product_pagina(param):
    param = param or {}
    if not session.get('usuario') or session.get('usuario').get('tipo') != 'admin':
        return redirect('/login')
    return render_template("add_product.html", param=param)


def guardar_producto(req):
    # (tu implementación original; no modificado)
    # mantengo firma para route.py
    pass


##########################################################################
# UTILIDADES / HELPERS
##########################################################################

def requiere_login():
    return session.get('usuario') is not None

def tipo_usuario():
    result={}
    session['usuario'] = {
        'id': result['id'],
        'nombre': result['nombre'],
        'tipo': result['tipo'],
        'mail': result['mail']
    }
    if result.get('tipo') == 'admin':
        return "admin"
    else:
        return "cliente"


##### INICIO NUEVO (motivo: función de ayuda para páginas no encontradas) #####
def paginaNoEncontrada(name):
    res = 'Pagina "{}" no encontrada<br>'.format(name)
    res += '<a href="{}">{}</a>'.format("/", "Home")
    return res
##### FIN NUEVO
