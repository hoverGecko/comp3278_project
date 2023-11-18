-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: sophia
-- Generation Time: Nov 18, 2023 at 07:38 PM
-- Server version: 5.7.42-0ubuntu0.18.04.1
-- PHP Version: 8.2.7

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

-- --------------------------------------------------------

--
-- Table structure for table `Account`
--
DROP TABLE IF EXISTS `Account`;

CREATE TABLE `Account` (
  `last_login_date` datetime NOT NULL,
  `last_login_duration` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `account_name` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Account`
--

INSERT INTO `Account` (`last_login_date`, `last_login_duration`, `uid`, `account_name`) VALUES
('2023-11-18 18:40:54', 15, 1, 'johndoe1');

-- --------------------------------------------------------

--
-- Table structure for table `contains`
--
DROP TABLE IF EXISTS `contains`;

CREATE TABLE `contains` (
  `title` varchar(200) NOT NULL,
  `course_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `contains`
--

INSERT INTO `contains` (`title`, `course_id`) VALUES
('Computer Database Fundamentals', 2);

-- --------------------------------------------------------

--
-- Table structure for table `Course`
--
DROP TABLE IF EXISTS `Course`;

CREATE TABLE `Course` (
  `course_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `code` int(11) NOT NULL,
  `teacher_message` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Course`
--

INSERT INTO `Course` (`course_id`, `title`, `code`, `teacher_message`) VALUES
(1, 'Computer Science', 1111, 'Have a nice lecture!'),
(2, 'Computer Database', 1112, 'Lorem ipsum');

-- --------------------------------------------------------

--
-- Table structure for table `CourseClass`
--
DROP TABLE IF EXISTS `CourseClass`;

CREATE TABLE `CourseClass` (
  `type` varchar(200) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `venue` varchar(200) NOT NULL,
  `course_id` int(11) NOT NULL,
  `weekday` enum('1','2','3','4','5','6','7') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `CourseClass`
--

INSERT INTO `CourseClass` (`type`, `start_time`, `end_time`, `venue`, `course_id`, `weekday`) VALUES
('lecture', '14:30:00', '15:30:00', 'MWT2', 2, '4');

-- --------------------------------------------------------

--
-- Table structure for table `CourseResource`
--
DROP TABLE IF EXISTS `CourseResource`;

CREATE TABLE `CourseResource` (
  `file_type` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `link` varchar(200) NOT NULL,
  `title` varchar(200) NOT NULL,
  `course_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `CourseResource`
--

INSERT INTO `CourseResource` (`file_type`, `category`, `link`, `title`, `course_id`) VALUES
('pdf', 'notes', 'www.google.com', 'Computer Database Fundamentals', 2);

-- --------------------------------------------------------

--
-- Table structure for table `creates`
--
DROP TABLE IF EXISTS `creates`;

CREATE TABLE `creates` (
  `account_name` varchar(200) NOT NULL,
  `uid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `creates`
--

INSERT INTO `creates` (`account_name`, `uid`) VALUES
('johndoe1', 1);

-- --------------------------------------------------------

--
-- Table structure for table `enrolls`
--
DROP TABLE IF EXISTS `enrolls`;

CREATE TABLE `enrolls` (
  `uid` int(11) NOT NULL,
  `course_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `enrolls`
--

INSERT INTO `enrolls` (`uid`, `course_id`) VALUES
(1, 1),
(1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `has`
--
DROP TABLE IF EXISTS `has`;

CREATE TABLE `has` (
  `start_time` time NOT NULL,
  `course_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `has`
--

INSERT INTO `has` (`start_time`, `course_id`) VALUES
('14:30:00', 2);

-- --------------------------------------------------------

--
-- Table structure for table `Personnel`
--
DROP TABLE IF EXISTS `Personnel`;

CREATE TABLE `Personnel` (
  `uid` int(11) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `registered_email` varchar(200) NOT NULL,
  `is_student` bit(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Personnel`
--

INSERT INTO `Personnel` (`uid`, `full_name`, `registered_email`, `is_student`) VALUES
(1, 'john doe', 'abc@abc.abc', b'1'),
(2, 'jane doe', 'jane@abc.hk', b'0');

-- --------------------------------------------------------

--
-- Table structure for table `teaches`
--
DROP TABLE IF EXISTS `teaches`;

CREATE TABLE `teaches` (
  `uid` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `role` set('lecturer','tutor','TA') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `teaches`
--

INSERT INTO `teaches` (`uid`, `course_id`, `role`) VALUES
(2, 2, 'lecturer');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Account`
--
ALTER TABLE `Account`
  ADD PRIMARY KEY (`account_name`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `contains`
--
ALTER TABLE `contains`
  ADD PRIMARY KEY (`title`,`course_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `Course`
--
ALTER TABLE `Course`
  ADD PRIMARY KEY (`course_id`);

--
-- Indexes for table `CourseClass`
--
ALTER TABLE `CourseClass`
  ADD PRIMARY KEY (`start_time`,`weekday`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `CourseResource`
--
ALTER TABLE `CourseResource`
  ADD PRIMARY KEY (`title`,`course_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `creates`
--
ALTER TABLE `creates`
  ADD PRIMARY KEY (`account_name`,`uid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `enrolls`
--
ALTER TABLE `enrolls`
  ADD PRIMARY KEY (`uid`,`course_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `has`
--
ALTER TABLE `has`
  ADD PRIMARY KEY (`start_time`,`course_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `Personnel`
--
ALTER TABLE `Personnel`
  ADD PRIMARY KEY (`uid`);

--
-- Indexes for table `teaches`
--
ALTER TABLE `teaches`
  ADD PRIMARY KEY (`uid`,`course_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Account`
--
ALTER TABLE `Account`
  ADD CONSTRAINT `Account_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `Personnel` (`uid`);

--
-- Constraints for table `contains`
--
ALTER TABLE `contains`
  ADD CONSTRAINT `contains_ibfk_1` FOREIGN KEY (`title`) REFERENCES `CourseResource` (`title`),
  ADD CONSTRAINT `contains_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`);

--
-- Constraints for table `CourseClass`
--
ALTER TABLE `CourseClass`
  ADD CONSTRAINT `CourseClass_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`);

--
-- Constraints for table `CourseResource`
--
ALTER TABLE `CourseResource`
  ADD CONSTRAINT `CourseResource_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`);

--
-- Constraints for table `creates`
--
ALTER TABLE `creates`
  ADD CONSTRAINT `creates_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `Personnel` (`uid`),
  ADD CONSTRAINT `creates_ibfk_2` FOREIGN KEY (`account_name`) REFERENCES `Account` (`account_name`);

--
-- Constraints for table `enrolls`
--
ALTER TABLE `enrolls`
  ADD CONSTRAINT `enrolls_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `Personnel` (`uid`),
  ADD CONSTRAINT `enrolls_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`);

--
-- Constraints for table `has`
--
ALTER TABLE `has`
  ADD CONSTRAINT `has_ibfk_1` FOREIGN KEY (`start_time`) REFERENCES `CourseClass` (`start_time`),
  ADD CONSTRAINT `has_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`);

--
-- Constraints for table `teaches`
--
ALTER TABLE `teaches`
  ADD CONSTRAINT `teaches_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `Personnel` (`uid`),
  ADD CONSTRAINT `teaches_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
