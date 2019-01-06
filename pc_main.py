from camera import *
from generator import *
from internet import *
from password import *
from scanner import *
import time
from pc_transmissions import *
from internet import *

def main():
    # setting up necessary packages
    get_owner_image_encoding()
    pc_node = PC_Node()

    is_running = True
    while is_running:

        # if motion is detected, start the camera
        motion_signal_stuck = True
        motion_detected = False
        while motion_signal_stuck:
            try:
                motion_detected = pc_node.signal_motion()
                motion_signal_stuck = False
            except ConnectionRefusedError:
                time.sleep(0.5)
                print("Connecting to pi server 1")
            except OSError:
                time.sleep(0.5)
                print("Connecting to pi server 1")

        if motion_detected:
            camera = Camera()
            open_door_data = camera.run()
            owner = open_door_data[0]
            is_owner_known = open_door_data[1]
            del camera

            # if owner is known, send qrcode otp to owner gmail
            if is_owner_known:
                token = mkpassword()
                create_qr_code(token)
                send_password = Password(owner)
                send_password.run()
                qrscanner = QRScanner(token)
                is_password_verified = qrscanner.run()
                del qrscanner

                verified_signal_stuck = True
                while verified_signal_stuck:
                    try:
                        pc_node.is_owner_face_and_password_verified(is_owner_known, is_password_verified)
                        verified_signal_stuck = False
                    except ConnectionRefusedError:
                        time.sleep(0.5)
                        print("Connecting to pi server 2")

                # if password is verified, open the door
                if is_password_verified:
                    door_signal_stuck = True
                    print("send signal to open door")
                    while door_signal_stuck:
                        try:
                            pc_node.signal_door_state("1")
                            door_signal_stuck = False
                        except ConnectionRefusedError:
                            time.sleep(0.5)
                            print("Connecting to pi server 3")
                    start_time = time.time()
                    end_time = time.time()

                    # if door open more than 1 min, automatically close the door
                    while end_time - start_time < 30:
                        end_time = time.time()
                    print("send signal to close door")
                    door_signal_stuck = True
                    while door_signal_stuck:
                        try:
                            pc_node.signal_door_state("0")
                            door_signal_stuck = False
                        except ConnectionRefusedError:
                            time.sleep(0.5)
                            print("Connecting to pi server 4")
            else:
                verified_signal_stuck = True
                while verified_signal_stuck:
                    try:
                        pc_node.is_owner_face_and_password_verified(False, False)
                        verified_signal_stuck = False
                    except ConnectionRefusedError:
                        time.sleep(0.5)
                        print("Connecting to pi server 2")

if __name__ == "__main__":
    response = test_internet_connectivity()
    if response:
        main()
    else:
        print("You need internet connection")
    main()
