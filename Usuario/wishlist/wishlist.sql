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
-- Este insert agrega un producto a la wishlist del cliente solo si:
-- 1) El cliente y el producto existen realmente en sus tablas.
-- 2) Aún no hay una relación entre ambos en la wishlist.
-- Así se evita romper las claves foráneas o tener duplicados.
-- ===========================================================
SELECT * FROM clientes;
SELECT * FROM productos WHERE id = 1;
select * from productos;
SELECT* FROM wishlist;

INSERT INTO wishlist (cliente_id, producto_id)
SELECT c.id, p.id
FROM clientes  c,
     productos p
WHERE c.id = 1          -- ← cliente existente
  AND p.id = 1        -- ← producto existente
  AND NOT EXISTS (
        SELECT 1
        FROM wishlist w
        WHERE w.cliente_id = c.id
          AND w.producto_id = p.id
  )
LIMIT 1;

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
  AND w.producto_id = 1;          -- ← producto

-- ===========================================================
-- 5) ELIMINAR un producto de la wishlist
DELETE FROM wishlist WHERE cliente_id = 1 AND producto_id = 5;

SELECT * from wishlist;

alter table wishlist auto_increment = 1;
