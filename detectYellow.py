import cv2
import numpy as np

def threshold_range(im, lo, hi):
    unused, t1 = cv2.threshold(im, lo, 255, type=cv2.THRESH_BINARY)
    unused, t2 = cv2.threshold(im, hi, 255, type=cv2.THRESH_BINARY_INV)
    return cv2.bitwise_and(t1, t2)
'''def findContoursList(inputList, mode, method):
    outputList = []
    for i in range(0, len(inputList)):
        outputList.append(cv2.findContours(inputList[i].copy(), mode, method)[1])
    return outputList'''



cam = cv2.VideoCapture(0)
running = True
while(running):


    frame = cam.read()[1]
    img = frame

    #cv2.imshow('img', img)
    oimg = img.copy()
    #bgr = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv)

    h = threshold_range(h, 14, 59)
    #cv2.imshow('h', h)
    s = threshold_range(s, 57, 255)
    #cv2.imshow('s', s)
    v = threshold_range(v, 49, 255)
    #cv2.imshow('v', v)

    combined = cv2.bitwise_and(h, cv2.bitwise_and(s,v))
    #cv2.imshow('Combined', combined)
    img2 = combined.copy()

    trash, contours, hierarchy = cv2.findContours(combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    #cv2.imshow('contouryb4', oimg)
    #makes contours into polygons
    p = []

    for contour in range(0, len(contours)):
        t = cv2.approxPolyDP(contours[contour], 100, True)
        #print t
        p.append(t)
    bp = 0
    pp = []
    #Sorts small  groups and shows biggest polygon
    #print len(p), 'plength'
    for contour in range(0, len(p)):
        ap = cv2.arcLength(p[contour], True)
        if ap > 400:
            pp.append(p[contour])

    #print pp
        #print ap
    #x, y, xlen, ylen = cv2.boundingRect(pp)
    #print pp
    '''if cv2.arcLength(p[contour], True) > 300:
        nContours.append(p[contour])'''


    cv2.drawContours(oimg, pp, -1,(0,0,255), 3)
    cv2.imshow('contoury', oimg)
    if cv2.waitKey(1)  & 0xFF == ord('q'):
        break

cam.releas()
cv2.destroyAllWindows()
