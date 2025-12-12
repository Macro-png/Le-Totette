# controller.py
from flask import request, session, redirect, render_template, url_for, flash
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
from appConfig import config
import model

ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.gif'}

# ---------------- Helper: guardar archivo en uploads ----------------
def guardar_archivo(file_obj):
    """
    Guarda archivo en static/uploads con nombre único.
    Devuelve nombre del archivo o None.
    """
    if not file_obj or file_obj.filename == '':
        return None
    filename = secure_filename(file_obj.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXT:
        return None
    unique_name = uuid4().hex + ext
    destino = os.path.join(config['upload_folder'], unique_name)
    try:
        file_obj.save(destino)
    except Exception as e:
        print("Error guardando archivo:", e)
        return None
    return unique_name

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

# ---------------- Decoradores ----------------
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
    # redirigir a home (según tu preferencia) o a wishlist:
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
    imagen = guardar_archivo(request.files.get("imagen"))
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
    imagen = guardar_archivo(request.files.get("imagen"))
    form['img'] = imagen or ''
    if model.crearProducto(form):
        flash("Producto creado exitosamente.", "success")
        return redirect(url_for("admin_estadisticas_route"))
    else:
        flash("Error creando producto.", "error")
        return render_template("add_product.html")










OTRO
'''### info:
    CONTROL
    Contiene las funciones que resuelven las peticiones.
    - Usa el model.py (ya adaptado a la BD real) como verdad.
    - Mantengo tu estilo: nombres en español, funciones pequeñas, comentarios en español.
    - No modifico model.py. Todas las llamadas a la BD se realizan a través de las funciones del model.
'''
from flask import request, session, redirect, render_template, url_for, jsonify
from model import *
from werkzeug.utils import secure_filename
import os
from datetime import datetime

##### INICIO NUEVO (motivo: compatibilidad con templates que pasan 'param' como dict;
# convierte render_template(..., param=param) en render_template con variables desempaquetadas)
_original_render_template = render_template
def render_template(template_name, *args, **kwargs):
    # Si el caller pasó 'param' como dict, lo desempaquetamos en el contexto de Jinja.
    param = kwargs.pop('param', None)
    if isinstance(param, dict):
        # mezclamos param con otros kwargs (otros kwargs prevalecen)
        new_kwargs = {}
        new_kwargs.update(param)
        new_kwargs.update(kwargs)
        return _original_render_template(template_name, *args, **new_kwargs)
    # comportamiento por defecto
    return _original_render_template(template_name, *args, **kwargs)
##### FIN NUEVO


##########################################################################
# + + I N I C I O + + FUNCIONES DE PAGINAS PRINCIPALES + + + + + + + + + +
##########################################################################

def home_pagina(param):
    '''Carga la pagina del home con listado de productos'''
    param = param or {}
    ##### INICIO NUEVO (motivo: asegurar que home no se muestre ...hay sesión; requisito: "home NUNCA se muestre si no hay sesión")
    # Si no hay usuario en session, redirijo al login (mínimo cambio para proteger la vista)
    usuario = session.get('usuario')
    if not usuario:
        return redirect('/login')
    ##### FIN NUEVO
    productos = obtenerTodosLosProductos()
    # INICIO NUEVO (motivo: mapear lista de tuplas a lista de dicts para templates que usan producto['clave'])
    lista_productos = []
    for p in productos:
        lista_productos.append(_producto_tuple_a_dict(p))
    param['productos'] = lista_productos
    # FIN NUEVO
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
    # INICIO NUEVO (motivo: asegurar que 'producto' en template sea un dict accesible por keys)
    producto_dict = _producto_tuple_a_dict(fila) if fila else None
    param['producto'] = producto_dict
    # FIN NUEVO
    return render_template("producto.html", param=param)

def index_cliente(param):
    param = param or {}
    return render_template("index.html", param=param)

def registrarUsuario(param):
    # (tu implementación original; no modificado)
    return render_template("signup.html", param=param)

def ingresoUsuarioValido(param, req):
    # (tu implementación original; no modificado)
    pass

def cerrarSesion(param):
    # (tu implementación original; no modificado)
    pass

def login_get(param):
    # (tu implementación original; no modificado)
    pass

def registro_get(param):
    # (tu implementación original; no modificado)
    pass

def editarUsuario_pagina(param):
    # (tu implementación original; no modificado)
    pass

def actualizarDatosDeUsuarios(param):
    # (tu implementación original; no modificado)
    pass

##########################################################################
# + + I N I C I O + + CARRITO (RUTAS LÓGICAS) + + + + + + + + + + + + + +
##########################################################################

def view_carrito(param):
    '''Muestra el carrito del usuario'''
    param = param or {}
    ##### INICIO NUEVO (motivo: proteger ruta - solo clientes pueden ver el carrito)
    usuario = session.get('usuario')
    if not usuario or usuario.get('tipo') != 'cliente':
        return redirect('/login')
    ##### FIN NUEVO
    cliente_id = usuario['id']
    filas = obtenerCarritoPorCliente(cliente_id)
    param['carrito'] = filas
    return render_template("carrito.html", param=param)

def add_to_cart_ajax():
    # (tu implementación original; no modificado)
    pass

def remove_from_cart_ajax():
    # (tu implementación original; no modificado)
    pass

def view_wishlist(param):
    '''Muestra la wishlist del usuario'''
    param = param or {}
    ##### INICIO NUEVO (motivo: proteger ruta - solo clientes pueden acceder a wishlist)
    usuario = session.get('usuario')
    if not usuario or usuario.get('tipo') != 'cliente':
        return redirect('/login')
    ##### FIN NUEVO
    cliente_id = usuario['id']
    filas = obtenerWishlistPorCliente(cliente_id)
    # INICIO NUEVO (motivo: convertir filas (tuplas) a lista de dicts para que template use producto['nombre'])
    lista = []
    for r in filas:
        lista.append(_wishlist_row_a_dict(r))
    param['wishlist'] = lista
    # FIN NUEVO
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
# + + I N I C I O + + PEDIDOS (CLIENTE y ADMIN) + + + + + + + + + + + + +
##########################################################################

def crear_pedido_desde_carrito(param):
    '''Crea pedido a partir del carrito del usuario.
       Flujo simplificado: recibe cliente_id desde session, toma productos del carrito,
       calcula precio_total como suma de precio_unidad (no considera cantidades en carrito).
       Inserta pedido + detalle_pedido y limpia carrito.
       NOTA: este flujo mantiene la estructura mínima para que funcione con la BD real.
    '''
    # (Tu implementación original aquí — no la toqué)

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

# INICIO NUEVO
# Motivo: normalizar y aceptar tanto 'retirar' (valor del select en el template)
# como 'para retirar' (valor esperado en la BD). Evita que el admin no pueda actualizar.
def actualizar_estado_pedido_ajax():
    '''Recibe POST AJAX con pedido_id y estado -> actualiza el pedido en la BD'''
    try:
        # Acepto distintos nombres de campos que el JS pueda enviar
        pedido_id = request.form.get('pedido_id') or request.form.get('pedidoId') or request.form.get('id')
        estado = request.form.get('estado')
        if not pedido_id or not estado:
            return jsonify({'ok': False, 'msg': 'Faltan parametros'})

        # Normalizo: si viene 'retirar', lo mapearé a 'para retirar' antes de persistir.
        if estado == 'retirar':
            estado_db = 'para retirar'
        else:
            estado_db = estado

        # Acepto ambos en la validación para mayor tolerancia (no cambio la BD).
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
# FIN NUEVO

def estadisticas_pagina(param):
    param = param or {}
    if not session.get('usuario') or session.get('usuario').get('tipo') != 'admin':
        return redirect('/login')
    totemascomprado = productoMasVendido()
    nombre = totemascomprado[0] if totemascomprado else ''
    cantidad = totemascomprado[1] if totemascomprado else 0
    param['totemascomprado_nombre'] = nombre
    param['totemascomprado_cantidaddeventas'] = cantidad
    categorias = ventasPorCategoria()
    # INICIO NUEVO (motivo: convertir filas (tuplas) a dicts {'nombre','ventas'} para coincidir con template)
    lista_cat = []
    for c in categorias:
        lista_cat.append(_categoria_row_a_dict(c))
    param['categorias'] = lista_cat
    # FIN NUEVO
    return render_template("estadisticas.html", param=param)

def add_product_pagina(param):
    param = param or {}
    if not session.get('usuario') or session.get('usuario').get('tipo') != 'admin':
        return redirect('/login')
    return render_template("add_product.html", param=param)

def guardar_producto(param):
    # (tu implementación original; no modificado)
    pass

def requiere_login(param):
    '''Helper simple para verificar sesion'''
    return session.get('usuario') is not None

# FIN controller.py

########## ERROR NO ENCONTRADA ###########
def paginaNoEncontrada(name):
    ''' Info:
      Retorna una pagina generica indicando que la ruta 'name' no existe
    '''
    res='Pagina "{}" no encontrada<br>'.format(name)
    res+='<a href="{}">{}</a>'.format("/","Home")
    
    return res

