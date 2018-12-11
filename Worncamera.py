from picamera import PiCamera
from time import sleep
import sys  # System bindings
import cv2 # OpenCV bindings
import numpy as np
from PIL import Image
import os
import math

#Camera stuff

counter=0

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

# Use TM locate ROI
def Template_Matching(img, temp):
    row, col = temp.shape[:-1]

    img_copy = img.copy()
    method = 'cv2.TM_SQDIFF_NORMED'
    method = eval(method)
    res = cv2.matchTemplate(img_copy, temp, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = min_loc
    bottom_right = (top_left[0] + row + 300, top_left[1] + col - 200)

    return top_left, bottom_right


#3.Convert the picture to binary and grayscale
def convertBinaryEven(nametext):
    image = cv2.imread(nametext)
    temp = cv2.imread("TemplateDownWorn.jpg")
    top_left, bottom_right = Template_Matching(image, temp)
    original = cv2.imread(nametext)
    image = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    ##cv2.imwrite("Template" + nametext,image)
    im_gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #adaptive thresholding
    im_at = cv2.adaptiveThreshold(im_gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 15)
    ##cv2.imwrite('adaptive' + nametext, im_at)


    #Morphology
    erode_kernel = np.ones((2,2), np.uint8)
    dilate_kernel = np.ones((3,3), np.uint8)

    erosion = cv2.erode(im_at, erode_kernel, iterations=1)
    dilation = cv2.dilate(erosion, dilate_kernel, iterations=1)
    ##cv2.imwrite('morpho' + nametext, dilation)
    
    ##contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
##
##    cont = dilation
    
    ##cv2.drawContours(dilation ,contours,-1,(0,255,0),2)

    ##cv2.imwrite('democontour' + nametext, dilation)
    
##    ret,thresh1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
##    (thresh, im_bw) = cv2.threshold(im_gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
####        cv2.imwrite("gray"+nametext, im_gray)
####        cv2.imwrite("bw" + nametext, thresh1)
##
##
##    imgray = cv2.cvtColor(thresh1,cv2.COLOR_BGR2GRAY)    
##    ret,thresh = cv2.threshold(imgray,127,255,0)
##    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
##        
##    cv2.drawContours(thresh1 ,contours,-1,(0,255,0),2)
##
##    ##cv2.circle(im,(750,350),3,(255,0,0),-1,8)
##    ##cv2.circle(im,(750,700),3,(255,0,0),-1,8)
##    ##cv2.circle(im,(1100,350),3,(255,0,0),-1,8)
##    ##cv2.circle(im,(1100,700),3,(255,0,0),-1,8)
##
##    ##cv2.imwrite("OddContour.jpg", thresh1)
##
    edges = cv2.Canny(dilation, 100, 255)  
    indices = np.where(edges != [0])
    coordinates = zip(indices[0], indices[1])
    #print(coordinates)
    pointer_lst = []
    row_number = 0
    
    for i in range(len(coordinates)-2):
        if (coordinates[i+1][0] != coordinates[i+2][0]):
            if (abs(coordinates[i][1] < 500) and coordinates[i+1][1] > coordinates[i][1] ):
                pointer_lst.append([coordinates[i+1][0],coordinates[i+1][1]])
                


    slope_lst = []
    for p in range(len(pointer_lst)-1):
        y_difference = float(pointer_lst[p+1][1] - pointer_lst[p][1])
        x_difference = float(pointer_lst[p+1][0] - pointer_lst[p][0])
        slope = float(y_difference/x_difference)
        if(abs(slope) < 10 and abs(slope) > 0.5):
            slope_lst.append(abs(slope))

    AvgSlope = np.mean(slope_lst)
    Angle = 90-(180*math.atan(AvgSlope)/math.pi)

    
    #print(str(Angle) + nametext)
        
            
    ##print(slope_lst)

            
    ##cv2.imwrite("Contour" + nametext, thresh1)
    text = "The slope is "
    text += str(AvgSlope)
    text2 = "The Angle we are measuring is "
    text2 += str(Angle)
    text3 = "The result is: "
    if (Angle < 22):
        text3 += "Inspection Failed!"
    else:
        text3 += "Inspection Passed!"

        
    
    cv2.putText(original,text2, (50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
    cv2.putText(original,text3, (50,150),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
    ##cv2.putText(original,text, (50,250),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
    cv2.imwrite("Result" + nametext, original)



################################
def convertBinaryOdd(nametext):
    image = cv2.imread(nametext)
    temp = cv2.imread("TemplateUpWorn.jpg")
    top_left, bottom_right = Template_Matching(image, temp)
    original = cv2.imread(nametext)
    image = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    ##cv2.imwrite("Template" + nametext,image)

    im_gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #adaptive thresholding
    im_at = cv2.adaptiveThreshold(im_gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 15)
    ##cv2.imwrite('adaptive' + nametext, im_at)


    #Morphology
    erode_kernel = np.ones((2,2), np.uint8)
    dilate_kernel = np.ones((3,3), np.uint8)

    erosion = cv2.erode(im_at, erode_kernel, iterations=1)
    dilation = cv2.dilate(erosion, dilate_kernel, iterations=1)
    ##cv2.imwrite('morpho' + nametext, dilation)

    ##contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    ##cv2.drawContours(dilation ,contours,-1,(0,255,0),2)

    ##cv2.imwrite('democontour' + nametext, dilation)
    
##    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

##    cont = dilation
    
##    cv2.drawContours(dilation, contours,-1,(0,255,0),2)
##
##    cv2.imwrite('contour' + nametext, dilation)
    
##    ret,thresh1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
##    (thresh, im_bw) = cv2.threshold(im_gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
####        cv2.imwrite("gray"+nametext, im_gray)
####        cv2.imwrite("bw" + nametext, thresh1)
##
##
##    imgray = cv2.cvtColor(thresh1,cv2.COLOR_BGR2GRAY)    
##    ret,thresh = cv2.threshold(imgray,127,255,0)
##    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
##        
##    cv2.drawContours(thresh1 ,contours,-1,(0,255,0),2)

    ##cv2.circle(im,(750,350),3,(255,0,0),-1,8)
    ##cv2.circle(im,(750,700),3,(255,0,0),-1,8)
    ##cv2.circle(im,(1100,350),3,(255,0,0),-1,8)
    ##cv2.circle(im,(1100,700),3,(255,0,0),-1,8)

    ##cv2.imwrite("EvenContour.jpg", thresh1)

    edges = cv2.Canny(dilation, 100, 255)  
    indices = np.where(edges != [0])
    coordinates = zip(indices[0], indices[1])
    #print(coordinates)
    pointer_lst = []
    row_number = 0

    for i in range(len(coordinates)-2):
        if (coordinates[i+1][0] != coordinates[i+2][0]):
            
            if (abs(coordinates[i][1] < 500) and coordinates[i+1][1] > coordinates[i][1] ):
                pointer_lst.append([coordinates[i+1][0],coordinates[i+1][1]])


    slope_lst = []
    for p in range(len(pointer_lst)-1):
        y_difference = float(pointer_lst[p+1][1] - pointer_lst[p][1])
        x_difference = float(pointer_lst[p+1][0] - pointer_lst[p][0])
        slope = float(y_difference/x_difference)
        if(abs(slope) < 10 and abs(slope) > 0.5):
            slope_lst.append(abs(slope))

    AvgSlope = np.mean(slope_lst)
    Angle = 90-(180*math.atan(AvgSlope)/math.pi)

    
    #print(Angle)
##    print("coordinate: ", coordinates)
##    
##    print("ptrlst: ", pointer_lst)

    
            
    ##cv2.imwrite("Contour" + nametext, dilation)
    text = "The slope is "
    text += str(AvgSlope)
    text2 = "The Angle we are measuring is "
    text2 += str(Angle)
    text3 = "The result is: "
    if (Angle < 22):
        text3 += "Inspection Failed!"
    else:
        text3 += "Inspection Passed!"

        
    
    cv2.putText(original,text2, (50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
    cv2.putText(original,text3, (50,150),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
    ##cv2.putText(original,text3, (50,250),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
    cv2.imwrite("Result" + nametext, original)
##



#################################

##i = 1
##while(i < 32):     
##    textname = "test"
##    textname += str(i)
##    textname += ".jpg"
##    convertBinaryOdd(textname)
##    i += 2
##
##
##j = 0
##while(j < 31):     
##    textname = "test"
##    textname += str(j)
##    textname += ".jpg"
##    convertBinaryEven(textname)
##    j += 2



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

##
##    cv2.startWindowThread()
##    cv2.namedWindow("ImageWindow")
##    cv2.imshow('ImageWindow', im)
    
    cv2.imwrite('sideWorn_bw_image_contour.png', im)

