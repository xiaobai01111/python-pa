/*
 Navicat Premium Dump SQL

 Source Server         : PostgreSQL
 Source Server Type    : PostgreSQL
 Source Server Version : 180001 (180001)
 Source Host           : localhost:5432
 Source Catalog        : recommend_job
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 180001 (180001)
 File Encoding         : 65001

 Date: 09/12/2025 00:15:50
*/


-- ----------------------------
-- Sequence structure for auth_group_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."auth_group_id_seq";
CREATE SEQUENCE "public"."auth_group_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."auth_group_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for auth_group_permissions_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."auth_group_permissions_id_seq";
CREATE SEQUENCE "public"."auth_group_permissions_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER SEQUENCE "public"."auth_group_permissions_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for auth_permission_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."auth_permission_id_seq";
CREATE SEQUENCE "public"."auth_permission_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."auth_permission_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for auth_user_groups_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."auth_user_groups_id_seq";
CREATE SEQUENCE "public"."auth_user_groups_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER SEQUENCE "public"."auth_user_groups_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for auth_user_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."auth_user_id_seq";
CREATE SEQUENCE "public"."auth_user_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."auth_user_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for auth_user_user_permissions_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."auth_user_user_permissions_id_seq";
CREATE SEQUENCE "public"."auth_user_user_permissions_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER SEQUENCE "public"."auth_user_user_permissions_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for django_admin_log_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."django_admin_log_id_seq";
CREATE SEQUENCE "public"."django_admin_log_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."django_admin_log_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for django_content_type_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."django_content_type_id_seq";
CREATE SEQUENCE "public"."django_content_type_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."django_content_type_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for django_migrations_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."django_migrations_id_seq";
CREATE SEQUENCE "public"."django_migrations_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;
ALTER SEQUENCE "public"."django_migrations_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for job_data_job_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."job_data_job_id_seq";
CREATE SEQUENCE "public"."job_data_job_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."job_data_job_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for send_list_send_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."send_list_send_id_seq";
CREATE SEQUENCE "public"."send_list_send_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."send_list_send_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for spider_info_spider_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."spider_info_spider_id_seq";
CREATE SEQUENCE "public"."spider_info_spider_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."spider_info_spider_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Sequence structure for user_expect_expect_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."user_expect_expect_id_seq";
CREATE SEQUENCE "public"."user_expect_expect_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."user_expect_expect_id_seq" OWNER TO "xiaobai";

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_group";
CREATE TABLE "public"."auth_group" (
  "id" int4 NOT NULL DEFAULT nextval('auth_group_id_seq'::regclass),
  "name" varchar(150) COLLATE "pg_catalog"."default" NOT NULL
)
;
ALTER TABLE "public"."auth_group" OWNER TO "xiaobai";

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_group_permissions";
CREATE TABLE "public"."auth_group_permissions" (
  "id" int8 NOT NULL DEFAULT nextval('auth_group_permissions_id_seq'::regclass),
  "group_id" int4 NOT NULL,
  "permission_id" int4 NOT NULL
)
;
ALTER TABLE "public"."auth_group_permissions" OWNER TO "xiaobai";

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_permission";
CREATE TABLE "public"."auth_permission" (
  "id" int4 NOT NULL DEFAULT nextval('auth_permission_id_seq'::regclass),
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "content_type_id" int4 NOT NULL,
  "codename" varchar(100) COLLATE "pg_catalog"."default" NOT NULL
)
;
ALTER TABLE "public"."auth_permission" OWNER TO "xiaobai";

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_user";
CREATE TABLE "public"."auth_user" (
  "id" int4 NOT NULL DEFAULT nextval('auth_user_id_seq'::regclass),
  "password" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "last_login" timestamp(6),
  "is_superuser" bool NOT NULL,
  "username" varchar(150) COLLATE "pg_catalog"."default" NOT NULL,
  "first_name" varchar(150) COLLATE "pg_catalog"."default" NOT NULL,
  "last_name" varchar(150) COLLATE "pg_catalog"."default" NOT NULL,
  "email" varchar(254) COLLATE "pg_catalog"."default" NOT NULL,
  "is_staff" bool NOT NULL,
  "is_active" bool NOT NULL,
  "date_joined" timestamp(6) NOT NULL
)
;
ALTER TABLE "public"."auth_user" OWNER TO "xiaobai";

-- ----------------------------
-- Records of auth_user
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_user_groups";
CREATE TABLE "public"."auth_user_groups" (
  "id" int8 NOT NULL DEFAULT nextval('auth_user_groups_id_seq'::regclass),
  "user_id" int4 NOT NULL,
  "group_id" int4 NOT NULL
)
;
ALTER TABLE "public"."auth_user_groups" OWNER TO "xiaobai";

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_user_user_permissions";
CREATE TABLE "public"."auth_user_user_permissions" (
  "id" int8 NOT NULL DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass),
  "user_id" int4 NOT NULL,
  "permission_id" int4 NOT NULL
)
;
ALTER TABLE "public"."auth_user_user_permissions" OWNER TO "xiaobai";

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS "public"."django_admin_log";
CREATE TABLE "public"."django_admin_log" (
  "id" int4 NOT NULL DEFAULT nextval('django_admin_log_id_seq'::regclass),
  "action_time" timestamp(6) NOT NULL,
  "object_id" text COLLATE "pg_catalog"."default",
  "object_repr" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "action_flag" int2 NOT NULL,
  "change_message" text COLLATE "pg_catalog"."default" NOT NULL,
  "content_type_id" int4,
  "user_id" int4 NOT NULL
)
;
ALTER TABLE "public"."django_admin_log" OWNER TO "xiaobai";

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."django_content_type";
CREATE TABLE "public"."django_content_type" (
  "id" int4 NOT NULL DEFAULT nextval('django_content_type_id_seq'::regclass),
  "app_label" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "model" varchar(100) COLLATE "pg_catalog"."default" NOT NULL
)
;
ALTER TABLE "public"."django_content_type" OWNER TO "xiaobai";

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS "public"."django_migrations";
CREATE TABLE "public"."django_migrations" (
  "id" int8 NOT NULL DEFAULT nextval('django_migrations_id_seq'::regclass),
  "app" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "applied" timestamp(6) NOT NULL
)
;
ALTER TABLE "public"."django_migrations" OWNER TO "xiaobai";

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS "public"."django_session";
CREATE TABLE "public"."django_session" (
  "session_key" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "session_data" text COLLATE "pg_catalog"."default" NOT NULL,
  "expire_date" timestamp(6) NOT NULL
)
;
ALTER TABLE "public"."django_session" OWNER TO "xiaobai";

-- ----------------------------
-- Records of django_session
-- ----------------------------
BEGIN;
INSERT INTO "public"."django_session" ("session_key", "session_data", "expire_date") VALUES ('w1u41dtlocj1vp779ymcqfb8b0yek2k7', 'eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6IjIyNDM4ODY5MDcifQ:1vSdcl:LkAZVaMLqPT50jR7Xxiecoce4nb7l0i6AXsS9VM2W0U', '2025-12-22 15:58:07.166249');
INSERT INTO "public"."django_session" ("session_key", "session_data", "expire_date") VALUES ('qyxhfhop83qxond1gnkb65f9jkxgsyma', 'eyJ1c2VyX2lkIjoxLCJ1c2VyX25hbWUiOiIyMjQzODg2OTA3In0:1vSdlz:9PvZXqU_fjU6E_binHf88ZgUStQPCFB4uDhI1HKIueA', '2025-12-22 16:07:39.432075');
COMMIT;

-- ----------------------------
-- Table structure for job_data
-- ----------------------------
DROP TABLE IF EXISTS "public"."job_data";
CREATE TABLE "public"."job_data" (
  "job_id" int4 NOT NULL DEFAULT nextval('job_data_job_id_seq'::regclass),
  "name" varchar(255) COLLATE "pg_catalog"."default",
  "salary" varchar(255) COLLATE "pg_catalog"."default",
  "place" varchar(255) COLLATE "pg_catalog"."default",
  "education" varchar(255) COLLATE "pg_catalog"."default",
  "experience" varchar(255) COLLATE "pg_catalog"."default",
  "company" varchar(255) COLLATE "pg_catalog"."default",
  "label" varchar(255) COLLATE "pg_catalog"."default",
  "scale" varchar(255) COLLATE "pg_catalog"."default",
  "href" text COLLATE "pg_catalog"."default",
  "key_word" varchar(255) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."job_data" OWNER TO "xiaobai";
COMMENT ON COLUMN "public"."job_data"."name" IS '岗位名';
COMMENT ON COLUMN "public"."job_data"."salary" IS '薪资';
COMMENT ON COLUMN "public"."job_data"."place" IS '工作地';
COMMENT ON COLUMN "public"."job_data"."education" IS '学历';
COMMENT ON COLUMN "public"."job_data"."experience" IS '经验';
COMMENT ON COLUMN "public"."job_data"."company" IS '公司名';
COMMENT ON COLUMN "public"."job_data"."label" IS '行业';
COMMENT ON COLUMN "public"."job_data"."scale" IS '规模';
COMMENT ON COLUMN "public"."job_data"."key_word" IS '关键字';

-- ----------------------------
-- Records of job_data
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for send_list
-- ----------------------------
DROP TABLE IF EXISTS "public"."send_list";
CREATE TABLE "public"."send_list" (
  "send_id" int4 NOT NULL DEFAULT nextval('send_list_send_id_seq'::regclass),
  "job_id" int4,
  "user_id" int4
)
;
ALTER TABLE "public"."send_list" OWNER TO "xiaobai";

-- ----------------------------
-- Records of send_list
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for spider_info
-- ----------------------------
DROP TABLE IF EXISTS "public"."spider_info";
CREATE TABLE "public"."spider_info" (
  "spider_id" int4 NOT NULL DEFAULT nextval('spider_info_spider_id_seq'::regclass),
  "spider_name" varchar(255) COLLATE "pg_catalog"."default",
  "count" int4,
  "page" int4
)
;
ALTER TABLE "public"."spider_info" OWNER TO "xiaobai";

-- ----------------------------
-- Records of spider_info
-- ----------------------------
BEGIN;
INSERT INTO "public"."spider_info" ("spider_id", "spider_name", "count", "page") VALUES (1, 'spider', 11, 21);
COMMIT;

-- ----------------------------
-- Table structure for user_expect
-- ----------------------------
DROP TABLE IF EXISTS "public"."user_expect";
CREATE TABLE "public"."user_expect" (
  "expect_id" int4 NOT NULL DEFAULT nextval('user_expect_expect_id_seq'::regclass),
  "key_word" varchar(255) COLLATE "pg_catalog"."default",
  "user_id" int4,
  "place" varchar(255) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."user_expect" OWNER TO "xiaobai";

-- ----------------------------
-- Records of user_expect
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_list
-- ----------------------------
DROP TABLE IF EXISTS "public"."user_list";
CREATE TABLE "public"."user_list" (
  "user_id" int4 NOT NULL,
  "user_name" varchar(255) COLLATE "pg_catalog"."default",
  "pass_word" varchar(255) COLLATE "pg_catalog"."default",
  "user_account" varchar(50) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."user_list" OWNER TO "xiaobai";

-- ----------------------------
-- Records of user_list
-- ----------------------------
BEGIN;
INSERT INTO "public"."user_list" ("user_id", "user_name", "pass_word", "user_account") VALUES (1, '2243886907', '20040226Bx', '2243886907');
COMMIT;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."auth_group_id_seq"
OWNED BY "public"."auth_group"."id";
SELECT setval('"public"."auth_group_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."auth_group_permissions_id_seq"
OWNED BY "public"."auth_group_permissions"."id";
SELECT setval('"public"."auth_group_permissions_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."auth_permission_id_seq"
OWNED BY "public"."auth_permission"."id";
SELECT setval('"public"."auth_permission_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."auth_user_groups_id_seq"
OWNED BY "public"."auth_user_groups"."id";
SELECT setval('"public"."auth_user_groups_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."auth_user_id_seq"
OWNED BY "public"."auth_user"."id";
SELECT setval('"public"."auth_user_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."auth_user_user_permissions_id_seq"
OWNED BY "public"."auth_user_user_permissions"."id";
SELECT setval('"public"."auth_user_user_permissions_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."django_admin_log_id_seq"
OWNED BY "public"."django_admin_log"."id";
SELECT setval('"public"."django_admin_log_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."django_content_type_id_seq"
OWNED BY "public"."django_content_type"."id";
SELECT setval('"public"."django_content_type_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."django_migrations_id_seq"
OWNED BY "public"."django_migrations"."id";
SELECT setval('"public"."django_migrations_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."job_data_job_id_seq"
OWNED BY "public"."job_data"."job_id";
SELECT setval('"public"."job_data_job_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."send_list_send_id_seq"
OWNED BY "public"."send_list"."send_id";
SELECT setval('"public"."send_list_send_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."spider_info_spider_id_seq"
OWNED BY "public"."spider_info"."spider_id";
SELECT setval('"public"."spider_info_spider_id_seq"', 1, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."user_expect_expect_id_seq"
OWNED BY "public"."user_expect"."expect_id";
SELECT setval('"public"."user_expect_expect_id_seq"', 1, false);

-- ----------------------------
-- Uniques structure for table auth_group
-- ----------------------------
ALTER TABLE "public"."auth_group" ADD CONSTRAINT "auth_group_name_key" UNIQUE ("name");

-- ----------------------------
-- Primary Key structure for table auth_group
-- ----------------------------
ALTER TABLE "public"."auth_group" ADD CONSTRAINT "auth_group_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table auth_group_permissions
-- ----------------------------
ALTER TABLE "public"."auth_group_permissions" ADD CONSTRAINT "auth_group_permissions_group_id_permission_id_key" UNIQUE ("group_id", "permission_id");

-- ----------------------------
-- Primary Key structure for table auth_group_permissions
-- ----------------------------
ALTER TABLE "public"."auth_group_permissions" ADD CONSTRAINT "auth_group_permissions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table auth_permission
-- ----------------------------
ALTER TABLE "public"."auth_permission" ADD CONSTRAINT "auth_permission_content_type_id_codename_key" UNIQUE ("content_type_id", "codename");

-- ----------------------------
-- Primary Key structure for table auth_permission
-- ----------------------------
ALTER TABLE "public"."auth_permission" ADD CONSTRAINT "auth_permission_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table auth_user
-- ----------------------------
ALTER TABLE "public"."auth_user" ADD CONSTRAINT "auth_user_username_key" UNIQUE ("username");

-- ----------------------------
-- Primary Key structure for table auth_user
-- ----------------------------
ALTER TABLE "public"."auth_user" ADD CONSTRAINT "auth_user_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table auth_user_groups
-- ----------------------------
ALTER TABLE "public"."auth_user_groups" ADD CONSTRAINT "auth_user_groups_user_id_group_id_key" UNIQUE ("user_id", "group_id");

-- ----------------------------
-- Primary Key structure for table auth_user_groups
-- ----------------------------
ALTER TABLE "public"."auth_user_groups" ADD CONSTRAINT "auth_user_groups_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table auth_user_user_permissions
-- ----------------------------
ALTER TABLE "public"."auth_user_user_permissions" ADD CONSTRAINT "auth_user_user_permissions_user_id_permission_id_key" UNIQUE ("user_id", "permission_id");

-- ----------------------------
-- Primary Key structure for table auth_user_user_permissions
-- ----------------------------
ALTER TABLE "public"."auth_user_user_permissions" ADD CONSTRAINT "auth_user_user_permissions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table django_admin_log
-- ----------------------------
CREATE INDEX "django_admin_log_content_type_id_idx" ON "public"."django_admin_log" USING btree (
  "content_type_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "django_admin_log_user_id_idx" ON "public"."django_admin_log" USING btree (
  "user_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Checks structure for table django_admin_log
-- ----------------------------
ALTER TABLE "public"."django_admin_log" ADD CONSTRAINT "django_admin_log_action_flag_check" CHECK (action_flag >= 0);

-- ----------------------------
-- Primary Key structure for table django_admin_log
-- ----------------------------
ALTER TABLE "public"."django_admin_log" ADD CONSTRAINT "django_admin_log_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table django_content_type
-- ----------------------------
ALTER TABLE "public"."django_content_type" ADD CONSTRAINT "django_content_type_app_label_model_key" UNIQUE ("app_label", "model");

-- ----------------------------
-- Primary Key structure for table django_content_type
-- ----------------------------
ALTER TABLE "public"."django_content_type" ADD CONSTRAINT "django_content_type_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table django_migrations
-- ----------------------------
ALTER TABLE "public"."django_migrations" ADD CONSTRAINT "django_migrations_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table django_session
-- ----------------------------
CREATE INDEX "django_session_expire_date_idx" ON "public"."django_session" USING btree (
  "expire_date" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table django_session
-- ----------------------------
ALTER TABLE "public"."django_session" ADD CONSTRAINT "django_session_pkey" PRIMARY KEY ("session_key");

-- ----------------------------
-- Primary Key structure for table job_data
-- ----------------------------
ALTER TABLE "public"."job_data" ADD CONSTRAINT "job_data_pkey" PRIMARY KEY ("job_id");

-- ----------------------------
-- Indexes structure for table send_list
-- ----------------------------
CREATE INDEX "send_list_job_id_idx" ON "public"."send_list" USING btree (
  "job_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "send_list_user_id_idx" ON "public"."send_list" USING btree (
  "user_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table send_list
-- ----------------------------
ALTER TABLE "public"."send_list" ADD CONSTRAINT "send_list_pkey" PRIMARY KEY ("send_id");

-- ----------------------------
-- Primary Key structure for table spider_info
-- ----------------------------
ALTER TABLE "public"."spider_info" ADD CONSTRAINT "spider_info_pkey" PRIMARY KEY ("spider_id");

-- ----------------------------
-- Indexes structure for table user_expect
-- ----------------------------
CREATE INDEX "user_expect_user_id_idx" ON "public"."user_expect" USING btree (
  "user_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table user_expect
-- ----------------------------
ALTER TABLE "public"."user_expect" ADD CONSTRAINT "user_expect_pkey" PRIMARY KEY ("expect_id");

-- ----------------------------
-- Primary Key structure for table user_list
-- ----------------------------
ALTER TABLE "public"."user_list" ADD CONSTRAINT "user_list_pkey" PRIMARY KEY ("user_id");

-- ----------------------------
-- Foreign Keys structure for table auth_group_permissions
-- ----------------------------
ALTER TABLE "public"."auth_group_permissions" ADD CONSTRAINT "auth_group_permissions_group_id_fkey" FOREIGN KEY ("group_id") REFERENCES "public"."auth_group" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE "public"."auth_group_permissions" ADD CONSTRAINT "auth_group_permissions_permission_id_fkey" FOREIGN KEY ("permission_id") REFERENCES "public"."auth_permission" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT;

-- ----------------------------
-- Foreign Keys structure for table auth_permission
-- ----------------------------
ALTER TABLE "public"."auth_permission" ADD CONSTRAINT "auth_permission_content_type_id_fkey" FOREIGN KEY ("content_type_id") REFERENCES "public"."django_content_type" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT;

-- ----------------------------
-- Foreign Keys structure for table auth_user_groups
-- ----------------------------
ALTER TABLE "public"."auth_user_groups" ADD CONSTRAINT "auth_user_groups_group_id_fkey" FOREIGN KEY ("group_id") REFERENCES "public"."auth_group" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE "public"."auth_user_groups" ADD CONSTRAINT "auth_user_groups_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT;

-- ----------------------------
-- Foreign Keys structure for table auth_user_user_permissions
-- ----------------------------
ALTER TABLE "public"."auth_user_user_permissions" ADD CONSTRAINT "auth_user_user_permissions_permission_id_fkey" FOREIGN KEY ("permission_id") REFERENCES "public"."auth_permission" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE "public"."auth_user_user_permissions" ADD CONSTRAINT "auth_user_user_permissions_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT;

-- ----------------------------
-- Foreign Keys structure for table django_admin_log
-- ----------------------------
ALTER TABLE "public"."django_admin_log" ADD CONSTRAINT "django_admin_log_content_type_id_fkey" FOREIGN KEY ("content_type_id") REFERENCES "public"."django_content_type" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE "public"."django_admin_log" ADD CONSTRAINT "django_admin_log_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT;

-- ----------------------------
-- Foreign Keys structure for table send_list
-- ----------------------------
ALTER TABLE "public"."send_list" ADD CONSTRAINT "send_list_job_id_fkey" FOREIGN KEY ("job_id") REFERENCES "public"."job_data" ("job_id") ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE "public"."send_list" ADD CONSTRAINT "send_list_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."user_list" ("user_id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table user_expect
-- ----------------------------
ALTER TABLE "public"."user_expect" ADD CONSTRAINT "user_expect_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."user_list" ("user_id") ON DELETE NO ACTION ON UPDATE NO ACTION;
