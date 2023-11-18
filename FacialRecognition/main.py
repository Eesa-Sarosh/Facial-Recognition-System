import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://faceattendancerealtime-252f7-default-rtdb.firebaseio.com/',
    'storageBucket': "faceattendancerealtime-252f7.appspot.com"
})

bucket = storage.bucket()

capture = cv2.VideoCapture(0)

imgBackground = cv2.imread('recources/bck1.png')

#importing background images in a list
FolderPath = 'recources/modes'
ModesPathList = os.listdir(FolderPath)
ImgList = []
for path in ModesPathList:
    ImgList.append(cv2.imread(os.path.join(FolderPath, path)))
#print(len(ImgList))

#Loading Encoding file
file = open("EncodeFile.p", "rb")
EncodedListWithIDs = pickle.load(file)
file.close()
EncodedList, StudentIDS = EncodedListWithIDs
#print(StudentIDS)

modeType = 0
counter = 0
studentInfo = " "
StudentImage = []
while True:
    success, img = capture.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    #Finding location of face in webcam
    FaceCurrentFrame = face_recognition.face_locations(imgS)
    EncodeCurrentFrame = face_recognition.face_encodings(imgS, FaceCurrentFrame)


    imgBackground[85:85+480, 20:20+640] = img
    imgBackground[0:0+1080, 700:700 + 720] = ImgList[modeType]

    if FaceCurrentFrame: # if a face is detected then do all the process
        for encodeFace, faceLoc in zip(EncodeCurrentFrame, FaceCurrentFrame):
            matches = face_recognition.compare_faces(EncodedList, encodeFace)
            FaceDistance = face_recognition.face_distance(EncodedList, encodeFace)
            print("matches", matches)
            print("Distance", FaceDistance)

            MinIndex = np.argmin(FaceDistance)

            if matches[MinIndex]:
                #print("Known Face Detected")
                #print(StudentIDS[MinIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                #had to add 20 and 85 because the image starts from there
                bbox = 20 + x1, 85 + y1, x2-x1, y2-y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=1, colorR=(0, 255, 0), colorC=(0, 0, 0))
                id = StudentIDS[MinIndex]
                #we only want to download data from database when we detect a known face
                if counter == 0:
                    modeType = 1
                    counter = 1

        if counter != 0:
            #downloading data only 1 time
            if counter == 1:
                studentInfo = db.reference(f'Students/{id}').get()
                blob = bucket.get_blob(f'images/{id}.jpg')
                array =np.frombuffer(blob.download_as_string(), np.uint8)
                StudentImage = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                #update attendance
                last_time = datetime.strptime(studentInfo['last_attendance'],
                                             "%Y-%m-%d %H:%M:%S")
                TotalSecondsElapsed = (datetime.now() - last_time).total_seconds()
                if TotalSecondsElapsed > 25:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] = studentInfo['total_attendance'] + 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[0:0 + 1080, 700:700 + 720] = ImgList[modeType]

            if modeType != 3: #Checking if already not marked
                #change mode type to marked
                if counter>=10 and counter<20:
                    modeType = 2
                    imgBackground[0:0 + 1080, 700:700 + 720] = ImgList[modeType]
                #print data when you detect face
                if counter < 10:
                    cv2.putText(imgBackground, f'Name: {studentInfo["name"]}', (750, 200),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)
                    cv2.putText(imgBackground, f'Major: {studentInfo["major"]}', (750, 250),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)
                    cv2.putText(imgBackground, f'Starting Year: {studentInfo["starting_year"]}', (750, 300),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)
                    cv2.putText(imgBackground, f'Total Attendance: {studentInfo["total_attendance"]}', (750, 350),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)
                    imgBackground[400:400+216, 820:820 + 216] = StudentImage

                counter = counter + 1
                #after marking reset everything
                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    StudentImage = []
                    imgBackground[0:0 + 1080, 700:700 + 720] = ImgList[modeType]
    else:
        counter = 0
        modeType = 0
    cv2.imshow('Face Attendance', imgBackground)
    cv2.waitKey(1)