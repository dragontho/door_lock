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
    pi_node = PI_Node()
    initalize_pins()
    is_running = True
    while is_running:
        if check_motion():
            try:
                pi_node.signal_motion()
            except ConnectionRefusedError:
                print("Did you ensure the pc server is up?")
            if pi_node.signal_door_state():
                open_door()
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

