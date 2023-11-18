# Real-Time Facial Recognition Attendance System

This repository contains the code for a real-time facial recognition attendance system. The system utilizes OpenCV, face_recognition library, and Firebase for storage. The project involves three main scripts: `Main.py`, `AddToDataBase.py`, and `EncodingGenerator.py`.

## Overview

The project has the following components:

- **Main.py**: This script is the core of the real-time facial recognition system. It uses a webcam feed to detect faces, match them with pre-encoded faces, and manage attendance records in the Firebase database.

- **AddToDataBase.py**: This script populates the Firebase database with student information and uploads their images to Firebase storage.

- **EncodingGenerator.py**: This script generates face encodings for the student images provided, using the `face_recognition` library, and stores these encodings in a pickle file.

## Usage

1. Run the following file to generate face encodings for the images provided in the 'images' folder:

    ```bash
    EncodingGenerator.py
    ```

2. Execute the below file to populate the Firebase database with student information and upload their images to Firebase storage:

    ```bash
    AddToDataBase.py
    ```

3. Start the real-time facial recognition system by running the following file. This script uses the webcam to detect faces, match them with stored encodings, and manage attendance records in Firebase:

    ```bash
    Main.py
    ```
   
**Note**: Ensure to update the Firebase credentials in the scripts (`Main.py`, `AddToDataBase.py`) with your own credentials to connect to your Firebase project.
