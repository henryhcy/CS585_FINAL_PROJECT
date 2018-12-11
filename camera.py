from picamera import PiCamera
from time import sleep
import sys  # System bindings
import cv2 # OpenCV bindings
import numpy as np
from PIL import Image
import os




#Camera stuff

counter=0

camera = PiCamera()
camera.start_preview(fullscreen=False, window = (100, 20, 640, 480))
sleep(10)
camera.close()

def reset():
    counter = 0


#1.Open Camera
def openCamera():
    camera = PiCamera()
    camera.rotation = 0
    camera.start_preview(fullscreen=False, window = (100, 50, 640, 480))
    sleep(10)
    #camera.stop_preview()
    camera.close()

#2.Take Picture
def takePicture():
    camera = PiCamera()
    camera.rotation = 180
    camera.start_preview()
    sleep(10)
    name = "test" + str(counter) + ".jpg"
    camera.capture(name)
    counter+=1
    camera.stop_preview()



#3.Convert the picture to binary and grayscale
def convertBinary():
    if __name__ == "__main__":
        image = cv2.imread('lightworn.jpg')
        im_gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (thresh, im_bw) = cv2.threshold(im_gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cv2.imwrite('side_New_im_gray.png', im_gray)
        cv2.imwrite('side_New_bw_image.png', im_bw)



#4.Find the coordniates at the edge/contour
def findContour():
    img = cv2.imread('side_New_bw_image.png', 0)
    edges = cv2.Canny(img, 100, 255)  
    indices = np.where(edges != [0])
    coordinates = zip(indices[0], indices[1])
    print(coordinates)

#5.Draw the Contour for binary image Green as new Red as used
def drawContour():
    im = cv2.imread('side_Worn_bw_image.png')
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(im,contours,-1,(0,0,255),2)

    #5.1Write text on image
    cv2.putText(im,'Inspection pass!', (10,500),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    #5.2Draw a point on image
    cv2.circle(im,(324,31),3,(0,255,0),-1,8)

    cv2.circle(im,(303,64),3,(0,255,0),-1,8)

    slope = float(64-31)
    slope = float(slope/21)

    print(slope)

    message = "The slope is: "
    message += str(slope)

    cv2.putText(im,message, (150,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)


    cv2.startWindowThread()
    cv2.namedWindow("ImageWindow")
    cv2.imshow('ImageWindow', im)
    cv2.imwrite('sideWorn_bw_image_contour.png', im)

