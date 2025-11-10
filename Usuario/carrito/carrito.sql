USE base_le_totette;

-- ==============================================
-- 1) VERIFICAR ESTRUCTURA DE TABLAS RELACIONADAS
-- ==============================================
SELECT * FROM clientes;
SELECT * FROM productos;
SELECT * FROM carrito;

-- evitar duplicados:
ALTER TABLE carrito ADD UNIQUE KEY uq_cliente_producto (clientes_id, productos_id);

-- ==============================================
-- 2) AGREGAR PRODUCTO AL CARRITO
-- ==============================================
-- Un cliente puede agregar varios productos a su carrito. --> Ejemplo: el cliente con id = 1 agrega el producto con id = 3.
INSERT INTO carrito (clientes_id, productos_id) 
VALUES (1, 1);

-- Si el cliente agrega otro producto:
INSERT INTO carrito (clientes_id, productos_id)
VALUES (1, 4);

-- si asignamos un id de producto no existente:
INSERT INTO carrito (clientes_id, productos_id)
VALUES (1, 5);
-- ==============================================
-- 3) VER PRODUCTOS DEL CARRITO DE UN CLIENTE
-- ==============================================
-- Muestra todos los productos que el cliente tiene actualmente en su carrito,
-- junto con su nombre, precio y descripción.

SELECT
  c.id AS id_carrito,
  cl.nombre AS cliente,
  p.nombre AS producto,
  p.descripcion,
  p.precio_unidad
FROM carrito c
JOIN clientes cl ON cl.id = c.clientes_id
JOIN productos p ON p.id = c.productos_id
WHERE c.clientes_id = 1;

-- ==============================================
-- 4) ACTUALIZAR CANTIDAD DE UN PRODUCTO EN EL CARRITO
-- ==============================================
-- Si el carrito no tiene columna “cantidad”, primero se debe agregar:
ALTER TABLE carrito ADD COLUMN cantidad INT DEFAULT 1;

-- Cambiar la cantidad de un producto específico del cliente.
UPDATE carrito
SET cantidad = 2
WHERE clientes_id = 1 AND productos_id = 3;

-- ==============================================
-- 5) ELIMINAR UN PRODUCTO DEL CARRITO
-- ==============================================
-- Borra un producto puntual del carrito del cliente.
DELETE FROM carrito
WHERE clientes_id = 1 AND productos_id = 3;

-- ==============================================
-- 6) VACIAR COMPLETAMENTE EL CARRITO DE UN CLIENTE
-- ==============================================
DELETE FROM carrito
WHERE clientes_id = 1;

-- ==============================================
-- 7) CONSULTA FINAL PARA VERIFICAR CAMBIOS --> cliente, product, cantidad y precio
-- ==============================================
SELECT
  c.id AS id_carrito,
  cl.nombre AS cliente,
  p.nombre AS producto,
  c.cantidad,
  p.precio_unidad,
  (c.cantidad * p.precio_unidad) AS subtotal
--   SUM(c.cantidad * p.precio_unidad) AS total_general
FROM carrito c
JOIN clientes cl ON cl.id = c.clientes_id
JOIN productos p ON p.id = c.productos_id
WHERE c.clientes_id = 1

UNION ALL

SELECT
  NULL AS id_carrito,
  NULL AS cliente,
  'TOTAL GENERAL' AS producto,
  NULL AS cantidad,
  NULL AS precio_unidad,
  SUM(c.cantidad * p.precio_unidad) AS subtotal
FROM carrito c
JOIN clientes cl ON cl.id = c.clientes_id
JOIN productos p ON p.id = c.productos_id
WHERE c.clientes_id = 1;
