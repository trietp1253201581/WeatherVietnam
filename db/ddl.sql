--Create new schema
CREATE SCHEMA whether_vietnam;

--Use this schema
USE whether_vietnam;

--Create country table
CREATE TABLE `country` (
  `country_code` varchar(10) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`country_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

--Create city table
CREATE TABLE `city` (
  `city_id` int NOT NULL,
  `name` varchar(60) DEFAULT NULL,
  `lon` float NOT NULL,
  `lat` float NOT NULL,
  `time_zone` int DEFAULT NULL,
  `country_code` varchar(10) NOT NULL,
  PRIMARY KEY (`city_id`),
  KEY `country_of_city_idx` (`country_code`),
  CONSTRAINT `country_of_city` FOREIGN KEY (`country_code`) REFERENCES `country` (`country_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

--Create country_record table
CREATE TABLE `country_record` (
  `country_code` varchar(10) NOT NULL,
  `collect_date` date NOT NULL,
  `sunrise` datetime DEFAULT NULL,
  `sunset` datetime DEFAULT NULL,
  PRIMARY KEY (`country_code`,`collect_date`),
  CONSTRAINT `record_of_country` FOREIGN KEY (`country_code`) REFERENCES `country` (`country_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

--Create general_weather table
CREATE TABLE `general_weather` (
  `status_id` int NOT NULL,
  `description` varchar(200) NOT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `weather_status` (
  `city_id` int NOT NULL,
  `collect_time` datetime NOT NULL,
  `base` varchar(45) DEFAULT NULL,
  `temp` float DEFAULT NULL,
  `feels_temp` float DEFAULT NULL,
  `temp_min` float DEFAULT NULL,
  `temp_max` float DEFAULT NULL,
  `pressure` int DEFAULT NULL,
  `humidity` int DEFAULT NULL,
  `sea_level` int DEFAULT NULL,
  `grnd_level` int DEFAULT NULL,
  `visibility` int DEFAULT NULL,
  `wind_speed` float DEFAULT NULL,
  `wind_deg` int DEFAULT NULL,
  `wind_gust` float DEFAULT NULL,
  `clouds_all` int DEFAULT NULL,
  PRIMARY KEY (`city_id`,`collect_time`),
  CONSTRAINT `weather_at_city` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `weather_condition` (
  `city_id` int NOT NULL,
  `collect_time` datetime NOT NULL,
  `general_weather_status` int NOT NULL,
  PRIMARY KEY (`city_id`,`collect_time`,`general_weather_status`),
  KEY `status_of_general_weather_idx` (`general_weather_status`),
  CONSTRAINT `status_of_date_city` FOREIGN KEY (`city_id`, `collect_time`) REFERENCES `weather_status` (`city_id`, `collect_time`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `status_of_general_weather` FOREIGN KEY (`general_weather_status`) REFERENCES `general_weather` (`status_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci