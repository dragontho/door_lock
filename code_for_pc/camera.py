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
    print("processing images of owner")
    list_of_images = os.listdir("images")
    for image in list_of_images:
        load_name = constants_name[image]
        load_image = face_recognition.load_image_file("images/" + image)
        image_encoding = face_recognition.face_encodings(load_image)[0]
        constants_known_face_encoding.append(image_encoding)
        constants_known_face_names.append(load_name)
    print("finished processing images of owners")

# start the camera
class Camera:

    def __init__(self):
        print("Starting camera for facial recognition")
        self.video_capture = cv2.VideoCapture(0)
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        self.is_running = True
        self.open_door = False

    def run(self):
        # returns the name of the first person on the list and a boolean whether the door opens
        start_time = time.time()
        end_time = time.time()

        while self.is_running and end_time - start_time < 10:
            # get a single frame of video
            ret, frame = self.video_capture.read()

            # resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # only process every other frame of video to save time
            if self.process_this_frame:
                self.get_face_names(rgb_small_frame)
            self.process_this_frame = not self.process_this_frame

            person_name = self.check_person()
            self.display_image(frame)

            self.quit()
            if self.open_door:
                cv2.imwrite("client.png", frame)

            end_time = time.time()
        return (person_name, self.open_door)

    def check_person(self):
        person_name = ""
        for name in self.face_names:
            if name is not "Unknown":
                self.is_running = False
                self.open_door = True
                person_name = name
        return person_name

    def get_face_names(self, rgb_small_frame):
        # find all the faces and face encodings in the current frame of video
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

        self.face_names = []
        for face_encoding in self.face_encodings:
            # see if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(constants_known_face_encoding, face_encoding)
            name = "Unknown"

            # if a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = constants_known_face_names[first_match_index]

            self.face_names.append(name)

    def display_image(self, frame):
        # display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # display the resulting image
        cv2.imshow('Facial Recognition', frame)

    def quit(self):
        # hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.is_running = False

    def __del__(self):
        print("Closing camera")
        self.video_capture.release()
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
