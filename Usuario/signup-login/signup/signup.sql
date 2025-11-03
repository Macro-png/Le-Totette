use base_le_totette

show tables

describe clientes

select * from clientes


--AGREGAR USUARIOS

INSERT INTO clientes
(id,nombre,tipo,mail,contrasena)
VALUES
(null, "Maru", "admin", "admin@gmail.com","contrasena");

INSERT INTO clientes
(id,nombre,tipo,mail,contrasena)
VALUES
(null, "Mari", "cliente", "mari@gmail.com","contrasena");

INSERT INTO clientes
(id,nombre,tipo,mail,contrasena)
VALUES
(null, "Mari", "cliente", "mari@gmail.com","contrasena");
--el mail es unique


INSERT INTO clientes
(id,nombre,tipo,mail,contrasena)
VALUES
(null, "Mari", "hola", "mari@gmail.com","contrasena");
--el tipo es un enum (solo puede ser cliente o admin)


INSERT INTO clientes
(id,nombre,tipo,mail,contrasena)
VALUES
(null, "Mariano", "cliente", "mariano@gmail.com","contrasena"),
(null, "Oscar", "cliente", "oscar@gmail.com","contrasena"),
(null, "Fede", "cliente", "fede@gmail.com","contrasena"),
(null, "Ale", "cliente", "ale@gmail.com","contrasena"),
(null, "Nico", "cliente", "nico@gmail.com","contrasena"),
(null, "Dante", "cliente", "dante@gmail.com","contrasena"),
(null, "Lou", "cliente", "lou@gmail.com","contrasena"),
(null, "Mora", "cliente", "mora@gmail.com","contrasena"),
(null, "Sol", "cliente", "sol@gmail.com","contrasena"),
(null, "Lara", "cliente", "lara@gmail.com","contrasena"),
(null, "Cecilia", "cliente", "cecilia@gmail.com","contrasena"),
(null, "Emi", "cliente", "emi@gmail.com","contrasena"),
(null, "Vicky", "cliente", "vicky@gmail.com","contrasena");

INSERT INTO clientes
(id,nombre,tipo,mail,contrasena)
VALUES
(null, "Roberto", "cliente", "robert@gmail.com","contrasena"),
(null, "Roberto", "cliente", "r@gmail.com","contrasena"),
(null, "Gerberto", "cliente", "gerbert@gmail.com","contrasena");


-- ELIMINAR USUARIOS (va a tener la opcion el admin)
DELETE FROM clientes where id=1

DELETE FROM clientes where id=2

DELETE FROM clientes where id=4



