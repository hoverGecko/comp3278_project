import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys
import PySimpleGUI as sg
from typing import Optional, Union, List, Tuple
from face_capture import face_capture
from train import train as train_model
import textwrap

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
recognizer.read("train.yml")

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

# create text to speech
engine = pyttsx3.init("dummy")
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

# Define camera and detect face
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# Define pysimplegui setting
sg.theme("LightGrey1")

# When called, shows the welcome window
# Return the user name if sign in is successful
def welcome_window() -> str:
    # Initial welcome screen
    layout =  [
        [sg.Text('Welcome!', size=(18,1), font=('Any', 18))],
        [sg.Text("Please sign in or sign up via face capture.", size=50, font=('Any', 10))],
        # for showing if sign up is successful or not
        [sg.Text("", key="MESSAGE", size=200, font=('Any', 8), text_color='black')],
        [sg.Button("Sign in"), sg.Button(button_text="Sign up")]]
    win = sg.Window('Attendance System - Sign in',
            default_element_size=(21,1),
            text_justification='c',
            element_justification='c',
            auto_size_text=False,
            layout=layout,
            size=(500, 180))
    while True:
        event, values = win.Read()
        if event is None or event =='Cancel':
            win.close()
            exit()
        elif event == "Sign in":
            sign_in_successful, user_name = face_detection_window()
            if not sign_in_successful:
                win["MESSAGE"].update(f"Sign in failed: {user_name}", text_color='red')
            elif sign_in_successful:
                win.close()
                return user_name
        elif event == "Sign up":
            sign_up_successful, user_name = sign_up_window()
            if not sign_up_successful:
                win["MESSAGE"].update(f"Account creation failed: {user_name}", text_color='red')
            elif sign_up_successful:
                if user_name == None:
                    continue
                else:
                    win["MESSAGE"].update(f"New account {user_name} has been created.", text_color='green')
        else:
            raise Exception(f"Unexpected welcome_window event value: {event}.")

# Return [True, user name] if sign up is successful
# Return [False, failed reason] if sign up failed
# Return [True, None] if user cancelled sign up
def sign_up_window() -> Tuple[bool, Optional[str]]:
    layout =  [
        [sg.Text('Name (must be in student database)', size=30, font=('Any', 10))],
        [sg.Input('', enable_events=True, key="USER_NAME_INPUT")],
        # [sg.Text('Confidence'), sg.Slider(range=(0,100),orientation='h', resolution=1, default_value=60, size=(15,15), key='confidence')],
        [sg.OK(button_text="Sign up")]
    ]
    win = sg.Window('Attendance System - Sign up',
        default_element_size=(21,1),
        text_justification='c',
        element_justification='c',
        auto_size_text=False,
        layout=layout,
        size=(400, 100))
    while True:
        event, values = win.Read()
        if event is None or event =='Cancel':
            win.close()
            return (True, None)
        # must be the button text of the OK button
        elif event == "Sign up":
            user_name = values["USER_NAME_INPUT"]
            # if account does not exist in DB, sign up fails
            # else
            try:
                face_capture(user_name, video_capture=cap)
            except: 
                win.close()
                return (False, 'Error when attempting to capture face.')
            try:
                train_model()
            except: 
                win.close()
                return (False, 'Error when training model.')
            win.close()
            return (True, user_name)

# Try to open a window and capture user's face to get the user's identity
# If capturing failed, returns [False, failed reason]
# If capturing is successful, returns [True, user_name]
def face_detection_window() -> Tuple[bool, str]:
    win = None
    # 4 Open the camera and start face recognition
    for _ in range(FACE_DETECT_TIMEOUT):
        ret, frame = cap.read()
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except:
            print("Failed to start video capturing. Please check if camera is connected.")
            exit(-1)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            print(x, w, y, h)
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
                name = labels[id_]
                current_name = name
                color = (255, 0, 0)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

                # Find the student information in the database.
                select = "SELECT student_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Student WHERE name='%s'" % (name)
                name = cursor.execute(select)
                result = cursor.fetchall()
                # print(result)
                data = "error"

                for x in result:
                    data = x

                # If the student's information is not found in the database
                if data == "error":
                    # the student's data is not in the database
                    if win is not None: 
                        win.close()
                    return (False, f"The student {current_name} is not found in the database.")

                # If the student's information is found in the database
                else:
                    if win is not None: 
                        win.close()
                    return (True, current_name)

            # If the face is unrecognized
            # else: 
            #     color = (255, 0, 0)
            #     stroke = 2
            #     font = cv2.QT_FONT_NORMAL
            #     cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            #     hello = ("Your face is not recognized")
            #     print(hello)
            #     engine.say(hello)
            #     # engine.runAndWait()

        # GUI
        imgbytes = cv2.imencode('.png', frame)[1].tobytes() 
        if win is None:
            layout = [
                [sg.Image(data=imgbytes, key='_IMAGE_')]
            ]
            win = sg.Window('Attendance System - Face capture',
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
    return (False, "Cannot recognize your face.")

# window post login
def main_window(user_name: str):
    display_name = user_name.capitalize()
    """
    Implement useful functions here.
    Check the course and classroom for the student.
        If the student has class room within one hour, the corresponding course materials
            will be presented in the GUI.
        if the student does not have class at the moment, the GUI presents a personal class 
            timetable for the student.

    """
    update =  "UPDATE Student SET login_date=%s WHERE name=%s"
    val = (date, user_name)
    cursor.execute(update, val)
    update = "UPDATE Student SET login_time=%s WHERE name=%s"
    val = (current_time, user_name)
    cursor.execute(update, val)
    myconn.commit()

    hello = ("Hello ", user_name, "You did attendance today")
    print(hello)
    engine.say(hello)

    # GUI
    home_layout = [
        [sg.Text(f"Welcome, {display_name}!", size=20, font=('Any', 18))],
        [sg.Text('Upcoming Lecture:')]
    ]
    timetable_layout = [[sg.Text('Course Timetable')]]
    main_layout = [
        [sg.TabGroup([[
            sg.Tab('Home', home_layout),
            sg.Tab('Course Timetable', timetable_layout)
        ]])]
    ]
    win = sg.Window(f"Attendance system - {display_name}", main_layout, size=(1000, 400))
    while True:
        event, values = win.read()
        if event is None or event == 'Close':
            break
    win.close()
    exit()

def main():
    user_name = welcome_window()
    main_window(user_name)
    cap.release()

if __name__ == "__main__":
    main()