from flask import request, session, redirect
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

    @app.route("/cliente/producto/<int:producto_id>", methods=["GET", "POST"])
    def producto(producto_id):
        param = {}
        if request.method == "GET":
            return producto_pagina(param, producto_id)

        accion = request.form.get("accion")

        if accion == "carrito":
            return model.agregar_producto_carrito(param, producto_id)

        elif accion == "wishlist":
            return agregar_producto_wishlist(param, producto_id)

        return redirect("/cliente/home")


    @app.route("/cliente/creatote", methods=["GET", "POST"])
    def creatote():
        param = {}
        if request.method == "GET":
            return creatote_pagina(param)
        return creatote_formulario(param)

    # -------------------- CARRITO --------------------

    @app.route("/cliente/carrito", methods=["GET"])
    def carrito():
        param = {}
        return ver_carrito(param)

    from flask import session, redirect, url_for, abort

    #@app.route("/cliente/carrito/agregar/<int:producto_id>", methods=["POST"])
    #def carrito_agregar(producto_id):

        #if "cliente_id" not in session:
            #return redirect(url_for("login"))

        #cliente_id = session["cliente_id"]

        #agregar_producto_carrito(cliente_id, producto_id)

        #return redirect(url_for("carrito"))
    
    @app.route('/cliente/carrito/agregar/<int:producto_id>', methods=['POST'])
    def carrito_agregar(producto_id):
        if not requiere_login():
            return redirect(url_for('login'))

        if es_admin():
            return redirect("/admin")

        cliente_id = session['usuario']['id']
        model.agregar_producto_carrito(cliente_id, producto_id)

        return redirect(url_for('carrito'))



    @app.route("/cliente/carrito/eliminar/<int:producto_id>", methods=["POST"])
    def carrito_eliminar(producto_id):
        if not requiere_login() or es_admin():
            return redirect('/login')

        cliente_id = session['usuario']['id']
        model.eliminar_producto_carrito(cliente_id, producto_id)

        return redirect('/cliente/carrito')


    @app.route("/cliente/carrito/vaciar", methods=["POST"])
    def carrito_vaciar():
        if not requiere_login() or es_admin():
            return redirect('/login')

        cliente_id = session['usuario']['id']
        model.vaciar_carrito(cliente_id)

        return redirect('/cliente/carrito')


    # -------------------- WISHLIST --------------------

    @app.route("/cliente/wishlist")
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

    
    @app.route("/cliente/pedido", methods=["GET", "POST"])
    def pedidosusuario_pagina():
        param = {}
        return pedidos_usuario(param)
    
    @app.route("/cliente/pedido/confirmar", methods=["POST"])
    def pedido_confirmar():
        param = {}
        return confirmar_pedido(param)


    @app.route("/cliente/miCuenta", methods=["GET"])
    def miCuenta():
        param = {}
        return miCuenta_pagina(param)

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
        else:
            diRequest={}
            return guardar_producto(param, diRequest)

    # -----------------------------------------------------------------
    # NOT FOUND
    # -----------------------------------------------------------------

    @app.errorhandler(404)
    def not_found(e):
        if 'usuario' in session and session['usuario']['tipo'] == 'admin':
            return redirect('/admin/estadisticas')
        return redirect('/cliente/home')
    
    #=============================
    # EXTRA PARA EL CREA TU TOTE
    #====================-==========
    
    #def extracreatote():
        
    
    #@app.route{{ url_for('producto', producto_id=producto['id']) }}
    #@app.route("/cliente/creatote", methods=["GET", "POST"])
    #def creatote():
    #    param = {}
    #    if request.method == "GET":
    #        return creatote_pagina(param)
    #    return creatote_formulario(param)