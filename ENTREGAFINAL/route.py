from flask import request
from controller import *

def route(app):

    # -----------------------------------------------------------------
    # LOGIN / SIGNUP / LOGOUT
    # -----------------------------------------------------------------

    @app.route("/", methods=["GET", "POST"])
    @app.route("/login", methods=["GET", "POST"])
    def login():
        param = {}
        if request.method == "GET":
            return login_pagina(param)
        return ingreso_usuario_valido(param)

    @app.route("/signup", methods=["GET", "POST"])
    def signup_route():
        param = {}
        if request.method == "GET":
            return signup_pagina(param)
        return signup(param)

    @app.route("/logout", methods=["GET"])
    def logout():
        return cerrar_sesion()

    # -----------------------------------------------------------------
    # CLIENTE
    # -----------------------------------------------------------------

    @app.route("/cliente/home", methods=["GET"])
    def home():
        param = {}
        return home_pagina(param)

    @app.route("/cliente/catalogo", methods=["GET"])
    def catalogo():
        param = {}
        return catalogo_pagina(param)

    @app.route("/cliente/producto/<int:producto_id>", methods=["GET"])
    def producto(producto_id):
        param = {}
        return producto_pagina(param, producto_id)

    # -------------------- CARRITO --------------------

    @app.route("/cliente/carrito", methods=["GET"])
    def carrito():
        param = {}
        return ver_carrito(param)

    @app.route("/cliente/carrito/agregar/<int:producto_id>", methods=["POST"])
    def carrito_agregar(producto_id):
        param = {}
        return agregar_producto_carrito(param, producto_id)

    @app.route("/cliente/carrito/eliminar/<int:producto_id>", methods=["POST"])
    def carrito_eliminar(producto_id):
        param = {}
        return eliminar_producto_carrito(param, producto_id)

    @app.route("/cliente/carrito/vaciar", methods=["POST"])
    def carrito_vaciar():
        param = {}
        return vaciar_carrito(param)

    # -------------------- WISHLIST --------------------

    @app.route("/cliente/wishlist", methods=["GET"])
    def wishlist():
        param = {}
        return view_wishlist(param)

    @app.route("/cliente/wishlist/agregar/<int:producto_id>", methods=["POST"])
    def wishlist_agregar(producto_id):
        param = {}
        return agregar_producto_wishlist(param, producto_id)

    @app.route("/cliente/wishlist/eliminar/<int:producto_id>", methods=["POST"])
    def wishlist_eliminar(producto_id):
        param = {}
        return eliminar_wishlist(param, producto_id)

    # -------------------- PEDIDOS CLIENTE --------------------

    @app.route("/cliente/pedidos", methods=["GET"])
    def pedidos_cliente():
        param = {}
        return pedidos_usuario(param)

    @app.route("/cliente/micuenta", methods=["GET"])
    def micuenta():
        param = {}
        return mi_cuenta_pagina(param)

    # -----------------------------------------------------------------
    # ADMIN
    # -----------------------------------------------------------------

    @app.route("/admin/estadisticas", methods=["GET"])
    def estadisticas():
        param = {}
        return admin_estadisticas_pagina(param)

    @app.route("/admin/pedidos", methods=["GET"])
    def pedidos_admin():
        param = {}
        return pedidos_admin_pagina(param)

    @app.route("/admin/pedidos/<int:pedido_id>", methods=["POST"])
    def pedidos_admin_estado(pedido_id):
        param = {}
        return pedidos_admin_modificar_estado(param, pedido_id)

    @app.route("/admin/add_product", methods=["GET", "POST"])
    def add_product():
        param = {}
        if request.method == "GET":
            return add_product_pagina(param)
        return guardar_producto(param)

    # -----------------------------------------------------------------
    # NOT FOUND
    # -----------------------------------------------------------------

    @app.errorhandler(404)
    def not_found(e):
        if 'usuario' in session and session['usuario']['tipo'] == 'admin':
            return redirect('/admin/estadisticas')
        return redirect('/cliente/home')
