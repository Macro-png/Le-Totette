use base_le_totette;

show tables;

describe filtros;

select * from filtros;

insert into filtros
(id, productos_id, filtro)
values
(NULL, 13, "arte"),
(NULL, 14, "abstracto"),
(NULL, 14, "naturaleza"),
(NULL, 15, "abstracto"),
(NULL, 16, "vintage");

select * from filtros;

delete from filtros;