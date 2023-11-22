SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `facerecognition`
--

-- Dropping Tables

DROP TABLE IF EXISTS `CourseClass`;
DROP TABLE IF EXISTS `CourseResource`;
DROP TABLE IF EXISTS `CourseEnrollment`;
DROP TABLE IF EXISTS `CourseTeacher`;
DROP TABLE IF EXISTS `Account`;
DROP TABLE IF EXISTS `Personnel`;
DROP TABLE IF EXISTS `Course`;

-- Creating Tables

CREATE TABLE `Course` (
  `course_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL,
  `teacher_message` varchar(100) DEFAULT NULL,
  `section` varchar(10) NOT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Personnel` (
  `uid` int(11) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `registered_email` varchar(200) NOT NULL,
  `is_student` bit(1) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Account` (
  `last_login_date` datetime DEFAULT NULL,
  `last_login_duration` int(11) DEFAULT NULL,
  `creation_date` datetime NOT NULL,
  `uid` int(11) NOT NULL UNIQUE,
  `account_name` varchar(200) NOT NULL,
  PRIMARY KEY (`account_name`),
  FOREIGN KEY (`uid`) REFERENCES `Personnel` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `CourseClass` (
  `type` varchar(200) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `venue` varchar(30) NOT NULL,
  `course_id` int(11) NOT NULL,
  `weekday` enum('1','2','3','4','5','6','7') NOT NULL,
  PRIMARY KEY (`course_id`, `weekday`, `start_time`),
  FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `CourseResource` (
  `file_type` varchar(50) NOT NULL,
  `category` varchar(100) NOT NULL,
  `link` varchar(200) NOT NULL,
  `title` varchar(200) NOT NULL,
  `course_id` int(11) NOT NULL,
  `due_date` datetime,
  `creation_date` datetime NOT NULL,
  PRIMARY KEY (`course_id`, `title`),
  FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `CourseEnrollment` (
  `uid` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`uid`, `course_id`),
  FOREIGN KEY (`uid`) REFERENCES `Personnel` (`uid`),
  FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `CourseTeacher` (
  `uid` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `role` set('lecturer','tutor','TA') NOT NULL,
  PRIMARY KEY (`course_id`, `uid`),
  FOREIGN KEY (`uid`) REFERENCES `Personnel` (`uid`),
  FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;