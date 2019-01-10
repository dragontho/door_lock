import RPi.GPIO as GPIO
import time

class RPI:

    def __init__(self):
        print("pins are initialized")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(13, GPIO.OUT) # pin for red led
        GPIO.setup(15, GPIO.OUT) # pin for green led
        GPIO.setup(7, GPIO.OUT) # pin for servo
        GPIO.output(13, GPIO.HIGH)
        self.servo = GPIO.PWM(7,50)
        self.servo.start(12.5)

    def check_motion(self):
        user_input = input("motion detected? Enter 'y' for yes")
        if user_input == 'y' or user_input == 'Y':
            return True
        else:
            return False

    def open_door(self):
        GPIO.output(13, GPIO.LOW) 
        GPIO.output(15, GPIO.HIGH)
        print("door is opening")
        self.servo.ChangeDutyCycle(12.5)
        time.sleep(1)

    def close_door(self):
        GPIO.output(15, GPIO.LOW) 
        GPIO.output(13, GPIO.HIGH) 
        print("door is closing")
        self.servo.ChangeDutyCycle(7.5)
        time.sleep(1)

    def __del__(self):
        self.servo.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        rpi = RPI()
        while True:
            rpi.open_door()
            rpi.close_door()
    except KeyboardInterrupt:
        del rpi


    """
    while True:
        rpi.open_door()
        rpi.close_door()
        """


