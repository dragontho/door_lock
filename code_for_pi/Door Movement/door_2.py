#Servo_1 testing.

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#set up pin number
GPIO.setup(7, GPIO.OUT) #For motor

GPIO.setup(13, GPIO.OUT) #For LEDS
GPIO.setup(15, GPIO.OUT) #For LEDS

p = GPIO.PWM(7,50)
p.start(7.5)

try:
    while True:
        #Lets keep this as 7.5 and 13.5 for ChangeDutyCycle
        p.ChangeDutyCycle(7.5)
	GPIO.output(13, GPIO.HIGH) #turn on
	GPIO.output(15, GPIO.LOW) #turn off

        time.sleep(1)


        p.ChangeDutyCycle(13.5)
	GPIO.output(13, GPIO.LOW) #turn off
	GPIO.output(15, GPIO.HIGH) #turn on

        time.sleep(1)


#        p.ChangeDutyCycle(2.5)
 #       time.sleep(0.5)

except KeyboardInterrupt:
    p.stop()

    GPIO.cleanup()


