-- ===========================================================
-- 03_wishlist.sql
-- Wishlist del cliente: crear tabla, agregar y consultar
-- PK: id (AUTO_INCREMENT). FKs: cliente_id -> clientes(id),
--                              producto_id -> productos(id)
-- ===========================================================

-- 1) Seleccionar la base
USE base_le_totette;
-- ===========================================================
-- 2.b) AGREGAR evitando duplicados (usando NOT EXISTS)
--      Inserta SOLO si ese cliente aún no tiene ese producto en su wishlist.
-- ===========================================================
SELECT * FROM clientes WHERE id = 1;
SELECT * FROM productos WHERE id = 1;
select * from productos;

INSERT INTO wishlist (cliente_id, producto_id)
SELECT 1, 7
WHERE NOT EXISTS (
  SELECT 1
  FROM wishlist
  WHERE cliente_id = 1 AND producto_id = 7
);

-- (Podemos reutilizar el patrón cambiando los números:)
-- INSERT INTO wishlist (cliente_id, producto_id)
-- SELECT <cliente_id>, <producto_id>
-- WHERE NOT EXISTS (
--   SELECT 1 FROM wishlist
--   WHERE cliente_id = <cliente_id> AND producto_id = <producto_id>
-- );

-- ===========================================================
-- 3) CONSULTAR TODOS LOS PRODUCTOS DE LA WISHLIST DE UN CLIENTE
--    Une con 'productos' para mostrar info útil.
-- ===========================================================
SELECT
  w.id            AS wishlist_id,
  w.producto_id,
  p.nombre,
  p.descripcion,
  p.precio_unidad
FROM wishlist w
INNER JOIN productos p ON p.id = w.producto_id
WHERE w.cliente_id = 1;           -- ← cambia por el cliente que quieras


-- ===========================================================
-- 4) CONSULTAR UN PRODUCTO PUNTUAL EN LA WISHLIST DEL CLIENTE
--    Devuelve 0 filas si NO está; 1 fila si SÍ está.
-- ===========================================================
SELECT
  w.id            AS wishlist_id,
  w.producto_id,
  p.nombre,
  p.descripcion,
  p.precio_unidad
FROM wishlist w
INNER JOIN productos p ON p.id = w.producto_id
WHERE w.cliente_id = 1            -- ← cliente
  AND w.producto_id = 7;          -- ← producto

-- ===========================================================
-- 5) ELIMINAR un producto de la wishlist
DELETE FROM wishlist WHERE cliente_id = 1 AND producto_id = 5;

SELECT * from wishlist;

