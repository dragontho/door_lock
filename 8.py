import face_recognition
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

print("Loading known face image(s)")
obama_image = face_recognition.load_image_file("images/obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)
 
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    image = cv2.resize(image, (0, 0), fx=1, fy=1)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([obama_face_encoding], face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = constants_known_face_names[first_match_index]

        face_names.append(name)
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 1
        right *= 1
        bottom *= 1
        left *= 1
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)



 
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
 
    rawCapture.truncate(0)
    if key == ord("q"):
        break
