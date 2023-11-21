SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Delete from tables

DELETE FROM `CourseClass`;
DELETE FROM `CourseResource`;
DELETE FROM `CourseEnrollment`;
DELETE FROM `CourseTeacher`;
DELETE FROM `Account`;
DELETE FROM `Personnel`;
DELETE FROM `Course`;

INSERT INTO `Course` (`course_id`, `title`, `code`, `teacher_message`) VALUES
(1, 'Computer Science', 1111, 'Have a nice lecture!'),
(2, 'Computer Database', 1112, 'Lorem ipsum');

INSERT INTO `Personnel` (`uid`, `full_name`, `registered_email`, `is_student`) VALUES
(1, 'john doe', 'abc@abc.abc', b'1'), -- student, has account
(2, 'jane doe', 'jane@abc.hk', b'0'), -- not student
(3, 'Smith', 'test@hku.hk', b'1'); -- student, has no account

INSERT INTO `Account` (`last_login_date`, `last_login_duration`, `creation_date`, `uid`, `account_name`) VALUES
('2023-11-18 18:40:54', 15, '2023-11-18 18:00:00', 1, 'johndoe1');

INSERT INTO `CourseClass` (`type`, `start_time`, `end_time`, `venue`, `course_id`, `weekday`) VALUES
('lecture', '14:30:00', '15:30:00', 'MWT2', 2, '4');

INSERT INTO `CourseResource` (`file_type`, `category`, `link`, `title`, `course_id`) VALUES
('pdf', 'notes', 'www.google.com', 'Computer Database Fundamentals', 2);

INSERT INTO `CourseEnrollment` (`uid`, `course_id`) VALUES
(1, 1),
(1, 2);

INSERT INTO `CourseTeacher` (`uid`, `course_id`, `role`) VALUES
(2, 2, 'lecturer');

COMMIT;