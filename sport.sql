/*
 Navicat Premium Data Transfer

 Source Server         : sport
 Source Server Type    : PostgreSQL
 Source Server Version : 90606
 Source Host           : localhost
 Source Database       : sport
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 90606
 File Encoding         : utf-8

 Date: 01/18/2018 05:20:41 AM
*/

-- ----------------------------
--  Sequence structure for category_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."category_id_seq";
CREATE SEQUENCE "public"."category_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."category_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for competitor_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."competitor_id_seq";
CREATE SEQUENCE "public"."competitor_id_seq" INCREMENT 1 START 32 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."competitor_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for course_device_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."course_device_id_seq";
CREATE SEQUENCE "public"."course_device_id_seq" INCREMENT 1 START 6 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."course_device_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for course_device_type_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."course_device_type_id_seq";
CREATE SEQUENCE "public"."course_device_type_id_seq" INCREMENT 1 START 3 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."course_device_type_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for course_forerunner_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."course_forerunner_id_seq";
CREATE SEQUENCE "public"."course_forerunner_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."course_forerunner_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for course_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."course_id_seq";
CREATE SEQUENCE "public"."course_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."course_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for coursetter_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."coursetter_id_seq";
CREATE SEQUENCE "public"."coursetter_id_seq" INCREMENT 1 START 8 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."coursetter_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for data_in_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."data_in_id_seq";
CREATE SEQUENCE "public"."data_in_id_seq" INCREMENT 1 START 40 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."data_in_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for device_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."device_id_seq";
CREATE SEQUENCE "public"."device_id_seq" INCREMENT 1 START 6 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."device_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for device_type_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."device_type_id_seq";
CREATE SEQUENCE "public"."device_type_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."device_type_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for discipline_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."discipline_id_seq";
CREATE SEQUENCE "public"."discipline_id_seq" INCREMENT 1 START 14 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."discipline_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for forerunner_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."forerunner_id_seq";
CREATE SEQUENCE "public"."forerunner_id_seq" INCREMENT 1 START 8 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."forerunner_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for gender_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."gender_id_seq";
CREATE SEQUENCE "public"."gender_id_seq" INCREMENT 1 START 2 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."gender_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for jury_function_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."jury_function_id_seq";
CREATE SEQUENCE "public"."jury_function_id_seq" INCREMENT 1 START 7 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."jury_function_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for jury_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."jury_id_seq";
CREATE SEQUENCE "public"."jury_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."jury_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for mark_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."mark_id_seq";
CREATE SEQUENCE "public"."mark_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."mark_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for nation_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."nation_id_seq";
CREATE SEQUENCE "public"."nation_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."nation_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for race_competitor_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."race_competitor_id_seq";
CREATE SEQUENCE "public"."race_competitor_id_seq" INCREMENT 1 START 6 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."race_competitor_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for race_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."race_id_seq";
CREATE SEQUENCE "public"."race_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."race_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for race_jury_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."race_jury_id_seq";
CREATE SEQUENCE "public"."race_jury_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."race_jury_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for race_team_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."race_team_id_seq";
CREATE SEQUENCE "public"."race_team_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."race_team_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for report_type_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."report_type_id_seq";
CREATE SEQUENCE "public"."report_type_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."report_type_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for result_detail_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."result_detail_id_seq";
CREATE SEQUENCE "public"."result_detail_id_seq" INCREMENT 1 START 40 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."result_detail_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for result_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."result_id_seq";
CREATE SEQUENCE "public"."result_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."result_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for roles_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."roles_id_seq";
CREATE SEQUENCE "public"."roles_id_seq" INCREMENT 1 START 3 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."roles_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for run_info_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."run_info_id_seq";
CREATE SEQUENCE "public"."run_info_id_seq" INCREMENT 1 START 6 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."run_info_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for run_order_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."run_order_id_seq";
CREATE SEQUENCE "public"."run_order_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."run_order_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for status_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."status_id_seq";
CREATE SEQUENCE "public"."status_id_seq" INCREMENT 1 START 16 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."status_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for td_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."td_id_seq";
CREATE SEQUENCE "public"."td_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."td_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for tdrole_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."tdrole_id_seq";
CREATE SEQUENCE "public"."tdrole_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."tdrole_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for team_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."team_id_seq";
CREATE SEQUENCE "public"."team_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."team_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for users_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_id_seq";
CREATE SEQUENCE "public"."users_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."users_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for weather_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."weather_id_seq";
CREATE SEQUENCE "public"."weather_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."weather_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Table structure for device_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."device_type";
CREATE TABLE "public"."device_type" (
	"id" int4 NOT NULL DEFAULT nextval('device_type_id_seq'::regclass),
	"name" varchar COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."device_type" OWNER TO "postgres";

-- ----------------------------
--  Records of device_type
-- ----------------------------
BEGIN;
INSERT INTO "public"."device_type" VALUES ('1', 'test');
COMMIT;

-- ----------------------------
--  Table structure for gender
-- ----------------------------
DROP TABLE IF EXISTS "public"."gender";
CREATE TABLE "public"."gender" (
	"id" int4 NOT NULL DEFAULT nextval('gender_id_seq'::regclass),
	"fiscode" varchar COLLATE "default",
	"ru_name" varchar COLLATE "default",
	"en_name" varchar COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."gender" OWNER TO "postgres";

-- ----------------------------
--  Records of gender
-- ----------------------------
BEGIN;
INSERT INTO "public"."gender" VALUES ('1', 'Male', 'Male', 'Male');
INSERT INTO "public"."gender" VALUES ('2', 'Female', 'Female', 'Female');
COMMIT;

-- ----------------------------
--  Table structure for report_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."report_type";
CREATE TABLE "public"."report_type" (
	"id" int4 NOT NULL DEFAULT nextval('report_type_id_seq'::regclass),
	"name" varchar COLLATE "default",
	"function" varchar COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."report_type" OWNER TO "postgres";

-- ----------------------------
--  Table structure for mark
-- ----------------------------
DROP TABLE IF EXISTS "public"."mark";
CREATE TABLE "public"."mark" (
	"id" int4 NOT NULL DEFAULT nextval('mark_id_seq'::regclass),
	"name" varchar(4) COLLATE "default",
	"description" varchar(100) COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."mark" OWNER TO "postgres";

-- ----------------------------
--  Table structure for jury_function
-- ----------------------------
DROP TABLE IF EXISTS "public"."jury_function";
CREATE TABLE "public"."jury_function" (
	"id" int4 NOT NULL DEFAULT nextval('jury_function_id_seq'::regclass),
	"ru_function" varchar COLLATE "default",
	"en_function" varchar COLLATE "default",
	"attribute_values" varchar COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."jury_function" OWNER TO "postgres";

-- ----------------------------
--  Records of jury_function
-- ----------------------------
BEGIN;
INSERT INTO "public"."jury_function" VALUES ('1', 'ChiefRace', 'ChiefRace', 'ChiefRace');
INSERT INTO "public"."jury_function" VALUES ('2', 'Referee', 'Referee', 'Referee');
INSERT INTO "public"."jury_function" VALUES ('3', 'Assistantreferee', 'Assistantreferee', 'Assistantreferee');
INSERT INTO "public"."jury_function" VALUES ('4', 'ChiefCourse', 'ChiefCourse', 'ChiefCourse');
INSERT INTO "public"."jury_function" VALUES ('5', 'Startreferee', 'Startreferee', 'Startreferee');
INSERT INTO "public"."jury_function" VALUES ('6', 'Finishreferee', 'Finishreferee', 'Finishreferee');
INSERT INTO "public"."jury_function" VALUES ('7', 'ChiefTiming', 'ChiefTiming', 'ChiefTiming');
COMMIT;

-- ----------------------------
--  Table structure for status
-- ----------------------------
DROP TABLE IF EXISTS "public"."status";
CREATE TABLE "public"."status" (
	"id" int4 NOT NULL DEFAULT nextval('status_id_seq'::regclass),
	"name" varchar(4) COLLATE "default",
	"description" varchar(100) COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."status" OWNER TO "postgres";

-- ----------------------------
--  Records of status
-- ----------------------------
BEGIN;
INSERT INTO "public"."status" VALUES ('1', 'QLF', 'Qualified');
INSERT INTO "public"."status" VALUES ('2', 'DNS', 'Did not start ');
INSERT INTO "public"."status" VALUES ('3', 'DNS1', 'Did not start run 1');
INSERT INTO "public"."status" VALUES ('4', 'DNS2', 'Did not start run 2');
INSERT INTO "public"."status" VALUES ('5', 'DSQ', 'Disqualified');
INSERT INTO "public"."status" VALUES ('6', 'DSQ1', 'Disqualified run 1');
INSERT INTO "public"."status" VALUES ('7', 'DSQ2', 'Disqualified run 2');
INSERT INTO "public"."status" VALUES ('8', 'DNF', 'Did not finish ');
INSERT INTO "public"."status" VALUES ('9', 'DNF1', 'Did not finish run 1');
INSERT INTO "public"."status" VALUES ('10', 'DNF2', 'Did not finish run 2');
INSERT INTO "public"."status" VALUES ('11', 'DNQ', 'Did not qualify');
INSERT INTO "public"."status" VALUES ('12', 'DNQ1', 'Did not qualify run 1');
INSERT INTO "public"."status" VALUES ('13', 'DPO', 'Doping offense ');
INSERT INTO "public"."status" VALUES ('14', 'NPS', 'Not permitted to start ');
INSERT INTO "public"."status" VALUES ('15', 'DQB', 'Disqualification for unsportsmanlike behavior');
INSERT INTO "public"."status" VALUES ('16', 'DQO', 'Disqualified for over quota');
COMMIT;

-- ----------------------------
--  Table structure for discipline
-- ----------------------------
DROP TABLE IF EXISTS "public"."discipline";
CREATE TABLE "public"."discipline" (
	"id" int4 NOT NULL DEFAULT nextval('discipline_id_seq'::regclass),
	"fiscode" varchar COLLATE "default",
	"ru_name" varchar COLLATE "default",
	"en_name" varchar COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."discipline" OWNER TO "postgres";

-- ----------------------------
--  Records of discipline
-- ----------------------------
BEGIN;
INSERT INTO "public"."discipline" VALUES ('1', 'DH', 'Downhill', 'Downhill');
INSERT INTO "public"."discipline" VALUES ('2', 'SL', 'Slalom', 'Slalom');
INSERT INTO "public"."discipline" VALUES ('3', 'GS', 'Giant Slalom', 'Giant Slalom');
INSERT INTO "public"."discipline" VALUES ('4', 'SG', 'Super G', 'Super G');
INSERT INTO "public"."discipline" VALUES ('5', 'SC', 'Super Combined', 'Super Combined');
INSERT INTO "public"."discipline" VALUES ('6', 'TE', 'Team', 'Team');
INSERT INTO "public"."discipline" VALUES ('7', 'KOS', 'KO Slalom', 'KO Slalom');
INSERT INTO "public"."discipline" VALUES ('8', 'KOG', 'KO Giant Slalom', 'KO Giant Slalom');
INSERT INTO "public"."discipline" VALUES ('9', 'PGS', 'Parallel Giant Slalom', 'Parallel Giant Slalom');
INSERT INTO "public"."discipline" VALUES ('10', 'PSL', 'Parallel Slalom', 'Parallel Slalom');
INSERT INTO "public"."discipline" VALUES ('11', 'CE', 'City Event', 'City Event');
INSERT INTO "public"."discipline" VALUES ('12', 'IND', 'Indoor', 'Indoor');
INSERT INTO "public"."discipline" VALUES ('13', 'P', 'Parallel', 'Parallel');
INSERT INTO "public"."discipline" VALUES ('14', 'CAR', 'Carving', 'Carving');
COMMIT;

-- ----------------------------
--  Table structure for tdrole
-- ----------------------------
DROP TABLE IF EXISTS "public"."tdrole";
CREATE TABLE "public"."tdrole" (
	"id" int4 NOT NULL DEFAULT nextval('tdrole_id_seq'::regclass),
	"name" varchar COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."tdrole" OWNER TO "postgres";

-- ----------------------------
--  Table structure for td
-- ----------------------------
DROP TABLE IF EXISTS "public"."td";
CREATE TABLE "public"."td" (
	"id" int4 NOT NULL DEFAULT nextval('td_id_seq'::regclass),
	"tdnumber" varchar COLLATE "default",
	"ru_firstname" varchar COLLATE "default",
	"en_firstname" varchar COLLATE "default",
	"ru_lastname" varchar COLLATE "default",
	"en_lastname" varchar COLLATE "default",
	"ru_nation" varchar COLLATE "default",
	"en_nation" varchar COLLATE "default",
	"tdrole_id" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."td" OWNER TO "postgres";

-- ----------------------------
--  Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
	"id" int4 NOT NULL DEFAULT nextval('users_id_seq'::regclass),
	"email" varchar(64) COLLATE "default",
	"username" varchar(64) COLLATE "default",
	"role_id" int4,
	"password_hash" varchar(128) COLLATE "default",
	"confirmed" bool,
	"name" varchar(64) COLLATE "default",
	"location" varchar(64) COLLATE "default",
	"about_me" text COLLATE "default",
	"member_since" timestamp(6) NULL,
	"last_seen" timestamp(6) NULL,
	"lang" varchar(3) COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."users" OWNER TO "postgres";

-- ----------------------------
--  Records of users
-- ----------------------------
BEGIN;
INSERT INTO "public"."users" VALUES ('1', 'karasev_a_e@mail.ru', 'karasik', '3', 'pbkdf2:sha1:1000$crvb0XoV$4e13a1d62e0dc7a1245ec57d7aed5a0e02b9feb0', 't', null, null, null, '2017-12-17 21:56:49.929604', '2018-01-17 21:56:48.870986', 'ru');
COMMIT;

-- ----------------------------
--  Table structure for forerunner
-- ----------------------------
DROP TABLE IF EXISTS "public"."forerunner";
CREATE TABLE "public"."forerunner" (
	"id" int4 NOT NULL DEFAULT nextval('forerunner_id_seq'::regclass),
	"ru_lastname" varchar COLLATE "default",
	"ru_firstname" varchar COLLATE "default",
	"en_lastname" varchar COLLATE "default",
	"en_firstname" varchar COLLATE "default",
	"nation_id" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."forerunner" OWNER TO "postgres";

-- ----------------------------
--  Records of forerunner
-- ----------------------------
BEGIN;
INSERT INTO "public"."forerunner" VALUES ('1', 'surname1', 'name1', 'surname1', 'name1', '1');
INSERT INTO "public"."forerunner" VALUES ('2', 'surname2', 'name2', 'surname2', 'name2', '1');
INSERT INTO "public"."forerunner" VALUES ('3', 'surname3', 'name3', 'surname3', 'name3', '1');
INSERT INTO "public"."forerunner" VALUES ('4', 'surname4', 'name4', 'surname4', 'name4', '1');
INSERT INTO "public"."forerunner" VALUES ('5', 'surname1', 'name1', 'surname1', 'name1', '1');
INSERT INTO "public"."forerunner" VALUES ('6', 'surname2', 'name2', 'surname2', 'name2', '1');
INSERT INTO "public"."forerunner" VALUES ('7', 'surname3', 'name3', 'surname3', 'name3', '1');
INSERT INTO "public"."forerunner" VALUES ('8', 'surname4', 'name4', 'surname4', 'name4', '1');
COMMIT;

-- ----------------------------
--  Table structure for coursetter
-- ----------------------------
DROP TABLE IF EXISTS "public"."coursetter";
CREATE TABLE "public"."coursetter" (
	"id" int4 NOT NULL DEFAULT nextval('coursetter_id_seq'::regclass),
	"ru_lastname" varchar COLLATE "default",
	"ru_firstname" varchar COLLATE "default",
	"en_lastname" varchar COLLATE "default",
	"en_firstname" varchar COLLATE "default",
	"nation_id" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."coursetter" OWNER TO "postgres";

-- ----------------------------
--  Records of coursetter
-- ----------------------------
BEGIN;
INSERT INTO "public"."coursetter" VALUES ('1', 'surname1', 'name1', 'surname1', 'name1', '1');
INSERT INTO "public"."coursetter" VALUES ('2', 'surname2', 'name2', 'surname2', 'name2', '1');
INSERT INTO "public"."coursetter" VALUES ('3', 'surname3', 'name3', 'surname3', 'name3', '1');
INSERT INTO "public"."coursetter" VALUES ('4', 'surname4', 'name4', 'surname4', 'name4', '1');
INSERT INTO "public"."coursetter" VALUES ('5', 'surname1', 'name1', 'surname1', 'name1', '1');
INSERT INTO "public"."coursetter" VALUES ('6', 'surname2', 'name2', 'surname2', 'name2', '1');
INSERT INTO "public"."coursetter" VALUES ('7', 'surname3', 'name3', 'surname3', 'name3', '1');
INSERT INTO "public"."coursetter" VALUES ('8', 'surname4', 'name4', 'surname4', 'name4', '1');
COMMIT;

-- ----------------------------
--  Table structure for competitor
-- ----------------------------
DROP TABLE IF EXISTS "public"."competitor";
CREATE TABLE "public"."competitor" (
	"id" int4 NOT NULL DEFAULT nextval('competitor_id_seq'::regclass),
	"fiscode" varchar COLLATE "default",
	"ru_firstname" varchar COLLATE "default",
	"en_firstname" varchar COLLATE "default",
	"ru_lastname" varchar COLLATE "default",
	"en_lastname" varchar COLLATE "default",
	"gender_id" int4,
	"birth" date,
	"nation_code_id" int4,
	"national_code" varchar(1) COLLATE "default",
	"NSA" varchar COLLATE "default",
	"category_id" int4,
	"points" float8,
	"fis_points" float8
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."competitor" OWNER TO "postgres";

-- ----------------------------
--  Records of competitor
-- ----------------------------
BEGIN;
INSERT INTO "public"."competitor" VALUES ('4', '1', 'name1', 'name1', 'surname1', 'surname1', '1', '1966-05-19', '1', '1', '1', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('5', '2', 'name2', 'name2', 'surname2', 'surname2', '1', '1992-12-04', '1', '1', '2', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('6', '3', 'name3', 'name3', 'surname3', 'surname3', '2', '1983-03-05', '1', '1', '3', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('7', '4', 'name4', 'name4', 'surname4', 'surname4', '2', '2000-08-03', '1', '1', '4', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('8', '5', 'name5', 'name5', 'surname5', 'surname5', '1', '1960-12-05', '1', '1', '5', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('9', '6', 'name6', 'name6', 'surname6', 'surname6', '2', '1969-04-02', '1', '1', '6', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('10', '7', 'name7', 'name7', 'surname7', 'surname7', '1', '1992-03-26', '1', '1', '7', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('11', '8', 'name8', 'name8', 'surname8', 'surname8', '2', '1971-10-19', '1', '1', '8', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('12', '9', 'name9', 'name9', 'surname9', 'surname9', '2', '1966-12-20', '1', '1', '9', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('13', '10', 'name10', 'name10', 'surname10', 'surname10', '1', '1981-11-24', '1', '1', '10', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('14', '11', 'name11', 'name11', 'surname11', 'surname11', '2', '1996-12-24', '1', '1', '11', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('15', '12', 'name12', 'name12', 'surname12', 'surname12', '2', '1983-01-18', '1', '1', '12', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('16', '13', 'name13', 'name13', 'surname13', 'surname13', '1', '1987-06-24', '1', '1', '13', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('17', '14', 'name14', 'name14', 'surname14', 'surname14', '1', '1991-12-03', '1', '1', '14', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('18', '15', 'name15', 'name15', 'surname15', 'surname15', '2', '1955-09-08', '1', '1', '15', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('19', '16', 'name16', 'name16', 'surname16', 'surname16', '2', '1963-04-13', '1', '1', '16', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('20', '17', 'name17', 'name17', 'surname17', 'surname17', '2', '1968-08-10', '1', '1', '17', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('21', '18', 'name18', 'name18', 'surname18', 'surname18', '2', '1982-08-21', '1', '1', '18', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('22', '19', 'name19', 'name19', 'surname19', 'surname19', '2', '1964-03-26', '1', '1', '19', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('23', '20', 'name20', 'name20', 'surname20', 'surname20', '2', '1992-04-18', '1', '1', '20', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('24', '21', 'name21', 'name21', 'surname21', 'surname21', '1', '1965-06-23', '1', '1', '21', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('25', '22', 'name22', 'name22', 'surname22', 'surname22', '2', '1953-02-11', '1', '1', '22', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('26', '23', 'name23', 'name23', 'surname23', 'surname23', '2', '1956-09-26', '1', '1', '23', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('27', '24', 'name24', 'name24', 'surname24', 'surname24', '1', '1967-05-04', '1', '1', '24', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('28', '25', 'name25', 'name25', 'surname25', 'surname25', '1', '1985-12-02', '1', '1', '25', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('29', '26', 'name26', 'name26', 'surname26', 'surname26', '2', '1966-02-20', '1', '1', '26', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('30', '27', 'name27', 'name27', 'surname27', 'surname27', '2', '1975-07-09', '1', '1', '27', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('31', '28', 'name28', 'name28', 'surname28', 'surname28', '1', '1987-08-22', '1', '1', '28', '1', '1', '1');
INSERT INTO "public"."competitor" VALUES ('32', '29', 'name29', 'name29', 'surname29', 'surname29', '1', '1970-06-22', '1', '1', '29', '1', '1', '1');
COMMIT;

-- ----------------------------
--  Table structure for jury
-- ----------------------------
DROP TABLE IF EXISTS "public"."jury";
CREATE TABLE "public"."jury" (
	"id" int4 NOT NULL DEFAULT nextval('jury_id_seq'::regclass),
	"ru_lastname" varchar COLLATE "default",
	"ru_firstname" varchar COLLATE "default",
	"en_lastname" varchar COLLATE "default",
	"en_firstname" varchar COLLATE "default",
	"nation_id" int4,
	"phonenbr" varchar COLLATE "default",
	"email" varchar COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."jury" OWNER TO "postgres";

-- ----------------------------
--  Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS "public"."roles";
CREATE TABLE "public"."roles" (
	"id" int4 NOT NULL DEFAULT nextval('roles_id_seq'::regclass),
	"name" varchar(64) COLLATE "default",
	"default" bool,
	"permissions" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."roles" OWNER TO "postgres";

-- ----------------------------
--  Records of roles
-- ----------------------------
BEGIN;
INSERT INTO "public"."roles" VALUES ('1', 'User', 't', '7');
INSERT INTO "public"."roles" VALUES ('2', 'Moderator', 'f', '15');
INSERT INTO "public"."roles" VALUES ('3', 'Administrator', 'f', '255');
COMMIT;

-- ----------------------------
--  Table structure for nation
-- ----------------------------
DROP TABLE IF EXISTS "public"."nation";
CREATE TABLE "public"."nation" (
	"id" int4 NOT NULL DEFAULT nextval('nation_id_seq'::regclass),
	"name" varchar(3) COLLATE "default",
	"ru_description" varchar(50) COLLATE "default",
	"en_description" varchar(50) COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."nation" OWNER TO "postgres";

-- ----------------------------
--  Records of nation
-- ----------------------------
BEGIN;
INSERT INTO "public"."nation" VALUES ('1', 'Rus', 'Rus', 'Rus');
COMMIT;

-- ----------------------------
--  Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS "public"."category";
CREATE TABLE "public"."category" (
	"id" int4 NOT NULL DEFAULT nextval('category_id_seq'::regclass),
	"name" varchar(3) COLLATE "default",
	"description" varchar(150) COLLATE "default",
	"level" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."category" OWNER TO "postgres";

-- ----------------------------
--  Records of category
-- ----------------------------
BEGIN;
INSERT INTO "public"."category" VALUES ('1', 'te', 'test', '2');
COMMIT;

-- ----------------------------
--  Table structure for team
-- ----------------------------
DROP TABLE IF EXISTS "public"."team";
CREATE TABLE "public"."team" (
	"id" int4 NOT NULL DEFAULT nextval('team_id_seq'::regclass),
	"fis_code" varchar COLLATE "default",
	"en_teamname" varchar COLLATE "default",
	"ru_teamname" varchar COLLATE "default",
	"nation_id" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."team" OWNER TO "postgres";

-- ----------------------------
--  Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS "public"."course";
CREATE TABLE "public"."course" (
	"id" int4 NOT NULL DEFAULT nextval('course_id_seq'::regclass),
	"race_id" int4,
	"course_coursetter_id" int4,
	"run" int4,
	"ru_name" varchar COLLATE "default",
	"en_name" varchar COLLATE "default",
	"homologation" int4,
	"length" int4,
	"gates" int4,
	"tuminggates" int4,
	"startelev" int4,
	"finishelev" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."course" OWNER TO "postgres";

-- ----------------------------
--  Records of course
-- ----------------------------
BEGIN;
INSERT INTO "public"."course" VALUES ('1', '1', '1', '1', 'first course', 'first course', '1', '10000', '5', '12', '12', '12');
COMMIT;

-- ----------------------------
--  Table structure for race_jury
-- ----------------------------
DROP TABLE IF EXISTS "public"."race_jury";
CREATE TABLE "public"."race_jury" (
	"id" int4 NOT NULL DEFAULT nextval('race_jury_id_seq'::regclass),
	"jury_id" int4,
	"race_id" int4,
	"jury_function_id" int4,
	"phonenbr" varchar COLLATE "default",
	"email" varchar COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."race_jury" OWNER TO "postgres";

-- ----------------------------
--  Table structure for weather
-- ----------------------------
DROP TABLE IF EXISTS "public"."weather";
CREATE TABLE "public"."weather" (
	"id" int4 NOT NULL DEFAULT nextval('weather_id_seq'::regclass),
	"race_id" int4,
	"time" timestamp(6) NULL,
	"place" varchar COLLATE "default",
	"weather" varchar COLLATE "default",
	"snow" varchar COLLATE "default",
	"temperatureair" numeric,
	"temperaturesnow" numeric,
	"humiditystart" int4,
	"windspeed" numeric
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."weather" OWNER TO "postgres";

-- ----------------------------
--  Table structure for data_in
-- ----------------------------
DROP TABLE IF EXISTS "public"."data_in";
CREATE TABLE "public"."data_in" (
	"id" int4 NOT NULL DEFAULT nextval('data_in_id_seq'::regclass),
	"dt" timestamp(6) NULL,
	"race_id" int4,
	"src_sys" varchar COLLATE "default",
	"src_dev" varchar COLLATE "default",
	"bib" int4,
	"event_code" varchar COLLATE "default",
	"time" int8,
	"reserved" varchar COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."data_in" OWNER TO "postgres";

-- ----------------------------
--  Records of data_in
-- ----------------------------
BEGIN;
INSERT INTO "public"."data_in" VALUES ('4', null, null, 'sys0001', 'start0001', '1', 'x3', '1516225635161', '');
INSERT INTO "public"."data_in" VALUES ('5', null, null, 'sys0001', 'int0002', '1', 'x3', '1516225635518', '');
INSERT INTO "public"."data_in" VALUES ('6', null, null, 'sys0001', 'int0003', '1', 'x3', '1516225635995', '');
INSERT INTO "public"."data_in" VALUES ('7', null, null, 'sys0001', 'int0004', '1', 'x3', '1516225636253', '');
INSERT INTO "public"."data_in" VALUES ('8', null, null, 'sys0001', 'int0005', '1', 'x3', '1516225636511', '');
INSERT INTO "public"."data_in" VALUES ('9', null, null, 'sys0001', 'finish0006', '1', 'x3', '1516225636845', '');
INSERT INTO "public"."data_in" VALUES ('10', null, null, 'sys0001', 'start0001', '2', 'x3', '1516225637280', '');
INSERT INTO "public"."data_in" VALUES ('11', null, null, 'sys0001', 'int0002', '2', 'x3', '1516225637694', '');
INSERT INTO "public"."data_in" VALUES ('12', null, null, 'sys0001', 'int0003', '2', 'x3', '1516225638022', '');
INSERT INTO "public"."data_in" VALUES ('13', null, null, 'sys0001', 'int0004', '2', 'x3', '1516225638302', '');
INSERT INTO "public"."data_in" VALUES ('14', null, null, 'sys0001', 'int0005', '2', 'x3', '1516225638677', '');
INSERT INTO "public"."data_in" VALUES ('15', null, null, 'sys0001', 'finish0006', '2', 'x3', '1516225639152', '');
INSERT INTO "public"."data_in" VALUES ('16', null, null, 'sys0001', 'start0001', '4', 'x3', '1516225639524', '');
INSERT INTO "public"."data_in" VALUES ('17', null, null, 'sys0001', 'int0002', '4', 'x3', '1516225639808', '');
INSERT INTO "public"."data_in" VALUES ('18', null, null, 'sys0001', 'int0003', '4', 'x3', '1516225640235', '');
INSERT INTO "public"."data_in" VALUES ('19', null, null, 'sys0001', 'int0004', '4', 'x3', '1516225640498', '');
INSERT INTO "public"."data_in" VALUES ('20', null, null, 'sys0001', 'int0005', '4', 'x3', '1516225640874', '');
INSERT INTO "public"."data_in" VALUES ('21', null, null, 'sys0001', 'finish0006', '4', 'x3', '1516225641206', '');
INSERT INTO "public"."data_in" VALUES ('22', null, null, 'sys0001', 'start0001', '6', 'x3', '1516225642446', '');
INSERT INTO "public"."data_in" VALUES ('23', null, null, 'sys0001', 'int0002', '6', 'x3', '1516225643121', '');
INSERT INTO "public"."data_in" VALUES ('24', null, null, 'sys0001', 'int0003', '6', 'x3', '1516225645483', '');
INSERT INTO "public"."data_in" VALUES ('25', null, null, 'sys0001', 'int0004', '6', 'x3', '1516225649582', '');
INSERT INTO "public"."data_in" VALUES ('26', null, null, 'sys0001', 'int0005', '6', 'x3', '1516225650555', '');
INSERT INTO "public"."data_in" VALUES ('27', null, null, 'sys0001', 'finish0006', '6', 'x3', '1516225658584', '');
INSERT INTO "public"."data_in" VALUES ('28', null, null, 'sys0001', 'start0001', '8', 'x3', '1516225661001', '');
INSERT INTO "public"."data_in" VALUES ('29', null, null, 'sys0001', 'int0002', '8', 'x3', '1516225668663', '');
INSERT INTO "public"."data_in" VALUES ('30', null, null, 'sys0001', 'int0003', '8', 'x3', '1516225669036', '');
INSERT INTO "public"."data_in" VALUES ('31', null, null, 'sys0001', 'int0004', '8', 'x3', '1516225669412', '');
INSERT INTO "public"."data_in" VALUES ('32', null, null, 'sys0001', 'int0005', '8', 'x3', '1516225669843', '');
INSERT INTO "public"."data_in" VALUES ('33', null, null, 'sys0001', 'finish0006', '8', 'x3', '1516225670197', '');
INSERT INTO "public"."data_in" VALUES ('34', null, null, 'sys0001', 'start0001', '10', 'x3', '1516225670515', '');
INSERT INTO "public"."data_in" VALUES ('35', null, null, 'sys0001', 'int0002', '10', 'x3', '1516225670868', '');
INSERT INTO "public"."data_in" VALUES ('36', null, null, 'sys0001', 'int0003', '10', 'x3', '1516225671190', '');
INSERT INTO "public"."data_in" VALUES ('37', null, null, 'sys0001', 'int0004', '10', 'x3', '1516225672445', '');
INSERT INTO "public"."data_in" VALUES ('38', null, null, 'sys0001', 'int0005', '10', 'x3', '1516225673231', '');
INSERT INTO "public"."data_in" VALUES ('39', null, null, 'sys0001', 'finish0006', '10', 'x3', '1516225673981', '');
INSERT INTO "public"."data_in" VALUES ('40', null, null, 'sys0001', 'start0001', '1', 'x3', '1516226147159', '');
COMMIT;

-- ----------------------------
--  Table structure for race_competitor
-- ----------------------------
DROP TABLE IF EXISTS "public"."race_competitor";
CREATE TABLE "public"."race_competitor" (
	"id" int4 NOT NULL DEFAULT nextval('race_competitor_id_seq'::regclass),
	"competitor_id" int4,
	"race_id" int4,
	"age_class" varchar COLLATE "default",
	"chip" varchar COLLATE "default",
	"bib" int4,
	"classified" bool,
	"rank" int4,
	"status_id" int4,
	"order" int4,
	"run_id" int4,
	"gate" varchar COLLATE "default",
	"reason" varchar COLLATE "default",
	"team_id" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."race_competitor" OWNER TO "postgres";

-- ----------------------------
--  Records of race_competitor
-- ----------------------------
BEGIN;
INSERT INTO "public"."race_competitor" VALUES ('1', '4', '1', '1', '1', '1', null, null, null, null, '1', null, null, null);
INSERT INTO "public"."race_competitor" VALUES ('2', '5', '1', '1', '2', '2', null, null, null, null, '1', null, null, null);
INSERT INTO "public"."race_competitor" VALUES ('3', '10', '1', '1', '4', '4', null, null, null, null, '1', null, null, null);
INSERT INTO "public"."race_competitor" VALUES ('4', '13', '1', '1', '6', '6', null, null, null, null, '1', null, null, null);
INSERT INTO "public"."race_competitor" VALUES ('5', '22', '1', '1', '8', '8', null, null, null, null, '1', null, null, null);
INSERT INTO "public"."race_competitor" VALUES ('6', '29', '1', '1', '10', '10', null, null, null, null, '1', null, null, null);
COMMIT;

-- ----------------------------
--  Table structure for course_forerunner
-- ----------------------------
DROP TABLE IF EXISTS "public"."course_forerunner";
CREATE TABLE "public"."course_forerunner" (
	"id" int4 NOT NULL DEFAULT nextval('course_forerunner_id_seq'::regclass),
	"order" int4,
	"forerunner_id" int4,
	"course_id" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."course_forerunner" OWNER TO "postgres";

-- ----------------------------
--  Records of course_forerunner
-- ----------------------------
BEGIN;
INSERT INTO "public"."course_forerunner" VALUES ('1', '1', '1', '1');
COMMIT;

-- ----------------------------
--  Table structure for run_order
-- ----------------------------
DROP TABLE IF EXISTS "public"."run_order";
CREATE TABLE "public"."run_order" (
	"id" int4 NOT NULL DEFAULT nextval('run_order_id_seq'::regclass),
	"run_id" int4,
	"race_competitor_id" int4,
	"order" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."run_order" OWNER TO "postgres";

-- ----------------------------
--  Table structure for race_team
-- ----------------------------
DROP TABLE IF EXISTS "public"."race_team";
CREATE TABLE "public"."race_team" (
	"id" int4 NOT NULL DEFAULT nextval('race_team_id_seq'::regclass),
	"race_id" int4,
	"team_id" int4,
	"run_id" int4,
	"bib" int4,
	"classified" bool,
	"en_teamname" varchar COLLATE "default",
	"ru_teamname" varchar COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."race_team" OWNER TO "postgres";

-- ----------------------------
--  Table structure for result
-- ----------------------------
DROP TABLE IF EXISTS "public"."result";
CREATE TABLE "public"."result" (
	"id" int4 NOT NULL DEFAULT nextval('result_id_seq'::regclass),
	"race_competitor_id" int4,
	"status_id" int4,
	"approve_time" timestamp(6) NULL,
	"timerun1" int8,
	"timerun2" int8,
	"timerun3" int8,
	"diff" int8,
	"racepoints" int8,
	"level" int4,
	"approve_user" int4,
	"is_manuale" bool
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."result" OWNER TO "postgres";

-- ----------------------------
--  Table structure for device
-- ----------------------------
DROP TABLE IF EXISTS "public"."device";
CREATE TABLE "public"."device" (
	"id" int4 NOT NULL DEFAULT nextval('device_id_seq'::regclass),
	"src_dev" varchar COLLATE "default",
	"name" varchar COLLATE "default",
	"type_id" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."device" OWNER TO "postgres";

-- ----------------------------
--  Records of device
-- ----------------------------
BEGIN;
INSERT INTO "public"."device" VALUES ('1', 'start0001', 'start0001', '1');
INSERT INTO "public"."device" VALUES ('2', 'int0002', 'int0002', '1');
INSERT INTO "public"."device" VALUES ('3', 'int0003', 'int0003', '1');
INSERT INTO "public"."device" VALUES ('4', 'int0004', 'int0004', '1');
INSERT INTO "public"."device" VALUES ('5', 'int0005', 'int0005', '1');
INSERT INTO "public"."device" VALUES ('6', 'finish0006', 'finish0006', '1');
COMMIT;

-- ----------------------------
--  Table structure for course_device_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."course_device_type";
CREATE TABLE "public"."course_device_type" (
	"id" int4 NOT NULL DEFAULT nextval('course_device_type_id_seq'::regclass),
	"name" varchar COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."course_device_type" OWNER TO "postgres";

-- ----------------------------
--  Records of course_device_type
-- ----------------------------
BEGIN;
INSERT INTO "public"."course_device_type" VALUES ('1', 'Start');
INSERT INTO "public"."course_device_type" VALUES ('2', 'Finish');
INSERT INTO "public"."course_device_type" VALUES ('3', 'Point');
COMMIT;

-- ----------------------------
--  Table structure for result_detail
-- ----------------------------
DROP TABLE IF EXISTS "public"."result_detail";
CREATE TABLE "public"."result_detail" (
	"id" int4 NOT NULL DEFAULT nextval('result_detail_id_seq'::regclass),
	"course_device_id" int4,
	"race_competitor_id" int4,
	"run_id" int4,
	"diff" int8,
	"time" int8,
	"rank" int4,
	"speed" float8,
	"sectortime" int8,
	"sectordiff" int8,
	"sectorrank" int4,
	"absolut_time" int8,
	"is_start" bool
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."result_detail" OWNER TO "postgres";

-- ----------------------------
--  Records of result_detail
-- ----------------------------
BEGIN;
INSERT INTO "public"."result_detail" VALUES ('4', '1', '1', '1', null, '0', null, null, '0', '0', '1', '1516225635161', 't');
INSERT INTO "public"."result_detail" VALUES ('5', '2', '1', '1', '0', '357', '1', '0.280112044817927', '357', '0', null, '1516225635518', null);
INSERT INTO "public"."result_detail" VALUES ('6', '3', '1', '1', '0', '834', '1', '1.88679245283019', '477', '0', null, '1516225635995', null);
INSERT INTO "public"."result_detail" VALUES ('7', '4', '1', '1', '0', '1092', '1', '7.75193798449612', '258', '0', null, '1516225636253', null);
INSERT INTO "public"."result_detail" VALUES ('8', '5', '1', '1', '0', '1350', '1', '7.75193798449612', '258', '0', null, '1516225636511', null);
INSERT INTO "public"."result_detail" VALUES ('9', '6', '1', '1', '0', '1684', '1', '14.9700598802395', '334', '0', null, '1516225636845', null);
INSERT INTO "public"."result_detail" VALUES ('10', '1', '2', '1', null, '0', null, null, '0', '0', '1', '1516225637280', 't');
INSERT INTO "public"."result_detail" VALUES ('11', '2', '2', '1', '57', '414', null, '0.241545893719807', '414', '57', null, '1516225637694', null);
INSERT INTO "public"."result_detail" VALUES ('12', '3', '2', '1', '-92', '742', null, '2.74390243902439', '328', '-149', null, '1516225638022', null);
INSERT INTO "public"."result_detail" VALUES ('13', '4', '2', '1', '-70', '1022', null, '7.14285714285714', '280', '22', null, '1516225638302', null);
INSERT INTO "public"."result_detail" VALUES ('14', '5', '2', '1', '47', '1397', null, '5.33333333333333', '375', '117', null, '1516225638677', null);
INSERT INTO "public"."result_detail" VALUES ('15', '6', '2', '1', '188', '1872', null, '10.5263157894737', '475', '141', null, '1516225639152', null);
INSERT INTO "public"."result_detail" VALUES ('16', '1', '3', '1', null, '0', null, null, '0', '0', '1', '1516225639524', 't');
INSERT INTO "public"."result_detail" VALUES ('17', '2', '3', '1', '-73', '284', null, '0.352112676056338', '284', '-73', null, '1516225639808', null);
INSERT INTO "public"."result_detail" VALUES ('18', '3', '3', '1', '-31', '711', null, '2.10772833723653', '427', '99', null, '1516225640235', null);
INSERT INTO "public"."result_detail" VALUES ('19', '4', '3', '1', '-48', '974', null, '7.60456273764259', '263', '5', null, '1516225640498', null);
INSERT INTO "public"."result_detail" VALUES ('20', '5', '3', '1', '0', '1350', null, '5.31914893617021', '376', '118', null, '1516225640874', null);
INSERT INTO "public"."result_detail" VALUES ('21', '6', '3', '1', '-2', '1682', null, '15.0602409638554', '332', '-2', null, '1516225641206', null);
INSERT INTO "public"."result_detail" VALUES ('22', '1', '4', '1', null, '0', null, null, '0', '0', '1', '1516225642446', 't');
INSERT INTO "public"."result_detail" VALUES ('23', '2', '4', '1', '391', '675', null, '0.148148148148148', '675', '391', null, '1516225643121', null);
INSERT INTO "public"."result_detail" VALUES ('24', '3', '4', '1', '2326', '3037', null, '0.381033022861981', '2362', '2034', null, '1516225645483', null);
INSERT INTO "public"."result_detail" VALUES ('25', '4', '4', '1', '6162', '7136', null, '0.487923883874116', '4099', '3841', null, '1516225649582', null);
INSERT INTO "public"."result_detail" VALUES ('26', '5', '4', '1', '6759', '8109', null, '2.05549845837616', '973', '715', null, '1516225650555', null);
INSERT INTO "public"."result_detail" VALUES ('27', '6', '4', '1', '14456', '16138', null, '0.622742558226429', '8029', '7697', null, '1516225658584', null);
INSERT INTO "public"."result_detail" VALUES ('28', '1', '5', '1', null, '0', null, null, '0', '0', '1', '1516225661001', 't');
INSERT INTO "public"."result_detail" VALUES ('29', '2', '5', '1', '7378', '7662', null, '0.013051422605064', '7662', '7378', null, '1516225668663', null);
INSERT INTO "public"."result_detail" VALUES ('30', '3', '5', '1', '7324', '8035', null, '2.41286863270777', '373', '45', null, '1516225669036', null);
INSERT INTO "public"."result_detail" VALUES ('31', '4', '5', '1', '7437', '8411', null, '5.31914893617021', '376', '118', null, '1516225669412', null);
INSERT INTO "public"."result_detail" VALUES ('32', '5', '5', '1', '7492', '8842', null, '4.64037122969838', '431', '173', null, '1516225669843', null);
INSERT INTO "public"."result_detail" VALUES ('33', '6', '5', '1', '7514', '9196', null, '14.1242937853107', '354', '22', null, '1516225670197', null);
INSERT INTO "public"."result_detail" VALUES ('34', '1', '6', '1', null, '0', null, null, '0', '0', '1', '1516225670515', 't');
INSERT INTO "public"."result_detail" VALUES ('35', '2', '6', '1', '69', '353', null, '0.28328611898017', '353', '69', null, '1516225670868', null);
INSERT INTO "public"."result_detail" VALUES ('36', '3', '6', '1', '-36', '675', null, '2.79503105590062', '322', '-6', null, '1516225671190', null);
INSERT INTO "public"."result_detail" VALUES ('37', '4', '6', '1', '956', '1930', null, '1.59362549800797', '1255', '997', null, '1516225672445', null);
INSERT INTO "public"."result_detail" VALUES ('38', '5', '6', '1', '1366', '2716', null, '2.54452926208651', '786', '528', null, '1516225673231', null);
INSERT INTO "public"."result_detail" VALUES ('39', '6', '6', '1', '1784', '3466', null, '6.66666666666667', '750', '418', null, '1516225673981', null);
INSERT INTO "public"."result_detail" VALUES ('40', '1', '1', '1', null, '0', null, null, '0', '0', '1', '1516226147159', 't');
COMMIT;

-- ----------------------------
--  Table structure for course_device
-- ----------------------------
DROP TABLE IF EXISTS "public"."course_device";
CREATE TABLE "public"."course_device" (
	"id" int4 NOT NULL DEFAULT nextval('course_device_id_seq'::regclass),
	"course_id" int4,
	"order" int4,
	"distance" int4,
	"device_id" int4,
	"course_device_type_id" int4
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."course_device" OWNER TO "postgres";

-- ----------------------------
--  Records of course_device
-- ----------------------------
BEGIN;
INSERT INTO "public"."course_device" VALUES ('1', '1', '1', '0', '1', '1');
INSERT INTO "public"."course_device" VALUES ('2', '1', '2', '100', '2', '3');
INSERT INTO "public"."course_device" VALUES ('3', '1', '3', '1000', '3', '3');
INSERT INTO "public"."course_device" VALUES ('4', '1', '4', '3000', '4', '3');
INSERT INTO "public"."course_device" VALUES ('5', '1', '5', '5000', '5', '3');
INSERT INTO "public"."course_device" VALUES ('6', '1', '6', '10000', '6', '2');
COMMIT;

-- ----------------------------
--  Table structure for run_info
-- ----------------------------
DROP TABLE IF EXISTS "public"."run_info";
CREATE TABLE "public"."run_info" (
	"id" int4 NOT NULL DEFAULT nextval('run_info_id_seq'::regclass),
	"race_id" int4,
	"course_id" int4,
	"number" int4,
	"starttime" timestamp(6) NULL,
	"endtime" timestamp(6) NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."run_info" OWNER TO "postgres";

-- ----------------------------
--  Records of run_info
-- ----------------------------
BEGIN;
INSERT INTO "public"."run_info" VALUES ('1', '1', '1', '1', '2018-01-18 04:39:36.181953', null);
INSERT INTO "public"."run_info" VALUES ('2', '1', '1', '2', '2018-01-18 08:39:36.182027', null);
INSERT INTO "public"."run_info" VALUES ('3', '1', '1', '3', '2018-01-18 11:39:36.182062', null);
COMMIT;

-- ----------------------------
--  Table structure for race
-- ----------------------------
DROP TABLE IF EXISTS "public"."race";
CREATE TABLE "public"."race" (
	"id" int4 NOT NULL DEFAULT nextval('race_id_seq'::regclass),
	"sector" varchar(2) COLLATE "default",
	"gender_id" int4,
	"season" int4,
	"codex" int4,
	"nation_id" int4,
	"discipline_id" int4,
	"category_id" int4,
	"type_of_content" varchar COLLATE "default",
	"training" varchar COLLATE "default",
	"speedcodex" int4,
	"eventname" varchar COLLATE "default",
	"td_delegate_tdnumber" varchar COLLATE "default",
	"td_delegate_ru_firstname" varchar COLLATE "default",
	"td_delegate_en_firstname" varchar COLLATE "default",
	"td_delegate_ru_lastname" varchar COLLATE "default",
	"td_delegate_en_lastname" varchar COLLATE "default",
	"td_delegate_nation_id" int4,
	"td_assistant_tdnumber" varchar COLLATE "default",
	"td_assistant_ru_firstname" varchar COLLATE "default",
	"td_assistant_en_firstname" varchar COLLATE "default",
	"td_assistant_ru_lastname" varchar COLLATE "default",
	"td_assistant_en_lastname" varchar COLLATE "default",
	"td_assistant_nation_id" int4,
	"place" varchar COLLATE "default",
	"racedate" date,
	"tempunit" varchar(1) COLLATE "default",
	"longunit" varchar(2) COLLATE "default",
	"speedunit" varchar(3) COLLATE "default",
	"windunit" varchar(3) COLLATE "default",
	"usedfislist" varchar COLLATE "default",
	"appliedpenalty" varchar COLLATE "default",
	"calculatedpenalty" int4,
	"fvalue" int4,
	"timingby" varchar COLLATE "default",
	"dataprocessingby" varchar COLLATE "default",
	"softwarecompany" varchar COLLATE "default",
	"softwarename" varchar COLLATE "default",
	"softwareversion" varchar COLLATE "default",
	"isTeam" bool
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."race" OWNER TO "postgres";

-- ----------------------------
--  Records of race
-- ----------------------------
BEGIN;
INSERT INTO "public"."race" VALUES ('1', '1', '1', '1', '1', '1', '1', '1', null, '1', '1', 'Test event individual competition', null, null, null, null, null, null, null, null, null, null, null, null, '12', '2018-01-18', null, null, null, null, null, null, null, null, null, null, null, null, null, 'f');
COMMIT;


-- ----------------------------
--  Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."category_id_seq" RESTART 2 OWNED BY "category"."id";
ALTER SEQUENCE "public"."competitor_id_seq" RESTART 33 OWNED BY "competitor"."id";
ALTER SEQUENCE "public"."course_device_id_seq" RESTART 7 OWNED BY "course_device"."id";
ALTER SEQUENCE "public"."course_device_type_id_seq" RESTART 4 OWNED BY "course_device_type"."id";
ALTER SEQUENCE "public"."course_forerunner_id_seq" RESTART 2 OWNED BY "course_forerunner"."id";
ALTER SEQUENCE "public"."course_id_seq" RESTART 2 OWNED BY "course"."id";
ALTER SEQUENCE "public"."coursetter_id_seq" RESTART 9 OWNED BY "coursetter"."id";
ALTER SEQUENCE "public"."data_in_id_seq" RESTART 41 OWNED BY "data_in"."id";
ALTER SEQUENCE "public"."device_id_seq" RESTART 7 OWNED BY "device"."id";
ALTER SEQUENCE "public"."device_type_id_seq" RESTART 2 OWNED BY "device_type"."id";
ALTER SEQUENCE "public"."discipline_id_seq" RESTART 15 OWNED BY "discipline"."id";
ALTER SEQUENCE "public"."forerunner_id_seq" RESTART 9 OWNED BY "forerunner"."id";
ALTER SEQUENCE "public"."gender_id_seq" RESTART 3 OWNED BY "gender"."id";
ALTER SEQUENCE "public"."jury_function_id_seq" RESTART 8 OWNED BY "jury_function"."id";
ALTER SEQUENCE "public"."jury_id_seq" RESTART 2 OWNED BY "jury"."id";
ALTER SEQUENCE "public"."mark_id_seq" RESTART 2 OWNED BY "mark"."id";
ALTER SEQUENCE "public"."nation_id_seq" RESTART 2 OWNED BY "nation"."id";
ALTER SEQUENCE "public"."race_competitor_id_seq" RESTART 7 OWNED BY "race_competitor"."id";
ALTER SEQUENCE "public"."race_id_seq" RESTART 2 OWNED BY "race"."id";
ALTER SEQUENCE "public"."race_jury_id_seq" RESTART 2 OWNED BY "race_jury"."id";
ALTER SEQUENCE "public"."race_team_id_seq" RESTART 2 OWNED BY "race_team"."id";
ALTER SEQUENCE "public"."report_type_id_seq" RESTART 2 OWNED BY "report_type"."id";
ALTER SEQUENCE "public"."result_detail_id_seq" RESTART 41 OWNED BY "result_detail"."id";
ALTER SEQUENCE "public"."result_id_seq" RESTART 2 OWNED BY "result"."id";
ALTER SEQUENCE "public"."roles_id_seq" RESTART 4 OWNED BY "roles"."id";
ALTER SEQUENCE "public"."run_info_id_seq" RESTART 7 OWNED BY "run_info"."id";
ALTER SEQUENCE "public"."run_order_id_seq" RESTART 2 OWNED BY "run_order"."id";
ALTER SEQUENCE "public"."status_id_seq" RESTART 17 OWNED BY "status"."id";
ALTER SEQUENCE "public"."td_id_seq" RESTART 2 OWNED BY "td"."id";
ALTER SEQUENCE "public"."tdrole_id_seq" RESTART 2 OWNED BY "tdrole"."id";
ALTER SEQUENCE "public"."team_id_seq" RESTART 2 OWNED BY "team"."id";
ALTER SEQUENCE "public"."users_id_seq" RESTART 2 OWNED BY "users"."id";
ALTER SEQUENCE "public"."weather_id_seq" RESTART 2 OWNED BY "weather"."id";
-- ----------------------------
--  Primary key structure for table device_type
-- ----------------------------
ALTER TABLE "public"."device_type" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table gender
-- ----------------------------
ALTER TABLE "public"."gender" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table report_type
-- ----------------------------
ALTER TABLE "public"."report_type" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table mark
-- ----------------------------
ALTER TABLE "public"."mark" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table jury_function
-- ----------------------------
ALTER TABLE "public"."jury_function" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table status
-- ----------------------------
ALTER TABLE "public"."status" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table discipline
-- ----------------------------
ALTER TABLE "public"."discipline" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table tdrole
-- ----------------------------
ALTER TABLE "public"."tdrole" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table td
-- ----------------------------
ALTER TABLE "public"."td" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Indexes structure for table users
-- ----------------------------
CREATE UNIQUE INDEX  "ix_users_email" ON "public"."users" USING btree(email COLLATE "default" "pg_catalog"."text_ops" ASC NULLS LAST);
CREATE UNIQUE INDEX  "ix_users_username" ON "public"."users" USING btree(username COLLATE "default" "pg_catalog"."text_ops" ASC NULLS LAST);

-- ----------------------------
--  Primary key structure for table forerunner
-- ----------------------------
ALTER TABLE "public"."forerunner" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table coursetter
-- ----------------------------
ALTER TABLE "public"."coursetter" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table competitor
-- ----------------------------
ALTER TABLE "public"."competitor" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table jury
-- ----------------------------
ALTER TABLE "public"."jury" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table roles
-- ----------------------------
ALTER TABLE "public"."roles" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Uniques structure for table roles
-- ----------------------------
ALTER TABLE "public"."roles" ADD CONSTRAINT "roles_name_key" UNIQUE ("name") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Indexes structure for table roles
-- ----------------------------
CREATE INDEX  "ix_roles_default" ON "public"."roles" USING btree("default" "pg_catalog"."bool_ops" ASC NULLS LAST);

-- ----------------------------
--  Primary key structure for table nation
-- ----------------------------
ALTER TABLE "public"."nation" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table category
-- ----------------------------
ALTER TABLE "public"."category" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table team
-- ----------------------------
ALTER TABLE "public"."team" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table course
-- ----------------------------
ALTER TABLE "public"."course" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table race_jury
-- ----------------------------
ALTER TABLE "public"."race_jury" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table weather
-- ----------------------------
ALTER TABLE "public"."weather" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table data_in
-- ----------------------------
ALTER TABLE "public"."data_in" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table race_competitor
-- ----------------------------
ALTER TABLE "public"."race_competitor" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table course_forerunner
-- ----------------------------
ALTER TABLE "public"."course_forerunner" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table run_order
-- ----------------------------
ALTER TABLE "public"."run_order" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table race_team
-- ----------------------------
ALTER TABLE "public"."race_team" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table result
-- ----------------------------
ALTER TABLE "public"."result" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table device
-- ----------------------------
ALTER TABLE "public"."device" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table course_device_type
-- ----------------------------
ALTER TABLE "public"."course_device_type" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table result_detail
-- ----------------------------
ALTER TABLE "public"."result_detail" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table course_device
-- ----------------------------
ALTER TABLE "public"."course_device" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table run_info
-- ----------------------------
ALTER TABLE "public"."run_info" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table race
-- ----------------------------
ALTER TABLE "public"."race" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table td
-- ----------------------------
ALTER TABLE "public"."td" ADD CONSTRAINT "td_tdrole_id_fkey" FOREIGN KEY ("tdrole_id") REFERENCES "public"."tdrole" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_role_id_fkey" FOREIGN KEY ("role_id") REFERENCES "public"."roles" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table forerunner
-- ----------------------------
ALTER TABLE "public"."forerunner" ADD CONSTRAINT "forerunner_nation_id_fkey" FOREIGN KEY ("nation_id") REFERENCES "public"."nation" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table coursetter
-- ----------------------------
ALTER TABLE "public"."coursetter" ADD CONSTRAINT "coursetter_nation_id_fkey" FOREIGN KEY ("nation_id") REFERENCES "public"."nation" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table competitor
-- ----------------------------
ALTER TABLE "public"."competitor" ADD CONSTRAINT "competitor_gender_id_fkey" FOREIGN KEY ("gender_id") REFERENCES "public"."gender" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."competitor" ADD CONSTRAINT "competitor_nation_code_id_fkey" FOREIGN KEY ("nation_code_id") REFERENCES "public"."nation" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."competitor" ADD CONSTRAINT "competitor_category_id_fkey" FOREIGN KEY ("category_id") REFERENCES "public"."category" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table jury
-- ----------------------------
ALTER TABLE "public"."jury" ADD CONSTRAINT "jury_nation_id_fkey" FOREIGN KEY ("nation_id") REFERENCES "public"."nation" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table team
-- ----------------------------
ALTER TABLE "public"."team" ADD CONSTRAINT "team_nation_id_fkey" FOREIGN KEY ("nation_id") REFERENCES "public"."nation" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table course
-- ----------------------------
ALTER TABLE "public"."course" ADD CONSTRAINT "course_race_id_fkey" FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."course" ADD CONSTRAINT "course_course_coursetter_id_fkey" FOREIGN KEY ("course_coursetter_id") REFERENCES "public"."coursetter" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table race_jury
-- ----------------------------
ALTER TABLE "public"."race_jury" ADD CONSTRAINT "race_jury_jury_id_fkey" FOREIGN KEY ("jury_id") REFERENCES "public"."jury" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race_jury" ADD CONSTRAINT "race_jury_race_id_fkey" FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race_jury" ADD CONSTRAINT "race_jury_jury_function_id_fkey" FOREIGN KEY ("jury_function_id") REFERENCES "public"."jury_function" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table weather
-- ----------------------------
ALTER TABLE "public"."weather" ADD CONSTRAINT "weather_race_id_fkey" FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table data_in
-- ----------------------------
ALTER TABLE "public"."data_in" ADD CONSTRAINT "data_in_race_id_fkey" FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table race_competitor
-- ----------------------------
ALTER TABLE "public"."race_competitor" ADD CONSTRAINT "race_competitor_competitor_id_fkey" FOREIGN KEY ("competitor_id") REFERENCES "public"."competitor" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race_competitor" ADD CONSTRAINT "race_competitor_race_id_fkey" FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race_competitor" ADD CONSTRAINT "race_competitor_status_id_fkey" FOREIGN KEY ("status_id") REFERENCES "public"."status" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race_competitor" ADD CONSTRAINT "race_competitor_run_id_fkey" FOREIGN KEY ("run_id") REFERENCES "public"."run_info" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race_competitor" ADD CONSTRAINT "race_competitor_team_id_fkey" FOREIGN KEY ("team_id") REFERENCES "public"."team" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table course_forerunner
-- ----------------------------
ALTER TABLE "public"."course_forerunner" ADD CONSTRAINT "course_forerunner_forerunner_id_fkey" FOREIGN KEY ("forerunner_id") REFERENCES "public"."forerunner" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."course_forerunner" ADD CONSTRAINT "course_forerunner_course_id_fkey" FOREIGN KEY ("course_id") REFERENCES "public"."course" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table run_order
-- ----------------------------
ALTER TABLE "public"."run_order" ADD CONSTRAINT "run_order_run_id_fkey" FOREIGN KEY ("run_id") REFERENCES "public"."run_info" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."run_order" ADD CONSTRAINT "run_order_race_competitor_id_fkey" FOREIGN KEY ("race_competitor_id") REFERENCES "public"."race_competitor" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table race_team
-- ----------------------------
ALTER TABLE "public"."race_team" ADD CONSTRAINT "race_team_race_id_fkey" FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race_team" ADD CONSTRAINT "race_team_team_id_fkey" FOREIGN KEY ("team_id") REFERENCES "public"."team" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race_team" ADD CONSTRAINT "race_team_run_id_fkey" FOREIGN KEY ("run_id") REFERENCES "public"."run_info" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table result
-- ----------------------------
ALTER TABLE "public"."result" ADD CONSTRAINT "result_race_competitor_id_fkey" FOREIGN KEY ("race_competitor_id") REFERENCES "public"."race_competitor" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."result" ADD CONSTRAINT "result_status_id_fkey" FOREIGN KEY ("status_id") REFERENCES "public"."status" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."result" ADD CONSTRAINT "result_approve_user_fkey" FOREIGN KEY ("approve_user") REFERENCES "public"."users" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table device
-- ----------------------------
ALTER TABLE "public"."device" ADD CONSTRAINT "device_type_id_fkey" FOREIGN KEY ("type_id") REFERENCES "public"."device_type" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table result_detail
-- ----------------------------
ALTER TABLE "public"."result_detail" ADD CONSTRAINT "result_detail_course_device_id_fkey" FOREIGN KEY ("course_device_id") REFERENCES "public"."course_device" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."result_detail" ADD CONSTRAINT "result_detail_race_competitor_id_fkey" FOREIGN KEY ("race_competitor_id") REFERENCES "public"."race_competitor" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."result_detail" ADD CONSTRAINT "result_detail_run_id_fkey" FOREIGN KEY ("run_id") REFERENCES "public"."run_info" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table course_device
-- ----------------------------
ALTER TABLE "public"."course_device" ADD CONSTRAINT "course_device_course_id_fkey" FOREIGN KEY ("course_id") REFERENCES "public"."course" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."course_device" ADD CONSTRAINT "course_device_device_id_fkey" FOREIGN KEY ("device_id") REFERENCES "public"."device" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."course_device" ADD CONSTRAINT "course_device_course_device_type_id_fkey" FOREIGN KEY ("course_device_type_id") REFERENCES "public"."course_device_type" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table run_info
-- ----------------------------
ALTER TABLE "public"."run_info" ADD CONSTRAINT "run_info_race_id_fkey" FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."run_info" ADD CONSTRAINT "run_info_course_id_fkey" FOREIGN KEY ("course_id") REFERENCES "public"."course" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table race
-- ----------------------------
ALTER TABLE "public"."race" ADD CONSTRAINT "race_gender_id_fkey" FOREIGN KEY ("gender_id") REFERENCES "public"."gender" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race" ADD CONSTRAINT "race_nation_id_fkey" FOREIGN KEY ("nation_id") REFERENCES "public"."nation" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race" ADD CONSTRAINT "race_discipline_id_fkey" FOREIGN KEY ("discipline_id") REFERENCES "public"."discipline" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race" ADD CONSTRAINT "race_category_id_fkey" FOREIGN KEY ("category_id") REFERENCES "public"."category" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race" ADD CONSTRAINT "race_td_delegate_nation_id_fkey" FOREIGN KEY ("td_delegate_nation_id") REFERENCES "public"."nation" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."race" ADD CONSTRAINT "race_td_assistant_nation_id_fkey" FOREIGN KEY ("td_assistant_nation_id") REFERENCES "public"."nation" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;

