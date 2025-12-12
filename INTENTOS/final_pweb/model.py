from _mysql_db import selectDB, insertDB, updateDB, deleteDB, BASE

# -------------------------
# CLIENTES
# -------------------------
def crearCliente(di):
    """
    Inserta un nuevo cliente debe contener: nombre, mail, contrasena
    El tipo siempre es cliente
    Para hacer un admin se hace de la base de datos
    """
    sql = "INSERT INTO clientes (nombre, tipo, mail, contrasena) VALUES (%s, %s, %s, %s)"
    val = (di.get('nombre'), 'cliente', di.get('email'), di.get('contrasena'))
    return insertDB(BASE, sql, val) == 1 #True o false dependiendo si se pudo
                                         #agregar correctamente o no

def obtenerClienteXMail(mail):
    sql = "SELECT id, nombre, tipo, mail, contrasena FROM clientes WHERE mail=%s"
    rows = selectDB(BASE, sql, (mail,))
    if rows:
        res=rows[0]
    else:
        res=None
    return res

def validarCliente(mail, contrasena):
    """
    Valida credenciales. Retorna (id, nombre, tipo, mail) o None.
    """
    sql = "SELECT id, nombre, tipo, mail FROM clientes WHERE mail=%s AND contrasena=%s"
    rows = selectDB(BASE, sql, (mail, contrasena))
    if rows:
        res=rows[0]
    else:
        res=None
    return res

# -------------------------
# PRODUCTOS
# -------------------------
def crearProducto(di):
    """
    Crea un producto  debe contener: nombre, precio_unidad, img, descripcion
    ventas se inicializa en 0.
    """
    sql = """INSERT INTO productos (nombre, precio_unidad, img, descripcion, ventas)
             VALUES (%s, %s, %s, %s, %s)"""
    val = (di.get('nombre'), di.get('precio_unidad'), di.get('img') or '', di.get('caract') or '', 0)
    return insertDB(BASE, sql, val) == 1

def obtenerProductos():
    sql = "SELECT id, nombre, precio_unidad, img, descripcion, ventas FROM productos"
    return selectDB(BASE, sql)

def obtenerProductoPorId(pid):
    sql = "SELECT id, nombre, precio_unidad, img, descripcion, ventas FROM productos WHERE id=%s"
    rows = selectDB(BASE, sql, (pid,))
    return rows[0] if rows else None

def obtenerColoresProducto(productos_id):
    """
    Devuelve una lista de colores para un producto.
    Cada color tiene: codigo (ej #F5F5F5)
    """
    sql = "SELECT codigo FROM colores WHERE productos_id=%s"
    return selectDB(BASE, sql, (productos_id,))

# -------------------------
# WISHLIST
# -------------------------
def agregarWishlist(clientes_id, productos_id):
    sql = "INSERT INTO wishlist (clientes_id, productos_id) VALUES (%s, %s)"
    return insertDB(BASE, sql, (clientes_id, productos_id)) == 1

def quitarWishlist(clientes_id, productos_id):
    sql = "DELETE FROM wishlist WHERE clientes_id=%s AND productos_id=%s"
    return deleteDB(BASE, sql, (clientes_id, productos_id)) >= 1

def obtenerWishlistCliente(clientes_id):
    sql = """SELECT p.id, p.nombre, p.precio_unidad, p.img, p.descripcion
             FROM productos p
             JOIN wishlist w ON w.productos_id = p.id
             WHERE w.clientes_id = %s"""
    return selectDB(BASE, sql, (clientes_id,))

# -------------------------
# CARRITO
# -------------------------
def agregarCarrito(clientes_id, productos_id):
    sql = "INSERT INTO carrito (clientes_id, productos_id) VALUES (%s, %s)"
    return insertDB(BASE, sql, (clientes_id, productos_id)) == 1

def quitarCarrito(clientes_id, productos_id):
    sql = "DELETE FROM carrito WHERE clientes_id=%s AND productos_id=%s"
    return deleteDB(BASE, sql, (clientes_id, productos_id)) >= 1

def obtenerCarritoCliente(clientes_id):
    sql = """SELECT p.id, p.nombre, p.precio_unidad, p.img, p.descripcion
             FROM productos p
             JOIN carrito c ON c.productos_id = p.id
             WHERE c.clientes_id = %s"""
    return selectDB(BASE, sql, (clientes_id,))

# -------------------------
# PEDIDOS
# -------------------------
def crearPedido(clientes_id, precio_total):
    """
    Inserta un pedido (cabecera). Retorna True/False.
    (Este método no devuelve el id insertado; si lo necesitás con precisión
    en producción hay que usar una transacción con lastrowid).
    """
    sql = "INSERT INTO pedidos (clientes_id, fecha, precio_total, estado) VALUES (%s, CURDATE(), %s, %s)"
    return insertDB(BASE, sql, (clientes_id, precio_total, 'espera')) == 1

def crearDetallePedido(pedidos_id, productos_id, cantidad, precio_unidad):
    sql = "INSERT INTO detalle_pedido (pedidos_id, productos_id, cantidad, precio_unidad) VALUES (%s, %s, %s, %s)"
    return insertDB(BASE, sql, (pedidos_id, productos_id, cantidad, precio_unidad)) == 1

def obtenerPedidosPorCliente(clientes_id):
    sql = "SELECT id, clientes_id, fecha, precio_total, estado FROM pedidos WHERE clientes_id=%s ORDER BY id DESC"
    return selectDB(BASE, sql, (clientes_id,))

def obtenerTodosPedidos():
    sql = "SELECT id, clientes_id, fecha, precio_total, estado FROM pedidos ORDER BY id DESC"
    return selectDB(BASE, sql)

def actualizarEstadoPedido(pedidos_id, nuevo_estado):
    sql = "UPDATE pedidos SET estado=%s WHERE id=%s"
    return updateDB(BASE, sql, (nuevo_estado, pedidos_id)) == 1

# -------------------------
# DETALLE PERSONALIZADOS
# -------------------------
def guardarTotePersonalizado(clientes_id, img_name, color=None, estampa=None):
    """
    Guarda una personalización 
    """
    sql = "INSERT INTO detalle_personalizados (clientes_id, img, color, estampa) VALUES (%s, %s, %s, %s)"
    return insertDB(BASE, sql, (clientes_id, img_name, color or '', estampa or '')) == 1

