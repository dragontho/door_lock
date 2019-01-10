import RPi.GPIO as GPIO
import time
import serial

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
        self.ser = serial.Serial('/dev/ttyACM0')
        self.motion_detect = False

    def warm_up(self):
        start = time.time()
        end = time.time()
        while (end - start < 2):
            raw_distance = self.ser.readline()
            end = time.time()

    def check_motion(self):
        try:
            raw_distance = self.ser.readline()
            distance = float(raw_distance.decode('utf-8'))
            print(distance)
            if distance < 25.0:
                self.motion_detect = True
        except ValueError:
            print("no reading recorded")
        return self.motion_detect

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
        self.motion_detect = False

    def __del__(self):
        self.servo.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        rpi = RPI()
        while True:
            #rpi.open_door()
            #rpi.close_door()
            rpi.check_motion()
    except KeyboardInterrupt:
        del rpi
