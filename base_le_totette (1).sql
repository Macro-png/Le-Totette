-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 10-11-2025 a las 12:21:14
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

CREATE DATABASE base_le_totette;
use base_le_totette;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `base_le_totette`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `id` int(11) NOT NULL,
  `clientes_id` int(11) NOT NULL COMMENT 'fk',
  `productos_id` int(11) NOT NULL COMMENT 'fk'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(10) NOT NULL,
  `tipo` enum('cliente','admin') NOT NULL,
  `mail` varchar(20) NOT NULL,
  `contrasena` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `nombre`, `tipo`, `mail`, `contrasena`) VALUES
(5, 'Oscar', 'cliente', 'oscar@gmail.com', 'contrasena'),
(6, 'Fede', 'cliente', 'fede@gmail.com', 'contrasena'),
(7, 'Ale', 'cliente', 'ale@gmail.com', 'contrasena'),
(8, 'Nico', 'cliente', 'nico@gmail.com', 'contrasena'),
(9, 'Dante', 'cliente', 'dante@gmail.com', 'contrasena'),
(10, 'Lou', 'cliente', 'lou@gmail.com', 'contrasena'),
(11, 'Mora', 'cliente', 'mora@gmail.com', 'contrasena'),
(12, 'Sol', 'cliente', 'sol@gmail.com', 'contrasena'),
(13, 'Lara', 'cliente', 'lara@gmail.com', 'contrasena'),
(15, 'Emi', 'cliente', 'emi@gmail.com', 'contrasena'),
(16, 'Vicky', 'cliente', 'vicky@gmail.com', 'contrasena'),
(17, 'Roberto', 'cliente', 'robert@gmail.com', 'contrasena'),
(18, 'Roberto', 'cliente', 'r@gmail.com', 'contrasena'),
(20, 'Maru', 'admin', 'admin@gmail.com', 'contrasena'),
(21, 'Mari', 'cliente', 'mari@gmail.com', 'contrasena');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `colores`
--

CREATE TABLE `colores` (
  `id` int(11) NOT NULL,
  `productos_id` int(11) NOT NULL COMMENT 'fk',
  `codigo_hexa` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `colores`
--

INSERT INTO `colores` (`id`, `productos_id`, `codigo_hexa`) VALUES
(21, 13, '#000000'),
(22, 14, '#FFFFFF'),
(23, 15, '#FF69B4'),
(24, 16, '#008080');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_pedido`
--

CREATE TABLE `detalle_pedido` (
  `id` int(11) NOT NULL,
  `pedidos_id` int(11) NOT NULL COMMENT 'FK',
  `productos_id` int(11) NOT NULL COMMENT 'FK',
  `cantidad` int(11) NOT NULL,
  `precio_unidad` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_personalizados`
--

CREATE TABLE `detalle_personalizados` (
  `id` int(11) NOT NULL,
  `detalle_pedido_id` int(11) NOT NULL COMMENT 'fk',
  `img` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `filtros`
--

CREATE TABLE `filtros` (
  `id` int(11) NOT NULL,
  `productos_id` int(11) NOT NULL COMMENT 'fk',
  `filtro` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id` int(11) NOT NULL COMMENT 'Enviado a detalles_pedido',
  `cliente_id` int(11) NOT NULL COMMENT 'FK',
  `fecha` date NOT NULL,
  `precio_total` float NOT NULL,
  `estado` enum('espera','produccion','para retirar','cancelado') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id`, `cliente_id`, `fecha`, `precio_total`, `estado`) VALUES
(16, 10, '2025-11-09', 20, 'espera'),
(17, 12, '2025-11-09', 80.3, 'espera'),
(18, 13, '2025-11-09', 15.2, 'espera'),
(19, 12, '2025-11-09', 25, 'espera'),
(20, 11, '2025-11-09', 30, 'espera'),
(21, 15, '2025-11-09', 50, 'espera'),
(22, 12, '2025-11-09', 50, 'espera'),
(23, 5, '2025-11-09', 50, 'espera'),
(24, 12, '2025-11-09', 50, 'espera'),
(25, 11, '2025-11-09', 60, 'espera'),
(26, 11, '2025-11-09', 70, 'espera'),
(27, 12, '2025-11-09', 90, 'espera'),
(28, 13, '2025-11-09', 10, 'espera'),
(29, 11, '2025-11-09', 10, 'espera'),
(30, 16, '2025-11-09', 50, 'espera');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `precio_unidad` float NOT NULL,
  `img` varchar(50) NOT NULL,
  `descripcion` varchar(60) NOT NULL,
  `ventas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `precio_unidad`, `img`, `descripcion`, `ventas`) VALUES
(13, 'Tote Minimalista', 1500, '../../0. img/logo minimalista.png', 'Bolso tote de diseño minimalista, ideal para uso diario ', 0),
(14, 'Tote Floral', 1800, '../../0. img/logo floral.png', 'Bolso tote con estampado floral vibrante,', 0),
(15, 'Tote Geométrico', 2000, '../../0. img/logo geometrico.png', 'Bolso tote con diseño geométrico moderno', 0),
(16, 'Tote Vintage', 2200, '../../0. img/logo vintage.png', 'Bolso tote con un toque vintage', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `wishlist`
--

CREATE TABLE `wishlist` (
  `id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL COMMENT 'fk',
  `producto_id` int(11) NOT NULL COMMENT 'fk'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `wishlist`
--

INSERT INTO `wishlist` (`id`, `cliente_id`, `producto_id`) VALUES
(21, 12, 14),
(22, 12, 13),
(23, 12, 16),
(24, 10, 13),
(25, 5, 14);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `carrito_fk_clientes_id` (`clientes_id`),
  ADD KEY `carrito_productos_id` (`productos_id`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `mail` (`mail`);

--
-- Indices de la tabla `colores`
--
ALTER TABLE `colores`
  ADD PRIMARY KEY (`id`),
  ADD KEY `colores_fk_productos_id` (`productos_id`);

--
-- Indices de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_pedidos_id` (`pedidos_id`),
  ADD KEY `fk_productos_id` (`productos_id`);

--
-- Indices de la tabla `detalle_personalizados`
--
ALTER TABLE `detalle_personalizados`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_detalle_pedido_id` (`detalle_pedido_id`);

--
-- Indices de la tabla `filtros`
--
ALTER TABLE `filtros`
  ADD PRIMARY KEY (`id`),
  ADD KEY `filtros_fk_productos_id` (`productos_id`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cliente_id` (`cliente_id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`),
  ADD UNIQUE KEY `img` (`img`);

--
-- Indices de la tabla `wishlist`
--
ALTER TABLE `wishlist`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_clientes_id` (`cliente_id`),
  ADD KEY `fk_producto_id` (`producto_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `colores`
--
ALTER TABLE `colores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalle_personalizados`
--
ALTER TABLE `detalle_personalizados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `filtros`
--
ALTER TABLE `filtros`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Enviado a detalles_pedido', AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `wishlist`
--
ALTER TABLE `wishlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD CONSTRAINT `carrito_fk_clientes_id` FOREIGN KEY (`clientes_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `carrito_productos_id` FOREIGN KEY (`productos_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `colores`
--
ALTER TABLE `colores`
  ADD CONSTRAINT `colores_fk_productos_id` FOREIGN KEY (`productos_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD CONSTRAINT `fk_pedidos_id` FOREIGN KEY (`pedidos_id`) REFERENCES `pedidos` (`id`),
  ADD CONSTRAINT `fk_productos_id` FOREIGN KEY (`productos_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `detalle_personalizados`
--
ALTER TABLE `detalle_personalizados`
  ADD CONSTRAINT `fk_detalle_pedido_id` FOREIGN KEY (`detalle_pedido_id`) REFERENCES `detalle_pedido` (`id`);

--
-- Filtros para la tabla `filtros`
--
ALTER TABLE `filtros`
  ADD CONSTRAINT `filtros_fk_productos_id` FOREIGN KEY (`productos_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `cliente_id_fk` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`);

--
-- Filtros para la tabla `wishlist`
--
ALTER TABLE `wishlist`
  ADD CONSTRAINT `fk_clientes_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `fk_producto_id` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
