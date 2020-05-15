CREATE DATABASE `OBSdb` /*!40100 DEFAULT CHARACTER SET utf8 */

CREATE TABLE `host` (
 `hostname` varchar(255) NOT NULL,
 `port` varchar(5) NOT NULL,
 `pass` varchar(255) NOT NULL,
 PRIMARY KEY (`hostname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
CREATE TABLE `scedules` (
 `id` bigint(20) NOT NULL AUTO_INCREMENT,
 `swtime` time NOT NULL,
 `swdate` date NOT NULL DEFAULT current_timestamp(),
 `scene` varchar(255) NOT NULL,
 `transition` varchar(255) NOT NULL,
 `sourceoff` varchar(255) NOT NULL,
 `sourceon` varchar(255) NOT NULL,
 `duration` time NOT NULL,
 `repeattime` int(11) NOT NULL,
 `processed` tinyint(1) NOT NULL DEFAULT 0,
 UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8
CREATE TABLE `scenenames` (
 `scene` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
CREATE TABLE `sourcenames` (
 `scene` varchar(255) NOT NULL,
 `source` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
CREATE TABLE `transitionnames` (
 `transition` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
