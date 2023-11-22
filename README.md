# Face Recognition

Face recognition using python and mysql.

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

### 1. Create Database
```
sudo mysql -u root
(mysql)
CREATE DATABASE facerecognition;
CREATE USER 'user'@'localhost';
GRANT ALL PRIVILEGES ON facerecognition.* TO 'user'@'localhost';
exit
(bash)
mysql -u user facerecognition < facerecognition.sql
mysql -u user facerecognition < facerecognition_example_data.sql
```

### 2. Run the app
```
python main.py
```
The face data collection and training can be accessed through the sign-up function of the app with the following user details:
- UID: 3
- Email: smith@hku.hk
- Display name: (can be anything or left blank)