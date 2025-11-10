use base_le_totette;

show tables;

describe productos;

select * from productos;

select * from productos where id = 2;

update productos
set 
    nombre = "Tote Floral Deluxe",
    precio_unidad = 2100,
    img = "../../0. img/logo floral deluxe.png",
    descripcion = "Versión mejorada del bolso tote floral, con nuevos colores y materiales de alta calidad."
where id = 2;

insert into filtros
(productos_id, filtro)
values
(2, "deluxe");

select
    p.id as producto_id,
    p.nombre as nombre_producto,
    p.precio_unidad,
    group_concat(distinct f.filtro order by f.filtro separator ', ') as filtros,
    group_concat(distinct c.codigo_hexa order by c.codigo_hexa separator ', ') as colores
from productos p
left join filtros f on p.id = f.productos_id
left join colores c on p.id = c.productos_id
-- where filtro = 'abstracto' -- SOLO MOSTRAR PRODUCTOS CON FILTRO ABSTRACTO
group by p.id, p.nombre, p.precio_unidad
order by p.id;

select * from productos where id = 2;