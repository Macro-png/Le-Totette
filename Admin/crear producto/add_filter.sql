use base_le_totette;

show tables;

describe filtros;

select * from filtros;

insert into filtros
(id, productos_id, filtro)
values
(NULL, 1, "naturaleza"),
(NULL, 1, "abstracto"),
(NULL, 2, "arte"),
(NULL, 3, "anime");

select * from filtros;

delete from filtros;