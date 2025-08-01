-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 01-08-2025 a las 04:06:47
-- Versión del servidor: 9.1.0
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hotel`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

DROP TABLE IF EXISTS `reservas`;
CREATE TABLE IF NOT EXISTS `reservas` (
  `id_reserva` int NOT NULL AUTO_INCREMENT,
  `fecha_ingreso` date NOT NULL,
  `fecha_salida` date NOT NULL,
  `tipo_habitacion` varchar(50) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `fecha_reserva` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `correo_usuario` varchar(100) DEFAULT NULL,
  `noches` int DEFAULT NULL,
  PRIMARY KEY (`id_reserva`),
  KEY `fk_reservas_usuarios_correo` (`correo_usuario`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`id_reserva`, `fecha_ingreso`, `fecha_salida`, `tipo_habitacion`, `precio`, `fecha_reserva`, `correo_usuario`, `noches`) VALUES
(8, '2025-08-01', '2025-08-02', 'Suite Ejecutiva - $400.000', 400000.00, '2025-08-01 03:33:43', 'a.felipemg16@gmail.com', 1),
(7, '2025-07-17', '2025-07-25', 'Estándar - $150.000', 150000.00, '2025-08-01 03:31:45', 'janerarana23@gmail.com', 8),
(9, '2025-08-09', '2025-08-16', 'Suite Junior - $250.000', 250000.00, '2025-08-01 03:34:03', 'a.felipemg16@gmail.com', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` enum('admin','usuario') NOT NULL,
  `creado_en` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`),
  UNIQUE KEY `correo_2` (`correo`),
  UNIQUE KEY `correo_3` (`correo`),
  UNIQUE KEY `correo_4` (`correo`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `usuario`, `correo`, `password`, `rol`, `creado_en`) VALUES
(14, 'admin', 'admin@admin.com', '$2b$12$EJmmM5MYJEH51/1ool6tz.XBUmBk9DqT7OsDdIyVZInY3Lbkws45q', 'admin', '2025-08-01 03:34:47'),
(13, 'Janer', 'janer3@gmail.com', '$2b$12$.xyCcwD8.hkIKXVYy8MHVulxJvbnT0xGEJbzZzuYDAjqbD7oIFFBW', 'usuario', '2025-08-01 03:24:45'),
(12, 'Felixix', 'a.fe16@gmail.com', '$2b$12$WvY9a4PHcIzXRwdiXf5zAutsPtZ5uLOkOdEd8TBvGrYgpSprFxS/e', 'usuario', '2025-08-01 03:17:40');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
