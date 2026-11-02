/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `oigapzpc_ecertificate` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `oigapzpc_ecertificate`;

CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','manager','staff') NOT NULL DEFAULT 'staff',
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `email_verified` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `last_login_at` datetime DEFAULT NULL,
  `reset_token_hash` varchar(64) DEFAULT NULL,
  `reset_token_expires_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_email` (`email`),
  KEY `ix_users_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `users` (`id`, `name`, `email`, `password_hash`, `role`, `is_active`, `email_verified`, `created_at`, `updated_at`, `last_login_at`, `reset_token_hash`, `reset_token_expires_at`) VALUES
	(1, 'Vigneshwaran P', 'ytdark310@gmail.com', 'scrypt:32768:8:1$2fM9B3Eica1UDZMn$97f879e803f2561273c29d6ae260e99d650c6f055bc738e8b6a872df7322310ec6e20f82a51b1cd3c19dc4d82e54723edda8904625f0cbe49b29e5057b1e940d', 'admin', 1, 0, '2026-09-11 16:28:42', '2026-09-11 17:59:52', '2026-09-11 17:59:52', NULL, NULL);

CREATE TABLE IF NOT EXISTS `audit_logs` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) unsigned DEFAULT NULL,
  `action` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `ix_audit_logs_user_id` (`user_id`),
  KEY `ix_audit_logs_action` (`action`),
  KEY `ix_audit_logs_created_at` (`created_at`),
  CONSTRAINT `fk_audit_logs_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `colleges` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `code` varchar(100) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_colleges_code` (`code`),
  KEY `ix_colleges_name` (`name`),
  KEY `ix_colleges_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `colleges` (`id`, `name`, `code`, `email`, `phone`, `address`, `city`, `district`, `state`, `is_active`, `created_at`, `updated_at`) VALUES
	(1, 'Bharathiar University', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2026-09-11 16:33:49', '2026-09-11 16:33:49'),
	(2, 'SNS College', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2026-09-11 16:33:50', '2026-09-11 16:33:50'),
	(3, 'Nehru Arts & Science College', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2026-09-11 16:33:50', '2026-09-11 16:33:50'),
	(4, 'Sree Narayana Guru College', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2026-09-11 16:33:50', '2026-09-11 16:33:50');


CREATE TABLE IF NOT EXISTS `certificate_batches` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) unsigned NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `source_filename` varchar(255) NOT NULL,
  `total_records` int(11) NOT NULL DEFAULT 0,
  `valid_records` int(11) NOT NULL DEFAULT 0,
  `generated_records` int(11) NOT NULL DEFAULT 0,
  `failed_records` int(11) NOT NULL DEFAULT 0,
  `status` enum('pending','processing','completed','completed_with_errors','failed') NOT NULL DEFAULT 'pending',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `completed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_certificate_batches_user_id` (`user_id`),
  KEY `ix_certificate_batches_status` (`status`),
  CONSTRAINT `fk_certificate_batches_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `certificate_batches` (`id`, `user_id`, `title`, `description`, `source_filename`, `total_records`, `valid_records`, `generated_records`, `failed_records`, `status`, `created_at`, `completed_at`) VALUES
	(1, 1, 'Participation Certificate', 'This certificate is proudly presented to {name} of {college_name} in recognition of their active participation in the event and for their valuable contribution, enthusiasm, and commitment. Their participation and dedication are sincerely appreciated, and we congratulate them on their achievement.', 'test-ecertificate.xlsx', 4, 4, 4, 0, 'completed', '2026-09-11 16:33:49', '2026-09-11 16:33:50');

CREATE TABLE IF NOT EXISTS `certificates` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `batch_id` bigint(20) unsigned NOT NULL,
  `college_id` bigint(20) unsigned DEFAULT NULL,
  `recipient_name` varchar(255) NOT NULL,
  `college_name` varchar(255) NOT NULL,
  `certificate_number` varchar(100) NOT NULL,
  `public_token` varchar(128) NOT NULL,
  `pdf_filename` varchar(255) DEFAULT NULL,
  `pdf_path` varchar(500) DEFAULT NULL,
  `status` enum('pending','generated','failed') NOT NULL DEFAULT 'pending',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_certificates_certificate_number` (`certificate_number`),
  UNIQUE KEY `uq_certificates_public_token` (`public_token`),
  KEY `ix_certificates_batch_id` (`batch_id`),
  KEY `ix_certificates_college_id` (`college_id`),
  KEY `ix_certificates_recipient_name` (`recipient_name`),
  KEY `ix_certificates_college_name` (`college_name`),
  KEY `ix_certificates_certificate_number` (`certificate_number`),
  KEY `ix_certificates_public_token` (`public_token`),
  KEY `ix_certificates_status` (`status`),
  CONSTRAINT `fk_certificates_batch` FOREIGN KEY (`batch_id`) REFERENCES `certificate_batches` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_certificates_college` FOREIGN KEY (`college_id`) REFERENCES `colleges` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `certificates` (`id`, `batch_id`, `college_id`, `recipient_name`, `college_name`, `certificate_number`, `public_token`, `pdf_filename`, `pdf_path`, `status`, `created_at`) VALUES
	(1, 1, 1, 'VIGNESHWARAN P', 'Bharathiar University', 'CERT-2026-000001', 'hrdTo7BArdsZs6YED8h67Dw8GlTwBIY_DHZtnWx0mUk', '1cebb22cead54e252ed108db11c7106a.pdf', '1\\1cebb22cead54e252ed108db11c7106a.pdf', 'generated', '2026-09-11 16:33:50'),
	(2, 1, 2, 'Gokul S', 'SNS College', 'CERT-2026-000002', '6VFPOfIZoVqffPyBKPjU8G64k_7go_mwGwVCJLxSm5I', 'cacb3b658089aee1bce05dac5fa4963e.pdf', '1\\cacb3b658089aee1bce05dac5fa4963e.pdf', 'generated', '2026-09-11 16:33:50'),
	(3, 1, 3, 'Ajeesh', 'Nehru Arts & Science College', 'CERT-2026-000003', 'dI6xqtLEVkaGn8aSvXCJRNPq1_nfjRLaDIcKJzUrXK8', '29aa920ff628b1620a75a5e759e7f205.pdf', '1\\29aa920ff628b1620a75a5e759e7f205.pdf', 'generated', '2026-09-11 16:33:50'),
	(4, 1, 4, 'Vicky', 'Sree Narayana Guru College', 'CERT-2026-000004', 'SDBDXzcdT9VEelNunDXocrDe_seRa2-Xk4AZbP9l0so', '0b2433a3efedc0f966e0210809b7976f.pdf', '1\\0b2433a3efedc0f966e0210809b7976f.pdf', 'generated', '2026-09-11 16:33:50');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
