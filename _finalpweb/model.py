# model.py
# (Archivo completo — modificado ligeramente en dos funciones del bloque CARRITO / WISHLIST)
from _mysql_db import *

# ---------------------------------------------------------------------------
#                                 CLIENTES
# ---------------------------------------------------------------------------

def crearCliente(di):
    ''' Inserta un nuevo cliente en la tabla 'clientes'.
        Recibe 'di' con claves: nombre, mail, contrasena, tipo ('cliente' por default)
        Retorna True si se inserteo (1 fila afectada)
    '''
    sQuery = """
    INSERT INTO clientes
    (id, nombre, tipo, mail, contrasena)
    VALUES
    (NULL, %s, %s, %s, %s);
    """
    tipo = di.get('tipo', 'cliente')
    val = (di.get('nombre'), tipo, di.get('mail'), di.get('contrasena'))
    res = insertDB(BASE, sQuery, val)
    return res == 1


def obtenerClientePorMail(param, mail, clave='usuario'):
    '''Carga en param[clave] la información del cliente con el mail dado.'''
    sSql = """SELECT id, nombre, tipo, mail, contrasena FROM clientes WHERE mail=%s;"""
    val = (mail,)
    fila = selectDB(BASE, sSql, val)

    if fila and len(fila) > 0:
        param[clave] = {
            'id': fila[0][0],
            'nombre': fila[0][1],
            'tipo': fila[0][2],
            'mail': fila[0][3],
            'contrasena': fila[0][4]
        } 
    else:
        param[clave] = {}


def obtenerClientePorId(param, cliente_id, clave='usuario'):
    '''Carga en param[clave] la info del cliente por id'''
    sSql = """SELECT id, nombre, tipo, mail, contrasena FROM clientes WHERE id=%s;"""
    val = (cliente_id,)
    fila = selectDB(BASE, sSql, val)

    if fila and len(fila) > 0:
        param[clave] = {
            'id': fila[0][0],
            'nombre': fila[0][1],
            'tipo': fila[0][2],
            'mail': fila[0][3],
            'contrasena': fila[0][4]
        }
    else:
        param[clave] = {}


def validarClientePorMailYContrasena(result, mail, contrasena):
    '''Verifica si existe un cliente con mail y contrasena.
       Si existe llena 'result' y retorna True, sino False.
    '''
    sSql = """SELECT id, nombre, tipo, mail, contrasena 
              FROM clientes WHERE mail=%s AND contrasena=%s;"""
    val = (mail, contrasena)
    fila = selectDB(BASE, sSql, val)

    if fila and len(fila) > 0:
        result['id'] = fila[0][0]
        result['nombre'] = fila[0][1]
        result['tipo'] = fila[0][2]
        result['mail'] = fila[0][3]
        result['contrasena'] = fila[0][4]
        return True
    return False


def actualizarCliente(di, mail):
    '''Actualiza nombre y contrasena para el cliente identificado por mail'''
    sQuery = """UPDATE clientes SET nombre=%s, contrasena=%s WHERE mail=%s;"""
    val = (di.get('nombre'), di.get('contrasena'), mail)
    res = updateDB(BASE, sQuery, val)
    return res == 1


# ---------------------------------------------------------------------------
# PRODUCTOS
# ---------------------------------------------------------------------------

def crearProducto(di):
    '''Inserta un producto en tabla productos.
    di es un diccionario cuyas claves son nombre, precio_unidad, img y descripcion'''
    sQuery = """
    INSERT INTO productos
    (id, nombre, precio_unidad, img, descripcion, ventas)
    VALUES
    (NULL, %s, %s, %s, %s, 0);
    """
    val = (
        di.get('nombre'),
        di.get('precio_unidad'),
        di.get('img'),
        di.get('descripcion')
    )
    res = insertDB(BASE, sQuery, val)
    return res == 1 #TRUE SI SE AGREGO, FALSE SI HUBO ERROR


def obtenerTodosLosProductos():
    '''Retorna lista completa de productos.'''
    sSql = "SELECT id, nombre, precio_unidad, img, descripcion, ventas FROM productos;"
    filas = selectDB(BASE, sSql)
    if filas:
        return filas
    else:
        return []


def obtenerProductoPorId(producto_id):
    '''Retorna una tupla del producto solicitado o None.'''
    sSql = "SELECT id, nombre, precio_unidad, img, descripcion, ventas FROM productos WHERE id=%s;"
    fila = selectDB(BASE, sSql, (producto_id,))
    if fila:
        return fila[0]
    # Si se encontró una fila, esta línea accede al primer (y único)
    # elemento de la lista fila, que es la tupla que contiene los datos del producto
    else:
        return None



def actualizarProducto(di, producto_id):
    '''Actualiza un producto por id.'''
    sQuery = """
    UPDATE productos
    SET nombre=%s, precio_unidad=%s, img=%s, descripcion=%s
    WHERE id=%s;
    """
    val = (
        di.get('nombre'),
        di.get('precio_unidad'),
        di.get('img'),
        di.get('descripcion'),
        producto_id
    )
    res = updateDB(BASE, sQuery, val)
    return res == 1


def incrementarVentasProducto(producto_id, cantidad):
    '''Incrementa el campo ventas.'''
    sQuery = "UPDATE productos SET ventas = ventas + %s WHERE id=%s;"
    val = (cantidad, producto_id)
    res = updateDB(BASE, sQuery, val)
    return res ==1


# ---------------------------------------------------------------------------
# COLORES y FILTROS
# ---------------------------------------------------------------------------

def agregarColorProducto(producto_id, codigo_hexa):
    sQuery = "INSERT INTO colores (id, productos_id, codigo_hexa) VALUES (NULL, %s, %s);"
    return insertDB(BASE, sQuery, (producto_id, codigo_hexa)) == 1


def obtenerColoresPorProducto(producto_id):
    sSql = "SELECT codigo_hexa FROM colores WHERE productos_id=%s;"
    filas = selectDB(BASE, sSql, (producto_id,))
    return [f[0] for f in filas] if filas else []


def agregarFiltroProducto(producto_id, filtro):
    sQuery = "INSERT INTO filtros (id, productos_id, filtro) VALUES (NULL, %s, %s);"
    return insertDB(BASE, sQuery, (producto_id, filtro)) == 1


def obtenerFiltrosPorProducto(producto_id):
    sSql = "SELECT filtro FROM filtros WHERE productos_id=%s;"
    filas = selectDB(BASE, sSql, (producto_id,))
    return [f[0] for f in filas] if filas else []

def obtenerProductosporFiltros(filtro):
    sSql = """
        SELECT
            productos.nombre AS 'Nombre del Producto'
        FROM
            productos
        INNER JOIN
            filtros ON productos.id = filtros.productos_id
        WHERE
            filtros.filtro=%$ ;"""
    filas = selectDB(BASE, sSql, (filtro,))
    return [f[0] for f in filas] if filas else []
    
    
    


# ---------------------------------------------------------------------------
# CARRITO
# ---------------------------------------------------------------------------

def agregarAlCarrito(cliente_id, producto_id):
    sCheck = "SELECT id FROM carrito WHERE clientes_id=%s AND productos_id=%s;"
    filas = selectDB(BASE, sCheck, (cliente_id, producto_id))

    if filas not in (None, []):
        return False

    sQuery = "INSERT INTO carrito (id, clientes_id, productos_id) VALUES (NULL, %s, %s);"
    return insertDB(BASE, sQuery, (cliente_id, producto_id)) == 1


def quitarDelCarrito(cliente_id, producto_id):
    sQuery = "DELETE FROM carrito WHERE clientes_id=%s AND productos_id=%s;"
    return updateDB(BASE, sQuery, (cliente_id, producto_id)) >= 0


# INICIO NUEVO
# Justificación: carrito.html utiliza producto['descripcion'], así que la consulta debe traer la columna descripcion.
# Se añade p.descripcion al SELECT para que controller pueda mapearlo a los diccionarios que las templates esperan.
def obtenerCarritoPorCliente(cliente_id):
    sSql = """
    SELECT c.id, p.id, p.nombre, p.precio_unidad, p.img, p.descripcion
    FROM carrito c
    JOIN productos p ON c.productos_id = p.id
    WHERE c.clientes_id = %s;
    """
    filas = selectDB(BASE, sSql, (cliente_id,))
    return filas or []
# FIN NUEVO


# ---------------------------------------------------------------------------
# WISHLIST
# ---------------------------------------------------------------------------

def agregarWishlist(cliente_id, producto_id):
    sCheck = "SELECT id FROM wishlist WHERE cliente_id=%s AND producto_id=%s;"
    filas = selectDB(BASE, sCheck, (cliente_id, producto_id))

    if filas not in (None, []):
        return False

    sQuery = "INSERT INTO wishlist (id, cliente_id, producto_id) VALUES (NULL, %s, %s);"
    return insertDB(BASE, sQuery, (cliente_id, producto_id)) == 1


def quitarWishlist(cliente_id, producto_id):
    sQuery = "DELETE FROM wishlist WHERE cliente_id=%s AND producto_id=%s;"
    return updateDB(BASE, sQuery, (cliente_id, producto_id)) >= 0


# INICIO NUEVO
# Justificación: wishlist.html muestra precio, img y podría necesitar descripcion en otros lugares; agrego descripcion al SELECT.
def obtenerWishlistPorCliente(cliente_id):
    sSql = """
    SELECT w.id, p.id, p.nombre, p.precio_unidad, p.img, p.descripcion
    FROM wishlist w
    JOIN productos p ON w.producto_id = p.id
    WHERE w.cliente_id = %s;
    """
    filas = selectDB(BASE, sSql, (cliente_id,))
    return filas or []
# FIN NUEVO


# ---------------------------------------------------------------------------
# PEDIDOS y DETALLE
# ---------------------------------------------------------------------------

def crearPedido(cliente_id, precio_total, fecha=None, estado='espera'):
    if fecha:
        sQuery = """INSERT INTO pedidos (id, cliente_id, fecha, precio_total, estado)
                    VALUES (NULL, %s, %s, %s, %s);"""
        val = (cliente_id, fecha, precio_total, estado)
    else:
        sQuery = """INSERT INTO pedidos (id, cliente_id, fecha, precio_total, estado)
                    VALUES (NULL, %s, CURDATE(), %s, %s);"""
        val = (cliente_id, precio_total, estado)

    res = insertDB(BASE, sQuery, val)

    if res == 1:
        fila = selectDB(BASE, "SELECT MAX(id) FROM pedidos WHERE cliente_id=%s;", (cliente_id,))
        if fila and fila[0][0] is not None:
            return fila[0][0]
    return None


def agregarDetallePedido(pedido_id, producto_id, cantidad, precio_unidad):
    sQuery = """
    INSERT INTO detalle_pedido 
    (id, pedidos_id, productos_id, cantidad, precio_unidad)
    VALUES (NULL, %s, %s, %s, %s);
    """
    return insertDB(BASE, sQuery, (pedido_id, producto_id, cantidad, precio_unidad)) == 1


def obtenerPedidosPorCliente(cliente_id):
    sSql = """SELECT id, cliente_id, fecha, precio_total, estado 
              FROM pedidos WHERE cliente_id=%s ORDER BY fecha DESC;"""
    filas = selectDB(BASE, sSql, (cliente_id,))
    return filas or []


def obtenerPedidoPorId(pedido_id):
    sSql = """SELECT id, cliente_id, fecha, precio_total, estado 
              FROM pedidos WHERE id=%s;"""
    fila = selectDB(BASE, sSql, (pedido_id,))
    return fila[0] if fila else None


def obtenerDetallePedido(pedido_id):
    sSql = """
    SELECT dp.id, p.id, p.nombre, dp.cantidad, dp.precio_unidad
    FROM detalle_pedido dp
    JOIN productos p ON dp.productos_id = p.id
    WHERE dp.pedidos_id = %s;
    """
    filas = selectDB(BASE, sSql, (pedido_id,))
    return filas or []


def actualizarEstadoPedido(pedido_id, nuevo_estado):
    sQuery = "UPDATE pedidos SET estado=%s WHERE id=%s;"
    return updateDB(BASE, sQuery, (nuevo_estado, pedido_id)) >= 0


# ---------------------------------------------------------------------------
# DETALLES PERSONALIZADOS
# ---------------------------------------------------------------------------

def agregarDetallePersonalizado(detalle_pedido_id, img):
    sQuery = "INSERT INTO detalle_personalizados (id, detalle_pedido_id, img) VALUES (NULL, %s, %s);"
    return insertDB(BASE, sQuery, (detalle_pedido_id, img)) == 1


def obtenerPersonalizadosPorDetalle(detalle_pedido_id):
    sSql = "SELECT id, detalle_pedido_id, img FROM detalle_personalizados WHERE detalle_pedido_id=%s;"
    filas = selectDB(BASE, sSql, (detalle_pedido_id,))
    return filas or []


# ---------------------------------------------------------------------------
# ESTADISTICAS
# ---------------------------------------------------------------------------

def productoMasComprado():
    sSql = """
    SELECT p.nombre, COALESCE(SUM(dp.cantidad),0) as total
    FROM detalle_pedido dp
    JOIN productos p ON dp.productos_id = p.id
    GROUP BY p.id
    ORDER BY total DESC
    LIMIT 1;
    """
    fila = selectDB(BASE, sSql)
    return (fila[0][0], fila[0][1]) if fila else (None, 0)


def ventasPorCategoria():
    sSql = """
    SELECT f.filtro, COALESCE(SUM(dp.cantidad),0) as total
    FROM filtros f
    LEFT JOIN productos p ON f.productos_id = p.id
    LEFT JOIN detalle_pedido dp ON dp.productos_id = p.id
    GROUP BY f.filtro
    ORDER BY total DESC;
    """
    filas = selectDB(BASE, sSql)
    return filas or []


# ---------------------------------------------------------------------------
# UTILIDADES VARIAS
# ---------------------------------------------------------------------------

def contarProductos():
    fila = selectDB(BASE, "SELECT COUNT(*) FROM productos;")
    return fila[0][0] if fila else 0


def buscarProductosPorNombre(q):
    sSql = """SELECT id, nombre, precio_unidad, img, descripcion, ventas
              FROM productos WHERE nombre LIKE %s;"""
    val = ('%' + q + '%',)
    filas = selectDB(BASE, sSql, val)
    return filas or []


##### INICIO NUEVO (faltaban funciones llamadas por controller)

def obtenerPedidosParaAdmin():
    '''
        Devuelve lista de pedidos (JOIN con clientes) para el panel admin.
        Columnas devueltas:
            pedidos.id, clientes.nombre, pedidos.fecha, pedidos.estado, pedidos.total
    '''
    sQuery = """
        SELECT p.id, c.nombre, p.fecha, p.estado, p.total
        FROM pedidos p
        INNER JOIN clientes c ON p.clientes_id = c.id
        ORDER BY p.fecha DESC;
    """
    return selectDB(BASE, sQuery)


def productoMasVendido():
    '''
        Devuelve el producto con mayor cantidad de ventas.
        Columnas devueltas:
            id, nombre, ventas, precio, categoria, img
    '''
    sQuery = """
        SELECT id, nombre, ventas, precio, categoria, img
        FROM productos
        ORDER BY ventas DESC
        LIMIT 1;
    """
    return selectDB(BASE, sQuery)

##### FIN NUEVO
