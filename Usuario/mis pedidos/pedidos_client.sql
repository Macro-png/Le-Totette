-- ==============================================
-- CREAR PEDIDO + DETALLES
-- ==============================================
USE base_le_totette;

SELECT * FROM clientes;

SELECT * FROM pedidos;
alter table pedidos auto_increment = 1;
-- delete from pedidos;
delete from pedidos where id = 2;

-- 1) Insertar el pedido (cliente por mail; fecha y estado inicial)
INSERT INTO pedidos (cliente_id, fecha, estado, precio_total)
VALUES
(1,NOW(),'espera', 20),
(2,NOW(),'espera', 80.30),
(3,NOW(),'espera', 15.20),
(2,NOW(),'espera', 25),
(1,NOW(),'espera', 30),
(4,NOW(),'espera', 50),
(2,NOW(),'espera', 50),
(5,NOW(),'espera', 50),
(2,NOW(),'espera', 50),
(1,NOW(),'espera', 60),
(1,NOW(),'espera', 70),
(2,NOW(),'espera', 90),
(3,NOW(),'espera', 10),
(4,NOW(),'espera', 10),
(6,NOW(),'espera', 50);

-- ============================================
-- 2) Insertar los detalles del pedido
-- ============================================
-- Antes de esto, hay que ver el id del pedido recién creado.

-- Producto 1, cantidad 2:
INSERT INTO detalle_pedido (pedidos_id, productos_id, cantidad, precio_unidad)
SELECT 8, p.id, 2, p.precio_unidad
FROM productos p
WHERE p.id = 1;

-- Producto 3, cantidad 1:
INSERT INTO detalle_pedido (pedidos_id, productos_id, cantidad, precio_unidad)
SELECT 8, p.id, 1, p.precio_unidad
FROM productos p
WHERE p.id = 3;

-- Producto 5, cantidad 4 -----> no devuelve nada cuando colocas un id que no existe:
INSERT INTO detalle_pedido (pedidos_id, productos_id, cantidad, precio_unidad)
SELECT 8, p.id, 4, p.precio_unidad
FROM productos p
WHERE p.id = 5;

-- ============================================
-- 3) Actualizar el precio total del pedido
-- ============================================
UPDATE pedidos
SET precio_total = (
  SELECT SUM(dp.cantidad * dp.precio_unidad)
  FROM detalle_pedido dp
  WHERE dp.pedidos_id = 8
)
WHERE id = 8;

-- ============================================
-- 4) Consultar el pedido y sus detalles
-- ============================================

-- Cabecera:
SELECT
  p.id AS pedido_id,
  c.nombre AS cliente,
  p.fecha,
  p.estado,
  p.precio_total
FROM pedidos p
JOIN clientes c ON c.id = p.cliente_id
WHERE p.id = 8;

-- Detalles:
SELECT
  dp.id AS detalle_id,
  pr.nombre AS producto,
  dp.cantidad,
  dp.precio_unidad,
  (dp.cantidad * dp.precio_unidad) AS subtotal
FROM detalle_pedido dp
JOIN productos pr ON pr.id = dp.productos_id
WHERE dp.pedidos_id = 8
ORDER BY dp.id;