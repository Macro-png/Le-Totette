use base_le_totette;

show tables;

describe colores;

select * from colores;

insert into colores
(productos_id, codigo_hexa)
values
(1, "#000000"),
(1, "#FFFFFF"),
(2, "#FF69B4"),
(3, "#008080");

select * from colores;