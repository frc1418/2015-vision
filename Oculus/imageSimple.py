from sklearn.cluster import MiniBatchKMeans
import numpy as np
import cv2

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
def quantifyList(inputList):
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

#Function to draw a list of contours onto an image
def drawContoursList(dst, inputList, contourIdx, color, thick):
    for i in range(0, len(inputList)):
        cv2.drawContours(dst, inputList[i], contourIdx, color, thickness=thick)

camera = cv2.VideoCapture(0)

#Creates global variables to fix the flickering bug
pastContours = None
blankContours = [[], [], [], []]

while(1):

    #Pulls a frame from the camera
    frame = camera.read()[1]

    #Resizes image to reduce processsing time
    image = cv2.resize(frame, (250, 100))

    #pulls the hieght and width from the image
    (h, w) = image.shape[:2]

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
    quantifiedLayers = quantifyList(layers)
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

    #Draws all contours onto the quant
    drawContoursList(quantifiedImage, layerContours, -1, (0,0,255), 1)

    #Resizes the quantified image so that it is easy to see
    newImage = cv2.resize(quantifiedImage, (1150,600))

    #Shows the final product
    cv2.imshow("image", newImage)

    for i in range(0,len(threshLayers)):
        cv2.imshow("Thresh %s" % i, quantifiedLayers[i])
        cv2.moveWindow("Thresh %s" % i, (i*250), 0)
    cv2.imshow("Meh", image)
    cv2.moveWindow("Meh", 1000, 0)

    #Wait for 1 ms if esc pressed break main while loop
    key = cv2.waitKey(1)
    if key == 27:
        break


#Destroys the "Image" window
cv2.destroyWindow("image")
