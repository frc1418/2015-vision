import cv2
import numpy as np
import networktables

def threshold_range(im, lo, hi):
    unused, t1 = cv2.threshold(im, lo, 255, type=cv2.THRESH_BINARY)
    unused, t2 = cv2.threshold(im, hi, 255, type=cv2.THRESH_BINARY_INV)
    return cv2.bitwise_and(t1, t2)

def detect_black(img):
    
    width = img.shape[0]
    
    #convert the color to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #split into images for each of those variables
    h, s, v = cv2.split(hsv)
    #look for a certain range of each variable
    '''
    h = threshold_range(h, 0, 256)
    cv2.imshow('h', h)
    '''
    s = threshold_range(s, 10, 160)
    #cv2.imshow('s', s)
    v = threshold_range(v, 0, 120)
    #cv2.imshow('v', v)
    #combine each of those images
    combined = cv2.bitwise_and(s,v)
    #cv2.imshow('combined', combined)

    #find contours on the image
    trash, contours, hierarchy = cv2.findContours(combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #get the raw x coordinate of each point in the contour and then take the average
    #of those points to find the center
    xCoordTotal = 0
    xCoordCounter= 0
    goodContours = []
    biggestArea = 0
    biggestContour = []
    for contour in range(0, len(contours)):
        contourArea = cv2.contourArea(contours[contour])
        if contourArea >= (width*2):
            if contourArea > biggestArea:
                biggestArea = contourArea
                biggestContour = contours[contour]
            c = contours[contour]
            goodContours.append(c)
            for co in range(0, len(c)):
                con = c[co]
                for cont in range(0, len(con)):
                    conto = con[cont]
                    xcoord = conto[0]
                    xCoordTotal = xCoordTotal + xcoord
                    xCoordCounter = xCoordCounter + 1
    if xCoordCounter != 0:
        xCoordAverage = xCoordTotal/xCoordCounter
    else:
        xCoordAverage = 1
    #create a value between -1 & 1. -1 being left. 1 being right
    if len(biggestContour) > 0:
        x, y, w, h = cv2.boundingRect(biggestContour)
    else:
        x, y, w, h = 0, 0, 0, 0
    rectangle = [x, y, x + w, y, x + w, y + h, x, y +h]
    coordinates = networktables.NumberArray()
    for i in range(0, len(rectangle)):
        coordinates.append(rectangle[i])
    centerValue = (xCoordAverage-(width/2))/(width/2)
    cv2.drawContours(img, goodContours, -1, (0, 0, 255), 3)
    return centerValue, coordinates




#img = cv2.imread("GreenBinPhotos/Bin12.jpg")
#detect_black(img, 240)
