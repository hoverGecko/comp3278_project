import tkinter as tk
from tkinter import *
import mysql.connector
import webbrowser
import smtplib
from email.message import EmailMessage

mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="course_information"
)

def course_window(course_code):
    def send_email():
        email = email_entry.get()

        subject = "Course Details"
        message = f'''
            Course Code: {detail["course_code"]}\n\
            Course Name: {detail["course_name"]}\n\
            Course Venue: {detail["course_venue"]}\n\
            Teacher Message{detail["teacher_message"]}\n
        '''
        for n in notes_link:
            message += n[3] + ': ' + n[2] + '\n'
        for z in zoom_link:
            message += z[3] + ': ' + z[2] + '\n'

        FROM_EMAIL = "comptemp66@gmail.com" 
        PASSWORD = "ecsp jndp mpbm tqzf"  

        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subject 
        msg['From'] = FROM_EMAIL
        msg['To'] = email

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(FROM_EMAIL, PASSWORD)
                smtp.send_message(msg)
        except Exception as e:
            print("Error:", e)

    cursor = mydb.cursor()

    sql = f'''
    SELECT * FROM Course WHERE course_id = {course_code}
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        course = [x for x in row]
    print('course',  course)

    sql = f'''
    SELECT * FROM CourseClass WHERE course_id = {course_code}
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        course_class = [x for x in row]
    print('course_class', course_class)

    sql = f'''
    SELECT * FROM CourseResource WHERE course_id = {course_code}
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    course_resource_all = []
    for row in rows:
        course_resource = [x for x in row]
        course_resource_all.append(course_resource)
    print('course_resource', course_resource)

    detail = {
        'course_code': course[2], 
        'course_name': course[1], 
        'teacher_message': course[3],
        'course_venue': course_class[3], 
    }

    window = Tk()
    window.title('Course Details')
    window.config(bg = 'white')
    window.geometry("600x600")
    bg_image = PhotoImage(file='hku.png')
    label = Label(window, image=bg_image)
    label.place(x=0, y=0, relwidth=1, relheight=1)

    title_bar = Label(window, text="Course Details", bg="light green", fg="white", font=("Arial",30,"bold"), width=150) 
    title_bar.pack(anchor='w', pady=15)

    label_font = ("Times New Roman", 25)

    for x in detail:
        label = Label(text = f'{x}: ' + str(detail[x]), font = label_font)
        label.pack(anchor='w', pady = 10)

    zoom_link = []
    notes_link = []
    for course_resource in course_resource_all:
        if course_resource[1] == 'notes':
            notes_link.append(course_resource)
        elif course_resource[1] == 'zoom':
            zoom_link.append(course_resource)

    label = Label(text = 'Notes Links', font = ("Times New Roman", 25, 'bold'))
    label.pack(anchor='w', pady = 10)

    for n in notes_link:
        frame = Frame(window)
        frame.pack(anchor = 'w')
        label = Label(frame, text = n[3] + ':  ', font = ('Times New Roman', 15))
        label.pack(anchor = 'w', side = 'left', pady = 5)
        button = Button(frame, text = n[2], font = ('Times New Roman', 15), command = lambda link=n[2]: webbrowser.open(link))
        button.pack(anchor = 'w', side = 'left', pady = 5)

    label = Label(text = 'Zoom Links', font = ("Times New Roman", 25, 'bold'))
    label.pack(anchor='w', pady = 10)

    for z in zoom_link:
        frame = Frame(window)
        frame.pack(anchor = 'w')
        label = Label(frame, text = z[3] + ':  ', font = ('Times New Roman', 15))
        label.pack(side='left', pady = 5)
        button = Button(frame, text = z[2], font = ('Times New Roman', 15), command = lambda link=z[2]: webbrowser.open(link))
        button.pack(side = 'left', pady = 5)
    
    email_entry = Entry(window)
    email_entry.pack()

    button = Button(text = 'Send Email', command = send_email)
    button.pack(anchor = 'center')


    window.mainloop()


course_window(2)

