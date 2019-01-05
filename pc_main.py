from camera import *
from generator import *
from internet import *
from password import *
from scanner import *
import time
import keyboard

def main():
    get_owner_image_encoding()
    is_running = True
    while is_running:
        motion_detected = check_motion()
        # if motion is detected, start the camera
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
                # if password is verified, open the door
                if is_password_verified:
                    print("send signal to open door")
                    start_time = time.time()
                    end_time = time.time()
                    # if door open more than 1 min, automatically close the door
                    while end_time - start_time > 60:
                        if keyboard.is_pressed('q'):
                            break
                    print("send signal to close door")

if __name__ == "__main__":
    try:
        main()
    except:
        pi_cleanup()
