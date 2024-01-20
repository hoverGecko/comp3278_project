# Course Management System

### Features

- Register and login your account through facial recognition (face recognition code provided)
- Manage your courses with features such as:
  - Front page showing the upcoming lecture and assignment due dates,
  - Course timetable, and
  - Course detail page for each course listing course teachers and links to course materials.
 
### ER diagram
![圖片](https://github.com/hoverGecko/comp3278_project/assets/46785140/add4d2c7-6b38-4ded-a62c-ebbca4b13199)

### Video Demo
[COMP3278 Group 32 Demo Recording.webm](https://github.com/hoverGecko/comp3278_project/assets/46785140/4667cb2e-970e-4216-8de9-27da145ded25)

*******

## Usage

### 1. Clone Repository and Create Environment

```bash
# Clone repo
git clone https://github.com/hoverGecko/comp3278_project.git
cd comp3278_project
# Create virtual environment using Anaconda.
conda create -n face python=3.x
conda activate face
pip install -r requirements.txt
```

### 2. Create Database and Load Data
```bash
# In Bash
mysql -u root -p
# In MySQL
CREATE DATABASE facerecognition;
CREATE USER 'user'@'localhost';
GRANT ALL PRIVILEGES ON facerecognition.* TO 'user'@'localhost';
exit
# In Bash
mysql -u user facerecognition < facerecognition.sql
mysql -u user facerecognition < facerecognition_example_data.sql
```

### 3. Run the app
```
python main.py
```
The facial data collection and training features can be accessed through the sign-up function of the app with the following sample user details:
- UID: 3
- Email: smith@hku.hk
