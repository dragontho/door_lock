def initalize_pins():
    print("pins are initialized")

def open_door():
    print("door is opening")

def close_door():
    print("door is closing")

def check_motion():
    user_input = input("motion detected? Enter 'y' for yes")
    if user_input == 'y' or user_input == 'Y':
        return True
    else:
        return False

def pi_cleanup():
    print("shutting down")

