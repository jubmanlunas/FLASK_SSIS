CREATE DATABASE `SSIS_DB`;

USE `SSIS_DB`;

CREATE TABLE `college` (
    `college_code` VARCHAR(10) NOT NULL,
    `college_name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`college_code`)
);

CREATE TABLE `course` (
    `course_code` VARCHAR(10) NOT NULL,
    `course_name` VARCHAR(50) NOT NULL,
    `course_college` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`course_code`), 
    FOREIGN KEY (`course_college`) REFERENCES `college` (`college_code`)
);

CREATE TABLE `students` (
    `id_number` CHAR(9) NOT NULL,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `course` VARCHAR(10) NOT NULL,
    `year_level` INTEGER NOT NULL,
    `gender` VARCHAR(20) NOT NULL, 
    PRIMARY KEY (`id_number`),
    FOREIGN KEY (`course`) REFERENCES `course` (`course_name`)
);


