import face_recognition
import cv2
import os
import time
from constants import *
from internet import *

# image encoding of person
constants_known_face_encoding = []
# name of person
constants_known_face_names = []

# get encodings of the images of person
def get_owner_image_encoding():
    print("processing images")
    list_of_images = os.listdir("images")
    for image in list_of_images:
        load_name = constants_name[image]
        load_image = face_recognition.load_image_file("images/" + image)
        image_encoding = face_recognition.face_encodings(load_image)[0]
        constants_known_face_encoding.append(image_encoding)
        constants_known_face_names.append(load_name)
    print("finished processing images")

# start the camera
class Camera:

    def __init__(self):
        print("Starting camera for facial recognition")
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.open_door = False

    def run(self):
        start_time = time.time()
        end_time = time.time()
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            image = cv2.resize(image, (0, 0), fx=1, fy=1)
            self.face_locations = face_recognition.face_locations(image)
            self.face_encodings = face_recognition.face_encodings(image, self.face_locations)
            self.face_names = []
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(constants_known_face_encoding, face_encoding)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = constants_known_face_names[first_match_index]

                self.face_names.append(name)
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 1
                right *= 1
                bottom *= 1
                left *= 1
                cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            cv2.imshow("Facial Recognition", image)
            rawCapture.truncate(0)
            self.quit()
            person_name = self.check_person()
            end_time = time.time()
            if (self.open_door or (end_time - start_time > 60)):
                break

        return (person_name, self.open_door)

    def check_person(self):
        person_name = ""
        for name in self.face_names:
            if name is not "Unknown":
                self.open_door = True
                person_name = name
        return person_name

    def quit(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.is_running = False

    def __del__(self):
        print("Closing camera")
        cv2.destroyAllWindows()

if __name__ == "__main__":
    response =  test_internet_connectivity()
    if response == 0:
        print("internet connection is up")
        get_owner_image_encoding()
        camera = Camera()
        open_door_data = camera.run()
        if open_door_data[1]:
            print("door is opening")
            print("Welcome " + open_door_data[0])
        else:
            print("door will not open")
    else:
        print("internet connection is down")
