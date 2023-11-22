import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime,date,timedelta
import sys
import PySimpleGUI as sg
from typing import Optional, Union, List, Tuple, Dict
from face_capture import face_capture
from train import train as train_model
import textwrap
import time
from datetime import datetime

# Constants
# Range: 0 - 100
FACE_DETECT_CONFIDENCE: int = 65
FACE_DETECT_TIMEOUT: int = 200

# 1 Create database connection
myconn = mysql.connector.connect(host="localhost", user="user", database="facerecognition")

date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()

#2 Load recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
is_recognizer_loaded = False
# runs only if recognizer is not loaded (most likely due to train.yml not existing)
def load_recognizer():
    global recognizer, is_recognizer_loaded
    try:
        recognizer.read("train.yml")
        is_recognizer_loaded = True
    except:
        is_recognizer_loaded = False
load_recognizer()

labels = {"person_name": 1}
is_labels_loaded = False
def load_labels_pickle():
    global labels, is_labels_loaded
    labels = {"person_name": 1}
    try:
        with open("labels.pickle", "rb") as f:
            labels = pickle.load(f)
            labels = {v: k for k, v in labels.items()}
        is_labels_loaded = True
    except:
        is_labels_loaded = False
load_labels_pickle()

# create text to speech
engine = pyttsx3.init("dummy")
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

# Define camera and detect face
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# Define pysimplegui setting
sg.theme("LightGrey1")

# execute query_str and return the result
def query(query_str: str, query_params: Optional[Union[dict, tuple]] = None, commit = False):
    try:
        print('Query string: ', textwrap.dedent(query_str))
        if query_params is None:
            cursor.execute(textwrap.dedent(query_str))
        else:
            print('Query params: ', query_params)
            cursor.execute(textwrap.dedent(query_str), query_params)
        if commit: 
            myconn.commit()
        if cursor.description is None: 
            return []
        cols = [col[0] for col in cursor.description]
        result = [dict(zip(cols, row)) for row in cursor.fetchall()]
        print('Query result: ', result)
        return result
    except Exception as e:
        print(f'Query exception: ', e)
        return []

# When called, shows the welcome window
# Return the account dict if sign in is successful
def welcome_window() -> dict:
    # Initial welcome screen
    layout =  [
        [sg.Text('Welcome!', font=('Any', 18))],
        [sg.Text("Please sign in or sign up via face capture.", size=50, font=('Any', 10))],
        # for showing if sign up is successful or not
        [sg.Text("", key="MESSAGE", font=('Any', 8), text_color='black')],
        [sg.Button("Sign in"), sg.Button(button_text="Sign up")]]
    win = sg.Window('Attendance System - Sign in',
            default_element_size=(21,1),
            text_justification='c',
            element_justification='c',
            auto_size_text=True,
            layout=layout,
            auto_size_buttons=True,
            size=(500, 180))
    while True:
        event, values = win.Read()
        if event is None or event =='Cancel':
            win.close()
            exit()
        elif event == "Sign in":
            if not is_labels_loaded or not is_recognizer_loaded:
                win["MESSAGE"].update(f"Face recognition has not been set up yet. Please create an account.", text_color='red')
                continue
            face_detection_result = face_detection_window()
            if type(face_detection_result) == str:
                win["MESSAGE"].update(f"Sign in failed: {face_detection_result}", text_color='red')
            elif type(face_detection_result) == dict:
                win.close()
                return face_detection_result
        elif event == "Sign up":
            sign_up_window()
        else:
            raise Exception(f"Unexpected welcome_window event value: {event}.")

def sign_up_window():
    layout =  [
        [sg.Text('UID*', font=('Any', 10))],
        [sg.Input('', key="UID_INPUT")],
        [sg.Text('Email*', font=('Any', 10))],
        [sg.Text('Must match the registered email.', font=('Any', 6))],
        [sg.Input('', key="EMAIL_INPUT")],
        [sg.Text('Display name', font=('Any', 10))],
        [sg.Text('Default: your full name.', font=('Any', 6))],
        [sg.Input('', key="ACCOUNT_NAME_INPUT")],
        [sg.Text('', key="MESSAGE", font=('Any', 10), text_color='red')],
        [sg.OK(button_text="Sign up")]
    ]
    win = sg.Window('Attendance System - Sign up',
        default_element_size=(21,1),
        auto_size_text=True,
        layout=layout,
        auto_size_buttons=True,
        size=(600, 300))
    while True:
        event, values = win.Read()
        if event is None or event =='Cancel':
            win.close()
            return
        # must be the button text of the OK button
        elif event == "Sign up":
            account_name = values["ACCOUNT_NAME_INPUT"]
            try:
                uid = int(values["UID_INPUT"])
            except:
                win['MESSAGE'].update('UID must be an integer.', text_color='red')
                continue
            email = values["EMAIL_INPUT"]
            if email == "" or email is None:
                win['MESSAGE'].update('Email must not be empty.', text_color='red')
                continue

            # check if uid and email are correct
            student_query_result = query(
                """
                SELECT full_name 
                FROM Personnel 
                WHERE is_student=1
                    AND uid=%s
                    AND registered_email=%s
                """, 
                (uid, email)
            )
            if len(student_query_result) == 0:
                win['MESSAGE'].update("Incorrect UID or email.", text_color='red')
                continue
            student = student_query_result[0]
            print('student: ', student)
            
            # if account name is empty, fill it with student's full name
            if account_name == "" or account_name is None:
                account_name = student['full_name']

            # check if an account of the student already exists
            account_query_result = query(
                """
                SELECT COUNT(*)
                FROM Account
                WHERE uid=%s
                """, 
                (uid,)
            )
            if account_query_result[0]['COUNT(*)'] != 0:
                win['MESSAGE'].update(f'An account of UID {uid} already exists.', text_color='red')
                continue

            # check if an account of the same account name already exists
            account_query_result = query(
                """
                SELECT COUNT(*)
                FROM Account
                WHERE account_name=%s
                """, 
                (account_name,)
            )
            if account_query_result[0]['COUNT(*)'] != 0:
                win['MESSAGE'].update(f'{account_name} has been used by another student already.', text_color='red')
                continue

            if account_name == "" or account_name is None:
                account_name = student['full_name']
            # try to capture the face
            win['MESSAGE'].update('Please wait for face capture and training.', text_color='grey')
            try:
                face_capture(account_name, video_capture=cap)
            except: 
                win['MESSAGE'].update('Error when attempting to capture face.', text_color='red')
                continue
            try:
                train_model()
                load_labels_pickle()
                load_recognizer()
            except: 
                win['MESSAGE'].update('Error when training model.', text_color='red')
                continue
            query(
                'INSERT INTO Account (uid, account_name, creation_date) VALUES (%s, %s, %s)',
                (uid, account_name, datetime.now()),
                commit=True
            )
            win['MESSAGE'].update(f'Account {account_name} has been created successfully.', text_color='green')

# Try to open a window and capture user's face to get the user's identity
# If capturing failed, returns failed reason as str
# If capturing is successful, returns account dict
def face_detection_window() -> Union[str, dict]:
    win = None
    # 4 Open the camera and start face recognition
    for _ in range(FACE_DETECT_TIMEOUT):
        ret, frame = cap.read()
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except:
            return "Failed to start video capturing. Please check if camera is connected."
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            # predict the id and confidence for faces
            id_, conf = recognizer.predict(roi_gray)

            # If the face is recognized
            if conf >= FACE_DETECT_CONFIDENCE:
                # print(id_)
                # print(labels[id_])
                font = cv2.QT_FONT_NORMAL
                id = 0
                id += 1
                account_name = labels[id_]
                current_name = account_name
                color = (255, 0, 0)
                stroke = 2
                cv2.putText(frame, account_name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

                # Find the student information in the database.
                result = query(
                    """
                    SELECT account_name, uid
                    FROM Account 
                    WHERE account_name=%s
                    """, (account_name,)
                )

                # If the student's information is not found in the database
                if len(result) == 0:
                    # the student's data is not in the database
                    if win is not None: 
                        win.close()
                    return f"The student {current_name} is not found in the database."

                # If the student's information is found in the database
                else:
                    if win is not None: 
                        win.close()
                    return result[0]

        # GUI
        imgbytes = cv2.imencode('.png', frame)[1].tobytes() 
        if win is None:
            layout = [
                [sg.Image(data=imgbytes, key='_IMAGE_')]
            ]
            win = sg.Window('ICMS - Face capture',
                    default_element_size=(14, 1),
                    text_justification='right',
                    auto_size_text=False).Layout(layout).Finalize()
            image_elem = win.FindElement('_IMAGE_')
        else:
            image_elem.Update(data=imgbytes)
        event, values = win.Read(timeout=20)
        if event is None:
            win.close()
            break
    win.close()
    return "Cannot recognize your face."

#function to update the table value
def update_ttb(uid:int,start_hour:int ,end_hour:int,date_of_week):
    weekday=[1,2,3,4,5,6,7]

    times=[]
    for i in range (start_hour,end_hour+1):
        times.append("{hour}:30:00".format(hour=i))
    
    
    ttb_values=[[" "for i in range(len(weekday)+1)] for j in range(len(times)+1)] 

    ttb_values[0]=[" ",str(date_of_week[0])[:10],str(date_of_week[1])[:10],str(date_of_week[2])[:10],str(date_of_week[3])[:10],
                 str(date_of_week[4])[:10],str(date_of_week[5])[:10],str(date_of_week[6])[:10]]

    for i in range (len(times)):
        ttb_values[i+1][0]= str(times[i])[:-3]

    for i in range (len(weekday)):
        for j in range (len(times)):
            find_course="""
            SElECT C.code,C.title,CC.type,CC.venue,CC.start_time,CC.end_time
            FROM CourseClass CC,Course C,CourseEnrollment CE
            WHERE C.course_id=CE.course_id AND CC.course_id=C.course_id 
            AND CC.weekday=%s AND CC.start_time=%s
            AND CE.uid =%s
            """
            val=(weekday[i],times[j],uid)
            
            cursor.execute(find_course,val)
            result=cursor.fetchall()

            if result:
                Course_code=str(result[0][0])
                Course_title=result[0][1]
                Course_type=result[0][2]
                venue=result[0][3]
                start_times=str(result[0][4])
                end_time=str(result[0][5])
                output=(Course_code+'-----'+Course_type).center(30)+'\n'+Course_title.center(30)+'\n'+venue.center(30)+'\n'+(start_times+'---'+end_time).center(30)
                ttb_values[j+1][i+1]=output
                while (j!=len(times) and end_time>times[j]):
                    ttb_values[j+1][i+1]=output
                    j+=1
    
    return ttb_values

# window post login
def main_window(account: dict):
    login_time = time.time()
    uid = account['uid']
    account_name = account['account_name']
    query(
        """
        UPDATE Account
        SET last_login_date=%s
        WHERE account_name=%s
        """,
        (datetime.now(), account_name),
        commit=True
    )

    hello = ("Hello ", uid, "You did attendance today")
    print(hello)
    engine.say(hello)

    #get the date of this week starting from monday
    today=date.today()
    date_of_week=[today-timedelta(days=today.weekday())]
    for i in range (1,7):
        date_of_week.append(date_of_week[0]+timedelta(days=i))
    
    #the default hour is 8
    start_hour=8
    #the default hour is 18
    end_hour=18
    

    # GUI
    home_layout = [
        [sg.Text(f"Welcome, {account_name}!", size=20, font=('Any', 18))],
        [sg.Text('Upcoming Lecture:')]
    ]

    #timetable GUI
    ttb_values=update_ttb(uid,start_hour,end_hour,date_of_week)
    ttb_heading=['Times','[Monday] ','[Tuesday] ','[Wednesday] ','[Thurday] ',
                 '[Friday] ','[Saturday] ','[Sunday] ']
    
    tbl1=sg.Table(values=ttb_values,headings=ttb_heading,
                  col_widths=[8,18,18,18,18,18,18,18],
                  auto_size_columns=False,
                  display_row_numbers=False,
                  justification='center',
                  key="-TimeTable-",
                  num_rows=12,
                  row_height=70)
    
    timetable_layout = [
        [sg.Text('Course Timetable'),sg.Button("< previous 7 days"),sg.Text("The week from {0} to {1}".format(str(date_of_week[0])[:10],str(date_of_week[6])[:10]),key="-Week-"),sg.Button("next 7 days >")],
        [sg.Text('Starting Hour: '),sg.Input("8",key='-Start_Hour-',size=(3,1)),sg.Text('Ending Hour: '),sg.Input("18",key='-End_Hour-',size=(3,1)),sg.Button('Change Time'),sg.Text(" ",key='-Error-')],
        [tbl1]]

    #main_layout
    main_layout = [
        [sg.TabGroup([[
            sg.Tab('Home', home_layout),
            sg.Tab('Course Timetable', timetable_layout)
        ]])]
    ]
    win = sg.Window(
        f"ICMS - {account_name}", 
        main_layout, 
        size=(1300, 600), 
        auto_size_buttons=True, 
        auto_size_text=True
    )

    while True:
        event, values = win.read()
        if event is None or event == 'Close':
            # write the login duration
            query(
                """
                UPDATE Account
                SET last_login_duration=%s
                WHERE account_name=%s
                """,
                (time.time() - login_time, account['account_name']),
                commit=True
            )
            break

        #ttb event handler
        elif event == 'Change Time':
            try:
                start_hour=int(values['-Start_Hour-'])
                end_hour=int(values['-End_Hour-'])
                if start_hour in range(0,25) and end_hour in range(0,25):
                    if int(start_hour)<int(end_hour):
                        ttb_values=update_ttb(uid,start_hour,end_hour,date_of_week)
                        win['-TimeTable-'].update(values= ttb_values)
                        win['-Error-'].update(" ")
                    else:
                        win['-Error-'].update("Starting hour must be smaller than Ending hour")
                else:
                    win['-Error-'].update("invalid input, Please input number from 0 to 24")
            except:
                win['-Error-'].update("Please input [0-24] in both box")
            

        elif event == "< previous 7 days":
            for i in range (7):
                date_of_week[i]=(date_of_week[i]-timedelta(days=7))
            ttb_values=update_ttb(uid,int(start_hour),int(end_hour),date_of_week)
            win['-TimeTable-'].update(values= ttb_values)
            win['-Week-'].update("The week from {0} to {1}".format(str(date_of_week[0])[:10],str(date_of_week[6])[:10]))

        elif event=="next 7 days >":
            for i in range (7):
                date_of_week[i]=(date_of_week[i]+timedelta(days=7))
            ttb_values=update_ttb(uid,int(start_hour),int(end_hour),date_of_week)
            win['-TimeTable-'].update(values= ttb_values)
            win['-Week-'].update("The week from {0} to {1}".format(str(date_of_week[0])[:10],str(date_of_week[6])[:10]))

    win.close()
    exit()

def main():
    account = welcome_window()

    main_window(account)
    cap.release()
    myconn.close()

if __name__ == "__main__":
    main()