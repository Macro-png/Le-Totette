'''
### info:
    CONTROL DE RUTAS
'''
from flask import render_template, request
from controller import *

def route(app):

    # -----------------------------
    # LOGIN
    # -----------------------------
    @app.route("/")
    @app.route("/login", methods=["GET"])
    def login_get_route():
        '''
        Info:
          Carga la página de login
        '''
        return login_get()

    @app.route("/login", methods=["POST"])
    def login_post_route():
        '''
        Info:
          Procesa los datos enviados desde el formulario de login
        '''
        return login_post()

    # -----------------------------
    # LOGOUT
    # -----------------------------
    @app.route("/logout")
    def logout_route():
        '''
        Info:
          Cierra la sesión del usuario
        '''
        return logout()

    # -----------------------------
    # SIGNUP
    # -----------------------------
    @app.route("/signup", methods=["GET"])
    def signup_get_route():
        '''
        Info:
          Carga la página de registro
        '''
        return signup_get()

    @app.route("/signup", methods=["POST"])
    def signup_post_route():
        '''
        Info:
          Procesa el registro de usuario
        '''
        return signup_post()

    # -----------------------------
    # CLIENTE
    # -----------------------------
    @app.route("/home")
    def home_route():
        '''
        Info:
          Página principal del usuario logueado
        '''
        return home()

    @app.route("/catalogo")
    def catalogo_route():
        '''
        Info:
          Lista de productos disponibles
        '''
        return catalogo()

    @app.route("/producto/<int:pid>")
    def producto_route(pid):
        '''
        Info:
          Página del producto seleccionado
        '''
        return ver_producto(pid)

    @app.route("/mi-cuenta")
    def mi_cuenta_route():
        '''
        Info:
          Página con los datos del usuario
        '''
        return mi_cuenta()

    # -----------------------------
    # WISHLIST
    # -----------------------------
    @app.route("/mi-wishlist")
    def wishlist_route():
        '''
        Info:
          Muestra la wishlist del usuario
        '''
        return wishlist_get()

    @app.route("/mi-wishlist/agregar", methods=["POST"])
    def wishlist_agregar_route():
        '''
        Info:
          Agrega un producto a la wishlist
        '''
        return wishlist_add()

    @app.route("/mi-wishlist/quitar", methods=["POST"])
    def wishlist_quitar_route():
        '''
        Info:
          Quita un producto de la wishlist
        '''
        return wishlist_remove()

    # -----------------------------
    # CARRITO
    # -----------------------------
    @app.route("/carrito")
    def carrito_route():
        '''
        Info:
          Muestra el carrito del usuario
        '''
        return carrito_get()

    @app.route("/carrito/agregar", methods=["POST"])
    def carrito_agregar_route():
        '''
        Info:
          Agrega un producto al carrito
        '''
        return carrito_add()

    @app.route("/carrito/quitar", methods=["POST"])
    def carrito_quitar_route():
        '''
        Info:
          Quita un producto del carrito
        '''
        return carrito_remove()

    # -----------------------------
    # PEDIDOS CLIENTE
    # -----------------------------
    @app.route("/mis-pedidos")
    def mis_pedidos_route():
        '''
        Info:
          Lista los pedidos del usuario
        '''
        return mis_pedidos()

    # -----------------------------
    # CREA TU TOTE
    # -----------------------------
    @app.route("/crea-tu-tote", methods=["GET", "POST"])
    def crea_tote_route_path():
        '''
        Info:
          Página para crear tote personalizada
        '''
        return crea_tote_route()

    # -----------------------------
    # ADMIN
    # -----------------------------
    @app.route("/admin/pedidos")
    def admin_pedidos_route():
        '''
        Info:
          Panel de pedidos del administrador
        '''
        return admin_pedidos()

    @app.route("/admin/estadisticas")
    def admin_estadisticas_route():
        '''
        Info:
          Panel de estadísticas del administrador
        '''
        return admin_estadisticas()

    @app.route("/admin/productos/agregar", methods=["GET"])
    def admin_add_product_get_route():
        '''
        Info:
          Muestra formulario para agregar productos
        '''
        return add_product_get()

    @app.route("/admin/productos/agregar", methods=["POST"])
    def admin_add_product_post_route():
        '''
        Info:
          Procesa el formulario de agregar productos
        '''
        return add_product_post()

    # -----------------------------
    # ERROR NO ENCONTRADA
    # -----------------------------
    @app.route('/<name>',methods = ['POST', 'GET'])
    def noEncontrada(name):
        ''' Info:
          Entra en esta ruta todo direccionamiento recibido que 
          no machea con ningun otro route. Es decir no es un pagina (dirección)
            válida en el sistema.
          Retorna una pagina indicando el error. 
        '''  
        return paginaNoEncontrada(name)
    

