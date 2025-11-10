-- ELIMINAR TODOS LOS USUARIOS (Y RELACIONADOS)

delete from detalle_personalizado;
alter table detalle_personalizado auto_increment = 1;

delete from detalle_pedidos;
alter table detalle_pedidos auto_increment = 1;

delete from pedidos;
alter table pedidos auto_increment = 1;

delete from wishlist;
alter table wishlist auto_increment = 1;

delete from carrito;
alter table carrito auto_increment = 1;

delete from clientes;
alter table clientes auto_increment = 1;

-- ELIMINAR TODOS LOS PRODUCTOS (Y RELACIONADOS)

delete from colores;
alter table colores auto_increment = 1;

delete from filtros;
alter table filtros auto_increment = 1;

delete from productos;
alter table productos auto_increment = 1;