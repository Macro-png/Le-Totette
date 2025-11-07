use base_le_totette;

show tables;

describe productos;

select * from productos;

insert into productos
(id,nombre,precio_unidad,img,descripcion,ventas)
values
(null, "Tote Minimalista", "1500", "../../0. img/logo minimalista.png", "Bolso tote de diseño minimalista, ideal para uso diario y ocasiones casuales.", 0),
(null, "Tote Floral", "1800", "../../0. img/logo floral.png", "Bolso tote con estampado floral vibrante, perfecto para añadir un toque de color a tu atuendo.", 0),
(null, "Tote Geométrico", "2000", "../../0. img/logo geometrico.png", "Bolso tote con diseño geométrico moderno, ideal para quienes buscan un estilo contemporáneo.", 0),
(null, "Tote Vintage", "2200", "../../0. img/logo vintage.png", "Bolso tote con un toque vintage, perfecto para amantes de la moda retro y clásica.", 0);

delete from productos where id=1;
delete from productos where id=2;  

delete from productos;
alter table productos auto_increment = 1;