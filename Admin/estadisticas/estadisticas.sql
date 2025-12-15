use base_le_totette;

show tables;

SELECT 
    c.nombre,
    COALESCE(SUM(dp.cantidad), 0) AS ventas
FROM filtros c
JOIN productos p ON p.categoria_id = c.id
JOIN detalle_pedido dp ON dp.productos_id = p.id
JOIN pedidos pe ON pe.id = dp.pedidos_id
WHERE pe.estado <> 'cancelado'
GROUP BY c.id, c.nombre
ORDER BY ventas DESC;

DESCRIBE productos;
DESCRIBE filtros;