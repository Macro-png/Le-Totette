
from flask import request, redirect, render_template
import functools
from controller import *

def route(app):

    # -----------------------------------------------------------------
    #                             LOGIN
    # -----------------------------------------------------------------
    
    # GET sirve únicamente para mostrar la página.
    # POST sirve únicamente para procesar datos enviados por un formulario.
    # Esto separa claramente “mostrar formulario” de “procesar formulario”.
    
    @app.route("/", methods=["GET", "POST"])
    @app.route("/login", methods=["GET","POST"])
    def login():
        param = {}
        if request.method == "GET":
            return login_pagina(param)
        else:
            return ingresoUsuarioValido(param , request)
        
        #GET ES PARA OBTENER INFO DEL SERVIDOR, POST PARA SUBIR INFO
    
    
    # -----------------------------------------------------------------
    #                             SIGNUP
    # -----------------------------------------------------------------
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        param = {}
        if request.method == "GET":
            return signup_pagina(param)
        else:
            return registrarUsuario(param , request)
  

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
    @app.route("/cliente", methods=["GET"])
    @app.route("/cliente/home", methods=["GET"])
    def home():
        param = {}
        return home_pagina(param)

    @app.route("/cliente/catalogo", methods=["GET"])
    def catalogo():
        param = {}
        # controller.catalogo_pagina devuelve la vista de catálogo
        return catalogo_pagina(param)

    @app.route("/cliente/creatote", methods=["GET","POST"])
    def creatote():
        param = {}
        if request.method == "GET":
            return creatote_pagina(param)
        else:
            return creatote_formulario(param)

    # -----------------------------------------------------------------
    # PRODUCTO (detalle)
    # -----------------------------------------------------------------

    @app.route("/cliente/producto/<int:producto_id>", methods=["GET","POST"])
    def producto_detalle(producto_id):
        param = {}
        if request.method == "GET":
            return producto_pagina(param, producto_id)
        else:
            accion = request.form.get("accion")

            if accion == "carrito":
                return agregar_producto_carrito(param, request, producto_id)

            elif accion == "wishlist":
                return agregar_producto_wishlist(param, request, producto_id)


    # -----------------------------------------------------------------
    # CARRITO
    # -----------------------------------------------------------------
    @app.route("/cliente/carrito", methods=["GET", "POST"])
    def carrito():
        param = {}
    
        if request.method == "GET":
            return view_carrito(param)
    
        # POST
        accion = request.form.get("accion")

        if accion == "modificar":
            return carrito_modificar_cantidad(param, request)

        elif accion == "eliminar":
            return carrito_eliminar_producto(param, request)

        elif accion == "vaciar":
            return carrito_vaciar(param)

        else:
            # acción no reconocida
            return view_carrito(param)

            

    # -----------------------------------------------------------------
    # WISHLIST
    # -----------------------------------------------------------------
    @app.route("/cliente/wishlist", methods=["GET","POST"])
    def wishlist():
        param = {}
        if request.method == "GET":
            return view_wishlist(param)
        else:
            return eliminar_wishlist
            

    # -----------------------------------------------------------------
    # PEDIDOS (usuario / admin) y actualización estado
    # -----------------------------------------------------------------
    @app.route("/cliente/pedidosusuario", methods=["GET"])
    def pedidos_usuario():
        param = {}
        return pedidos_usuario(param)

    @app.route("/admin/pedidosadmin", methods=["GET", "POST"])
    def pedidos_admin():
        param = {}
        if request.method == "GET"
            return pedidos_admin_pagina(param)
        else:
            return pedidos_admin_modificarestado(param)

#actualizar_estado_pedido_ajax()

    # -----------------------------------------------------------------
    # ADMIN: estadisticas / add product
    # -----------------------------------------------------------------
    @app.route("/admin", methods=["GET"])
    @app.route("/admin/estadisticas", methods=["GET"])
    def estadisticas():
        param = {}
        return estadisticas_pagina(param)

    @app.route("/admin/add_product", methods=["GET","POST"], endpoint="add_product")
    def add_product():
        param = {}
        if request.method == "GET":
            return add_product_pagina(param)
        else:
            return guardar_producto(param)

    # -----------------------------------------------------------------
    # MI CUENTA / EDITAR
    # -----------------------------------------------------------------
    @app.route("/cliente/miCuenta", methods=["GET"], endpoint="mi_cuenta")
    def miCuenta():
        param = {}
        if request.method == "GET":
            return miCuenta_pagina(param)
        else:
            return editarUsuario(param)



    # -----------------------------------------------------------------
    # RUTA POR DEFECTO (NOT FOUND)
    # -----------------------------------------------------------------
    @app.route('/<name>')
    def noEncontrada(name):
        ''' Info:
          Entra en esta ruta todo direccionamiento recibido que 
          no machea con ningun otro route. Es decir no es un pagina (dirección)
            válida en el sistema.
          Retorna una pagina indicando el error. 
        '''  
        
        return paginaNoEncontrada(name)
