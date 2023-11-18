import firebase_admin
from firebase_admin import credentials, db, storage
import os

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://faceattendancerealtime-252f7-default-rtdb.firebaseio.com/',
    'storageBucket': "faceattendancerealtime-252f7.appspot.com"
})

ref = db.reference('Students')

data = {
    '100': {
        "name": "Eesa Sarosh",
        "major": "Computer Science",
        "starting_year": "2020",
        "last_attendance": "2023-1-1 00:00:00",
        "total_attendance": 4
    },
    '101': {
            "name": "Cristiano Ronaldo",
            "major": "Electrical Engineer",
            "starting_year": "2018",
            "last_attendance": "2023-1-1 00:00:00",
            "total_attendance": 6
        },
    '102': {
            "name": "Lionel Messi",
            "major": "Computer Science",
            "starting_year": "2021",
            "last_attendance": "2023-1-1 00:00:00",
            "total_attendance": 1
        },
}

#we use child to create a directory and using set to send values in that directory
for key, value in data.items():
    ref.child(key).set(value)

#importing images in a list
FolderPathImages = 'images'
PathList = os.listdir(FolderPathImages)
#uploading images to database
for path in PathList:
    fileName = f'{FolderPathImages}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
