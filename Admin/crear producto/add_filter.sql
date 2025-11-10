use base_le_totette;

show tables;

describe filtros;

select * from filtros;

insert into filtros
(id, productos_id, filtro)
values
(NULL, 1, "arte"),
(NULL, 1, "abstracto"),
(NULL, 2, "naturaleza"),
(NULL, 3, "abstracto"),
(NULL, 4, "vintage");

select * from filtros;

delete from filtros;