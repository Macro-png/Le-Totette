from flask import render_template, redirect, request, session, url_for
import os
import model
from datetime import datetime
from werkzeug.utils import secure_filename
from uuid import uuid4
from appConfig import config
import _mysql_db
import random
import string

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def requiere_login():
    return 'usuario' in session


def es_admin():
    return requiere_login() and session['usuario']['tipo'] == 'admin'


def cerrar_sesion():
    session.clear()
    return redirect('/login')


# ---------------------------------------------------------------------------
# AUTH
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

    param['error'] = 'Mail o contraseña incorrectos'
    return render_template('login.html', param=param)



def signup(param):
    nombre = request.form.get("nombre")
    mail = request.form.get("mail")
    contrasena = request.form.get("contrasena")
    verificar = request.form.get("verificarcontrasena")

    # Validaciones básicas
    if not nombre or not mail or not contrasena:
        param["error"] = "Faltan datos"
        return render_template("signup.html", **param)

    if contrasena != verificar:
        param["error"] = "Las contraseñas no coinciden"
        return render_template("signup.html", **param)

    if len(contrasena) < 6:
        param["error"] = "Contraseña muy corta"
        return render_template("signup.html", **param)

    data = {
        "nombre": nombre,
        "mail": mail,
        "contrasena": contrasena
    }

    if model.crearCliente(data):
        return redirect(url_for("login"))

    param["error"] = "No se pudo crear la cuenta"
    return render_template("signup.html", **param)


# ---------------------------------------------------------------------------
# CLIENTE
# ---------------------------------------------------------------------------

def home_pagina(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    param['productos'] = model.obtenerTodosLosProductos()
    return render_template('index.html', param=param)


def catalogo_pagina(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    productos_db = model.obtenerTodosLosProductos()

    productos = []
    for p in productos_db:
        productos.append({
            'id': p[0],
            'nombre': p[1],
            'precio_unidad': p[2],
            'img': p[3],
            'descripcion': p[4],
        })

    param['productos'] = productos
    return render_template('catalogo.html', **param)



def producto_pagina(param, producto_id):
    if not requiere_login() or es_admin():
        return redirect('/login')

    producto = model.obtenerProductoPorId(producto_id)
    if not producto:
        return redirect('/cliente/home')

    param['producto'] = producto
    return render_template('producto.html', **param)

def cambiar_contrasena(param):
    if not requiere_login():
        return redirect('/login')

    cliente_id = session['usuario']['id']

    actual = request.form.get('contrasena_actual')
    nueva = request.form.get('nueva_contrasena')
    repetir = request.form.get('repetir_contrasena')

    # Validaciones
    if not actual or not nueva or not repetir:
        param['error'] = "Faltan datos"
        return render_template('miCuenta.html', **param)

    if nueva != repetir:
        param['error'] = "Las contraseñas no coinciden"
        return render_template('miCuenta.html', **param)

    if len(nueva) < 6:
        param['error'] = "La contraseña debe tener al menos 6 caracteres"
        return render_template('miCuenta.html', **param)

    # Verificar contraseña actual
    result = {}
    if not model.validarClientePorMailYContrasena(
        result,
        session['usuario']['mail'],
        actual
    ):
        param['error'] = "Contraseña actual incorrecta"
        return render_template('miCuenta.html', **param)

    # Actualizar contraseña
    if model.actualizar_contrasena(cliente_id, nueva):
        param['success'] = "Contraseña actualizada correctamente"
    else:
        param['error'] = "No se pudo actualizar la contraseña"

    return render_template('miCuenta.html', **param)



def confirmar_pedido(param):
    if not requiere_login():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    
    BASE = { "host":"localhost",
        "user":"root",
        "pass":"",
        "dbname":"base_le_totette"}

    # -------------------------
    # Crear pedido
    # -------------------------
    sSql = """
    INSERT INTO pedidos (id, cliente_id, fecha, precio_total, estado)
    VALUES (NULL, %s, CURDATE(), %s, 'espera');
    """
    precio_total = model.obtener_total_carrito(cliente_id) or 0
    
    model.insertDB(BASE, sSql, (cliente_id, precio_total))
    
    pedido_id=model.selectDB(BASE, """SELECT id FROM pedidos WHERE fecha = CURDATE() AND cliente_id = %s;""", (cliente_id))

    total = 0

    # -------------------------
    # Productos del carrito
    # -------------------------
    carrito = model.obtener_carrito(cliente_id) or []

    for prod in carrito:
        producto_id = prod[0]
        precio = prod[2]
        cantidad = prod[4]

        subtotal = precio * cantidad
        total += subtotal

        model.insertDB(BASE, """
                       INSERT INTO detalle_pedido
                       (pedidos_id, productos_id, cantidad, precio_unidad)
                       VALUES (%s, %s, %s, %s);""", (pedido_id, producto_id, cantidad, precio))
        
        #model.agregar_detalle_pedido(pedido_id, producto_id, cantidad, precio)

        
        model.aumentar_ventas_producto(producto_id, cantidad)
        
        
                    
        
    # -------------------------
    # Totes personalizados
    # -------------------------
    for item in session.get('totes_temp', []):
        producto_id = item['producto_id']

        precio = model.selectDB(
            BASE,
            "SELECT precio_unidad FROM productos WHERE id=%s;",
            (producto_id,)
        )[0][0]

        total += precio

        model.insertDB(BASE, """
            INSERT INTO detalle_pedido
            (pedidos_id, productos_id, cantidad, precio_unidad)
            VALUES (%s, %s, 1, %s);
        """, (pedido_id, producto_id, precio))

        detalle_id = model.selectDB(BASE, "SELECT LAST_INSERT_ID();")[0][0]

        model.insertDB(BASE, """
            INSERT INTO detalle_personalizados
            (detalle_pedido_id, img)
            VALUES (%s, %s);
        """, (detalle_id, item['img']))

        # sumar venta del tote
        model.aumentar_ventas_producto(producto_id, 1)

    # -------------------------
    # Actualizar total
    # -------------------------
    model.updateDB(BASE, """
        UPDATE pedidos
        SET precio_total = %s
        WHERE id = %s;
    """, (total, pedido_id))

    # -------------------------
    # Limpiar carrito y sesión
    # -------------------------
    model.vaciar_carrito(cliente_id)
    session.pop('totes_temp', None)

    return redirect('/cliente/pedido')



# ---------------------------------------------------------------------------
# CARRITO
# ---------------------------------------------------------------------------

def ver_carrito(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']

    productos_carrito = model.obtener_carrito(cliente_id) or []
    total_compra = model.obtener_total_carrito(cliente_id) or 0

    return render_template(
        'carrito.html',
        productos=productos_carrito,
        total=total_compra
    )


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





# ---------------------------------------------------------------------------
# WISHLIST
# ---------------------------------------------------------------------------

def view_wishlist(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    cliente_id = session['usuario']['id']
    param['productos'] = model.obtener_wishlist(cliente_id)

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
    model.eliminar_producto_wishlist(cliente_id, producto_id)

    return redirect('/cliente/wishlist')


# ---------------------------------------------------------------------------
# PEDIDOS CLIENTE
# ---------------------------------------------------------------------------

def pedidos_usuario(param):

    if 'usuario' not in session:
        return redirect('/login')

    if session['usuario'].get('tipo') == 'admin':
        return redirect('/admin')
    
    cliente_id = session['usuario']['id']
    pedidos = model.obtener_pedidos_cliente(cliente_id)
    return render_template('pedidosusuario.html', pedidos=pedidos, param=param)

    


def miCuenta_pagina(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    # datos desde la sesión
    param['nombre_usuario'] = session['usuario']['nombre']
    param['mail_usuario'] = session['usuario']['mail']

    return render_template('miCuenta.html', **param)



# ---------------------------------------------------------------------------
# ADMIN
# ---------------------------------------------------------------------------

def admin_estadisticas_pagina(param):
    if not es_admin():
        return redirect('/login')

    producto = model.obtener_producto_mas_vendido()
    categorias_db = model.obtener_ventas_por_categoria()

    return render_template(
        'estadisticas.html',
        totemascomprado_nombre=producto[0] if producto else "—",
        totemascomprado_cantidaddeventas=producto[1] if producto else 0,
        categorias=[
            {"nombre": c[0], "ventas": c[1]} for c in categorias_db
        ]
    )


def pedidos_admin_pagina(param):
    if not es_admin():
        return redirect('/login')

    pedidos = model.obtener_pedidos_admin()

    return render_template(
        'pedidosadmin.html',
        pedidos=pedidos,
        param=param
    )


def pedidos_admin_modificar_estado(param, pedido_id):
    if not es_admin():
        return redirect('/login')

    estado = request.form.get('estado')
    model.actualizar_estado_pedido(pedido_id, estado)
    return redirect('/admin/pedidos')


def add_product_pagina(param):
    if not es_admin():
        return redirect('/login')

    return render_template('add_product.html', param=param)

def guardar_producto(param, diRequest):
    if not es_admin():
        return redirect('/login')

    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')

    # subir imagen
    #diResult = getRequest(diRequest)
    filename= upload_file(diRequest)

    # crear producto
    model.crear_producto(
        nombre=nombre,
        precio=precio,
        img=filename,
        descripcion=descripcion
    )


    return redirect('/admin/add_product')


##########################################################################
#                MANEJO DE  SUBIDA DE ARCHIVOS  
##########################################################################

def upload_file (diResult) :
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.jpeg']
    MAX_CONTENT_LENGTH = 1024 * 1024     
    if request.method == 'POST' :         
        for key in request.files.keys():  
            diResult[key]={} 
            diResult[key]['file_error']=False            
            
            f = request.files[key] 
            if f.filename!="":     
                #filename_secure = secure_filename(f.filename)
                file_extension=str(os.path.splitext(f.filename)[1])
                filename_unique = uuid4().__str__() + file_extension
                path_filename=os.path.join( config['upload_folder'] , filename_unique)
                # Validaciones
                if file_extension not in UPLOAD_EXTENSIONS:
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: No se admite subir archivos con extension '+file_extension
                if os.path.exists(path_filename):
                    diResult[key]['file_error']=True
                    diResult[key]['file_msg']='Error: el archivo ya existe.'
                    diResult[key]['file_name']=f.filename
                try:
                    if not diResult[key]['file_error']:
                        diResult[key]['file_error']=True
                        diResult[key]['file_msg']='Se ha producido un error.'

                        f.save(path_filename)   
                        diResult[key]['file_error']=False
                        diResult[key]['file_name_new']=filename_unique
                        diResult[key]['file_name']=f.filename
                        diResult[key]['file_msg']='OK. Archivo cargado exitosamente'
                    return filename_unique
 
                except:
                        pass
            else:
                diResult[key]={} # viene vacio el input del file upload
                
def getRequest(diResult):
    if request.method=='POST':
        for name in request.form.to_dict().keys():
            li=request.form.getlist(name)
            if len(li)>1:
                diResult[name]=request.form.getlist(name)
            elif len(li)==1:
                diResult[name]=li[0]
            else:
                diResult[name]=""
    elif request.method=='GET':  
        for name in request.args.to_dict().keys():
            li=request.args.getlist(name)
            if len(li)>1:
                diResult[name]=request.args.getlist(name)
            elif len(li)==1:
                diResult[name]=li[0]
            else:
                diResult[name]=""     
 
 
 # ---------------------------------------------------------------------------
# CREATOTE
# ---------------------------------------------------------------------------

def creatote_pagina(param):
    if not requiere_login() or es_admin():
        return redirect('/login')

    return render_template('creatote.html', param=param)


# ---------------------------------------------------------------------------
# CREA TU TOTE - resolviendo problemas de la base de datos
# ---------------------------------------------------------------------------

def creatote_funcion(param, diRequest):
    nombre = "Tu tote{}".format(generar_string_aleatorio(10))
    descripcion = ""
    precio = "3000"

    # subir imagen
    #diResult = getRequest(diRequest)
    filename= upload_file(diRequest)

    # crear producto
    model.crear_producto(
        nombre=nombre,
        precio=precio,
        img=filename,
        descripcion=descripcion
    )
    return redirect('/cliente/carrito')




def generar_string_aleatorio(longitud):
    # caracteres posibles
    caracteres = string.ascii_letters + string.digits # Incluye (a-z, A-Z, 0-9)
    
    # caracteres random hasta long
    string_aleatorio = ''.join(random.choice(caracteres) for i in range(longitud))
    
    return string_aleatorio