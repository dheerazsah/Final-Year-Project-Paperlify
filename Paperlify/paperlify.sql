CREATE DATABASE IF NOT EXISTS `paperlify`;
USE `paperlify`;

CREATE TABLE IF NOT EXISTS `document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT 0,
  `doc_name` varchar(255) DEFAULT NULL,
  `doc_type` varchar(255) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `FK_document_user` (`user_id`),
  CONSTRAINT `FK_document_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) DEFAULT NULL,
  `activity` longtext DEFAULT NULL,
  `ip_address` varchar(50) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `process` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_id` int(11) NOT NULL DEFAULT 0,
  `doc_data` longtext DEFAULT NULL,
  `sum_data` longtext DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `FK_process_document` (`doc_id`),
  CONSTRAINT `FK_process_document` FOREIGN KEY (`doc_id`) REFERENCES `document` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` longtext DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
);