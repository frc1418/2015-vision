import cv2
import numpy as np


def threshold_range(im, lo, hi):
    unused, t1 = cv2.threshold(im, lo, 255, type=cv2.THRESH_BINARY)
    unused, t2 = cv2.threshold(im, hi, 255, type=cv2.THRESH_BINARY_INV)
    return cv2.bitwise_and(t1, t2)

def detect_black(img):
    #convert the color to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #split into images for each of those variables
    h, s, v = cv2.split(hsv)
    #look for a certain range of each variable
    '''
    h = threshold_range(h, 0, 256)
    cv2.imshow('h', h)
    '''
    s = threshold_range(s, 55, 255)
    #cv2.imshow('s', s)
    v = threshold_range(v, 0, 20)
    #cv2.imshow('v', v)
    #combine each of those images
    combined = cv2.bitwise_and(s,v)
    #cv2.imshow('Combined', combined)

    #find contours on the image
    trash, contours, hierarchy = cv2.findContours(combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #get the raw coordinates of the contour and determine which side of the image it is on
    leftCounter = 0
    rightCounter = 0
    #image size 240X160 pixels halfway 120 pixels
    for contour in range(0, len(contours)):
        c = contours[contour]
        for co in range(0, len(c)):
            con = c[co]
            for cont in range(0, len(con)):
                conto = con[cont]
                xcoord = conto[0]
                if xcoord > 120:
                    rightCounter = rightCounter + 1
                elif xcoord <= 120:
                    leftCounter = leftCounter + 1
    #create booleans to tell which side has more detected black on it default false
    leftside = False
    rightside = False

    if leftCounter >= rightCounter:
        leftside = True
    if rightCounter >= leftCounter:
        rightside = True
    return leftside, rightside


#img = cv2.imread("GreenBinPhotos/Bin4.jpg")
#detect_black(img)
