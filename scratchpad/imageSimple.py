from sklearn.cluster import MiniBatchKMeans
import numpy as np
import cv2
import sys

#Import other classes
import drawImage as di
import tapeContourFinder as tcf
import colorAverages as ca
import copy


#Function to filter lists into binary lists to find specific values
def listFilter(inputList, minValue, maxValue, blankValue, fillValue):
    outputList = []
    diff = maxValue-minValue
    t = 0
    for i in range(minValue, maxValue+1):
        outputList.append([])
        current = inputList.copy()
        if(i != 0):
            current[current != i] = 0
            current[current == i] = 1
        else:
            current[current != i] = 1
            current[current == i] = 0
        outputList[t].append(current)
        t += 1
    return outputList

#Function to covert quantified info back to see able image
def quantifyList(inputList, clt):
    outputList = []
    for i in range(0, len(inputList)):
        outputList.append(clt.cluster_centers_.astype("uint8")[inputList[i]])
    return outputList

#Function to reshape input images
def reshapeList(inputList, h, w, d):
    outputList = []
    for i in range(0, len(inputList)):
        outputList.append(inputList[i].reshape((h, w, d)))
    return outputList

#Function to cvt lists of images to diffrent colros
def cvtList(inputList, cvt):
    outputList = []
    for i in range(0, len(inputList)):
        outputList.append(cv2.cvtColor(inputList[i], cvt))
    return outputList

#Function to thresh a list of images
'''RETURNS THRESH ONLY'''
def threshList(inputList, thresh, maxValue, type):
    outputList = []
    for i in range(0, len(inputList)):
        outputList.append(cv2.threshold(inputList[i], thresh, maxValue, type)[1])
    return outputList

#Function to findcountours of a list of images
'''RETURNS CONTOURS ONLY'''
def findContoursList(inputList, mode, method):
    outputList = []
    for i in range(0, len(inputList)):
        outputList.append(cv2.findContours(inputList[i].copy(), mode, method)[1])
    return outputList



def run(content, showContours, findTape, showColors, waitTime, imageInput, running):

    #Creates global variables to fix the flickering bug
    pastContours = None
    blankContours = [[], [], [], []]

    while(running):
        #if it is image input leave the frame alone and run
        if imageInput:
            frame = content
        #If not image input pull one frame from the camera
        else:
            frame = content.read()[1]


        #pulls the origonal hieght
        OriginalSize = frame.shape[:2]

        #Resizes image to reduce processsing time
        image = cv2.resize(frame, (250, 100))

        #pulls the hieght and width from the image
        (h, w) = image.shape[:2]
        #grabs a copy of the original image for color averaging
        OriginalImage = copy.copy(image)
        #cv2.imshow("original Image", image)
        #Changes color to LAB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        #Reshapes into a two deminsional array
        image2D = image.reshape((image.shape[0] * image.shape[1], 3))

        # apply k-means using the specified number of clusters and
        # then create the quantized image based on the predictions
        clt = MiniBatchKMeans(n_clusters = 4)
        labels = clt.fit_predict(image2D)

        #Filters the labels list into 4 peices of 2 color
        layers = listFilter(labels,0,3,0,1)

        #Coverts back into image
        quantifiedLayers = quantifyList(layers, clt)
        quantifiedImage = clt.cluster_centers_.astype("uint8")[labels]

        #Reshapes the output back into a three demisional array
        quantifiedLayers = reshapeList(quantifiedLayers, h, w, 3)
        quantifiedImage = quantifiedImage.reshape((h, w, 3))

        #Converts from LAB to BGR
        #Contverts from BGR to gray-scale for findingcontours
        quantifiedLayers = cvtList(quantifiedLayers, cv2.COLOR_LAB2BGR)
        quantifiedImage = cv2.cvtColor(quantifiedImage, cv2.COLOR_LAB2BGR)


        #Convert Layers to Gray
        grayLayers = cvtList(quantifiedLayers, cv2.COLOR_BGR2GRAY)

        #Convert the layers to binary
        threshLayers = threshList(grayLayers, 100, 255, cv2.THRESH_BINARY)

        #Finds the contours of the output
        layerContours = findContoursList(threshLayers, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        #Tests if no contours then draws the last contours
        if layerContours == blankContours:
            if pastContours != None:
                layerContours = pastContours
        else:
            pastContours = layerContours
        abimg = cv2.imread('Images/BlackScreen.png')

        if len(layerContours) != 0:
            if showColors:
                contcopy = copy.copy(layerContours)
                #grayimg = cv2.cvtColor(OriginalImage, cv2.COLOR_BGR2GRAY)
                colors = ca.findColorAverages(OriginalImage, layerContours)
                ca.fillContours(abimg, contcopy, colors)


        if showContours:
            di.showContourImage(abimg, layerContours, OriginalSize)
        if findTape:
            tcf.findContourTape(quantifiedImage, layerContours, OriginalSize)

        #Wait for 1 ms if esc pressed break main while loop
        key = cv2.waitKey(waitTime)
        if key == 27:
            break


    #Destroys the "Image" window
    cv2.destroyWindow("image")
