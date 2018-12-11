from Tkinter import *
from picamera import PiCamera
from time import sleep
from PIL import Image
import sys  # System bindings
import cv2 # OpenCV bindings
import numpy as np
import os
import RPi.GPIO as GPIO
import Worncamera
import psutil

GPIO.setmode(GPIO.BOARD)
trigger = 35
direction = 36
MS1 = 37
MS2 = 38
TX = 31
RX = 32
GPIO.setup(trigger, GPIO.OUT, initial = 0)
GPIO.setup(direction, GPIO.OUT, initial = 0)
GPIO.setup(TX, GPIO.OUT, initial = 0)
GPIO.setup(RX, GPIO.IN)

eighths = 0
quarters = 0
halfs = 0
fulls = 0

# CONTROLS STEP SIZE:
# MS1 LOW + MS2 LOW = FULL STEP
# MS1 LOW + MS2 HIGH = HALF STEP (? Actually quarter step according to sheet)
GPIO.setup(MS1, GPIO.OUT, initial = 0)
GPIO.setup(MS2, GPIO.OUT, initial = 1)
    
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

##Open camera function
def Start():
    camera = PiCamera()
    camera.start_preview(fullscreen=False, window = (100, 20, 640, 480))
    sleep(5)
    for i in range(33):
        name = "test" + str(i) + ".jpg"
        camera.capture(name)
        if(i%2 == 0):
            Worncamera.convertBinaryEven(name)
        else:
            Worncamera.convertBinaryOdd(name)

        size = 512, 512
        im = Image.open("Result"+name)
        im.thumbnail(size, Image.ANTIALIAS)
        im.show()
        sleep(2)
        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()
        StartMotor()
        sleep(1)
    camera.close()




##Start motor function
def StartMotor():
    rotate_motor(267,0)


##draw points/ output function
def Open():
    camera = PiCamera()
    camera.start_preview(fullscreen=False, window = (100, 50, 640, 480))
    sleep(10)
    camera.close()

def Calibrate():
    ## Start motor and ESP loop 
    ## Motor will run a full revolution to allow ESP to find maximum voltages.
    GPIO.output(MS1, GPIO.HIGH)
    GPIO.output(MS2, GPIO.LOW)
    
    GPIO.output(TX, GPIO.HIGH) ## High on the TX tells the ESP to start measuring.
    rotate_motor(300,0)
    
    GPIO.output(TX, GPIO.LOW) ## Low on the TX tells the ESP to stop measuring.
    ## Once the ESP has the maximum voltage,
    ## run the motor in quarter steps until the ESP sees the maximum (RX high)
    GPIO.output(MS1, GPIO.LOW)
    GPIO.output(MS2, GPIO.HIGH)
    while not GPIO.input(RX):
        rotate_motor(1,0)
    
    GPIO.output(MS1, GPIO.HIGH)
    GPIO.output(MS2, GPIO.HIGH)
    ## ESP will hold Pi's RX high until it sees the next link, when it will go low.
    global eighths
    global quarters
    global halfs
    global fulls
    
    eighths = 0
    quarters = 0
    halfs = 0
    fulls = 0
    while GPIO.input(RX):
        rotate_motor(1,0)
        eighths += 1
    print(eighths)
    ## record number of eighth steps in global variable.
    ## do math to see how many eighth, quarter, half, and full steps are needed.
    
    

 
window = Tk()
 
window.title("Chainsaw Inspection GUI")

lbl = Label(window, text="Welcome to the Chainsaw Inspection Device!", font=("Arial Bold", 10))
 
lbl.grid(column=0, row=0)


lbl2 = Label(window, text="", font=("Arial Bold", 10))

lbl2.grid(column=0, row=1)

btn1 = Button(window, text="Start",command=Start)
 
btn1.grid(column=0, row=2)

btn2 = Button(window, text="Open Camera",command=Open)

btn2.grid(column=0, row=3)

btn3 = Button(window, text="Calibrate (EXPERIMENTAL)",command=Calibrate)

btn3.grid(column=0, row=4)
##
##btn4 = Button(window, text="Convert Binary",command=ConvertBinary)
## 
##btn4.grid(column=0, row=5)
##
##btn5= Button(window, text="Draw Point",command=DrawPoint)
## 
##btn5.grid(column=0, row=6)
##
##btn6= Button(window, text="Reset",command=reset)
## 
##btn6.grid(column=0, row=7)


window.mainloop()
