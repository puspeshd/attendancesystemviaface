import numpy as np
import face_recognition 
import os
from datetime import datetime, time
import cv2
from _datetime import date
from dateutil.utils import today
import pandas as pd
import webbrowser
from tkinter import *
from tkinter import Radiobutton
 
path = 'imgs/'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

 
def findEncodings(images):
 encodeList = []
 for img in images:
  # print(img)     
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  encode = face_recognition.face_encodings(img)[0]
  encodeList.append(encode)
 return encodeList

 
def markAttendance(name):
 with open('Attendance.csv', 'r+') as f:
     myDataList = f.readlines()
     
     if(len(myDataList) == 0):
         f.writelines("Name, TIME AND DATE")
     nameList = []
     namel = []
     for line in myDataList:
         entry = line.split(',')
         nameList.append(entry)
         namel.append(entry[0])
     print(nameList)  
     print(namel)  
     if  name not in namel:
          now = datetime.now()
          dtString = now.strftime('%H:%M::%S %D')
          f.writelines(f'\n{name},{dtString}')
   

encodeListKnown = []
encodeListKnown = findEncodings(images)
print('Encoding Complete')
cont = True
while(cont == True):
    
    def positiveresponse():
        cap = cv2.VideoCapture(0)
        success, img = cap.read()
        
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
         
        facesCurFrame = face_recognition.face_locations(imgS)
        matches = [] 
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
       
            matchIndex = np.argmin(faceDis)
         
            if matches[matchIndex]:
             name = classNames[matchIndex].upper()
             now = datetime.now()
             dtn = now.strftime('%H_%M_%d_%m_%y')
             name1 = name + f'  ATTENDANCE MARKED SUCCESSFULLY  @ {dtn}'
             print(name1)       
             y1, x2, y2, x1 = faceLoc
             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
             cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
             cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
    
             cv2.putText(img, name1 , (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2) 
             markAttendance(name)
             root.destroy()
         
        cv2.imshow('Webcam', img)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        
        def savefile(): 
            csv = pd.read_csv('Attendance.csv')
            now = datetime.now()
            dts = now.strftime('%H_%M_%d_%m_%y')
            csv.to_html(f'attendance/Attendance_{dts}.html')
            webbrowser.open(f'C:/users/puspesh-deolal/desktop/att sys/attendance/Attendance_{dts}.html')
            with open('Attendance.csv', 'r+') as f:
                showcsv = f.readlines()
                f.close()

                def exitfunc():
                    with open('Attendance.csv', 'w') as f:
                      f.close()
                    exit()
                
                
                    
            root1.destroy()    
            
            
            cont = False    
            exitfunc()    
            
                
        root1 = Tk()
        root1.geometry("450x450")
        var1 = StringVar()
        bgimg = PhotoImage(file="bg2.png")
        Label(root1, image=bgimg).pack()
        Label(root1, text=" ").place(x=10, y=15)
        Label(root1, text="YOU CAN CHECK REPORTS IN ATTENDANCE FOLDER...........\nCLICK YES TO MARK MORE ATTENDANCES, NO TO EXIT AND SAVE THE FILE").place(x=10, y=20)
        Radiobutton(root1, text="YES", value="yes", variable=var1, command=root1.destroy,indicator=0).place(x=10, y=60)
        Radiobutton(root1, text="NO", value="no", variable=var1, command=savefile,indicator=0).place(x=10, y=80)
        root1.mainloop()
            
        # opt=input('Do you want to continue? Y or N')
        # if(opt!='Y' or opt!='y'):
             
    root = Tk()
    root.geometry("450x450")
    var = StringVar()
    bgimg1 = PhotoImage(file="bg1.png")
    Label(root, image=bgimg1).pack()
    Label(root, text="CLICK YES if you are ready to mark the attendance.Be in front of Camera\n and rest will be done ",bd="4").place(x=2, y=10)
    Button(root, text="YES", command=positiveresponse,bd="4").place(x=2, y=60)
           
    root.mainloop()
    
