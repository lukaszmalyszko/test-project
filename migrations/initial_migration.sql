CREATE DATABASE mydatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `download_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `url` varchar(248) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(8) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status_msg` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `text` text COLLATE utf8mb4_unicode_ci,
  `download_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(248) DEFAULT NULL,
  `download_content_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `download_content_id` (`download_content_id`),
  CONSTRAINT `image_ibfk_1` FOREIGN KEY (`download_content_id`) REFERENCES `download_content` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
