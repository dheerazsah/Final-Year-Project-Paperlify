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
  `otp` varchar(50) DEFAULT NULL,
  `otp_created_at` varchar(50) DEFAULT NULL,
  `otp_verified` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table paperlify.auth_user: ~21 rows (approximately)
INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `last_login`, `date_joined`, `is_staff`, `is_active`, `is_superuser`, `otp`, `otp_created_at`, `otp_verified`) VALUES
	(1, 'dhiraj1', 'Dhiraj K Sah', '', 'dhiraj@gmail.com', 'pbkdf2_sha256$720000$vme1Xb88AIXv8jsHWzWDo6$BQeAev9f1ENmwub4G7VKRE36hSOexL0FnlIo0z7YuOw=', '2024-02-18 04:29:52.068794', '2023-12-06 18:25:42.694369', 1, 1, 1, '469901', '2024-02-20 07:39:29.052900', '1'),
	(2, 'niraj', 'Niraj Kumar Sah', '', 'niraj@gmail.com', 'pbkdf2_sha256$720000$Ok1UCAPpSLCqyrEbx96b4E$hL9JGX9HzWnGQxmdhBtw2AC9gmkfckWek/0O036lhAg=', '2024-02-19 06:36:52.527124', '2023-12-06 18:27:23.024827', 0, 1, 1, NULL, NULL, NULL),
	(3, 'test', 'Test ', '', 'test@gmail.com', 'pbkdf2_sha256$720000$ZKiU9GwHYX5GFKHTxLJ0mp$JvAjBJLj3apGfY5/pVv1v2jw98n8U6Wrsbyi1peYo/0=', '2024-02-10 11:18:27.224690', '2023-12-06 18:27:51.431433', 0, 1, 0, '486622', '2024-02-20 09:05:40.007920', NULL),
	(4, 'madan', 'Madan K Khanal', '', 'dheerazsah31@gmail.com', 'pbkdf2_sha256$720000$M2aerZBBg3udHtSJoVIcok$tG8C/joysVSNBb+Fj9+P4TL6DtjPxjpnhmcwMdT8JxE=', '2024-02-26 10:46:00.595892', '2023-12-06 18:28:36.800011', 0, 1, 0, '883385', '2024-02-21 17:38:08.524833', NULL),
	(5, 'manoj', 'Manoj Karki', '', 'manoj@gmail.com', 'pbkdf2_sha256$600000$L6I6XVb5jrPJSxlWMzuWr7$8xESqncucGp6oqVbi3aor12z+/z3IRW8YrwlmACoHdo=', NULL, '2023-12-06 18:29:02.118192', 0, 1, 0, NULL, NULL, NULL),
	(6, 'nimisha', 'Nimisha Pradhan', '', 'nimisha@gmail.com', 'pbkdf2_sha256$720000$evnbVN0Rg3BlgyuDE4H8VX$yXZDw0LRFnpkUQed/YKIvJe7NEr69YFoqX7Hvmyaq6Y=', '2024-02-11 19:23:01.062576', '2023-12-06 18:31:24.813487', 0, 1, 0, NULL, NULL, NULL),
	(7, 'lujana', 'Lujana Bajracharya', '', 'lujana@gmail.com', 'pbkdf2_sha256$600000$2WyoHVdRV06ztOvWTLXBAL$mKsJNSpjZexA34dXq/57BJlDkZJznJp4O7XDuvqhbYE=', '2023-12-06 18:23:36.086264', '2023-12-06 18:10:28.541164', 0, 1, 0, '163191', '2023-12-06 18:16:22.851063', NULL),
	(8, 'rishan', 'Rishan Das', '', 'rishan@gmail.com', 'pbkdf2_sha256$600000$ZFn1YDNsuHRGbChCQi1SB8$ZqNSl8Rx2mUl4lKhithyJcHt3DtYkC8s9zLrJlonuaw=', NULL, '2023-12-08 08:12:43.844013', 0, 1, 0, NULL, NULL, NULL),
	(9, 'luja', 'Luja Shrestha', '', 'luja@gmail.com', 'pbkdf2_sha256$600000$Rlefe3RDEQCiFVGYVBCuHX$9SBA3FsgzQgvUtEnHOAJdi4hHKheX7CYZN7jFmpRuGM=', NULL, '2023-12-08 08:15:23.473755', 0, 1, 0, NULL, NULL, NULL),
	(10, 'bibek', 'Bibek Karki', '', 'bibek@gmail.com', 'pbkdf2_sha256$600000$gLKblwuKWewz1GI4IjmLZr$XTYa9S6oSAvh3ltN+8qnLtILMXK90RLjE15BHK7iYXE=', NULL, '2023-12-08 08:23:34.971721', 0, 1, 0, NULL, NULL, NULL),
	(11, 'heralddhiraj', 'Dhiraj Sah', '', 'dhirajherald@gmail.com', 'pbkdf2_sha256$720000$54uTEVG5hTwt6StXShT2Lp$fVexkX94rmA65NChq3ahK1KqPDkj+W5IPKw5JGMRRTQ=', '2024-01-08 18:16:37.369320', '2024-01-08 18:04:37.322071', 0, 1, 0, NULL, NULL, NULL),
	(12, 'admin', 'Admin', '', 'admin@gmail.com', 'pbkdf2_sha256$720000$UFweeiHjVLLh7sET6bM6lW$siElLK/cPeHkO0AqnGxZAzwc56KlvPMLrDvBAXbo8vA=', '2024-01-31 05:10:08.005425', '2024-01-31 04:55:56.008526', 1, 1, 1, NULL, NULL, NULL),
	(13, 'testdefense', 'Test Defense', '', 'testdefense@gmail.com', 'pbkdf2_sha256$720000$9mExUyvj6nMI6gYz9DY5Nn$bKWqmUSqCSpMOXkBzkbVuFiypk/yErEm9vXX3qrkWd0=', '2024-01-31 05:01:15.950030', '2024-01-31 05:00:39.242683', 0, 1, 0, NULL, NULL, NULL),
	(14, 'herald', 'Herald', '', 'mero@heraldcollege.edu.np', 'pbkdf2_sha256$720000$OuCuWFDVBjarsSQRVvYPo3$cv8RsJ4Z+Dwed3ts0vJKJ4Lq4lEP1pKl0L/h+Qkkd+I=', '2024-02-11 18:41:04.914658', '2024-02-11 18:40:19.927567', 0, 1, 0, NULL, NULL, NULL),
	(17, 'nodhiraj', 'Dhiraj Sah Kanu', '', 'dheerazsah30@gmail.com', 'pbkdf2_sha256$720000$hEMIMMgwqARzw1ejlLWbOz$kWIWHjyZya6Lo+Pr3JM/1LJYKMIrCmRd2LLfpx5Hh2w=', '2024-02-20 13:27:47.172974', '2024-02-18 03:11:19.720493', 0, 1, 0, '634004', '2024-02-20 14:33:25.867655', '1'),
	(22, 'dhir', 'Dhiraj', '', 'dhiraj@mmail.com', 'pbkdf2_sha256$720000$1PHtsLu0BYxDYGlikLg6VC$VkJ6OCeUkxHv1P4OcfdUISUoEuOtujsJs4LjTscujhY=', NULL, '2024-02-20 07:30:04.401397', 0, 0, 0, NULL, NULL, NULL),
	(25, 'dhirajadmin', 'Dhiraj Admin', '', 'dhirajadmin@gmail.com', 'pbkdf2_sha256$720000$zblgIfX0zb1LvluagVfQ9N$hwTB9sZx8svRLapFjaSlNDjzX2GmWFbXyWA617JMopk=', '2024-02-22 05:26:13.895255', '2024-02-22 05:25:26.398199', 1, 1, 1, NULL, NULL, NULL),
	(26, 'dhirajtest123', 'Dhiraj', '', 'dhirajkumarsah@gmail.com', 'pbkdf2_sha256$720000$BmQqjLvMDk5V2miQg134vQ$Zd0UOCQn5jH4+4zW4DLItwfzHs37hSpoiWxIaVylTZM=', '2024-02-22 06:42:18.562340', '2024-02-22 06:05:10.820613', 0, 1, 0, NULL, NULL, NULL),
	(27, 'dhiraj12345', 'Dhiraj K Sah', '', 'dhirajk@gmail.com', 'pbkdf2_sha256$720000$Zo4AY4ghAbyyujnliokQNq$Jg1wbRcQTjJ53b/9evR5lXReev3QlOPetnCtqqriu5o=', NULL, '2024-02-22 06:43:29.020712', 0, 0, 0, NULL, NULL, NULL),
	(29, 'iamdhiraj', 'Dhiraj', '', 'np03cs4m210013@heraldcollege.edu.np', 'pbkdf2_sha256$720000$nuVaYTY5RNJWqp83KLMx5e$lkJzm2ISCjEIFSgNujs76zBXxCcYhvzpcPwWSrWMlSY=', '2024-02-26 10:53:44.783643', '2024-02-26 10:53:19.074686', 0, 1, 0, NULL, NULL, NULL),
	(32, 'iamnotdhiraj', 'Dhiraj', '', 'dhirajkumarsahkanu@gmail.com', 'pbkdf2_sha256$720000$PWJp9rtSy2SagpHgAct2k1$VIZWRJ9NzP8AER7L4oI6OOyxtNAQS2AlDZd6/ZUVrKQ=', '2024-02-26 10:56:32.665011', '2024-02-26 10:55:52.227735', 0, 1, 0, NULL, NULL, NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
