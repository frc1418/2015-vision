import cv2
import numpy as np
import drawImage as di


def approxListPolyDP(contours, epsilon, closed):
    outputList = []
    for i in range(0, len(contours)):
        current = contours[i]
        for x in range(0, len(current)):
            outputList.append(cv2.approxPolyDP(current[x], epsilon, closed))
    return outputList

def filterApproxList(inputList):
    outputList = []
    #print len(inputList)
    for i in range(0, len(inputList)):
        if len(inputList[i]) == 6:
            outputList.append(inputList[i])
    return outputList

def findContourTape(Image, contours):
    polyLayer = approxListPolyDP(contours, 4, False)

    filteredPolyLayer = filterApproxList(polyLayer)

    di.drawContoursList(Image, filteredPolyLayer, -1, (0,0,255), 1)

    #Resizes the quantified image so that it is easy to see
    newImage = cv2.resize(Image, (1150,600))

    #Shows the final product
    cv2.imshow("image", newImage)
