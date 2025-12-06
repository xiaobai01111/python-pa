/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 50731
 Source Host           : localhost:3306
 Source Schema         : recommend_job

 Target Server Type    : MySQL
 Target Server Version : 50731
 File Encoding         : 65001

 Date: 30/09/2024 12:00:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add job data', 7, 'add_jobdata');
INSERT INTO `auth_permission` VALUES (26, 'Can change job data', 7, 'change_jobdata');
INSERT INTO `auth_permission` VALUES (27, 'Can delete job data', 7, 'delete_jobdata');
INSERT INTO `auth_permission` VALUES (28, 'Can view job data', 7, 'view_jobdata');
INSERT INTO `auth_permission` VALUES (29, 'Can add spider info', 8, 'add_spiderinfo');
INSERT INTO `auth_permission` VALUES (30, 'Can change spider info', 8, 'change_spiderinfo');
INSERT INTO `auth_permission` VALUES (31, 'Can delete spider info', 8, 'delete_spiderinfo');
INSERT INTO `auth_permission` VALUES (32, 'Can view spider info', 8, 'view_spiderinfo');
INSERT INTO `auth_permission` VALUES (33, 'Can add user list', 9, 'add_userlist');
INSERT INTO `auth_permission` VALUES (34, 'Can change user list', 9, 'change_userlist');
INSERT INTO `auth_permission` VALUES (35, 'Can delete user list', 9, 'delete_userlist');
INSERT INTO `auth_permission` VALUES (36, 'Can view user list', 9, 'view_userlist');
INSERT INTO `auth_permission` VALUES (37, 'Can add send list', 10, 'add_sendlist');
INSERT INTO `auth_permission` VALUES (38, 'Can change send list', 10, 'change_sendlist');
INSERT INTO `auth_permission` VALUES (39, 'Can delete send list', 10, 'delete_sendlist');
INSERT INTO `auth_permission` VALUES (40, 'Can view send list', 10, 'view_sendlist');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$260000$2NPGJqSuDFR32RY9OHlNbO$c1q66npQG/jj7N83+BcROLcSzBPGF5Iz3mODCDbOGSM=', '2024-09-30 03:12:02.888152', 1, '1', '', '', '', 1, 1, '2024-09-30 02:41:01.589772');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (7, 'job', 'jobdata');
INSERT INTO `django_content_type` VALUES (10, 'job', 'sendlist');
INSERT INTO `django_content_type` VALUES (8, 'job', 'spiderinfo');
INSERT INTO `django_content_type` VALUES (9, 'job', 'userlist');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2023-02-17 06:24:36.973478');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2023-02-17 06:25:25.774725');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2023-02-17 06:25:34.560833');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2023-02-17 06:25:34.742294');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2023-02-17 06:25:34.894299');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2023-02-17 06:25:42.124035');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2023-02-17 06:25:44.862348');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2023-02-17 06:25:45.687168');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2023-02-17 06:25:45.825708');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2023-02-17 06:25:49.669260');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2023-02-17 06:25:49.844874');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2023-02-17 06:25:49.949260');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2023-02-17 06:25:52.963850');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2023-02-17 06:25:57.565794');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2023-02-17 06:25:58.328442');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2023-02-17 06:25:58.627687');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2023-02-17 06:26:01.794639');
INSERT INTO `django_migrations` VALUES (18, 'sessions', '0001_initial', '2023-02-17 06:26:03.618668');
INSERT INTO `django_migrations` VALUES (19, 'job', '0001_initial', '2023-02-17 14:11:02.473704');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('2oc98d3fs6vf194f43b2u9r15b5st796', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6Ilx1NmQ0Ylx1OGJkNV8xIn0:1pT1lT:o67fkYA6MknLQ-Nxi4NqxRV2naq27FIRNlDqWYDZoEM', '2023-03-03 14:31:07.595210');
INSERT INTO `django_session` VALUES ('2xu7dqwcyewgj7db8mwowum6hk8n1g6o', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6Ilx1NmQ0Ylx1OGJkNV8xIn0:1pSvSk:JEY9rtW3eVLt-L-MGga4QKA8RCWBSJCoHwBp5Ba4N-c', '2023-03-03 07:47:22.808532');
INSERT INTO `django_session` VALUES ('598y1wvj5c1h5dlzxb8qv3tlfgy2rc67', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6Ilx1NmQ0Ylx1OGJkNV8xIn0:1pTLLf:CR8kikzV1_gc6H6mhVFX271ebqFk0ez2oPVIP4HqLCU', '2023-03-04 11:25:47.085256');
INSERT INTO `django_session` VALUES ('5oo5gbq4bjiy8fmu0aa8wau7dmhyu8q7', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6Ilx1NmQ0Ylx1OGJkNV8xIn0:1pvzPg:Z_GsAyW26jtIZQH99-K0k5IFgFxLm9OJWcBWIC6xNeA', '2023-05-22 11:52:20.944159');
INSERT INTO `django_session` VALUES ('6feq2lpi7memkbxc1zhtfzdkywifhr7q', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6Ilx1NmQ0Ylx1OGJkNV8xIn0:1sv64l:f7h2TpMFhk4Lr7Qzz0_I_m2NnOJFMRGW32uALXhlBmA', '2024-10-14 02:23:51.296191');
INSERT INTO `django_session` VALUES ('8dd8vrff5tlivkx0uin6vaxtlfrhzzlm', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6Ilx1NmQ0Ylx1OGJkNV8xIn0:1pTH64:5wASVywctOFi-kKUF55dC29OQdjQAFGi1bbyx50ZImo', '2023-03-04 06:53:24.701206');
INSERT INTO `django_session` VALUES ('biug7fnm6ezkzbfwfk0z78nm12ziob88', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6Ilx1NmQ0Ylx1OGJkNV8xIn0:1puXPR:Ina8ZBMmRXA5CFirtQ5BTIE0A1EDqbET_2kDWUoD6Eo', '2023-05-18 11:46:05.602261');
INSERT INTO `django_session` VALUES ('qb08pmh4fzj9h17oilfwpbr4yaivghkk', '.eJzFkMtuwyAQRX8lYp3YgMGPLLvvsqs6sgYPNKR-RLZZRf73Qp1IzUNZVJW6sEfDvRxm7om4UQ-VRbIljKyXroNW-750KQpVulyhrIJYgZv21fWFH2cK6k_dBQEP0H30Ud1302BVFCzRWR2j1x5183L2XgH2MO797RpYUdQ6RS554n-U0wxoITEFJTjjSkjBaEEVYmGkUcLkCaNAJRNcivwb2urOjZ71fipJWKck21VJytIJo5kvKU2NL5mC0GWCpiVZe4f1My9eA8PKwKa2Q93oRWzD5GOQ77CSCwwlMTTwJM_DIzzJ7rEqYOF4vFDd0CxSDNjaLj70Kg5xNHac4sUCiG_PXF4_O9WgAevBterxnL9df16v_mjleRdUbTGIjFL-AJ1yVL7kVOY3M9-hx4AOQWwm-yRQ_yFM8DzPi-lf4vz9zreJJrcHbN6R-Qu2_zdK:1sv6pO:wZGiQmVbV8Etfk2GAaBM4d3ekvPpLCceYY09lGaVHJo', '2024-10-14 03:12:02.914995');
INSERT INTO `django_session` VALUES ('u4zjuef3ecvuuatvaubatw31l3wswvwn', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6Ilx1NmQ0Ylx1OGJkNV8xIn0:1r6AtD:KFC94uq2i2rG4j5CsIFA57RIL6KSlKoueq1nnKPsuKk', '2023-12-07 14:41:11.588133');
INSERT INTO `django_session` VALUES ('yn9v3pp8nrpv6jggowv6xeoib42ht3yn', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6Ilx1NmQ0Ylx1OGJkNV8xIn0:1pVwMT:1Hv8oKPLZkKP-zOO32fr1_3vAMg6-7YTmaX9eJxZc3Y', '2023-03-11 15:21:21.231153');
INSERT INTO `django_session` VALUES ('zdj5mdvvjwricl6ue9agwecm587wkxd2', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6Ilx1NmQ0Ylx1OGJkNV8xIn0:1pSv6l:s7kmBdlDUe-jDlb9dmD-MHhljwqn3PijSNAKBMvY7Mw', '2023-03-03 07:24:39.307769');
INSERT INTO `django_session` VALUES ('zv3qbujt495ux9l3o7k8zk3wfiq07y6r', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6Ilx1NmQ0Ylx1OGJkNV8xIn0:1pSzTE:kKwmrado_KrJOJ2KJ8p9Ci4_xpZA1zJQ8ejaWQ2iMlk', '2023-03-03 12:04:08.922549');

-- ----------------------------
-- Table structure for job_data
-- ----------------------------
DROP TABLE IF EXISTS `job_data`;
CREATE TABLE `job_data`  (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '岗位名',
  `salary` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '薪资',
  `place` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '工作地',
  `education` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '学历',
  `experience` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '经验',
  `company` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '公司名',
  `label` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '行业',
  `scale` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '规模',
  `href` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '职位链接',
  `key_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '关键字',
  PRIMARY KEY (`job_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14960 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of job_data
-- ----------------------------


-- ----------------------------
-- Table structure for send_list
-- ----------------------------
DROP TABLE IF EXISTS `send_list`;
CREATE TABLE `send_list`  (
  `send_id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) NULL DEFAULT NULL,
  `user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`send_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `job_id`(`job_id`) USING BTREE,
  CONSTRAINT `send_list_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_list` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `send_list_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `job_data` (`job_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 42 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of send_list
-- ----------------------------
INSERT INTO `send_list` VALUES (8, 589, '1');
INSERT INTO `send_list` VALUES (10, 621, '1');
INSERT INTO `send_list` VALUES (11, 593, '1');
INSERT INTO `send_list` VALUES (14, 618, '1');
INSERT INTO `send_list` VALUES (17, 1182, '1');
INSERT INTO `send_list` VALUES (19, 1392, '1');
INSERT INTO `send_list` VALUES (20, 1447, '1');
INSERT INTO `send_list` VALUES (21, 14673, '1');
INSERT INTO `send_list` VALUES (22, 2190, '1');
INSERT INTO `send_list` VALUES (23, 589, '2');
INSERT INTO `send_list` VALUES (24, 2190, '2');
INSERT INTO `send_list` VALUES (25, 2404, '2');
INSERT INTO `send_list` VALUES (26, 2405, '2');
INSERT INTO `send_list` VALUES (27, 595, '2');
INSERT INTO `send_list` VALUES (28, 8137, '2');
INSERT INTO `send_list` VALUES (29, 2018, '2');
INSERT INTO `send_list` VALUES (30, 583, '2');
INSERT INTO `send_list` VALUES (31, 594, '2');
INSERT INTO `send_list` VALUES (32, 1960, '1');
INSERT INTO `send_list` VALUES (34, 597, '1');
INSERT INTO `send_list` VALUES (36, 11713, '1');
INSERT INTO `send_list` VALUES (37, 1783, '1');
INSERT INTO `send_list` VALUES (39, 14657, '1');
INSERT INTO `send_list` VALUES (40, 14959, '1');
INSERT INTO `send_list` VALUES (41, 14854, '1');

-- ----------------------------
-- Table structure for spider_info
-- ----------------------------
DROP TABLE IF EXISTS `spider_info`;
CREATE TABLE `spider_info`  (
  `spider_id` int(11) NOT NULL AUTO_INCREMENT,
  `spider_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `count` int(11) NULL DEFAULT NULL,
  `page` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`spider_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of spider_info
-- ----------------------------
INSERT INTO `spider_info` VALUES (1, 'spider', 45, 405);

-- ----------------------------
-- Table structure for user_expect
-- ----------------------------
DROP TABLE IF EXISTS `user_expect`;
CREATE TABLE `user_expect`  (
  `expect_id` int(11) NOT NULL AUTO_INCREMENT,
  `key_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `user_id` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `place` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`expect_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `user_expect_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_list` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_expect
-- ----------------------------
INSERT INTO `user_expect` VALUES (1, 'c', '1', '北京');
INSERT INTO `user_expect` VALUES (2, 'python', '2', '北京');

-- ----------------------------
-- Table structure for user_list
-- ----------------------------
DROP TABLE IF EXISTS `user_list`;
CREATE TABLE `user_list`  (
  `user_id` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `pass_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_list
-- ----------------------------
INSERT INTO `user_list` VALUES ('1', '测试_1', '1');
INSERT INTO `user_list` VALUES ('2', '测试_2', '2');

SET FOREIGN_KEY_CHECKS = 1;
