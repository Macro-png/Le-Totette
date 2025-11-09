-- ===========================================================
-- Acciones del Administrador sobre PEDIDOS:
--  A) Cambiar estado de un pedido (espera, produccion, retirar, cancelado)
-- ===========================================================
USE base_le_totette;
show tables;
-- ===========================================================
-- DATOS DE EJEMPLO PARA DEMOSTRACIÓN (INSERTS)
-- ===========================================================

-- 1 Insertar algunos clientes de ejemplo
INSERT INTO clientes (nombre, mail, tipo) VALUES
('Laura Gómez', 'laura@example.com', 'cliente'),
('Carlos Ruiz', 'carlos@example.com', 'cliente'),
('Mariana Pérez', 'mariana@example.com', 'cliente');

-- 2 Insertar algunos productos (totebags)
INSERT INTO productos (nombre, descripcion, precio_unidad, img) VALUES
('Tote Bag Clásica', 'Totebag blanca con logo minimalista', 25.00, 'img1'),
('Tote Bag Floral', 'Totebag con estampado de flores', 30.00, 'img2'),
('Tote Bag Negra', 'Totebag negra con diseño moderno', 28.50, 'img3');
select * from productos;
-- 3 Insertar algunos pedidos
INSERT INTO pedidos (cliente_id,  fecha, estado, precio_total) VALUES
(1, NOW(), 'espera', 55.00),
(2, NOW(), 'produccion', 30.00),
(3, NOW(), 'retirar', 28.50),
(1, NOW(), 'espera', 83.50),
(2, NOW(), 'produccion', 25.00);

-- 4 Insertar detalles de los pedidos
INSERT INTO detalle_pedido (pedidos_id, productos_id, cantidad, precio_unidad) VALUES
(1, 1, 1, 25.00),
(1, 1, 1, 25.00),
(1, 1, 1, 25.00),
(1, 2, 1, 30.00),
(2, 2, 1, 30.00),
(3, 3, 1, 28.50),
(4, 1, 2, 25.00),
(4, 2, 1, 33.50),
(5, 1, 1, 25.00);

-- ========= FIN DE INSERTS DE DEMOSTRACIÓN =========
-- (verificación rápida)
SELECT DISTINCT estado FROM pedidos;

-- ===========================================================
-- A) CAMBIAR ESTADO DE UN PEDIDO
--    Usando exactamente los valores del ENUM:
--    'espera' | 'produccion' | 'retirar' | 'cancelado'
-- ===========================================================

-- A.1) Cambiar a 'espera'
-- Reemplaza ? por el ID real del pedido
-- antes de actualizar, puedes verificar que el pedido existe
SELECT id, estado FROM pedidos WHERE id = ?;
UPDATE pedidos
SET estado = 'espera'
WHERE id = ?;

-- A.2) Cambiar a 'produccion'
SELECT id, estado FROM pedidos WHERE id = ?;
UPDATE pedidos
SET estado = 'produccion'
WHERE id = ?;

-- A.3) Cambiar a 'retirar'   (armonizado con el front)
SELECT id, estado FROM pedidos WHERE id = ?;
UPDATE pedidos
SET estado = 'retirar'
WHERE id = ?;

-- A.4) Cambiar a 'cancelado'   (armonizado con el front)
SELECT id, estado FROM pedidos WHERE id = ?;
UPDATE pedidos
SET estado = 'cancelado'
WHERE id = 2;

select * from pedidos;