use base_le_totette;

show tables;

describe filtros;

select * from filtros;

insert into filtros
(id, productos_id, filtro)
values
(NULL, 1, "Naturaleza"),
(NULL, 2, "Naturaleza"),
(NULL, 3, "Minimalista"),
(NULL, 4, "Naturaleza"),
(NULL, 5, "Naturaleza"),
(NULL, 5, "Minimalista"),
(NULL, 6, "Viaje"),
(NULL, 7, "Viaje"),
(NULL, 8, "Tendencia"),
(NULL, 9, "Arte"),
(NULL, 9, "Viaje"),
(NULL, 10, "Viaje"),
(NULL, 13, "Minimalista");



select * from filtros;

delete from filtros;