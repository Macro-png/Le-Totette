-- ===========================================================
-- Consultas del Administrador sobre PEDIDOS (incluye cancelados)
--   A) Ver todos los pedidos
--   B) Cantidad de pedidos por estado (incluye cancelado)
--   C) Filtros por estado (espera / produccion / retirar / cancelado)
--   D) Detalle de un pedido y cantidad total de artículos
-- ===========================================================

-- 0️⃣ Seleccionar la base de datos
USE base_le_totette;

-- ===========================================================
-- A) VER TODOS LOS PEDIDOS (incluye cancelado)
-- ===========================================================
SELECT 
  p.id            AS pedido_id,
  c.nombre        AS cliente,
  p.fecha,
  p.estado,
  p.precio_total
FROM pedidos p
INNER JOIN clientes c ON c.id = p.cliente_id
ORDER BY p.fecha DESC;

-- ===========================================================
-- B) TABLA DE CANTIDAD DE PEDIDOS POR ESTADO (incluye cancelado)
-- ===========================================================
SELECT 
  p.estado,
  COUNT(*) AS cantidad_pedidos
FROM pedidos p
GROUP BY p.estado
ORDER BY p.estado;

-- ===========================================================
-- C) CONSULTAR PEDIDOS POR ESTADO (FILTROS)
-- ===========================================================
-- Espera
SELECT 
  p.id, c.nombre, p.fecha, p.estado, p.precio_total
FROM pedidos p
INNER JOIN clientes c ON c.id = p.cliente_id
WHERE p.estado = 'espera'
ORDER BY p.fecha DESC;

-- Producción
SELECT 
  p.id, c.nombre, p.fecha, p.estado, p.precio_total
FROM pedidos p
INNER JOIN clientes c ON c.id = p.cliente_id
WHERE p.estado = 'produccion'
ORDER BY p.fecha DESC;

-- Retirar
SELECT 
  p.id, c.nombre, p.fecha, p.estado, p.precio_total
FROM pedidos p
INNER JOIN clientes c ON c.id = p.cliente_id
WHERE p.estado = 'retirar'
ORDER BY p.fecha ASC;

-- Cancelado
SELECT 
  p.id, c.nombre, p.fecha, p.estado, p.precio_total
FROM pedidos p
INNER JOIN clientes c ON c.id = p.cliente_id
WHERE p.estado = 'cancelado'
ORDER BY p.fecha DESC;
-- FIN DE CONSULTAS DEL ADMINISTRADOR

select * from detalle_pedido;
select * from pedidos;