'''### info:
    ENRUTAMIENTO DE LA PETICIÓN
    Este archivo conecta las URLs de Flask con las funciones del controller.
    Sigue el estilo original.

from flask import Flask, request, jsonify
##### INICIO NUEVO (motivo: redirect() ya se usaba; además necesitamos render_template para creatote)
from flask import redirect, render_template
##### FIN NUEVO
from controller import *

def route(app):

    # HOME / INDEX
    @app.route("/")
    @app.route("/home")
    def home():
        param = {}
        return home_pagina(param)

    ##### INICIO NUEVO (motivo: no existe catalogo_pagina en controller.py; usamos home_pagina que sí existe y muestra los productos)
    @app.route("/catalogo")
    def catalogo():
        param = {}
        return home_pagina(param)
    ##### FIN NUEVO

    @app.route("/creatote", methods=["GET", "POST"])
    def crea_tote_route():
        if request.method == "POST":
            return redirect('/home')
        return render_template("creatote.html")

    ##### INICIO NUEVO (motivo: alias necesario porque los templates llaman url_for('creatote'))
    @app.route("/creatote_alias", endpoint="creatote")
    def creatote_alias():
        return crea_tote_route()
    ##### FIN NUEVO


    # LOGIN / SIGNUP
    @app.route("/login", methods=["GET", "POST"])
    def login():
        param = {}
        if request.method == "POST":
            return ingresoUsuarioValido(param, request)
        else:
            return login_pagina(param)

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        param = {}
        if request.method == "POST":
            return registrarUsuario(param, request)
        else:
            return registro_pagina(param)

    @app.route("/logout")
    def logout_route():
        cerrarSesion()
        return redirect('/')

    # MI CUENTA (editar)
    @app.route("/miCuenta", methods=["GET"])
    def mi_cuenta():
        param = {}
        return editarUsuario_pagina(param)

    @app.route("/update_user", methods=["POST"])
    def update_user():
        param = {}
        return actualizarDatosDeUsuarios(param, request)

    # PRODUCTO (detalle)
    @app.route("/producto/<int:producto_id>", methods=["GET"])
    def producto_detalle(producto_id):
        param = {}
        return producto_pagina(param, producto_id)

    ##### INICIO NUEVO (motivo: alias para compatibilidad con templates que usan producto_route)
    @app.route("/producto_info/<int:pid>")
    def producto_route(pid):
        param = {}
        return producto_pagina(param, pid)
    ##### FIN NUEVO

    # CARRITO
    @app.route("/carrito", methods=["GET"])
    def ver_carrito():
        param = {}
        return view_carrito(param)

    ##### INICIO NUEVO (motivo: compatibilidad con templates que referencian estos endpoints)
    @app.route("/carrito_agregar", methods=["POST"])
    def carrito_agregar_route():
        return add_to_cart_ajax()

    @app.route("/carrito_quitar", methods=["POST"])
    def carrito_quitar_route():
        return remove_from_cart_ajax()
    ##### FIN NUEVO

    @app.route("/crear_pedido", methods=["POST","GET"])
    def crear_pedido():
        param={}
        return crear_pedido_desde_carrito(param)

    # WISHLIST
    @app.route("/wishlist", methods=["GET"])
    def ver_wishlist():
        param = {}
        return view_wishlist(param)

    ##### INICIO NUEVO (motivo: compatibilidad nombres en templates)
    @app.route("/wishlist_agregar", methods=["POST"])
    def wishlist_agregar_route():
        return add_to_wishlist_ajax()

    @app.route("/wishlist_quitar", methods=["POST"])
    def wishlist_quitar_route():
        return remove_from_wishlist_ajax()
    ##### FIN NUEVO

    # PEDIDOS USUARIO
    @app.route("/pedidosusuario", methods=["GET"])
    def ver_pedidos_usuario():
        param = {}
        return pedidos_usuario(param)

    # PEDIDOS ADMIN
    @app.route("/pedidosadmin", methods=["GET"])
    def ver_pedidos_admin():
        param = {}
        return pedidos_admin(param)

    @app.route("/actualizar_estado_pedido", methods=["POST"])
    def actualizar_estado_pedido():
        return actualizar_estado_pedido_ajax()

    # ESTADISTICAS (admin)
    @app.route("/estadisticas", methods=["GET"])
    def estadisticas():
        param = {}
        return estadisticas_pagina(param)

    # ADD PRODUCT (admin)
    @app.route("/add_product", methods=["GET"])
    def add_product():
        param = {}
        return add_product_pagina(param)

    @app.route("/guardar_producto", methods=["POST"])
    def guardar_producto_route():
        return guardar_producto(request)

    # RUTA POR DEFECTO PARA CUALQUIER OTRA URL (NOT FOUND)
    @app.route("/<path:name>", methods=["GET","POST"])
    def no_encontrada(name):
        try:
            return paginaNoEncontrada(name)
        except:
            return "Pagina '{}' no encontrada".format(name), 404
'''

'''### info:
    ENRUTAMIENTO DE LA PETICIÓN
    Este archivo conecta las URLs de Flask con las funciones del controller.
    Sigue el estilo original.


from flask import Flask, request, jsonify, redirect
from controller import *

def route(app):
    # HOME / INDEX
    @app.route("/")
    @app.route("/home")
    def home():
        param = {}
        return home_pagina(param)

    # CATALOGO
    @app.route("/catalogo", methods=["GET"])
    def catalogo():
        param = {}
        return catalogo_pagina(param)

    # PRODUCTO (detalle)
    @app.route("/producto/<int:pid>", methods=["GET"])
    def producto_route(pid):
        param = {}
        return producto_pagina(param, pid)

    # CREATOTE (diseña tu tote)
    @app.route("/creatote", methods=["GET", "POST"])
    def creatote_route():
        param = {}
        # si es POST, el controller creatote_pagina puede manejarlo según tu lógica
        if request.method == 'POST':
            return creatote_pagina(param)
        return creatote_pagina(param)

    # MI CUENTA
    @app.route("/mi-cuenta", methods=["GET", "POST"])
    def mi_cuenta_route():
        param = {}
        return editarUsuario_pagina(param)

    # WISHLIST
    @app.route("/wishlist", methods=["GET"])
    def wishlist_route():
        param = {}
        return view_wishlist(param)

    @app.route("/wishlist/agregar", methods=["POST"])
    def wishlist_agregar_route():
        return add_to_wishlist_ajax()

    @app.route("/wishlist/quitar", methods=["POST"])
    def wishlist_quitar_route():
        return remove_from_wishlist_ajax()

    # CARRITO
    @app.route("/carrito", methods=["GET"])
    def ver_carrito():
        param = {}
        return view_carrito(param)

    @app.route("/carrito/agregar", methods=["POST"])
    def carrito_agregar_route():
        return add_to_cart_ajax()

    @app.route("/carrito/quitar", methods=["POST"])
    def carrito_quitar_route():
        return remove_from_cart_ajax()

    # PEDIDOS USUARIO
    @app.route("/mis-pedidos", methods=["GET"])
    def ver_mis_pedidos():
        param = {}
        return pedidos_usuario(param)

    # PEDIDOS ADMIN
    @app.route("/admin/pedidos", methods=["GET"])
    def ver_pedidos_admin():
        param = {}
        return pedidos_admin(param)

    # ESTADISTICAS ADMIN
    @app.route("/admin/estadisticas", methods=["GET"])
    def estadisticas_route():
        param = {}
        return estadisticas_pagina(param)

    # LOGIN / SIGNUP
    @app.route("/login", methods=["GET", "POST"])
    def login_route():
        param = {}
        if request.method == 'POST':
            return login_pagina(param)
        return login_pagina(param)

    @app.route("/signup", methods=["GET", "POST"])
    def signup_route():
        param = {}
        if request.method == 'POST':
            return registrarUsuario(param)
        return registro_pagina(param)

    # AJAX actualizar estado pedido (admin)
    @app.route("/admin/pedidos/actualizar", methods=["POST"])
    def actualizar_estado_pedido_route():
        return actualizar_estado_pedido_ajax()

    ##### INICIO NUEVO (motivo: registrar aliases de endpoints para compatibilidad con templates existentes)
    # aliases que usan templates: creatote, crea_tote_route, mi_cuenta, estadisticas, add_product, guardar_producto_route, remove_from_cart, ver_carrito, ver_pedidos_admin
    try:
        # alias creatote / crea_tote_route -> creatote_route handler
        app.add_url_rule('/creatote', endpoint='creatote', view_func=creatote_route)
        app.add_url_rule('/crea_tote_route', endpoint='crea_tote_route', view_func=creatote_route)
    except Exception:
        pass
    try:
        app.add_url_rule('/mi-cuenta', endpoint='mi_cuenta', view_func=mi_cuenta_route)
    except Exception:
        pass
    try:
        app.add_url_rule('/admin/estadisticas', endpoint='estadisticas', view_func=estadisticas_route)
    except Exception:
        pass
    try:
        app.add_url_rule('/admin/add_product', endpoint='add_product', view_func=add_product_pagina)
        app.add_url_rule('/guardar_producto', endpoint='guardar_producto_route', view_func=guardar_producto)
    except Exception:
        pass
    try:
        app.add_url_rule('/carrito/quitar', endpoint='remove_from_cart', view_func=carrito_quitar_route)
    except Exception:
        pass
    try:
        app.add_url_rule('/admin/pedidos', endpoint='ver_pedidos_admin', view_func=ver_pedidos_admin)
    except Exception:
        pass
    ##### FIN NUEVO

    ##### INICIO NUEVO (motivo: aliases para endpoints 'login' y 'signup' usados por templates)
    try:
        app.add_url_rule('/login', endpoint='login', view_func=login_route)
    except Exception:
        pass
    try:
        app.add_url_rule('/signup', endpoint='signup', view_func=signup_route)
    except Exception:
        pass
    ##### FIN NUEVO

    ##### INICIO NUEVO (motivo: alias para endpoint AJAX usado por pedidosadmin.js)
    try:
        app.add_url_rule('/actualizar_estado_pedido', endpoint='actualizar_estado_pedido', view_func=actualizar_estado_pedido_route)
    except Exception:
        pass
    ##### FIN NUEVO

    # -----------------------------
    # ERROR NO ENCONTRADA
    # -----------------------------
    @app.route('/<name>',methods = ['POST', 'GET'])
    def noEncontrada(name):
        return paginaNoEncontrada(name)

    ##### INICIO NUEVO (motivo: estructura comentada para logout, implementable después)
    # ----- FUTURO LOGOUT -----
    # @app.route('/logout')
    # def logout_route():
    #     return logout_pagina({})
    ##### FIN NUEVO



### info:
# ENRUTAMIENTO DE LA PETICIÓN
# Este archivo conecta las URLs de Flask con las funciones del controller.
# Sigue el estilo original.

from flask import Flask, request, jsonify, redirect, render_template, session
from controller import *

def route(app):

    # ------------------------------------------
    # PÁGINA INICIAL → LOGIN (obligatorio)
    # ------------------------------------------
    @app.route("/")
    def inicio():
        return redirect('/login')

    # ------------------------------------------
    # HOME CLIENTE
    # ------------------------------------------
    @app.route("/home")
    def home():
        param = {}
        return home_pagina(param)

    # ------------------------------------------
    # CATÁLOGO
    # ------------------------------------------
    @app.route("/catalogo")
    def catalogo():
        param = {}
        return catalogo_pagina(param)

    # ------------------------------------------
    # CREAR TOTE
    # ------------------------------------------
    @app.route("/creatote", methods=["GET", "POST"])
    def creatote_route():
        param = {}
        return creatote_pagina(param)

    @app.route("/creatote_alias", endpoint="creatote")
    def creatote_alias():
        param = {}
        return creatote_pagina(param)

    # ------------------------------------------
    # LOGIN
    # ------------------------------------------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        param = {}
        if request.method == "POST":
            return ingresoUsuarioValido(param, request)
        return login_pagina(param)

    # ------------------------------------------
    # SIGNUP
    # ------------------------------------------
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        param = {}
        if request.method == "POST":
            return registrarUsuario(param, request)
        return registro_pagina(param)

    # ------------------------------------------
    # LOGOUT (estructura mínima)
    # ------------------------------------------
    @app.route("/logout")
    def logout_route():
        try:
            return cerrarSesion()
        except:
            return redirect('/login')

    # ------------------------------------------
    # MI CUENTA
    # ------------------------------------------
    @app.route("/miCuenta", methods=["GET"])
    def miCuenta_route():
        param = {}
        return editarUsuario_pagina(param)

    @app.route("/update_user", methods=["POST"])
    def actualizar_usuario_route():
        param = {}
        return actualizarDatosDeUsuarios(param)

    # ------------------------------------------
    # PRODUCTO INDIVIDUAL
    # ------------------------------------------
    @app.route("/producto/<int:producto_id>", methods=["GET"])
    def producto_route(producto_id):
        param = {}
        return producto_pagina(param, producto_id)

    @app.route("/producto_info/<int:pid>")
    def producto_info_route(pid):
        param = {}
        return producto_pagina(param, pid)

    # ------------------------------------------
    # CARRITO
    # ------------------------------------------
    @app.route("/carrito", methods=["GET"])
    def ver_carrito():
        param = {}
        return view_carrito(param)

    @app.route("/carrito_agregar", methods=["POST"])
    def carrito_agregar_route():
        return add_to_cart_ajax()

    @app.route("/carrito_quitar", methods=["POST"])
    def carrito_quitar_route():
        return remove_from_cart_ajax()

    @app.route("/crear_pedido", methods=["POST","GET"])
    def crear_pedido_route():
        param = {}
        return crear_pedido_desde_carrito(param)

    # ------------------------------------------
    # WISHLIST
    # ------------------------------------------
    @app.route("/wishlist", methods=["GET"])
    def wishlist_route():
        param = {}
        return view_wishlist(param)

    @app.route("/wishlist/agregar", methods=["POST"])
    def wishlist_agregar_route():
        return add_to_wishlist_ajax()

    @app.route("/wishlist/quitar", methods=["POST"])
    def wishlist_quitar_route():
        return remove_from_wishlist_ajax()

    # ------------------------------------------
    # PEDIDOS USUARIO
    # ------------------------------------------
    @app.route("/mis-pedidos", methods=["GET"])
    def ver_mis_pedidos():
        param = {}
        return pedidos_usuario(param)

    # ------------------------------------------
    # PEDIDOS ADMIN
    # ------------------------------------------
    @app.route("/admin/pedidos", methods=["GET"])
    def ver_pedidos_admin():
        param = {}
        return pedidos_admin(param)

    # ------------------------------------------
    # ESTADISTICAS ADMIN
    # ------------------------------------------
    @app.route("/estadisticas", methods=["GET"])
    def estadisticas():
        param = {}
        return estadisticas_pagina(param)

    # ------------------------------------------
    # AGREGAR PRODUCTO (admin)
    # ------------------------------------------
    @app.route("/add_product", methods=["GET"])
    def add_product_route():
        param = {}
        return add_product_pagina(param)

    @app.route("/guardar_producto", methods=["POST"])
    def guardar_producto_route():
        param = {}
        return guardar_producto(param)

    # ------------------------------------------
    # AJAX estado pedido (admin)
    # ------------------------------------------
    @app.route("/admin/pedidos/actualizar", methods=["POST"])
    def actualizar_estado_pedido_route():
        return actualizar_estado_pedido_ajax()

    # ------------------------------------------
    # ALIASES para compatibilidad con templates
    # ------------------------------------------
    try:
        app.add_url_rule('/creatote', endpoint='creatote', view_func=creatote_route)
        app.add_url_rule('/crea_tote_route', endpoint='crea_tote_route', view_func=creatote_route)
    except: pass

    try:
        app.add_url_rule('/mi-cuenta', endpoint='mi_cuenta', view_func=miCuenta_route)
    except: pass

    try:
        app.add_url_rule('/admin/estadisticas', endpoint='estadisticas', view_func=estadisticas)
    except: pass

    try:
        app.add_url_rule('/admin/add_product', endpoint='add_product', view_func=add_product_route)
        app.add_url_rule('/guardar_producto', endpoint='guardar_producto_route', view_func=guardar_producto_route)
    except: pass

    try:
        app.add_url_rule('/carrito/quitar', endpoint='remove_from_cart', view_func=carrito_quitar_route)
    except: pass

    try:
        app.add_url_rule('/admin/pedidos', endpoint='ver_pedidos_admin', view_func=ver_pedidos_admin)
    except: pass

    # ------------------------------------------
    # ALIASES LOGIN / SIGNUP
    # ------------------------------------------
    try:
        app.add_url_rule('/login', endpoint='login', view_func=login)
    except: pass

    try:
        app.add_url_rule('/signup', endpoint='signup', view_func=signup)
    except: pass

    # ------------------------------------------
    # ALIAS AJAX pedidos (JS)
    # ------------------------------------------
    try:
        app.add_url_rule('/actualizar_estado_pedido', endpoint='actualizar_estado_pedido', view_func=actualizar_estado_pedido_route)
    except: pass

    # ------------------------------------------
    # RUTA NO ENCONTRADA → REDIRECCIÓN POR ROL
    # ------------------------------------------
    @app.route('/<name>', methods=['GET','POST'])
    def noEncontrada(name):
        usuario = session.get('usuario')

        if not usuario:
            return redirect('/login')

        if usuario.get('tipo') == 'admin':
            return redirect('/estadisticas')

        return redirect('/home')

    # ------------------------------------------
    # LOGOUT FUTURO (comentado)
    # ------------------------------------------
    # @app.route('/logout')
    # def logout_route():
    #     return logout_pagina({})

### info:
# ENRUTAMIENTO DE LA PETICIÓN
# Este archivo conecta las URLs de Flask con las funciones del controller.
# Sigue el estilo original.

from flask import Flask, request, jsonify, redirect, render_template, session, url_for
from controller import *

def route(app):

    # ------------------------------------------
    # PÁGINA INICIAL → LOGIN (obligatorio)
    # ------------------------------------------
    @app.route("/")
    def inicio():
        return redirect('/login')

    # ------------------------------------------
    # HOME CLIENTE
    # ------------------------------------------
    @app.route("/home")
    def home():
        param = {}
        return home_pagina(param)

    # ------------------------------------------
    # CATÁLOGO
    # ------------------------------------------
    @app.route("/catalogo")
    def catalogo():
        param = {}
        return catalogo_pagina(param)

    # ------------------------------------------
    # CREAR TOTE
    # ------------------------------------------
    @app.route("/creatote", methods=["GET", "POST"])
    def creatote_route():
        param = {}
        return creatote_pagina(param)

    # alias para compatibilidad con templates que usan 'creatote' endpoint
    @app.route("/creatote_alias")
    def creatote_alias():
        param = {}
        return creatote_pagina(param)

    # ------------------------------------------
    # LOGIN
    # ------------------------------------------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        param = {}
        if request.method == "POST":
            return ingresoUsuarioValido(param, request)
        return login_pagina(param)

    # ------------------------------------------
    # SIGNUP / REGISTRO
    # ------------------------------------------
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        param = {}
        if request.method == "POST":
            return registrarUsuario(param, request)
        return registro_pagina(param)

    # ------------------------------------------
    # LOGOUT (estructura mínima)
    # ------------------------------------------
    @app.route("/logout")
    def logout_route():
        try:
            return cerrarSesion()
        except Exception:
            return redirect('/login')

    # ------------------------------------------
    # MI CUENTA
    # ------------------------------------------
    @app.route("/miCuenta", methods=["GET"])
    def miCuenta_route():
        param = {}
        return editarUsuario_pagina(param)

    @app.route("/update_user", methods=["POST"])
    def actualizar_usuario_route():
        param = {}
        return actualizarDatosDeUsuarios(param)

    # ------------------------------------------
    # PRODUCTO INDIVIDUAL
    # ------------------------------------------
    @app.route("/producto/<int:producto_id>", methods=["GET"])
    def producto_route(producto_id):
        param = {}
        return producto_pagina(param, producto_id)

    @app.route("/producto_info/<int:pid>")
    def producto_info_route(pid):
        param = {}
        return producto_pagina(param, pid)

    # ------------------------------------------
    # CARRITO
    # ------------------------------------------
    @app.route("/carrito", methods=["GET"])
    def ver_carrito():
        param = {}
        return view_carrito(param)

    @app.route("/carrito_agregar", methods=["POST"])
    def carrito_agregar_route():
        return add_to_cart_ajax()

    @app.route("/carrito_quitar", methods=["POST"])
    def carrito_quitar_route():
        return remove_from_cart_ajax()

    @app.route("/crear_pedido", methods=["POST","GET"])
    def crear_pedido_route():
        param = {}
        return crear_pedido_desde_carrito(param)

    # ------------------------------------------
    # WISHLIST
    # ------------------------------------------
    @app.route("/wishlist", methods=["GET"])
    def wishlist_route():
        param = {}
        return view_wishlist(param)

    @app.route("/wishlist/agregar", methods=["POST"])
    def wishlist_agregar_route():
        return add_to_wishlist_ajax()

    @app.route("/wishlist/quitar", methods=["POST"])
    def wishlist_quitar_route():
        return remove_from_wishlist_ajax()

    # ------------------------------------------
    # PEDIDOS USUARIO
    # ------------------------------------------
    @app.route("/mis-pedidos", methods=["GET"])
    def ver_mis_pedidos():
        param = {}
        return pedidos_usuario(param)

    # ------------------------------------------
    # PEDIDOS ADMIN
    # ------------------------------------------
    @app.route("/admin/pedidos", methods=["GET"])
    def ver_pedidos_admin():
        param = {}
        return pedidos_admin(param)

    # ------------------------------------------
    # ESTADISTICAS ADMIN
    # ------------------------------------------
    @app.route("/estadisticas", methods=["GET"])
    def estadisticas():
        param = {}
        return estadisticas_pagina(param)

    # ------------------------------------------
    # AGREGAR PRODUCTO (admin)
    # ------------------------------------------
    @app.route("/add_product", methods=["GET"])
    def add_product_route():
        param = {}
        return add_product_pagina(param)

    @app.route("/guardar_producto", methods=["POST"])
    def guardar_producto_route():
        param = {}
        return guardar_producto(param)

    # ------------------------------------------
    # AJAX estado pedido (admin)
    # ------------------------------------------
    @app.route("/admin/pedidos/actualizar", methods=["POST"])
    def actualizar_estado_pedido_route():
        return actualizar_estado_pedido_ajax()

    # ------------------------------------------
    # ALIASES para compatibilidad con templates
    # ------------------------------------------
    ##### INICIO NUEVO (motivo: asegurar que templates que llaman endpoints por nombres diferentes no rompan)
    try:
        # alias posible en templates: url_for('login_pagina') -> mapeo a endpoint 'login'
        app.add_url_rule('/login', endpoint='login_pagina', view_func=login)
    except Exception:
        pass
    try:
        # alias posible: url_for('registro_pagina') -> mapeo a signup()
        app.add_url_rule('/signup', endpoint='registro_pagina', view_func=signup)
    except Exception:
        pass
    try:
        app.add_url_rule('/signup', endpoint='registro', view_func=signup)
    except Exception:
        pass
    ##### FIN NUEVO

    # alias para creatote forms that used 'crea_tote_route' etc.
    try:
        app.add_url_rule('/crea_tote_route', endpoint='crea_tote_route', view_func=creatote_route)
    except Exception:
        pass

    try:
        app.add_url_rule('/mi-cuenta', endpoint='mi_cuenta', view_func=miCuenta_route)
    except Exception:
        pass

    try:
        app.add_url_rule('/admin/estadisticas', endpoint='estadisticas', view_func=estadisticas)
    except Exception:
        pass

    try:
        app.add_url_rule('/admin/add_product', endpoint='add_product', view_func=add_product_route)
        app.add_url_rule('/guardar_producto', endpoint='guardar_producto_route', view_func=guardar_producto_route)
    except Exception:
        pass

    try:
        app.add_url_rule('/carrito/quitar', endpoint='remove_from_cart', view_func=carrito_quitar_route)
    except Exception:
        pass

    try:
        app.add_url_rule('/admin/pedidos', endpoint='ver_pedidos_admin', view_func=ver_pedidos_admin)
    except Exception:
        pass

    # ------------------------------------------
    # ALIAS AJAX pedidos (JS)
    # ------------------------------------------
    try:
        app.add_url_rule('/actualizar_estado_pedido', endpoint='actualizar_estado_pedido', view_func=actualizar_estado_pedido_route)
    except Exception:
        pass

    # ------------------------------------------
    # RUTA NO ENCONTRADA → REDIRECCIÓN POR ROL
    # ------------------------------------------
    @app.route('/<name>', methods=['GET','POST'])
    def noEncontrada(name):
        usuario = session.get('usuario')

        if not usuario:
            return redirect('/login')

        # si es admin -> estadísticas, sino -> home
        if usuario.get('tipo') == 'admin':
            return redirect('/estadisticas')

        return redirect('/home')

    # ------------------------------------------
    # LOGOUT FUTURO (comentado)
    # ------------------------------------------
    # @app.route('/logout')
    # def logout_route():
    #     return logout_pagina({})

'''

# route.py
'''### info:
    ENRUTAMIENTO DE LA PETICIÓN
    Este archivo conecta las URLs de Flask con las funciones del controller.
    Sigue el estilo original.
'''

from flask import request, redirect, render_template
import functools
import controller

def route(app):

    # -----------------------------------------------------------------
    # ROOT / LOGIN
    # -----------------------------------------------------------------
    @app.route("/", methods=["GET"])
    @app.route("/login", methods=["GET"], endpoint="login_pagina")
    def login_get_route():
        param = {}
        return controller.login_pagina(param)
    #GET ES PARA OBTENER INFO DEL SERVIDOR, POST PARA SUBIR INFO
    @app.route("/login", methods=["POST"], endpoint="login_post")
    def login_post_route():
        param = {}
        # controller.ingresoUsuarioValido procesa POST login
        return controller.ingresoUsuarioValido(param, request)
    
    # -----------------------------------------------------------------
    # SIGNUP / REGISTRO
    # -----------------------------------------------------------------
    @app.route("/signup", methods=["GET"], endpoint="registro_pagina")
    def signup_get_route():
        param = {}
        return controller.registro_pagina(param)

    @app.route("/signup", methods=["POST"], endpoint="registrarUsuario")
    def signup_post_route():
        param = {}
        return controller.registrarUsuario(param, request)

    # -----------------------------------------------------------------
    # LOGOUT (estructura comentada para futura activación)
    # -----------------------------------------------------------------
    ##### INICIO NUEVO (motivo: dejar estructura preparada para logout, comentada)
    # @app.route("/logout", methods=["GET"], endpoint="logout")
    # def logout_route():
    #     # FUTURO: implementar logout definitivo
    #     # return controller.cerrarSesion()
    #     pass
    ##### FIN NUEVO #####

    # -----------------------------------------------------------------
    # HOME / CATALOGO / CREATOTE
    # -----------------------------------------------------------------
    @app.route("/home", methods=["GET"], endpoint="home")
    def home_route():
        param = {}
        return controller.home_pagina(param)

    @app.route("/catalogo", methods=["GET"], endpoint="catalogo_pagina")
    def catalogo_route():
        param = {}
        # controller.catalogo_pagina devuelve la vista de catálogo
        return controller.catalogo_pagina(param)

    # creatote: templates may call url_for('creatote') so provide endpoint name
    @app.route("/creatote", methods=["GET","POST"], endpoint="creatote_pagina")
    def creatote_route():
        param = {}
        # controller.creatote_pagina maneja GET y POST según tu diseño
        return controller.creatote_pagina(param)

    # -----------------------------------------------------------------
    # PRODUCTO (detalle)
    # -----------------------------------------------------------------
    # endpoint name expected by templates: 'producto_route' or 'producto_pagina'
    @app.route("/producto/<int:producto_id>", methods=["GET"], endpoint="producto_pagina")
    def producto_detalle(producto_id):
        param = {}
        return controller.producto_pagina(param, producto_id)

    # alias para compatibilidad: algunos templates usan producto_route with pid
    @app.route("/producto_info/<int:pid>", methods=["GET"], endpoint="producto_route")
    def producto_route_alias(pid):
        param = {}
        return controller.producto_pagina(param, pid)

    # -----------------------------------------------------------------
    # CARRITO
    # -----------------------------------------------------------------
    @app.route("/carrito", methods=["GET"], endpoint="carrito_get")
    def ver_carrito():
        param = {}
        return controller.view_carrito(param)

    @app.route("/carrito_agregar", methods=["POST"], endpoint="carrito_add")
    def carrito_agregar_route():
        return controller.add_to_cart_ajax()

    @app.route("/carrito_quitar", methods=["POST"], endpoint="carrito_remove")
    def carrito_quitar_route():
        return controller.remove_from_cart_ajax()

    @app.route("/crear_pedido", methods=["POST","GET"], endpoint="crear_pedido")
    def crear_pedido():
        param = {}
        return controller.crear_pedido_desde_carrito(param)

    # -----------------------------------------------------------------
    # WISHLIST
    # -----------------------------------------------------------------
    @app.route("/wishlist", methods=["GET"], endpoint="wishlist_get")
    def ver_wishlist():
        param = {}
        return controller.view_wishlist(param)

    @app.route("/wishlist_agregar", methods=["POST"], endpoint="wishlist_add")
    def wishlist_agregar_route():
        return controller.add_to_wishlist_ajax()

    @app.route("/wishlist_quitar", methods=["POST"], endpoint="wishlist_remove")
    def wishlist_quitar_route():
        return controller.remove_from_wishlist_ajax()

    # -----------------------------------------------------------------
    # PEDIDOS (usuario / admin) y actualización estado
    # -----------------------------------------------------------------
    @app.route("/pedidosusuario", methods=["GET"], endpoint="pedidosusuario")
    def ver_pedidos_usuario():
        param = {}
        return controller.pedidos_usuario(param)

    @app.route("/pedidosadmin", methods=["GET"], endpoint="admin_pedidos")
    def ver_pedidos_admin():
        param = {}
        return controller.pedidos_admin(param)

    @app.route("/actualizar_estado_pedido", methods=["POST"], endpoint="actualizar_estado_pedido")
    def actualizar_estado_pedido():
        return controller.actualizar_estado_pedido_ajax()

    # -----------------------------------------------------------------
    # ADMIN: estadisticas / add product
    # -----------------------------------------------------------------
    @app.route("/estadisticas", methods=["GET"], endpoint="admin_estadisticas")
    def estadisticas():
        param = {}
        return controller.estadisticas_pagina(param)

    @app.route("/add_product", methods=["GET"], endpoint="add_product")
    def add_product():
        param = {}
        return controller.add_product_pagina(param)

    @app.route("/guardar_producto", methods=["POST"], endpoint="guardar_producto")
    def guardar_producto_route():
        return controller.guardar_producto(request)

    # -----------------------------------------------------------------
    # MI CUENTA / EDITAR
    # -----------------------------------------------------------------
    @app.route("/miCuenta", methods=["GET"], endpoint="mi_cuenta")
    def mi_cuenta_route():
        param = {}
        return controller.editarUsuario_pagina(param)

    @app.route("/update_user", methods=["POST"], endpoint="update_user")
    def update_user_route():
        param = {}
        return controller.actualizarDatosDeUsuarios(param, request)

    # -----------------------------------------------------------------
    # RUTA POR DEFECTO (NOT FOUND)
    # -----------------------------------------------------------------
    @app.route("/<path:name>", methods=["GET","POST"])
    def no_encontrada(name):
        try:
            return controller.paginaNoEncontrada(name)
        except Exception:
            return "Pagina '{}' no encontrada".format(name), 404
