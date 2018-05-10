/*
Navicat PGSQL Data Transfer

Source Server         : ski-local
Source Server Version : 90603
Source Host           : localhost:5432
Source Database       : sport
Source Schema         : public

Target Server Type    : PGSQL
Target Server Version : 90603
File Encoding         : 65001

Date: 2018-04-06 04:09:49
*/


-- ----------------------------
-- Sequence structure for CASHE_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."CASHE_id_seq";
CREATE SEQUENCE "public"."CASHE_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 5
 CACHE 1;
SELECT setval('"public"."CASHE_id_seq"', 5, true);

-- ----------------------------
-- Sequence structure for category_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."category_id_seq";
CREATE SEQUENCE "public"."category_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for competitor_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."competitor_id_seq";
CREATE SEQUENCE "public"."competitor_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 33
 CACHE 1;

-- ----------------------------
-- Sequence structure for course_device_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."course_device_id_seq";
CREATE SEQUENCE "public"."course_device_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 7
 CACHE 1;

-- ----------------------------
-- Sequence structure for course_device_type_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."course_device_type_id_seq";
CREATE SEQUENCE "public"."course_device_type_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 4
 CACHE 1;

-- ----------------------------
-- Sequence structure for course_forerunner_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."course_forerunner_id_seq";
CREATE SEQUENCE "public"."course_forerunner_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for course_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."course_id_seq";
CREATE SEQUENCE "public"."course_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for coursetter_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."coursetter_id_seq";
CREATE SEQUENCE "public"."coursetter_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 9
 CACHE 1;

-- ----------------------------
-- Sequence structure for data_in_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."data_in_id_seq";
CREATE SEQUENCE "public"."data_in_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 5205
 CACHE 1;
SELECT setval('"public"."data_in_id_seq"', 5205, true);

-- ----------------------------
-- Sequence structure for device_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."device_id_seq";
CREATE SEQUENCE "public"."device_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 7
 CACHE 1;

-- ----------------------------
-- Sequence structure for device_type_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."device_type_id_seq";
CREATE SEQUENCE "public"."device_type_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for discipline_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."discipline_id_seq";
CREATE SEQUENCE "public"."discipline_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 15
 CACHE 1;

-- ----------------------------
-- Sequence structure for forerunner_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."forerunner_id_seq";
CREATE SEQUENCE "public"."forerunner_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 9
 CACHE 1;

-- ----------------------------
-- Sequence structure for gender_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."gender_id_seq";
CREATE SEQUENCE "public"."gender_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 3
 CACHE 1;

-- ----------------------------
-- Sequence structure for jury_function_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."jury_function_id_seq";
CREATE SEQUENCE "public"."jury_function_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 8
 CACHE 1;

-- ----------------------------
-- Sequence structure for jury_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."jury_id_seq";
CREATE SEQUENCE "public"."jury_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for mark_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."mark_id_seq";
CREATE SEQUENCE "public"."mark_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for nation_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."nation_id_seq";
CREATE SEQUENCE "public"."nation_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for race_competitor_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."race_competitor_id_seq";
CREATE SEQUENCE "public"."race_competitor_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 7
 CACHE 1;

-- ----------------------------
-- Sequence structure for race_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."race_id_seq";
CREATE SEQUENCE "public"."race_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for race_jury_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."race_jury_id_seq";
CREATE SEQUENCE "public"."race_jury_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for race_team_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."race_team_id_seq";
CREATE SEQUENCE "public"."race_team_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for report_type_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."report_type_id_seq";
CREATE SEQUENCE "public"."report_type_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for result_approved_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."result_approved_id_seq";
CREATE SEQUENCE "public"."result_approved_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 116
 CACHE 1;
SELECT setval('"public"."result_approved_id_seq"', 116, true);

-- ----------------------------
-- Sequence structure for result_detail_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."result_detail_id_seq";
CREATE SEQUENCE "public"."result_detail_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 4746
 CACHE 1;
SELECT setval('"public"."result_detail_id_seq"', 4746, true);

-- ----------------------------
-- Sequence structure for result_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."result_id_seq";
CREATE SEQUENCE "public"."result_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 73
 CACHE 1;
SELECT setval('"public"."result_id_seq"', 73, true);

-- ----------------------------
-- Sequence structure for roles_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."roles_id_seq";
CREATE SEQUENCE "public"."roles_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 4
 CACHE 1;

-- ----------------------------
-- Sequence structure for run_info_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."run_info_id_seq";
CREATE SEQUENCE "public"."run_info_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 7
 CACHE 1;

-- ----------------------------
-- Sequence structure for run_order_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."run_order_id_seq";
CREATE SEQUENCE "public"."run_order_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 18
 CACHE 1;
SELECT setval('"public"."run_order_id_seq"', 18, true);

-- ----------------------------
-- Sequence structure for status_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."status_id_seq";
CREATE SEQUENCE "public"."status_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 17
 CACHE 1;

-- ----------------------------
-- Sequence structure for td_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."td_id_seq";
CREATE SEQUENCE "public"."td_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for tdrole_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."tdrole_id_seq";
CREATE SEQUENCE "public"."tdrole_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for team_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."team_id_seq";
CREATE SEQUENCE "public"."team_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for users_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_id_seq";
CREATE SEQUENCE "public"."users_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Sequence structure for weather_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."weather_id_seq";
CREATE SEQUENCE "public"."weather_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 2
 CACHE 1;

-- ----------------------------
-- Table structure for CASHE
-- ----------------------------
DROP TABLE IF EXISTS "public"."CASHE";
CREATE TABLE "public"."CASHE" (
"id" int4 DEFAULT nextval('"CASHE_id_seq"'::regclass) NOT NULL,
"key" varchar COLLATE "default",
"data" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of CASHE
-- ----------------------------
INSERT INTO "public"."CASHE" VALUES ('1', 'Current_competitor', '{"run": 1, "order": 0}');

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS "public"."category";
CREATE TABLE "public"."category" (
"id" int4 DEFAULT nextval('category_id_seq'::regclass) NOT NULL,
"name" varchar(3) COLLATE "default",
"description" varchar(150) COLLATE "default",
"level" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO "public"."category" VALUES ('1', 'te', 'test', '2');

-- ----------------------------
-- Table structure for competitor
-- ----------------------------
DROP TABLE IF EXISTS "public"."competitor";
CREATE TABLE "public"."competitor" (
"id" int4 DEFAULT nextval('competitor_id_seq'::regclass) NOT NULL,
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
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of competitor
-- ----------------------------
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

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS "public"."course";
CREATE TABLE "public"."course" (
"id" int4 DEFAULT nextval('course_id_seq'::regclass) NOT NULL,
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
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO "public"."course" VALUES ('1', '1', '1', '1', 'first course', 'first course', '1', '10000', '5', '12', '12', '12');

-- ----------------------------
-- Table structure for course_device
-- ----------------------------
DROP TABLE IF EXISTS "public"."course_device";
CREATE TABLE "public"."course_device" (
"id" int4 DEFAULT nextval('course_device_id_seq'::regclass) NOT NULL,
"course_id" int4,
"order" int4,
"distance" int4,
"device_id" int4,
"course_device_type_id" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of course_device
-- ----------------------------
INSERT INTO "public"."course_device" VALUES ('1', '1', '1', '0', '1', '1');
INSERT INTO "public"."course_device" VALUES ('2', '1', '2', '100', '2', '3');
INSERT INTO "public"."course_device" VALUES ('3', '1', '3', '1000', '3', '3');
INSERT INTO "public"."course_device" VALUES ('4', '1', '4', '3000', '4', '3');
INSERT INTO "public"."course_device" VALUES ('5', '1', '5', '5000', '5', '3');
INSERT INTO "public"."course_device" VALUES ('6', '1', '6', '10000', '6', '2');

-- ----------------------------
-- Table structure for course_device_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."course_device_type";
CREATE TABLE "public"."course_device_type" (
"id" int4 DEFAULT nextval('course_device_type_id_seq'::regclass) NOT NULL,
"name" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of course_device_type
-- ----------------------------
INSERT INTO "public"."course_device_type" VALUES ('1', 'Start');
INSERT INTO "public"."course_device_type" VALUES ('2', 'Finish');
INSERT INTO "public"."course_device_type" VALUES ('3', 'Point');

-- ----------------------------
-- Table structure for course_forerunner
-- ----------------------------
DROP TABLE IF EXISTS "public"."course_forerunner";
CREATE TABLE "public"."course_forerunner" (
"id" int4 DEFAULT nextval('course_forerunner_id_seq'::regclass) NOT NULL,
"order" int4,
"forerunner_id" int4,
"course_id" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of course_forerunner
-- ----------------------------
INSERT INTO "public"."course_forerunner" VALUES ('1', '1', '1', '1');

-- ----------------------------
-- Table structure for coursetter
-- ----------------------------
DROP TABLE IF EXISTS "public"."coursetter";
CREATE TABLE "public"."coursetter" (
"id" int4 DEFAULT nextval('coursetter_id_seq'::regclass) NOT NULL,
"ru_lastname" varchar COLLATE "default",
"ru_firstname" varchar COLLATE "default",
"en_lastname" varchar COLLATE "default",
"en_firstname" varchar COLLATE "default",
"nation_id" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of coursetter
-- ----------------------------
INSERT INTO "public"."coursetter" VALUES ('1', 'surname1', 'name1', 'surname1', 'name1', '1');
INSERT INTO "public"."coursetter" VALUES ('2', 'surname2', 'name2', 'surname2', 'name2', '1');
INSERT INTO "public"."coursetter" VALUES ('3', 'surname3', 'name3', 'surname3', 'name3', '1');
INSERT INTO "public"."coursetter" VALUES ('4', 'surname4', 'name4', 'surname4', 'name4', '1');
INSERT INTO "public"."coursetter" VALUES ('5', 'surname1', 'name1', 'surname1', 'name1', '1');
INSERT INTO "public"."coursetter" VALUES ('6', 'surname2', 'name2', 'surname2', 'name2', '1');
INSERT INTO "public"."coursetter" VALUES ('7', 'surname3', 'name3', 'surname3', 'name3', '1');
INSERT INTO "public"."coursetter" VALUES ('8', 'surname4', 'name4', 'surname4', 'name4', '1');

-- ----------------------------
-- Table structure for data_in
-- ----------------------------
DROP TABLE IF EXISTS "public"."data_in";
CREATE TABLE "public"."data_in" (
"id" int4 DEFAULT nextval('data_in_id_seq'::regclass) NOT NULL,
"dt" timestamp(6),
"race_id" int4,
"src_sys" varchar COLLATE "default",
"src_dev" varchar COLLATE "default",
"bib" int4,
"event_code" varchar COLLATE "default",
"time" int8,
"reserved" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of data_in
-- ----------------------------

-- ----------------------------
-- Table structure for device
-- ----------------------------
DROP TABLE IF EXISTS "public"."device";
CREATE TABLE "public"."device" (
"id" int4 DEFAULT nextval('device_id_seq'::regclass) NOT NULL,
"src_dev" varchar COLLATE "default",
"name" varchar COLLATE "default",
"type_id" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of device
-- ----------------------------
INSERT INTO "public"."device" VALUES ('1', 'start0001', 'start0001', '1');
INSERT INTO "public"."device" VALUES ('2', 'int0002', 'int0002', '1');
INSERT INTO "public"."device" VALUES ('3', 'int0003', 'int0003', '1');
INSERT INTO "public"."device" VALUES ('4', 'int0004', 'int0004', '1');
INSERT INTO "public"."device" VALUES ('5', 'int0005', 'int0005', '1');
INSERT INTO "public"."device" VALUES ('6', 'finish0006', 'finish0006', '1');

-- ----------------------------
-- Table structure for device_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."device_type";
CREATE TABLE "public"."device_type" (
"id" int4 DEFAULT nextval('device_type_id_seq'::regclass) NOT NULL,
"name" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of device_type
-- ----------------------------
INSERT INTO "public"."device_type" VALUES ('1', 'test');

-- ----------------------------
-- Table structure for discipline
-- ----------------------------
DROP TABLE IF EXISTS "public"."discipline";
CREATE TABLE "public"."discipline" (
"id" int4 DEFAULT nextval('discipline_id_seq'::regclass) NOT NULL,
"fiscode" varchar COLLATE "default",
"ru_name" varchar COLLATE "default",
"en_name" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of discipline
-- ----------------------------
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

-- ----------------------------
-- Table structure for fis_points
-- ----------------------------
DROP TABLE IF EXISTS "public"."fis_points";
CREATE TABLE "public"."fis_points" (
"id" int4 NOT NULL,
"competitor_id" int4,
"discipline_id" int4,
"fispoint" float8,
"date_update" timestamp(6),
"date_expired" timestamp(6)
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of fis_points
-- ----------------------------
INSERT INTO "public"."fis_points" VALUES ('1', '4', '1', '571', '2018-01-23 04:39:07.576612', null);
INSERT INTO "public"."fis_points" VALUES ('2', '5', '1', '508', '2018-01-23 04:39:07.614462', null);
INSERT INTO "public"."fis_points" VALUES ('3', '10', '1', '569', '2018-01-23 04:39:07.614546', null);
INSERT INTO "public"."fis_points" VALUES ('4', '13', '1', '665', '2018-01-23 04:39:07.614589', null);
INSERT INTO "public"."fis_points" VALUES ('5', '22', '1', '555', '2018-01-23 04:39:07.614627', null);
INSERT INTO "public"."fis_points" VALUES ('6', '29', '1', '448', '2018-01-23 04:39:07.61467', null);

-- ----------------------------
-- Table structure for forerunner
-- ----------------------------
DROP TABLE IF EXISTS "public"."forerunner";
CREATE TABLE "public"."forerunner" (
"id" int4 DEFAULT nextval('forerunner_id_seq'::regclass) NOT NULL,
"ru_lastname" varchar COLLATE "default",
"ru_firstname" varchar COLLATE "default",
"en_lastname" varchar COLLATE "default",
"en_firstname" varchar COLLATE "default",
"nation_id" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of forerunner
-- ----------------------------
INSERT INTO "public"."forerunner" VALUES ('1', 'surname1', 'name1', 'surname1', 'name1', '1');
INSERT INTO "public"."forerunner" VALUES ('2', 'surname2', 'name2', 'surname2', 'name2', '1');
INSERT INTO "public"."forerunner" VALUES ('3', 'surname3', 'name3', 'surname3', 'name3', '1');
INSERT INTO "public"."forerunner" VALUES ('4', 'surname4', 'name4', 'surname4', 'name4', '1');
INSERT INTO "public"."forerunner" VALUES ('5', 'surname1', 'name1', 'surname1', 'name1', '1');
INSERT INTO "public"."forerunner" VALUES ('6', 'surname2', 'name2', 'surname2', 'name2', '1');
INSERT INTO "public"."forerunner" VALUES ('7', 'surname3', 'name3', 'surname3', 'name3', '1');
INSERT INTO "public"."forerunner" VALUES ('8', 'surname4', 'name4', 'surname4', 'name4', '1');

-- ----------------------------
-- Table structure for gender
-- ----------------------------
DROP TABLE IF EXISTS "public"."gender";
CREATE TABLE "public"."gender" (
"id" int4 DEFAULT nextval('gender_id_seq'::regclass) NOT NULL,
"fiscode" varchar COLLATE "default",
"ru_name" varchar COLLATE "default",
"en_name" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of gender
-- ----------------------------
INSERT INTO "public"."gender" VALUES ('1', 'Male', 'Male', 'Male');
INSERT INTO "public"."gender" VALUES ('2', 'Female', 'Female', 'Female');

-- ----------------------------
-- Table structure for jury
-- ----------------------------
DROP TABLE IF EXISTS "public"."jury";
CREATE TABLE "public"."jury" (
"id" int4 DEFAULT nextval('jury_id_seq'::regclass) NOT NULL,
"ru_lastname" varchar COLLATE "default",
"ru_firstname" varchar COLLATE "default",
"en_lastname" varchar COLLATE "default",
"en_firstname" varchar COLLATE "default",
"nation_id" int4,
"phonenbr" varchar COLLATE "default",
"email" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of jury
-- ----------------------------

-- ----------------------------
-- Table structure for jury_function
-- ----------------------------
DROP TABLE IF EXISTS "public"."jury_function";
CREATE TABLE "public"."jury_function" (
"id" int4 DEFAULT nextval('jury_function_id_seq'::regclass) NOT NULL,
"ru_function" varchar COLLATE "default",
"en_function" varchar COLLATE "default",
"attribute_values" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of jury_function
-- ----------------------------
INSERT INTO "public"."jury_function" VALUES ('1', 'ChiefRace', 'ChiefRace', 'ChiefRace');
INSERT INTO "public"."jury_function" VALUES ('2', 'Referee', 'Referee', 'Referee');
INSERT INTO "public"."jury_function" VALUES ('3', 'Assistantreferee', 'Assistantreferee', 'Assistantreferee');
INSERT INTO "public"."jury_function" VALUES ('4', 'ChiefCourse', 'ChiefCourse', 'ChiefCourse');
INSERT INTO "public"."jury_function" VALUES ('5', 'Startreferee', 'Startreferee', 'Startreferee');
INSERT INTO "public"."jury_function" VALUES ('6', 'Finishreferee', 'Finishreferee', 'Finishreferee');
INSERT INTO "public"."jury_function" VALUES ('7', 'ChiefTiming', 'ChiefTiming', 'ChiefTiming');

-- ----------------------------
-- Table structure for mark
-- ----------------------------
DROP TABLE IF EXISTS "public"."mark";
CREATE TABLE "public"."mark" (
"id" int4 DEFAULT nextval('mark_id_seq'::regclass) NOT NULL,
"name" varchar(4) COLLATE "default",
"description" varchar(100) COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of mark
-- ----------------------------

-- ----------------------------
-- Table structure for nation
-- ----------------------------
DROP TABLE IF EXISTS "public"."nation";
CREATE TABLE "public"."nation" (
"id" int4 DEFAULT nextval('nation_id_seq'::regclass) NOT NULL,
"name" varchar(3) COLLATE "default",
"ru_description" varchar(50) COLLATE "default",
"en_description" varchar(50) COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of nation
-- ----------------------------
INSERT INTO "public"."nation" VALUES ('1', 'Rus', 'Rus', 'Rus');

-- ----------------------------
-- Table structure for race
-- ----------------------------
DROP TABLE IF EXISTS "public"."race";
CREATE TABLE "public"."race" (
"id" int4 DEFAULT nextval('race_id_seq'::regclass) NOT NULL,
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
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of race
-- ----------------------------
INSERT INTO "public"."race" VALUES ('1', '1', '1', '1', '1', '1', '1', '1', null, '1', '1', 'Test event individual competition', null, null, null, null, null, null, null, null, null, null, null, null, '12', '2018-01-18', null, null, null, null, null, null, null, null, null, null, null, null, null, 'f');

-- ----------------------------
-- Table structure for race_competitor
-- ----------------------------
DROP TABLE IF EXISTS "public"."race_competitor";
CREATE TABLE "public"."race_competitor" (
"id" int4 DEFAULT nextval('race_competitor_id_seq'::regclass) NOT NULL,
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
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of race_competitor
-- ----------------------------
INSERT INTO "public"."race_competitor" VALUES ('1', '4', '1', '1', '1', '1', null, null, null, null, '1', null, null, null);
INSERT INTO "public"."race_competitor" VALUES ('2', '5', '1', '1', '2', '2', null, null, null, null, '1', null, null, null);
INSERT INTO "public"."race_competitor" VALUES ('3', '10', '1', '1', '4', '4', null, null, null, null, '1', null, null, null);
INSERT INTO "public"."race_competitor" VALUES ('4', '13', '1', '1', '6', '6', null, null, null, null, '1', null, null, null);
INSERT INTO "public"."race_competitor" VALUES ('5', '22', '1', '1', '8', '8', null, null, null, null, '1', null, null, null);
INSERT INTO "public"."race_competitor" VALUES ('6', '29', '1', '1', '10', '10', null, null, null, null, '1', null, null, null);

-- ----------------------------
-- Table structure for race_jury
-- ----------------------------
DROP TABLE IF EXISTS "public"."race_jury";
CREATE TABLE "public"."race_jury" (
"id" int4 DEFAULT nextval('race_jury_id_seq'::regclass) NOT NULL,
"jury_id" int4,
"race_id" int4,
"jury_function_id" int4,
"phonenbr" varchar COLLATE "default",
"email" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of race_jury
-- ----------------------------

-- ----------------------------
-- Table structure for race_team
-- ----------------------------
DROP TABLE IF EXISTS "public"."race_team";
CREATE TABLE "public"."race_team" (
"id" int4 DEFAULT nextval('race_team_id_seq'::regclass) NOT NULL,
"race_id" int4,
"team_id" int4,
"run_id" int4,
"bib" int4,
"classified" bool,
"en_teamname" varchar COLLATE "default",
"ru_teamname" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of race_team
-- ----------------------------

-- ----------------------------
-- Table structure for report_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."report_type";
CREATE TABLE "public"."report_type" (
"id" int4 DEFAULT nextval('report_type_id_seq'::regclass) NOT NULL,
"name" varchar COLLATE "default",
"function" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of report_type
-- ----------------------------

-- ----------------------------
-- Table structure for result
-- ----------------------------
DROP TABLE IF EXISTS "public"."result";
CREATE TABLE "public"."result" (
"id" int4 DEFAULT nextval('result_id_seq'::regclass) NOT NULL,
"race_competitor_id" int4,
"status_id" int4,
"approve_time" timestamp(6),
"timerun1" int8,
"timerun2" int8,
"timerun3" int8,
"diff" int8,
"racepoints" int8,
"level" int4,
"approve_user" int4,
"is_manuale" bool
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of result
-- ----------------------------

-- ----------------------------
-- Table structure for result_approved
-- ----------------------------
DROP TABLE IF EXISTS "public"."result_approved";
CREATE TABLE "public"."result_approved" (
"id" int4 DEFAULT nextval('result_approved_id_seq'::regclass) NOT NULL,
"race_competitor_id" int4,
"result_id" int4,
"run_id" int4,
"approve_user" int4,
"status_id" int4,
"approve_time" timestamp(6),
"timerun" int8,
"is_manual" bool,
"gate" varchar COLLATE "default",
"reason" varchar COLLATE "default",
"is_start" bool,
"is_finish" bool
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of result_approved
-- ----------------------------

-- ----------------------------
-- Table structure for result_detail
-- ----------------------------
DROP TABLE IF EXISTS "public"."result_detail";
CREATE TABLE "public"."result_detail" (
"id" int4 DEFAULT nextval('result_detail_id_seq'::regclass) NOT NULL,
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
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of result_detail
-- ----------------------------

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS "public"."roles";
CREATE TABLE "public"."roles" (
"id" int4 DEFAULT nextval('roles_id_seq'::regclass) NOT NULL,
"name" varchar(64) COLLATE "default",
"default" bool,
"permissions" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of roles
-- ----------------------------
INSERT INTO "public"."roles" VALUES ('1', 'User', 't', '7');
INSERT INTO "public"."roles" VALUES ('2', 'Moderator', 'f', '15');
INSERT INTO "public"."roles" VALUES ('3', 'Administrator', 'f', '255');

-- ----------------------------
-- Table structure for run_info
-- ----------------------------
DROP TABLE IF EXISTS "public"."run_info";
CREATE TABLE "public"."run_info" (
"id" int4 DEFAULT nextval('run_info_id_seq'::regclass) NOT NULL,
"race_id" int4,
"course_id" int4,
"number" int4,
"starttime" timestamp(6),
"endtime" timestamp(6)
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of run_info
-- ----------------------------
INSERT INTO "public"."run_info" VALUES ('1', '1', '1', '1', '2018-01-26 07:55:22.779225', null);
INSERT INTO "public"."run_info" VALUES ('3', '1', '1', '3', null, null);
INSERT INTO "public"."run_info" VALUES ('5', '1', '1', '2', null, null);

-- ----------------------------
-- Table structure for run_order
-- ----------------------------
DROP TABLE IF EXISTS "public"."run_order";
CREATE TABLE "public"."run_order" (
"id" int4 DEFAULT nextval('run_order_id_seq'::regclass) NOT NULL,
"run_id" int4,
"race_competitor_id" int4,
"order" int4,
"manual_order" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of run_order
-- ----------------------------
INSERT INTO "public"."run_order" VALUES ('13', '1', '4', '1', null);
INSERT INTO "public"."run_order" VALUES ('14', '1', '1', '2', null);
INSERT INTO "public"."run_order" VALUES ('15', '1', '3', '3', null);
INSERT INTO "public"."run_order" VALUES ('16', '1', '5', '4', null);
INSERT INTO "public"."run_order" VALUES ('17', '1', '2', '5', null);
INSERT INTO "public"."run_order" VALUES ('18', '1', '6', '6', null);

-- ----------------------------
-- Table structure for status
-- ----------------------------
DROP TABLE IF EXISTS "public"."status";
CREATE TABLE "public"."status" (
"id" int4 DEFAULT nextval('status_id_seq'::regclass) NOT NULL,
"name" varchar(4) COLLATE "default",
"description" varchar(100) COLLATE "default",
"filter_order" int2
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of status
-- ----------------------------
INSERT INTO "public"."status" VALUES ('1', 'QLF', 'Qualified', null);
INSERT INTO "public"."status" VALUES ('2', 'DNS', 'Did not start ', null);
INSERT INTO "public"."status" VALUES ('3', 'DNS1', 'Did not start run 1', null);
INSERT INTO "public"."status" VALUES ('4', 'DNS2', 'Did not start run 2', null);
INSERT INTO "public"."status" VALUES ('5', 'DSQ', 'Disqualified', null);
INSERT INTO "public"."status" VALUES ('6', 'DSQ1', 'Disqualified run 1', null);
INSERT INTO "public"."status" VALUES ('7', 'DSQ2', 'Disqualified run 2', null);
INSERT INTO "public"."status" VALUES ('8', 'DNF', 'Did not finish ', null);
INSERT INTO "public"."status" VALUES ('9', 'DNF1', 'Did not finish run 1', null);
INSERT INTO "public"."status" VALUES ('10', 'DNF2', 'Did not finish run 2', null);
INSERT INTO "public"."status" VALUES ('11', 'DNQ', 'Did not qualify', null);
INSERT INTO "public"."status" VALUES ('12', 'DNQ1', 'Did not qualify run 1', null);
INSERT INTO "public"."status" VALUES ('13', 'DPO', 'Doping offense ', null);
INSERT INTO "public"."status" VALUES ('14', 'NPS', 'Not permitted to start ', null);
INSERT INTO "public"."status" VALUES ('15', 'DQB', 'Disqualification for unsportsmanlike behavior', null);
INSERT INTO "public"."status" VALUES ('16', 'DQO', 'Disqualified for over quota', null);

-- ----------------------------
-- Table structure for td
-- ----------------------------
DROP TABLE IF EXISTS "public"."td";
CREATE TABLE "public"."td" (
"id" int4 DEFAULT nextval('td_id_seq'::regclass) NOT NULL,
"tdnumber" varchar COLLATE "default",
"ru_firstname" varchar COLLATE "default",
"en_firstname" varchar COLLATE "default",
"ru_lastname" varchar COLLATE "default",
"en_lastname" varchar COLLATE "default",
"ru_nation" varchar COLLATE "default",
"en_nation" varchar COLLATE "default",
"tdrole_id" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of td
-- ----------------------------

-- ----------------------------
-- Table structure for tdrole
-- ----------------------------
DROP TABLE IF EXISTS "public"."tdrole";
CREATE TABLE "public"."tdrole" (
"id" int4 DEFAULT nextval('tdrole_id_seq'::regclass) NOT NULL,
"name" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of tdrole
-- ----------------------------

-- ----------------------------
-- Table structure for team
-- ----------------------------
DROP TABLE IF EXISTS "public"."team";
CREATE TABLE "public"."team" (
"id" int4 DEFAULT nextval('team_id_seq'::regclass) NOT NULL,
"fis_code" varchar COLLATE "default",
"en_teamname" varchar COLLATE "default",
"ru_teamname" varchar COLLATE "default",
"nation_id" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of team
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
"id" int4 DEFAULT nextval('users_id_seq'::regclass) NOT NULL,
"email" varchar(64) COLLATE "default",
"username" varchar(64) COLLATE "default",
"role_id" int4,
"password_hash" varchar(128) COLLATE "default",
"confirmed" bool,
"name" varchar(64) COLLATE "default",
"location" varchar(64) COLLATE "default",
"about_me" text COLLATE "default",
"member_since" timestamp(6),
"last_seen" timestamp(6),
"lang" varchar(3) COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO "public"."users" VALUES ('1', 'karasev_a_e@mail.ru', 'karasik', '3', 'pbkdf2:sha1:1000$crvb0XoV$4e13a1d62e0dc7a1245ec57d7aed5a0e02b9feb0', 't', null, null, null, '2017-12-17 21:56:49.929604', '2018-04-05 20:54:59.346435', 'ru');

-- ----------------------------
-- Table structure for weather
-- ----------------------------
DROP TABLE IF EXISTS "public"."weather";
CREATE TABLE "public"."weather" (
"id" int4 DEFAULT nextval('weather_id_seq'::regclass) NOT NULL,
"race_id" int4,
"time" timestamp(6),
"place" varchar COLLATE "default",
"weather" varchar COLLATE "default",
"snow" varchar COLLATE "default",
"temperatureair" numeric,
"temperaturesnow" numeric,
"humiditystart" int4,
"windspeed" numeric
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of weather
-- ----------------------------

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------
ALTER SEQUENCE "public"."category_id_seq" OWNED BY "category"."id";
ALTER SEQUENCE "public"."competitor_id_seq" OWNED BY "competitor"."id";
ALTER SEQUENCE "public"."course_device_id_seq" OWNED BY "course_device"."id";
ALTER SEQUENCE "public"."course_device_type_id_seq" OWNED BY "course_device_type"."id";
ALTER SEQUENCE "public"."course_forerunner_id_seq" OWNED BY "course_forerunner"."id";
ALTER SEQUENCE "public"."course_id_seq" OWNED BY "course"."id";
ALTER SEQUENCE "public"."coursetter_id_seq" OWNED BY "coursetter"."id";
ALTER SEQUENCE "public"."data_in_id_seq" OWNED BY "data_in"."id";
ALTER SEQUENCE "public"."device_id_seq" OWNED BY "device"."id";
ALTER SEQUENCE "public"."device_type_id_seq" OWNED BY "device_type"."id";
ALTER SEQUENCE "public"."discipline_id_seq" OWNED BY "discipline"."id";
ALTER SEQUENCE "public"."forerunner_id_seq" OWNED BY "forerunner"."id";
ALTER SEQUENCE "public"."gender_id_seq" OWNED BY "gender"."id";
ALTER SEQUENCE "public"."jury_function_id_seq" OWNED BY "jury_function"."id";
ALTER SEQUENCE "public"."jury_id_seq" OWNED BY "jury"."id";
ALTER SEQUENCE "public"."mark_id_seq" OWNED BY "mark"."id";
ALTER SEQUENCE "public"."nation_id_seq" OWNED BY "nation"."id";
ALTER SEQUENCE "public"."race_competitor_id_seq" OWNED BY "race_competitor"."id";
ALTER SEQUENCE "public"."race_id_seq" OWNED BY "race"."id";
ALTER SEQUENCE "public"."race_jury_id_seq" OWNED BY "race_jury"."id";
ALTER SEQUENCE "public"."race_team_id_seq" OWNED BY "race_team"."id";
ALTER SEQUENCE "public"."report_type_id_seq" OWNED BY "report_type"."id";
ALTER SEQUENCE "public"."result_approved_id_seq" OWNED BY "result_approved"."id";
ALTER SEQUENCE "public"."result_detail_id_seq" OWNED BY "result_detail"."id";
ALTER SEQUENCE "public"."result_id_seq" OWNED BY "result"."id";
ALTER SEQUENCE "public"."roles_id_seq" OWNED BY "roles"."id";
ALTER SEQUENCE "public"."run_info_id_seq" OWNED BY "run_info"."id";
ALTER SEQUENCE "public"."run_order_id_seq" OWNED BY "run_order"."id";
ALTER SEQUENCE "public"."status_id_seq" OWNED BY "status"."id";
ALTER SEQUENCE "public"."td_id_seq" OWNED BY "td"."id";
ALTER SEQUENCE "public"."tdrole_id_seq" OWNED BY "tdrole"."id";
ALTER SEQUENCE "public"."team_id_seq" OWNED BY "team"."id";
ALTER SEQUENCE "public"."users_id_seq" OWNED BY "users"."id";
ALTER SEQUENCE "public"."weather_id_seq" OWNED BY "weather"."id";

-- ----------------------------
-- Primary Key structure for table CASHE
-- ----------------------------
ALTER TABLE "public"."CASHE" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table category
-- ----------------------------
ALTER TABLE "public"."category" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table competitor
-- ----------------------------
ALTER TABLE "public"."competitor" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table course
-- ----------------------------
ALTER TABLE "public"."course" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table course_device
-- ----------------------------
ALTER TABLE "public"."course_device" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table course_device_type
-- ----------------------------
ALTER TABLE "public"."course_device_type" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table course_forerunner
-- ----------------------------
ALTER TABLE "public"."course_forerunner" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table coursetter
-- ----------------------------
ALTER TABLE "public"."coursetter" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table data_in
-- ----------------------------
ALTER TABLE "public"."data_in" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table device
-- ----------------------------
ALTER TABLE "public"."device" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table device_type
-- ----------------------------
ALTER TABLE "public"."device_type" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table discipline
-- ----------------------------
ALTER TABLE "public"."discipline" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table fis_points
-- ----------------------------
ALTER TABLE "public"."fis_points" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table forerunner
-- ----------------------------
ALTER TABLE "public"."forerunner" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table gender
-- ----------------------------
ALTER TABLE "public"."gender" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table jury
-- ----------------------------
ALTER TABLE "public"."jury" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table jury_function
-- ----------------------------
ALTER TABLE "public"."jury_function" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table mark
-- ----------------------------
ALTER TABLE "public"."mark" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table nation
-- ----------------------------
ALTER TABLE "public"."nation" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table race
-- ----------------------------
ALTER TABLE "public"."race" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table race_competitor
-- ----------------------------
ALTER TABLE "public"."race_competitor" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table race_jury
-- ----------------------------
ALTER TABLE "public"."race_jury" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table race_team
-- ----------------------------
ALTER TABLE "public"."race_team" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table report_type
-- ----------------------------
ALTER TABLE "public"."report_type" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table result
-- ----------------------------
ALTER TABLE "public"."result" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table result_approved
-- ----------------------------
ALTER TABLE "public"."result_approved" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table result_detail
-- ----------------------------
ALTER TABLE "public"."result_detail" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table roles
-- ----------------------------
CREATE INDEX "ix_roles_default" ON "public"."roles" USING btree ("default");

-- ----------------------------
-- Uniques structure for table roles
-- ----------------------------
ALTER TABLE "public"."roles" ADD UNIQUE ("name");

-- ----------------------------
-- Primary Key structure for table roles
-- ----------------------------
ALTER TABLE "public"."roles" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table run_info
-- ----------------------------
ALTER TABLE "public"."run_info" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table run_order
-- ----------------------------
ALTER TABLE "public"."run_order" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table status
-- ----------------------------
ALTER TABLE "public"."status" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table td
-- ----------------------------
ALTER TABLE "public"."td" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table tdrole
-- ----------------------------
ALTER TABLE "public"."tdrole" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table team
-- ----------------------------
ALTER TABLE "public"."team" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table users
-- ----------------------------
CREATE UNIQUE INDEX "ix_users_email" ON "public"."users" USING btree ("email");
CREATE UNIQUE INDEX "ix_users_username" ON "public"."users" USING btree ("username");

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table weather
-- ----------------------------
ALTER TABLE "public"."weather" ADD PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Key structure for table "public"."competitor"
-- ----------------------------
ALTER TABLE "public"."competitor" ADD FOREIGN KEY ("gender_id") REFERENCES "public"."gender" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."competitor" ADD FOREIGN KEY ("nation_code_id") REFERENCES "public"."nation" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."competitor" ADD FOREIGN KEY ("category_id") REFERENCES "public"."category" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."course"
-- ----------------------------
ALTER TABLE "public"."course" ADD FOREIGN KEY ("course_coursetter_id") REFERENCES "public"."coursetter" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."course" ADD FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."course_device"
-- ----------------------------
ALTER TABLE "public"."course_device" ADD FOREIGN KEY ("course_id") REFERENCES "public"."course" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."course_device" ADD FOREIGN KEY ("course_device_type_id") REFERENCES "public"."course_device_type" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."course_device" ADD FOREIGN KEY ("device_id") REFERENCES "public"."device" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."course_forerunner"
-- ----------------------------
ALTER TABLE "public"."course_forerunner" ADD FOREIGN KEY ("forerunner_id") REFERENCES "public"."forerunner" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."course_forerunner" ADD FOREIGN KEY ("course_id") REFERENCES "public"."course" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."coursetter"
-- ----------------------------
ALTER TABLE "public"."coursetter" ADD FOREIGN KEY ("nation_id") REFERENCES "public"."nation" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."data_in"
-- ----------------------------
ALTER TABLE "public"."data_in" ADD FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."device"
-- ----------------------------
ALTER TABLE "public"."device" ADD FOREIGN KEY ("type_id") REFERENCES "public"."device_type" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."fis_points"
-- ----------------------------
ALTER TABLE "public"."fis_points" ADD FOREIGN KEY ("competitor_id") REFERENCES "public"."competitor" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."fis_points" ADD FOREIGN KEY ("discipline_id") REFERENCES "public"."discipline" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."forerunner"
-- ----------------------------
ALTER TABLE "public"."forerunner" ADD FOREIGN KEY ("nation_id") REFERENCES "public"."nation" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."jury"
-- ----------------------------
ALTER TABLE "public"."jury" ADD FOREIGN KEY ("nation_id") REFERENCES "public"."nation" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."race"
-- ----------------------------
ALTER TABLE "public"."race" ADD FOREIGN KEY ("category_id") REFERENCES "public"."category" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race" ADD FOREIGN KEY ("td_assistant_nation_id") REFERENCES "public"."nation" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race" ADD FOREIGN KEY ("td_delegate_nation_id") REFERENCES "public"."nation" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race" ADD FOREIGN KEY ("discipline_id") REFERENCES "public"."discipline" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race" ADD FOREIGN KEY ("nation_id") REFERENCES "public"."nation" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race" ADD FOREIGN KEY ("gender_id") REFERENCES "public"."gender" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."race_competitor"
-- ----------------------------
ALTER TABLE "public"."race_competitor" ADD FOREIGN KEY ("run_id") REFERENCES "public"."run_info" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race_competitor" ADD FOREIGN KEY ("team_id") REFERENCES "public"."team" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race_competitor" ADD FOREIGN KEY ("competitor_id") REFERENCES "public"."competitor" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race_competitor" ADD FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race_competitor" ADD FOREIGN KEY ("status_id") REFERENCES "public"."status" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."race_jury"
-- ----------------------------
ALTER TABLE "public"."race_jury" ADD FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race_jury" ADD FOREIGN KEY ("jury_function_id") REFERENCES "public"."jury_function" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race_jury" ADD FOREIGN KEY ("jury_id") REFERENCES "public"."jury" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."race_team"
-- ----------------------------
ALTER TABLE "public"."race_team" ADD FOREIGN KEY ("team_id") REFERENCES "public"."team" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race_team" ADD FOREIGN KEY ("run_id") REFERENCES "public"."run_info" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."race_team" ADD FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."result"
-- ----------------------------
ALTER TABLE "public"."result" ADD FOREIGN KEY ("approve_user") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."result" ADD FOREIGN KEY ("race_competitor_id") REFERENCES "public"."race_competitor" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."result" ADD FOREIGN KEY ("status_id") REFERENCES "public"."status" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."result_approved"
-- ----------------------------
ALTER TABLE "public"."result_approved" ADD FOREIGN KEY ("result_id") REFERENCES "public"."result" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."result_approved" ADD FOREIGN KEY ("race_competitor_id") REFERENCES "public"."race_competitor" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."result_approved" ADD FOREIGN KEY ("status_id") REFERENCES "public"."status" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."result_approved" ADD FOREIGN KEY ("approve_user") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."result_approved" ADD FOREIGN KEY ("run_id") REFERENCES "public"."run_info" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."result_detail"
-- ----------------------------
ALTER TABLE "public"."result_detail" ADD FOREIGN KEY ("course_device_id") REFERENCES "public"."course_device" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."result_detail" ADD FOREIGN KEY ("run_id") REFERENCES "public"."run_info" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."result_detail" ADD FOREIGN KEY ("race_competitor_id") REFERENCES "public"."race_competitor" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."run_info"
-- ----------------------------
ALTER TABLE "public"."run_info" ADD FOREIGN KEY ("course_id") REFERENCES "public"."course" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."run_info" ADD FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."run_order"
-- ----------------------------
ALTER TABLE "public"."run_order" ADD FOREIGN KEY ("race_competitor_id") REFERENCES "public"."race_competitor" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."run_order" ADD FOREIGN KEY ("run_id") REFERENCES "public"."run_info" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."td"
-- ----------------------------
ALTER TABLE "public"."td" ADD FOREIGN KEY ("tdrole_id") REFERENCES "public"."tdrole" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."team"
-- ----------------------------
ALTER TABLE "public"."team" ADD FOREIGN KEY ("nation_id") REFERENCES "public"."nation" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."users"
-- ----------------------------
ALTER TABLE "public"."users" ADD FOREIGN KEY ("role_id") REFERENCES "public"."roles" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."weather"
-- ----------------------------
ALTER TABLE "public"."weather" ADD FOREIGN KEY ("race_id") REFERENCES "public"."race" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
