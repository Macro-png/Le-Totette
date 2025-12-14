from flask import render_template, redirect, request, session
import model


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def requiere_login():
    return 'usuario' in session


def es_admin():
    return requiere_login() and session['usuario']['tipo'] == 'admin'


def cerrar_sesion():
    session.clear()
    return redirect('/login')


# ---------------------------------------------------------------------------
# auth
# ---------------------------------------------------------------------------

def login_pagina(param):
    return render_template('login.html', param=param)


def signup_pagina(param):
    return render_template('signup.html', param=param)


def ingreso_usuario_valido(param):
    mail = request.form.get('email', '').strip()
    contrasena = request.form.get('contrasena', '').strip()

    result = {}
    if model.validarClientePorMailYContrasena(result, mail, contrasena):
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

    param['error'] = 'mail o contraseña incorrectos'
    return render_template('login.html', param=param)


def signup(param):
    if model.crearCliente(request.form):
        return redirect('/login')

    param['error'] = 'error al crear el usuario'
    return render_template('signup.html', param=param)


# ---------------------------------------------------------------------------
# cliente
# ---------------------------------------------------------------------------

def home_pagina(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    param['productos'] = model.obtenerTodosLosProductos()
    return render_template('home.html', param=param)


def catalogo_pagina(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    param['productos'] = model.obtenerTodosLosProductos()
    return render_template('catalogo.html', param=param)


def producto_pagina(param, producto_id):
    if not requiere_login() or es_admin():
        return redirect('/login')

    param['producto'] = model.obtenerProductoPorId(producto_id)
    return render_template('producto.html', param=param)


def ver_carrito(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    param['carrito'] = model.obtener_carrito(cliente_id)
    return render_template('carrito.html', param=param)


def agregar_producto_carrito(param, producto_id):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    model.agregar_producto_carrito(cliente_id, producto_id)
    return redirect('/cliente/carrito')


def eliminar_producto_carrito(param, producto_id):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    model.eliminar_producto_carrito(cliente_id, producto_id)
    return redirect('/cliente/carrito')


def vaciar_carrito(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    model.vaciar_carrito(cliente_id)
    return redirect('/cliente/carrito')


def view_wishlist(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    param['wishlist'] = model.obtener_wishlist(cliente_id)
    return render_template('wishlist.html', param=param)


def agregar_producto_wishlist(param, producto_id):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    model.agregar_wishlist(cliente_id, producto_id)
    return redirect('/cliente/wishlist')


def eliminar_wishlist(param, producto_id):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    model.eliminar_wishlist(cliente_id, producto_id)
    return redirect('/cliente/wishlist')


def pedidos_usuario(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    param['pedidos'] = model.obtener_pedidos_cliente(cliente_id)
    return render_template('pedidos.html', param=param)


def mi_cuenta_pagina(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    return render_template('micuenta.html', param=param)


# ---------------------------------------------------------------------------
# admin
# ---------------------------------------------------------------------------

def admin_estadisticas_pagina(param):
    if not es_admin():
        return redirect('/login')

    param['estadisticas'] = model.obtenerEstadisticas()
    return render_template('admin_estadisticas.html', param=param)


def pedidos_admin_pagina(param):
    if not es_admin():
        return redirect('/login')

    param['pedidos'] = model.obtener_pedidos_admin()
    return render_template('admin_pedidos.html', param=param)


def pedidos_admin_modificar_estado(param, pedido_id):
    if not es_admin():
        return redirect('/login')

    estado = request.form.get('estado')
    model.actualizar_estado_pedido(pedido_id, estado)
    return redirect('/admin/pedidos')


def add_product_pagina(param):
    if not es_admin():
        return redirect('/login')

    return render_template('admin_add_product.html', param=param)


def guardar_producto(param):
    if not es_admin():
        return redirect('/login')

    # depende de tu model, acá solo queda el hook
    # model.crear_producto(request.form)
    return redirect('/admin/catalogo')
