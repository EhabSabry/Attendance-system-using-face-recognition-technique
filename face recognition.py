# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 23:09:15 2022

@author: IEEE
"""
import face_recognition
import os
import cv2
import numpy as np
import datetime
import smtplib
from pynput.keyboard import Key , Controller
import time

path='faces'
images = []
peoplenames = []
images_list = os.listdir(path)
print("\n")
print('THOSE ARE THE IMAGES NAMES:',images_list)
print("\n************************************************************")

for c1 in images_list:
    current_img = cv2.imread(f'{path}/{c1}')
    images.append(current_img)
    peoplenames.append(os.path.splitext(c1)[0])
print("PEOPLE NAMES ARE: ",peoplenames)
print("\n************************************************************")

#ENDCODING FUNCTION
def findencodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist


#SENDING MAILS FUNCTION
def sendingmails(name,date):
    
    gmail_user = 'mezo.messi36@gmail.com'
    gmail_password = 'puppkcembjijsuvo'

    sent_from = gmail_user
    to = ['ehabsabrygomaa@gmail.com']
    subject = 'Your employee is arrived right now!'
    body = '%s ARRIVED AT %s' %(name,date)

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print ('Email sent!')
    except:
        print ('Something went wrong...')




#ATTENDANCE FUNCTION
def markattendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            #DELAY TIME
        if name not in nameList:
            attenTime = datetime.datetime.now().time()
            timein = datetime.time(16, 00, 00)

            delay = datetime.timedelta(hours=(attenTime.hour - timein.hour), minutes=(attenTime.minute - timein.minute),
                                       seconds=(attenTime.second - timein.second))
            if attenTime > timein:

                f.writelines(f'\n{name},{attenTime},{delay}')
                # CALLING OF sendingmails FUNCTION
                sendingmails(name, attenTime)

            else:
                f.writelines(f'\n{name},{attenTime},{0}')
                sendingmails(name, attenTime)




known_encodes_list = findencodings(images)
print('THIS IS THE LENGTH OF THE ENCODED IMAGES:',len(known_encodes_list))
print("\n************************************************************")


#Taking an image from a camera to be matched with the image we have in our dataset
cap = cv2.VideoCapture(1)

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame, 1)
    small_frame = cv2.resize(frame,(0,0),None,0.25,0.25)
    small_frame = cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)
    
    faces_current_location = face_recognition.face_locations(small_frame)
    encodes_current_frame = face_recognition.face_encodings(small_frame,faces_current_location)
    
    
    for encodeface,facelocation in zip(encodes_current_frame,faces_current_location):
        matches = face_recognition.compare_faces(known_encodes_list, encodeface)
        Error = face_recognition.face_distance(known_encodes_list, encodeface)
        print("THIS IS THE MATCHING ERROR:",Error)
        print("\n************************************************************")
        matchindex = np.argmin(Error)
        
        if matches[matchindex]:
            name = peoplenames[matchindex].upper()
            print ("THIS IS THE NAME OF THE PERSON IN OUR VIDEO: ",name)
            
            y1,x2,y2,x1 = facelocation
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4 
            cv2.rectangle(frame,(x1+4, y1), (x2, y2+4),(0,255,0),2)
            cv2.rectangle(frame,(x1, y2+27), (x2+16, y2),(0,255,0),cv2.FILLED)
            cv2.putText(frame, name, (x1+3, y2+27), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            
            #CALLING OF markattendance FUNCTION
            markattendance(name)
    
        
        #DETECTING THE UNKNOWN PERSON
        else:
            img_counter = 1
            print("THIS IS THE NAME OF THE PERSON IN OUR VIDEO: unknown ")
            y1, x2, y2, x1 = facelocation
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(frame, (x1+4, y1), (x2, y2+4), (0, 0, 255), 2)
            cv2.rectangle(frame, (x1, y2+27), (x2+16, y2),(0,0, 255), cv2.FILLED)
            cv2.putText(frame, 'UNKNOWN', (x1+3, y2+27),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            #AUTOMATIC PRESS ON A KEY FROM THE KEYBOARD
            keyboard = Controller()
            time.sleep(0)
            keyboard.press("s")
            keyboard.release("s")
            
            #SAVING THE UNKNOWN PERSON'S IMAGE
            if cv2.waitKey(1) ==ord("s"):
                img_name = 'UNKNOWN{}.png'.format(img_counter)
                cv2.imwrite(img_name, frame)
                print("A photo is taken for an unkown person")
                img_counter+=1
            
            
        
    cv2.imshow('our camera',frame)
    if cv2.waitKey(1)==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    