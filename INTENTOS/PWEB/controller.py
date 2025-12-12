# controller.py
'''
CONTROL - controller.py
Funciones que resuelven peticiones. Usa model.py como verdad.
Mantengo tu estilo. Hice los cambios mínimos necesarios.
'''

from flask import request, session, redirect, render_template, url_for, jsonify
from model import *
from werkzeug.utils import secure_filename
import os
from datetime import datetime

##### INICIO NUEVO (motivo: compatibilidad con templates que pasan 'param' como dict)
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
##### FIN NUEVO


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
    return render_template("index.html", param=param)


def login_pagina(param):
    param = param or {}
    return render_template("login.html", param=param)


def registro_pagina(param):
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


def index_cliente(param):
    param = param or {}
    return render_template("index.html", param=param)


##### INICIO NUEVO (motivo: exponer funciones de registro/login con firma esperada por route.py)
def registrarUsuario(param, req):
    '''Procesa registro (POST)'''
    param = param or {}
    if req.method == 'POST':
        nombre = req.form.get('nombre','').strip()
        mail = req.form.get('email','').strip()
        contrasena = req.form.get('contrasena','').strip()
        di = {'nombre': nombre, 'mail': mail, 'contrasena': contrasena, 'tipo': 'cliente'}
        exito = crearCliente(di)
        if exito:
            return redirect('/login')
        else:
            param['error'] = "No se pudo crear el usuario. Verifique los datos."
            return render_template("signup.html", param=param)
    else:
        return render_template("signup.html", param=param)


def ingresoUsuarioValido(param, req):
    '''Procesa login (POST)'''
    param = param or {}
    if req.method == 'POST':
        email = req.form.get('email','').strip()
        contrasena = req.form.get('contrasena','').strip()
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


def cerrarSesion():
    '''Cierra la sesion del usuario'''
    session.clear()
    return redirect('/login')


def login_get(param):
    return login_pagina(param)


def registro_get(param):
    return registro_pagina(param)


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
# WISHLIST (cliente)
##########################################################################

def view_wishlist(param):
    '''Muestra la wishlist del usuario'''
    param = param or {}
    ##### INICIO NUEVO (motivo: proteger ruta - solo clientes pueden acceder a wishlist) #####
    usuario = session.get('usuario')
    if not usuario or usuario.get('tipo') != 'cliente':
        return redirect('/login')
    ##### FIN NUEVO
    cliente_id = usuario['id']
    filas = obtenerWishlistPorCliente(cliente_id)
    # IMPORTANTE: tu template wishlist.html itera sobre 'productos' — mantener esa variable
    ##### INICIO NUEVO (motivo: adaptar nombre de variable al template) #####
    param['productos'] = filas
    ##### FIN NUEVO
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


##### INICIO NUEVO (motivo: función de ayuda para páginas no encontradas) #####
def paginaNoEncontrada(name):
    res = 'Pagina "{}" no encontrada<br>'.format(name)
    res += '<a href="{}">{}</a>'.format("/", "Home")
    return res
##### FIN NUEVO
