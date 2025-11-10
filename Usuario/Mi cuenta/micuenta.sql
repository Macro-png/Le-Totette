    show databases;

    use base_le_totette;

    show tables;

    describe clientes;

    select id,mail,contrasena from clientes;

    UPDATE clientes
    set contrasena="contra"
    where id=3;

    SELECT
        clientes.id AS cliente_id,
        clientes.nombre AS nombre_cliente,
        GROUP_CONCAT(DISTINCT pw.nombre) AS productos_en_wishlist,
        GROUP_CONCAT(DISTINCT pedidos.id) AS ids_de_pedidos
    from clientes

    LEFT JOIN wishlist ON clientes.id = wishlist.cliente_id
    LEFT JOIN productos AS pw ON wishlist.producto_id = pw.id -- Alias corto 'pw'
    LEFT JOIN pedidos ON clientes.id = pedidos.cliente_id

    where clientes.tipo != 'admin'
    group by clientes.id, clientes.nombre
    order by clientes.id;

