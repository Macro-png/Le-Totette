-- ==============================================
-- CREAR PEDIDO + DETALLES
-- ==============================================
USE base_le_totette;

SELECT * FROM clientes;

SELECT * FROM pedidos;
alter table pedidos auto_increment = 1;
delete from pedidos;
SELECT * FROM productos;

-- 1) Insertar el pedido (cliente por mail; fecha y estado inicial)
INSERT INTO pedidos (cliente_id, fecha, estado, precio_total)
SELECT c.id, NOW(), 'espera', 0
FROM clientes c
WHERE c.mail = 'mariano@gmail.com'
LIMIT 1;

SELECT * FROM detalle_pedido;
-- 2) Insertar DETALLE 1 (trae productos_id y precio_unidad desde productos)
INSERT INTO detalle_pedido (pedidos_id, productos_id, cantidad, precio_unidad)
SELECT
  ( SELECT id
    FROM pedidos
    WHERE cliente_id = (SELECT id FROM clientes WHERE mail = 'mariano@gmail.com' LIMIT 1)
    ORDER BY id DESC
    LIMIT 1 ),
  p.id,
  1,                              -- << cantidad del producto 1
  p.precio_unidad
FROM productos p
WHERE p.nombre = 'Tote Bag Clásica'   -- << nombre exacto del producto 1
LIMIT 1;

-- 3) Insertar DETALLE 2
INSERT INTO detalle_pedido (pedidos_id, productos_id, cantidad, precio_unidad)
SELECT
  ( SELECT id
    FROM pedidos
    WHERE cliente_id = (SELECT id FROM clientes WHERE mail = 'mariano@gmail.com' LIMIT 1)
    ORDER BY id DESC
    LIMIT 1 ),
  p.id,
  2,                              -- << cantidad del producto 2
  p.precio_unidad
FROM productos p
WHERE p.nombre = 'Tote Bag Floral'    -- << nombre exacto del producto 2
LIMIT 1;

-- 4) Recalcular y actualizar el precio_total del pedido recién creado
UPDATE pedidos p
JOIN (
  SELECT d.pedidos_id, SUM(d.cantidad * d.precio_unidad) AS total
  FROM detalle_pedido d
  WHERE d.pedidos_id = (
    SELECT id
    FROM pedidos
    WHERE cliente_id = (SELECT id FROM clientes WHERE mail = 'mariano@gmail.com' LIMIT 1)
    ORDER BY id DESC
    LIMIT 1
  )
  GROUP BY d.pedidos_id
) x ON x.pedidos_id = p.id
SET p.precio_total = x.total
WHERE p.id = (
  SELECT id
  FROM pedidos
  WHERE cliente_id = (SELECT id FROM clientes WHERE mail = 'mariano@gmail.com' LIMIT 1)
  ORDER BY id DESC
  LIMIT 1
);

-- 5) Ver CABECERA del pedido creado
SELECT 
  p.id AS pedido_id,
  c.nombre AS cliente,
  DATE_FORMAT(p.fecha,'%d/%m/%Y') AS fecha,
  p.estado,
  p.precio_total
FROM pedidos p
INNER JOIN clientes c ON c.id = p.cliente_id
WHERE p.id = (
  SELECT id
  FROM pedidos
  WHERE cliente_id = (SELECT id FROM clientes WHERE mail = 'mariano@gmail.com' LIMIT 1)
  ORDER BY id DESC
  LIMIT 1
);

-- 6) Ver DETALLES del pedido
SELECT
  d.id AS detalle_id,
  pr.nombre AS producto,
  d.cantidad,
  d.precio_unidad,
  (d.cantidad * d.precio_unidad) AS subtotal
FROM detalle_pedido d
INNER JOIN productos pr ON pr.id = d.productos_id
WHERE d.pedidos_id = (
  SELECT id
  FROM pedidos
  WHERE cliente_id = (SELECT id FROM clientes WHERE mail = 'mariano@gmail.com' LIMIT 1)
  ORDER BY id DESC
  LIMIT 1
)
ORDER BY d.id;
