# route.py
from controller import *

def route(app):
    # LOGIN
    app.add_url_rule("/", methods=["GET"], view_func=login_get, endpoint="login_get_route")
    app.add_url_rule("/login", methods=["GET"], view_func=login_get, endpoint="login_get_route_alt")
    app.add_url_rule("/login", methods=["POST"], view_func=login_post, endpoint="login_post_route")

    # LOGOUT
    app.add_url_rule("/logout", view_func=logout, endpoint="logout_route")

    # SIGNUP
    app.add_url_rule("/signup", methods=["GET"], view_func=signup_get, endpoint="signup_get_route")
    app.add_url_rule("/signup", methods=["POST"], view_func=signup_post, endpoint="signup_post_route")

    # CLIENTE
    app.add_url_rule("/home", view_func=home, endpoint="home_route")
    app.add_url_rule("/catalogo", view_func=catalogo, endpoint="catalogo_route")
    app.add_url_rule("/producto/<int:pid>", view_func=ver_producto, endpoint="producto_route")
    app.add_url_rule("/mi-cuenta", view_func=mi_cuenta, endpoint="mi_cuenta_route")

    # WISHLIST
    app.add_url_rule("/mi-wishlist", view_func=wishlist_get, endpoint="wishlist_route")
    app.add_url_rule("/mi-wishlist/agregar", methods=["POST"], view_func=wishlist_add, endpoint="wishlist_agregar_route")
    app.add_url_rule("/mi-wishlist/quitar", methods=["POST"], view_func=wishlist_remove, endpoint="wishlist_quitar_route")

    # CARRITO
    app.add_url_rule("/carrito", view_func=carrito_get, endpoint="carrito_route")
    app.add_url_rule("/carrito/agregar", methods=["POST"], view_func=carrito_add, endpoint="carrito_agregar_route")
    app.add_url_rule("/carrito/quitar", methods=["POST"], view_func=carrito_remove, endpoint="carrito_quitar_route")

    # PEDIDOS CLIENTE
    app.add_url_rule("/mis-pedidos", view_func=mis_pedidos, endpoint="mis_pedidos_route")

    # CREA TU TOTE
    app.add_url_rule("/crea-tu-tote", methods=["GET", "POST"], view_func=crea_tote_route, endpoint="crea_tote_route")

    # ADMIN
    app.add_url_rule("/admin/pedidos", view_func=admin_pedidos, endpoint="admin_pedidos_route")
    app.add_url_rule("/admin/estadisticas", view_func=admin_estadisticas, endpoint="admin_estadisticas_route")
    app.add_url_rule("/admin/productos/agregar", methods=["GET"], view_func=add_product_get, endpoint="admin_add_product_get")
    app.add_url_rule("/admin/productos/agregar", methods=["POST"], view_func=add_product_post, endpoint="admin_add_product_post")

    # 404
    @app.errorhandler(404)
    def page_not_found(e):
        return "Página no encontrada", 404
