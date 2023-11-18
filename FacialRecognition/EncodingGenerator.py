import cv2
import face_recognition
import pickle
import os

#importing images in a list
FolderPathImages = 'images'
PathList = os.listdir(FolderPathImages)
ImgLists = []
StudentIDS = []
for path in PathList:
    ImgLists.append(cv2.imread(os.path.join(FolderPathImages, path)))
    StudentIDS.append(os.path.splitext(path)[0])


def FindEncodings(imageslist):
    encodeList = []
    for img in imageslist:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

EncodedList = FindEncodings(ImgLists)
EncodedListWithIDs = [EncodedList, StudentIDS]

file = open("EncodeFile.p", "wb")
pickle.dump(EncodedListWithIDs, file)
file.close()