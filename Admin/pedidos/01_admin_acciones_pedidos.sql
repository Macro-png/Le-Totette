-- ===========================================================
-- Acciones del Administrador sobre PEDIDOS:
--  A) Cambiar estado de un pedido (espera, produccion, retirar, cancelado)
-- ===========================================================
USE base_le_totette;
show tables;
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