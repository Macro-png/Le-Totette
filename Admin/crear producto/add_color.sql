use base_le_totette;

show tables;

describe colores;

select * from colores;

insert into colores
(id, productos_id, codigo_hexa)
values
(NULL, 1, "#000000"),
(NULL, 1, "#FFFFFF"),
(NULL, 2, "#FF69B4"),
(NULL, 3, "#008080"),
(NULL, 4, "#000000");

select * from colores;

delete from colores;