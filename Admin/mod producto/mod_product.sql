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

select * from productos where id = 2;