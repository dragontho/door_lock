from camera import *
from generator import *
from internet import *
from password import *
from scanner import *
import time
import keyboard
from pc_transmissions import *
from internet import *

def main():
    get_owner_image_encoding()
    pc_node = PC_Node()
    is_running = True
    while is_running:
        # if motion is detected, start the camera
        if pc_node.signal_motion():
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
                # if password is verified, open the door
                time.sleep(1)
                if is_password_verified:
                    print("send signal to open door")
                    try:
                        pc_node.signal_door_state("1")
                        start_time = time.time()
                        end_time = time.time()
                        # if door open more than 1 min, automatically close the door
                        while end_time - start_time > 60:
                            if keyboard.is_pressed('q'):
                                break
                        print("send signal to close door")
                        pc_node.signal_door_state("0")
                    except ConnectionRefusedError:
                        print("Did you ensure the pi server is up?")

if __name__ == "__main__":
    response = test_internet_connectivity()
    if response:
        main()
    else:
        print("You need internet connection")
    main()
