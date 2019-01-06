import platform
from pi_transmissions import *
from internet import *
import time

pc = platform.architecture()
if pc[0] == '64bit':
    from dev import *
else:
    from lock import *

def main():
    # setup packages
    pi_node = PI_Node()
    initalize_pins()

    is_running = True
    while is_running:
        if check_motion():

            # send signal that person is close by
            motion_signal_stuck = True
            while motion_signal_stuck:
                try:
                    pi_node.signal_motion()
                    motion_signal_stuck = False
                except ConnectionRefusedError:
                    time.sleep(0.5)
                    print("Connecting to pc server 1")

            verified_signal_stuck = True
            is_verified = False
            while verified_signal_stuck:
                try:
                    is_verified = pi_node.is_owner_face_and_password_verified()
                    verified_signal_stuck = False
                except ConnectionRefusedError:
                    time.sleep(0.5)
                    print("Connecting to pc server 2")

            if is_verified:
                # received signal of door state
                door_signal_stuck = True
                door_state = 0
                while door_signal_stuck:
                    try:
                        door_state = pi_node.signal_door_state()
                        door_signal_stuck = False
                    except ConnectionRefusedError:
                        time.sleep(0.5)
                        print("Connecting to pc server 3")
                if door_state:
                    open_door()
                    door_signal_stuck = True
                    door_state = 0
                    while door_signal_stuck:
                        try:
                            door_state = pi_node.signal_door_state()
                            door_signal_stuck = False
                        except ConnectionRefusedError:
                            time.sleep(0.5)
                            print("Connecting to pc server 4")
                    if not door_state:
                        close_door()
                else:
                    close_door()

if __name__ == "__main__":
    response = test_internet_connectivity()
    if response:
        try:
            main()
        except:
            pi_cleanup()
    else:
        print("You need internet connection")
    try:
        main()
    except:
        pi_cleanup()

