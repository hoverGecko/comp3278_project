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

INSERT INTO `Course` (`course_id`, `title`, `code`, `teacher_message`, `section`) VALUES
(1, 'Computer Science', 'COMP1101', 'Have a nice lecture!', '1A'),
(2, 'Computer Database Fundamentals', 'COMP3278', 'Database is fun!', '1A'),
(3, 'Calculus I', 'MATH1002', 'Do Math.', '1B');

INSERT INTO `Personnel` (`uid`, `full_name`, `registered_email`, `is_student`) VALUES
(1, 'John Doe', 'abc@abc.abc', b'1'), -- student, has account
(2, 'Jane Doe', 'jane@abc.hk', b'0'), -- not student
(3, 'Smith', 'smith@hku.hk', b'1'), -- student, has no account
(4, 'Alice', 'alice@hku.hk', b'0'); -- not student

INSERT INTO `Account` (`last_login_date`, `last_login_duration`, `creation_date`, `uid`, `account_name`) VALUES
('2023-11-18 18:40:54', 15, '2023-11-18 18:00:00', 1, 'johndoe1');

INSERT INTO `CourseClass` (`type`, `start_time`, `end_time`, `venue`, `course_id`, `weekday`) VALUES
('lecture', '14:30:00', '15:30:00', 'MWT2', 1, '1'),
('lecture', '10:30:00', '12:30:00', 'MB121', 1, '2'),
('tutorial', '12:30:00', '14:30:00', 'MB122', 1, '3'),
('lecture', '16:30:00', '17:30:00', 'MWT3', 2, '2'),
('lecture', '15:30:00', '16:30:00', 'CYM121', 2, '3'),
('tutorial', '12:30:00', '13:30:00', 'CPD-2.16', 2, '4'),
('lecture', '14:30:00', '16:30:00', 'CPD-2.17', 3, '5'),
('tutorial', '14:30:00', '15:30:00', 'MWT2', 3, '4');

INSERT INTO `CourseResource` (`file_type`, `category`, `link`, `title`, `course_id`, `due_date`, `creation_date`) VALUES
('zoom', 'Zoom', 'https://zoom.us/join', 'Lecture Zoom Link', 1, NULL, '2023-11-01 18:00:00'),
('zoom', 'Zoom', 'https://zoom.us/join', 'Lecture Zoom Link', 2, NULL, '2023-11-01 18:00:00'),
('zoom', 'Zoom', 'https://zoom.us/join', 'Lecture Zoom Link', 3, NULL, '2023-11-01 18:00:00'),
('pdf', 'Lecture slides', 'www.google.com', 'Lecture 1 - Course Introduction', 2, NULL, '2023-11-02 18:00:00'),
('pdf', 'Lecture slides', 'www.google.com', 'Lecture 2 - ER Diagram', 2, NULL, '2023-11-03 18:00:00'),
('pdf', 'Lecture slides', 'www.google.com', 'Lecture 3 - ER design', 2, NULL, '2023-11-04 18:00:00'),
('pdf', 'Tutorial notes', 'www.google.com', 'Tutorial 1 - MySQL', 2, NULL, '2023-11-05 18:00:00'),
('pdf', 'Assignment', 'www.google.com', 'A1 - ER Diagram', 2, '2023-12-01 23:59:59', '2023-11-06 18:00:00'),
('pdf', 'Assignment', 'www.google.com', 'A2 - SQL', 2, '2023-12-20 23:59:59', '2023-11-07 18:00:00'),
('pdf', 'Lecture slides', 'www.google.com', 'Lecture 1', 1, NULL, '2023-11-02 18:00:00'),
('pdf', 'Lecture slides', 'www.google.com', 'Lecture 2', 1, NULL, '2023-11-03 18:00:00'),
('pdf', 'Lecture slides', 'www.google.com', 'Lecture 3 - ER design', 1, NULL, '2023-11-04 18:00:00'),
('pdf', 'Assignment', 'www.google.com', 'A1 - Introduction to Python', 2, '2023-12-02 23:59:59', '2023-11-10 18:00:00'),
('pdf', 'Course Information', 'www.google.com', 'Course Introduction', 3, NULL, '2023-11-02 18:00:00'),
('pdf', 'Assignment', 'www.google.com', 'A1 - Limits', 3, '2023-12-03 23:59:59', '2023-11-03 18:00:00');

INSERT INTO `CourseEnrollment` (`uid`, `course_id`) VALUES
(1, 1),
(1, 2),
(1, 3),
(3, 1), 
(3, 2),
(3, 3);

INSERT INTO `CourseTeacher` (`uid`, `course_id`, `role`) VALUES
(2, 1, 'lecturer'),
(4, 1, 'tutor'),
(2, 2, 'lecturer'),
(4, 2, 'lecturer'),
(2, 3, 'tutor'),
(4, 3, 'lecturer'),
(1, 3, 'TA');


COMMIT;
