# Course Management System

Project of COMP3278. \
A course management system that allows students to register and login through facial recognition (face recognition code provided) and check course details such as a course timetable, course teachers and course materials including lecture notes and upcoming assignment due dates. \
Python (PySimpleGUI) and MySQL are used to create the app.

### Video Demo
[COMP3278 Group 32 Demo Recording.webm](https://github.com/hoverGecko/comp3278_project/assets/46785140/4667cb2e-970e-4216-8de9-27da145ded25)

*******

## Useage

### Environment

Create virtual environment using Anaconda.
```
conda create -n face python=3.x
conda activate face
pip install -r requirements.txt
```

### MySQL Install

[Mac](https://dev.mysql.com/doc/mysql-osx-excerpt/5.7/en/osx-installation-pkg.html)

[Ubuntu](https://dev.mysql.com/doc/mysql-linuxunix-excerpt/5.7/en/linux-installation.html)

[Windows](https://dev.mysql.com/downloads/installer/)

You'll obtain an account and password after installation, then you should modify the `faces.py`, with the corresponding
`user` and `passwd`:
```
# create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="xxxxx", database="facerecognition")
```

*******

## Run

### 1. Face Recognition Function

main.py is the file to be run. It contains a sign up function that calls face_capture.py and train.py.
face_capture.py, train.py, main.py are used to collect face data and train a face recognition model and test.py are used to test validity.


### 2. Create Database
```
(bash)
mysql -u root -p
(mysql)
CREATE DATABASE facerecognition;
CREATE USER 'user'@'localhost';
GRANT ALL PRIVILEGES ON facerecognition.* TO 'user'@'localhost';
exit
(bash)
mysql -u user facerecognition < facerecognition.sql
mysql -u user facerecognition < facerecognition_example_data.sql
```

### 3. Run the app
```
python main.py
```
The face data collection and training can be accessed through the sign-up function of the app with the following user details:
- UID: 3
- Email: smith@hku.hk
- Display name: (can be anything or left blank)
