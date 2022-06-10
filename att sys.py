import numpy as np
import face_recognition 
import os
from datetime import datetime, time
import cv2
from _datetime import date
from dateutil.utils import today
import pandas as pd

# from PIL import ImageGrab
 
path = 'C:/Users/Puspesh Deolal/Desktop/att sys/imgs/'
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
  #print(img)     
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  encode = face_recognition.face_encodings(img)[0]
  encodeList.append(encode)
 return encodeList
 
def markAttendance(name):
 with open('Attendance.csv','r+') as f:
     myDataList = f.readlines()
     if(len(myDataList)==0):
         f.writelines("Name, TIME AND DATE")
     nameList = []
     namel=[]
     for line in myDataList:
         entry = line.split(',')
         nameList.append(entry)
         namel=entry[0]
     print(nameList)    
     if  name not in namel:
          now = datetime.now()
          dtString = now.strftime('%H:%M::%S %D')
          f.writelines(f'\n{name},{dtString}')
 
#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300))
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr
encodeListKnown=[]
encodeListKnown = findEncodings(images)
print('Encoding Complete')
cont=True
while(cont==True):
    x=input("Input y to capture face")
    
    if(x=='y' or x=='Y'):
        cap = cv2.VideoCapture(0)
        
        
        success, img = cap.read()
        #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
         
        facesCurFrame = face_recognition.face_locations(imgS)
        matches=[] 
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
        
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
            matchIndex = np.argmin(faceDis)
         
            if matches[matchIndex]:
             name = classNames[matchIndex].upper()
             name1=name+'ATTENDANCE MARKED SUCCESSFULLY  @'
        #print(name)
             y1,x2,y2,x1 = faceLoc
             y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
             cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
             cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
             cv2.putText(img,name1 ,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2) 
             markAttendance(name)
         
        cv2.imshow('Webcam',img)
        cv2.waitKey(30) & 0xff
        opt=input('Do you want to continue? Y or N')
        if(opt=='Y'):
            continue
        else:
            csv=pd.read_csv('Attendance.csv')
            csv.to_html('Attendance.html')
            with open('Attendance.csv','w') as f:
                f.close()
            cont=False    