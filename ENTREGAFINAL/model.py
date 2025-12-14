
from _mysql_db import *

# ---------------------------------------------------------------------------
# CLIENTES
# ---------------------------------------------------------------------------

def crearCliente(di):
    sQuery = """
    INSERT INTO clientes (id, nombre, tipo, mail, contrasena)
    VALUES (NULL, %s, %s, %s, %s);
    """
    val = (
        di.get('nombre'),
        di.get('tipo', 'cliente'),
        di.get('mail'),
        di.get('contrasena')
    )
    return insertDB(BASE, sQuery, val) == 1


def validarClientePorMailYContrasena(result, mail, contrasena):
    sSql = """
    SELECT id, nombre, tipo, mail, contrasena
    FROM clientes
    WHERE mail=%s AND contrasena=%s;
    """
    val = (mail, contrasena)
    fila = selectDB(BASE, sSql, val)

    if fila and len(fila) > 0:
        fila = fila[0]
        result['id'] = fila[0]
        result['nombre'] = fila[1]
        result['tipo'] = fila[2]
        result['mail'] = fila[3]
        result['contrasena'] = fila[4]
        return True
    return False

# ---------------------------------------------------------------------------
# PRODUCTOS
# ---------------------------------------------------------------------------

def crear_producto(nombre, precio, img, descripcion):
    sSql = """
    INSERT INTO productos (nombre, precio_unidad, img, descripcion, ventas)
    VALUES (%s, %s, %s, %s, 0);
    """
    return insertDB(BASE, sSql, (nombre, precio, img, descripcion)) == 1

def actualizar_producto(pid, nombre, precio, img, descripcion):
    sSql = """
    UPDATE productos
    SET nombre=%s, precio_unidad=%s, img=%s, descripcion=%s
    WHERE id=%s;
    """
    return updateDB(BASE, sSql, (nombre, precio, img, descripcion, pid)) == 1

def eliminar_colores_producto(pid):
    return deleteDB(BASE, "DELETE FROM colores WHERE productos_id=%s;", (pid,)) > 0

def agregar_color(pid, codigo):
    return insertDB(BASE,
        "INSERT INTO colores (productos_id, codigo_hexa) VALUES (%s,%s);",
        (pid, codigo)
    ) == 1
    
def eliminar_filtros_producto(pid):
    return deleteDB(BASE, "DELETE FROM filtros WHERE productos_id=%s;", (pid,)) > 0

def agregar_filtro(pid, filtro):
    return insertDB(
        BASE,
        "INSERT INTO filtros (productos_id, filtro) VALUES (%s,%s);",
        (pid, filtro)
    ) == 1


def obtenerTodosLosProductos():
    sSql = """
    SELECT id, nombre, precio_unidad, img, descripcion, ventas
    FROM productos;
    """
    return selectDB(BASE, sSql)

def obtenerProductoPorId(pid):
    sSql = """
    SELECT id, nombre, precio_unidad, img, descripcion
    FROM productos
    WHERE id = %s;
    """
    fila = selectDB(BASE, sSql, (pid,))
    return fila[0] if fila else None

def obtenerProductosporFiltros(filtro):
    sSql = """
        SELECT
            productos.nombre AS 'Nombre del Producto'
        FROM
            productos
        INNER JOIN
            filtros ON productos.id = filtros.productos_id
        WHERE
            filtros.filtro=%s ;"""
    filas = selectDB(BASE, sSql, (filtro,))
    return [f[0] for f in filas] if filas else []


# ---------------------------------------------------------------------------
# CARRITO
# ---------------------------------------------------------------------------

def agregar_producto_carrito(cliente_id, producto_id):
    sSql = """
    INSERT INTO carrito (clientes_id, productos_id)
    VALUES (%s, %s);
    """
    return insertDB(BASE, sSql, (cliente_id, producto_id)) == 1

def obtener_carrito(cliente_id):
    sSql = """
    SELECT p.id, p.nombre, p.precio_unidad, p.img
    FROM carrito c
    JOIN productos p ON p.id = c.productos_id
    WHERE c.clientes_id = %s;
    """
    return selectDB(BASE, sSql, (cliente_id,))

def eliminar_producto_carrito(cliente_id, producto_id):
    sSql = """
    DELETE FROM carrito
    WHERE clientes_id = %s AND productos_id = %s;
    """
    return deleteDB(BASE, sSql, (cliente_id, producto_id)) > 0

def vaciar_carrito(cliente_id):
    sSql = """
    DELETE FROM carrito
    WHERE clientes_id = %s;
    """
    return deleteDB(BASE, sSql, (cliente_id,)) > 0

def obtener_total_carrito(cliente_id):
    sSql = """
    SELECT SUM(p.precio_unidad)
    FROM carrito c
    JOIN productos p ON p.id = c.productos_id
    WHERE c.clientes_id = %s;
    """
    fila = selectDB(BASE, sSql, (cliente_id,))
    return fila[0][0] if fila and fila[0][0] else 0



# ---------------------------------------------------------------------------
# WISHLIST
# ---------------------------------------------------------------------------

def agregar_wishlist(cliente_id, producto_id):
    sSql = """
    INSERT INTO wishlist (cliente_id, producto_id)
    VALUES (%s, %s);
    """
    return insertDB(BASE, sSql, (cliente_id, producto_id)) == 1

def obtener_wishlist(cliente_id):
    sSql = """
    SELECT p.id, p.nombre, p.precio_unidad, p.img
    FROM wishlist w
    JOIN productos p ON p.id = w.producto_id
    WHERE w.cliente_id = %s;
    """
    return selectDB(BASE, sSql, (cliente_id,))

def eliminar_wishlist(cliente_id, producto_id):
    sSql = """
    DELETE FROM wishlist
    WHERE cliente_id = %s AND producto_id = %s;
    """
    return deleteDB(BASE, sSql, (cliente_id, producto_id)) > 0


# ---------------------------------------------------------------------------
# PEDIDOS
# ---------------------------------------------------------------------------

def obtener_pedidos_cliente(cliente_id):
    sSql = """
    SELECT id, fecha, precio_total, estado
    FROM pedidos
    WHERE cliente_id = %s;
    """
    return selectDB(BASE, sSql, (cliente_id,))

def obtener_pedidos_admin():
    sSql = """
    SELECT p.id, c.nombre, p.fecha, p.precio_total, p.estado
    FROM pedidos p
    JOIN clientes c ON c.id = p.cliente_id;
    """
    return selectDB(BASE, sSql)

def actualizar_estado_pedido(pedido_id, estado):
    sSql = """
    UPDATE pedidos
    SET estado = %s
    WHERE id = %s;
    """
    return updateDB(BASE, sSql, (estado, pedido_id)) == 1


# ---------------------------------------------------------------------------
# ESTADÍSTICAS
# ---------------------------------------------------------------------------

def obtenerEstadisticas():
    data = {}

    sSql = """
    SELECT nombre, ventas
    FROM productos
    ORDER BY ventas DESC
    LIMIT 1;
    """
    fila = selectDB(BASE, sSql)
    data['nombre'] = fila[0][0] if fila else ""
    data['ventas'] = fila[0][1] if fila else 0

    sSql = """
    SELECT filtro, COUNT(*) 
    FROM filtros
    GROUP BY filtro;
    """
    data['categorias'] = selectDB(BASE, sSql)

    return data