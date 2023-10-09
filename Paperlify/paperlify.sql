-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.11.4-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for paperlify
CREATE DATABASE IF NOT EXISTS `paperlify` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `paperlify`;

-- Dumping structure for table paperlify.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.auth_group: ~0 rows (approximately)

-- Dumping structure for table paperlify.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.auth_group_permissions: ~0 rows (approximately)

-- Dumping structure for table paperlify.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.auth_permission: ~32 rows (approximately)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add my model', 7, 'add_mymodel'),
	(26, 'Can change my model', 7, 'change_mymodel'),
	(27, 'Can delete my model', 7, 'delete_mymodel'),
	(28, 'Can view my model', 7, 'view_mymodel'),
	(29, 'Can add registration', 8, 'add_registration'),
	(30, 'Can change registration', 8, 'change_registration'),
	(31, 'Can delete registration', 8, 'delete_registration'),
	(32, 'Can view registration', 8, 'view_registration');

-- Dumping structure for table paperlify.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `date_joined` datetime(6) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.auth_user: ~4 rows (approximately)
INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `last_login`, `date_joined`, `is_staff`, `is_active`, `is_superuser`) VALUES
	(3, 'dheerazsah', 'Dhiraj', '', 'dhiraj@gmail.com', 'pbkdf2_sha256$600000$4UuqePZScLpivSRnzJT7ws$8sIQ1yXdXW0LUxCWpLcaCfpmEmt7x6WPeTNaG3C1K0E=', NULL, '2023-09-25 12:31:44.214951', 0, 1, 0),
	(4, 'niraj', 'Niraj Sah', '', 'niraj@gmail.com', 'pbkdf2_sha256$600000$PJMOMx12HVZtWRpwtp0pdu$HO6p3vfolRkalBNuf3uJRnXMQSyw4eSnE4xNkpaTSoc=', '2023-10-05 17:38:42.556061', '2023-09-26 16:13:30.611963', 0, 1, 0),
	(5, 'madan', 'Madan Khanal', '', 'madan@gmail.com', 'pbkdf2_sha256$600000$FEwBgvzUbkVkWHMuLZlVRd$rprBKg1IJEOOPD7WdYaPCNCaSbkHOhj9eWRPTzpf2tA=', '2023-09-26 18:03:42.002039', '2023-09-26 18:03:30.017027', 0, 1, 0),
	(6, 'manoj', 'Manoj Karki', '', 'manoj@gmail.com', 'pbkdf2_sha256$600000$7fxvYYcjHIAwJTuBMmOvvt$pPaO4piC7TWNn7B6BgoNucINWMySLY1zC8gznkwcToc=', '2023-09-26 18:06:16.045015', '2023-09-26 18:05:58.798476', 0, 1, 0);

-- Dumping structure for table paperlify.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.auth_user_groups: ~0 rows (approximately)

-- Dumping structure for table paperlify.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.auth_user_user_permissions: ~0 rows (approximately)

-- Dumping structure for table paperlify.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.django_admin_log: ~0 rows (approximately)

-- Dumping structure for table paperlify.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.django_content_type: ~8 rows (approximately)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(7, 'home', 'mymodel'),
	(8, 'home', 'registration'),
	(6, 'sessions', 'session');

-- Dumping structure for table paperlify.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.django_migrations: ~19 rows (approximately)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2023-09-25 12:20:23.759291'),
	(2, 'auth', '0001_initial', '2023-09-25 12:20:24.327165'),
	(3, 'admin', '0001_initial', '2023-09-25 12:20:24.435871'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2023-09-25 12:20:24.444725'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2023-09-25 12:20:24.454698'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2023-09-25 12:20:24.530248'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2023-09-25 12:20:24.576287'),
	(8, 'auth', '0003_alter_user_email_max_length', '2023-09-25 12:20:24.607017'),
	(9, 'auth', '0004_alter_user_username_opts', '2023-09-25 12:20:24.614044'),
	(10, 'auth', '0005_alter_user_last_login_null', '2023-09-25 12:20:24.661171'),
	(11, 'auth', '0006_require_contenttypes_0002', '2023-09-25 12:20:24.664163'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2023-09-25 12:20:24.672875'),
	(13, 'auth', '0008_alter_user_username_max_length', '2023-09-25 12:20:24.700729'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2023-09-25 12:20:24.729236'),
	(15, 'auth', '0010_alter_group_name_max_length', '2023-09-25 12:20:24.760231'),
	(16, 'auth', '0011_update_proxy_permissions', '2023-09-25 12:20:24.767384'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2023-09-25 12:20:24.796718'),
	(18, 'home', '0001_initial', '2023-09-25 12:20:24.837025'),
	(19, 'sessions', '0001_initial', '2023-09-25 12:20:24.888794');

-- Dumping structure for table paperlify.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.django_session: ~1 rows (approximately)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('4unj6kov0oxym1an99d0dcd50x8uv1n4', '.eJy1j01vgzAMhv-KlTNCfCSk7NjbDpN6LxUyiWnpIEFJ6DRN--8jqJO6y7TLDj748avH9gdrcQmXdvHk2kGzJ8ZZ8sg6VK9k4kBf0ZxtqqwJbujSGEnvU5--WE3j_p79Ibigv0Rt3e9KkQmuhSqqPMOC80JIlZWi2Ik-l1Wd9VLyWtZ5r1VXdDrPS91ziVWu5HbVRN7jmfyqOx4b1rZXb803bVgCWQJ8rYYd0Ps36zRMiw8QT8bBAAYYCVdgDcEyz-QUelpZCOSSjfr3qbNjAmj01ptl6silUd6whp0S-H3xs7nhOGigCYcReusmDCkc4lqC2dnboAkQHkJ_d__bUyf2-QXNKqs7:1qoSJ8:wpXGoaE8_9PaamBY90uD2TJPtRqtacukqO6jxDO5oxk', '2023-10-19 17:38:42.564756');

-- Dumping structure for table paperlify.document
CREATE TABLE IF NOT EXISTS `document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT 0,
  `doc_name` varchar(255) DEFAULT NULL,
  `doc_size` int(11) DEFAULT NULL,
  `doc_type` varchar(255) DEFAULT NULL,
  `extracted_text` longtext DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `FK_document_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.document: ~47 rows (approximately)
INSERT INTO `document` (`id`, `user_id`, `doc_name`, `doc_size`, `doc_type`, `extracted_text`, `updated_on`) VALUES
	(11, 0, 'Weekly Log 04.docx', 21529, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 17:35:52'),
	(12, 0, 'Weekly Log 04.docx', 21529, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 17:35:58'),
	(13, 0, '4AC013_2065697.pdf', 1839487, 'application/pdf', NULL, '2023-09-30 17:38:01'),
	(14, 0, '4AC013_2065697.pdf', 1839487, 'application/pdf', NULL, '2023-09-30 18:00:45'),
	(15, 0, '4AC013_2065697.pdf', 1839487, 'application/pdf', NULL, '2023-09-30 18:02:58'),
	(16, 0, '4AC013_2065697.pdf', 1839487, 'application/pdf', NULL, '2023-09-30 18:10:37'),
	(17, 0, 'Final Portfolio.docx', 1971757, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:10:44'),
	(18, 0, 'Final Portfolio.docx', 1971757, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:16:40'),
	(19, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:18:02'),
	(20, 0, 'Test File.pdf', 38607, 'application/pdf', NULL, '2023-09-30 18:19:21'),
	(21, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:26:07'),
	(22, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:32:37'),
	(23, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:33:56'),
	(24, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:34:29'),
	(25, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:35:21'),
	(26, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:36:16'),
	(27, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:37:01'),
	(28, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:37:06'),
	(29, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:37:19'),
	(30, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:37:34'),
	(31, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:37:39'),
	(32, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:37:53'),
	(33, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:44:40'),
	(34, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:45:29'),
	(35, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:45:47'),
	(36, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:46:04'),
	(37, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:46:14'),
	(38, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:47:49'),
	(39, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:51:05'),
	(40, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:51:41'),
	(41, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:52:28'),
	(42, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:53:12'),
	(43, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 18:56:24'),
	(44, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-09-30 19:00:27'),
	(45, 0, 'Test File.pdf', 38607, 'application/pdf', NULL, '2023-10-02 10:33:43'),
	(46, 0, 'Test File.pdf', 38607, 'application/pdf', NULL, '2023-10-02 10:41:59'),
	(47, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-10-02 17:03:31'),
	(48, 0, 'Test File.docx', 12352, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NULL, '2023-10-02 17:07:15'),
	(49, 0, 'Test File.pdf', 38607, 'application/pdf', NULL, '2023-10-03 03:35:19'),
	(50, 0, 'Test File.pdf', 38607, 'application/pdf', NULL, '2023-10-03 03:55:32'),
	(51, 0, 'Test File.pdf', 38607, 'application/pdf', NULL, '2023-10-03 04:04:10'),
	(52, 0, 'Test File.pdf', 38607, 'application/pdf', 'Hi this is a test file  to show the uploaded document . ', '2023-10-05 17:48:19'),
	(53, 0, 'Test File.pdf', 38607, 'application/pdf', 'Hi this is a test file  to show the uploaded document . ', '2023-10-05 17:48:24'),
	(54, 0, 'Test File.pdf', 38607, 'application/pdf', 'Hi this is a test file  to show the uploaded document . ', '2023-10-05 17:59:57'),
	(55, 0, 'Test File.pdf', 38607, 'application/pdf', 'Hi this is a test file  to show the uploaded document . ', '2023-10-05 18:00:40'),
	(56, 0, 'Test File.pdf', 38607, 'application/pdf', 'Hi this is a test file  to show the uploaded document . ', '2023-10-05 18:00:47'),
	(57, 0, 'Test File.pdf', 38607, 'application/pdf', 'Hi this is a test file  to show the uploaded document . ', '2023-10-05 18:07:04');

-- Dumping structure for table paperlify.home_mymodel
CREATE TABLE IF NOT EXISTS `home_mymodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.home_mymodel: ~0 rows (approximately)

-- Dumping structure for table paperlify.logs
CREATE TABLE IF NOT EXISTS `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) DEFAULT NULL,
  `activity` longtext DEFAULT NULL,
  `ip_address` varchar(50) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.logs: ~0 rows (approximately)

-- Dumping structure for table paperlify.process
CREATE TABLE IF NOT EXISTS `process` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_id` int(11) NOT NULL DEFAULT 0,
  `doc_data` longtext DEFAULT NULL,
  `sum_data` longtext DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `FK_process_document` (`doc_id`),
  CONSTRAINT `FK_process_document` FOREIGN KEY (`doc_id`) REFERENCES `document` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.process: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
