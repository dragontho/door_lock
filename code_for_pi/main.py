from camera import *
from generator import *
from internet import *
from password import *
from scanner import *
import time
from internet import *
from constants import *
from lock import *

def main():
    # setting up necessary packages
    rpi = RPI()
    rpi.close_door()
    get_owner_image_encoding()

    is_running = True
    while is_running:

        # if motion is detected, start the camera
        if rpi.check_motion():
            camera = Camera()
            open_door_data = camera.run()
            owner = open_door_data[0]
            is_owner_known = open_door_data[1]
            del camera

            print("owner %s is verified" % owner)

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
                    rpi.open_door()
                    time.sleep(10)
                    rpi.close_door()
                    rpi.warm_up()
                else:
                    rpi.close_door()
                    rpi.warm_up()
            else:
                rpi.close_door()
                rpi.warm_up()

if __name__ == "__main__":
    response = test_internet_connectivity()
    if response == 0:
        print("Welcome to my Door Assistant")
        main()
    else:
        print("You need internet connection")
