use base_le_totette;

show tables;

describe productos

select * from productos;

insert into productos
(id,nombre,precio_unidad,img,descripcion,ventas)
values
(null, "Tote Minimalista", 1500, "../../0. img/logo minimalista.png", "Bolso tote de diseño minimalista, ideal para uso diario y ocasiones casuales.", 0),
(null, "Tote Floral", 1800, "../../0. img/logo floral.png", "Bolso tote con estampado floral vibrante, perfecto para añadir un toque de color a tu atuendo.", 0),
(null, "Tote Geométrico", 2000, "../../0. img/logo geometrico.png", "Bolso tote con diseño geométrico moderno, ideal para quienes buscan un estilo contemporáneo.", 0),
(null, "Tote Vintage", 2200, "../../0. img/logo vintage.png", "Bolso tote con un toque vintage, perfecto para amantes de la moda retro y clásica.", 0);

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

delete from colores where productos_id = 1;
delete from filtros where productos_id = 1;
delete from productos where id = 1;
delete from filtros where productos_id = 2;
delete from colores where productos_id = 2;
delete from productos where id=2;  

select * from productos;