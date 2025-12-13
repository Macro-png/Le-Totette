from flask import render_template, request, redirect, url_for, session

def route(app):

    # =========================
    # HOME / INDEX
    # =========================
    @app.route('/')
    def index():
        return render_template('index.html')


    # =========================
    # AUTH
    # =========================
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        return render_template('signup.html')


    # =========================
    # CATALOGO / PRODUCTOS
    # =========================
    @app.route('/catalogo')
    def catalogo():
        return render_template('catalogo.html')

    @app.route('/producto/<int:id>')
    def producto(id):
        return render_template('producto.html')


    # =========================
    # USUARIO
    # =========================
    @app.route('/mi-cuenta')
    def mi_cuenta():
        return render_template('miCuenta.html')

    @app.route('/wishlist')
    def wishlist():
        return render_template('wishlist.html')

    @app.route('/pedidos')
    def pedidos_usuario():
        return render_template('pedidosusuario.html')


    # =========================
    # ADMIN
    # =========================
    @app.route('/creatote', methods=['GET', 'POST'])
    def creatote():
        return render_template('creatote.html')

    @app.route('/mod-product/<int:id>', methods=['GET', 'POST'])
    def mod_product(id):
        return render_template('mod_product.html')
    
    @app.route('/admin/pedidos')
    def pedidos_admin():
        return render_template('pedidosadmin.html')

    @app.route('/admin/estadisticas')
    def estadisticas():
        return render_template('estadisticas.html')
