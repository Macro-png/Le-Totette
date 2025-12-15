
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

def actualizar_contrasena(cliente_id, nueva_contrasena):
    sSql = """
        UPDATE clientes
        SET contrasena = %s
        WHERE id = %s;
    """
    return updateDB(BASE, sSql, (nueva_contrasena, cliente_id))


# ---------------------------------------------------------------------------
# PRODUCTOS
# ---------------------------------------------------------------------------

def crear_producto(nombre, precio, img, descripcion):
    sSql = """
    INSERT INTO productos (nombre, precio_unidad, img, descripcion, ventas)
    VALUES (%s, %s, %s, %s, 0)
    ON DUPLICATE KEY UPDATE
        precio_unidad = VALUES(precio_unidad),
        img = VALUES(img),
        descripcion = VALUES(descripcion);
    """
    return insertDB(BASE, sSql, (nombre, precio, img, descripcion)) >= 1


def actualizar_producto(pid, nombre, precio, img, descripcion):
    sSql = """
    UPDATE productos
    SET nombre=%s, precio_unidad=%s, img=%s, descripcion=%s
    WHERE id=%s;
    """
    return updateDB(BASE, sSql, (nombre, precio, img, descripcion, pid)) == 1


def eliminar_filtros_producto(pid):
    return deleteDB(BASE, "DELETE FROM filtros WHERE productos_id=%s;", (pid,)) >= 0


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
    if not fila:
        return None

    fila = fila[0]
    return {
        'id': fila[0],
        'nombre': fila[1],
        'precio_unidad': fila[2],
        'img': fila[3],
        'descripcion': fila[4]
    }


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
    INSERT INTO carrito (clientes_id, productos_id, cantidad)
    VALUES (%s, %s, 1)
    ON DUPLICATE KEY UPDATE
        cantidad = cantidad + 1;
    """
    return insertDB(BASE, sSql, (cliente_id, producto_id)) is not None


def obtener_carrito(cliente_id):
    sSql = """
    SELECT 
        p.id,
        p.nombre,
        p.precio_unidad,
        p.img,
        c.cantidad,
        (p.precio_unidad * c.cantidad) AS subtotal
    FROM carrito c
    JOIN productos p ON p.id = c.productos_id
    WHERE c.clientes_id = %s;
    """
    return selectDB(BASE, sSql, (cliente_id,))


def eliminar_producto_carrito(cliente_id, producto_id):
    # baja cantidad
    sSql_update = """
    UPDATE carrito
    SET cantidad = cantidad - 1
    WHERE clientes_id = %s
      AND productos_id = %s
      AND cantidad > 1;
    """
    filas = updateDB(BASE, sSql_update, (cliente_id, producto_id))

    # 2. si no se actualizó nada, borrar
    if filas == 0:
        sSql_delete = """
        DELETE FROM carrito
        WHERE clientes_id = %s
          AND productos_id = %s
          AND cantidad = 1
        LIMIT 1;
        """
        return deleteDB(BASE, sSql_delete, (cliente_id, producto_id)) > 0

    return True


def vaciar_carrito(cliente_id):
    sSql = """
    DELETE FROM carrito
    WHERE clientes_id = %s;
    """
    return deleteDB(BASE, sSql, (cliente_id,)) > 0

def obtener_total_carrito(cliente_id):
    sSql = """
    SELECT SUM(p.precio_unidad * c.cantidad)
    FROM carrito c
    JOIN productos p ON p.id = c.productos_id
    WHERE c.clientes_id = %s;
    """
    fila = selectDB(BASE, sSql, (cliente_id,))
    return fila[0][0] if fila and fila[0][0] else 0

def crear_pedido(cliente_id, total):
    sSql = """
    INSERT INTO pedidos (cliente_id, fecha, precio_total, estado)
    VALUES (%s, CURDATE(), %s, 'espera');
    """
    return insertDB(BASE, sSql, (cliente_id, total))

def agregar_detalle_pedido(pedido_id, producto_id, cantidad, precio):
    sSql = """
    INSERT INTO detalle_pedido (pedidos_id, productos_id, cantidad, precio_unidad)
    VALUES (%s, %s, %s, %s);
    """
    return insertDB(BASE, sSql, (pedido_id, producto_id, cantidad, precio)) == 1


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



def eliminar_producto_wishlist(cliente_id, producto_id):
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


def obtener_pedidos_cliente_con_productos(cliente_id):
    sSql = """
    SELECT 
        p.id AS pedido_id,
        p.fecha,
        p.precio_total,
        p.estado,
        pr.id AS producto_id,
        pr.nombre,
        pr.img,
        dp.cantidad
    FROM pedidos p
    JOIN detalle_pedido dp ON dp.pedidos_id = p.id
    JOIN productos pr ON pr.id = dp.productos_id
    WHERE p.cliente_id = %s
    ORDER BY p.id DESC;
    """
    rows = selectDB(BASE, sSql, (cliente_id,))

    pedidos = {}
    for r in rows:
        pedido_id = r[0]

        if pedido_id not in pedidos:
            pedidos[pedido_id] = {
                "id": pedido_id,
                "fecha": r[1],
                "precio_total": r[2],
                "estado": r[3],
                "productos": []
            }

        pedidos[pedido_id]["productos"].append({
            "id": r[4],
            "nombre": r[5],
            "img": r[6],
            "cantidad": r[7]
        })

    return list(pedidos.values())

def actualizar_estado_pedido(pedido_id, estado):
    sSql = """
    UPDATE pedidos
    SET estado = %s
    WHERE id = %s;
    """
    return updateDB(BASE, sSql, (estado, pedido_id)) == 1

def aumentar_ventas_producto(producto_id, cantidad):
    sSql = """
    UPDATE productos
    SET ventas = ventas + %s
    WHERE id = %s;
    """
    return updateDB(BASE, sSql, (cantidad, producto_id)) == 1

# ---------------------------------------------------------------------------
# ESTADÍSTICAS
# ---------------------------------------------------------------------------

def obtener_producto_mas_vendido():
    sSql = """
    SELECT nombre, ventas
    FROM productos
    ORDER BY ventas DESC
    LIMIT 1;
    """
    fila = selectDB(BASE, sSql)
    return fila[0] if fila else None

def obtener_ventas_por_categoria():
    sSql = """
    SELECT c.nombre, COALESCE(SUM(p.ventas), 0)
    FROM categorias c
    LEFT JOIN productos p ON p.categoria_id = c.id
    GROUP BY c.id;
    """
    return selectDB(BASE, sSql) or []


#-----------------------------------------
#              CREA TU TOTE
#-----------------------------------------



def agregar_producto_carrito_por_nombre(cliente_id, nombre):
    sSql = """
    INSERT INTO carrito (clientes_id, productos_id, cantidad)
    VALUES (%s, (SELECT id FROM productos WHERE nombre = %s),  1) """
    return insertDB(BASE, sSql, (cliente_id, nombre)) is not None


def creatutote(nombre, precio, img, descripcion):
    sSql = """
    INSERT INTO productos (img)
    VALUES (%s)
    """
    return insertDB(BASE, sSql, (img))