from time import sleep
import RPi.GPIO as GPIO

#setup GPIO
GPIO.setmode(GPIO.BOARD)
trigger = 35
direction = 36
MS1 = 37
MS2 = 38
GPIO.setup(trigger, GPIO.OUT, initial = 0)
GPIO.setup(direction, GPIO.OUT, initial = 0)
# CONTROLS STEP SIZE:
# MS1 LOW + MS2 LOW = FULL STEP
# MS1 HIGH + MS2 LOW = HALF STEP
GPIO.setup(MS1, GPIO.OUT, initial = 0)
GPIO.setup(MS2, GPIO.OUT, initial = 1)
#Stepper control function

#0 is Clockwise, 1 is Counter-Clockwise
def rotate_motor(steps = 267, rotation = 0):
    if (rotation == 1):
        GPIO.output(direction, GPIO.HIGH)
    else:
        GPIO.output(direction, GPIO.LOW)
    for i in range(steps):
        # Do the desired number of steps
        GPIO.output(trigger, GPIO.HIGH)
        sleep(0.001)
        GPIO.output(trigger, GPIO.LOW)
        sleep(0.01)
    return

for i in range(3):
    #camera.capture(name)
    rotate_motor(267,0)
    sleep(1)
#Always do this when using GPIO pins!
GPIO.cleanup()


print("Exiting...")
