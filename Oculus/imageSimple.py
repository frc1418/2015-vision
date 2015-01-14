from sklearn.cluster import MiniBatchKMeans
import numpy as np
import cv2

def listFilter(inputList, value, blankValue, fillValue):
    outputList = []
    for i in range(0, len(inputList)):
        if inputList[i] == value:
            outputList.append(fillValue)
        else:
            outputList.append(blankValue)
    return outputList

cam = cv2.VideoCapture(0)
while(1):
    #Pulls a frame from the camera
    image = cam.read()[1]

    #Resizes image to reduce processsing time
    image = cv2.resize(image, (250, 100))

    #pulls the hieght and width from the image
    (h, w) = image.shape[:2]

    #Changes color to LAB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    #Reshapes into a two deminsional array
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # apply k-means using the specified number of clusters and
    # then create the quantized image based on the predictions
    clt = MiniBatchKMeans(n_clusters = 4)
    labels = clt.fit_predict(image)

    layer0 = listFilter(labels,0,0,1)
    layer1 = listFilter(labels,1,0,1)
    layer2 = listFilter(labels,2,0,1)
    layer3 = listFilter(labels,3,0,1)

    quant0 = clt.cluster_centers_.astype("uint8")[layer0]
    quant1 = clt.cluster_centers_.astype("uint8")[layer1]
    quant2 = clt.cluster_centers_.astype("uint8")[layer2]
    quant3 = clt.cluster_centers_.astype("uint8")[layer3]
    quant4 = clt.cluster_centers_.astype("uint8")[labels]

    #Reshapes the output back into a three demisional array
    quant0 = quant0.reshape((h, w, 3))
    quant1 = quant1.reshape((h, w, 3))
    quant2 = quant3.reshape((h, w, 3))
    quant3 = quant3.reshape((h, w, 3))
    quant4 = quant4.reshape((h, w, 3))

    #Converts from LAB to BGR
    #Contverts from BGR to gray-scale for findingcontours
    quant0_bgr = cv2.cvtColor(quant0, cv2.COLOR_LAB2BGR)
    quant1_bgr = cv2.cvtColor(quant1, cv2.COLOR_LAB2BGR)
    quant2_bgr = cv2.cvtColor(quant2, cv2.COLOR_LAB2BGR)
    quant3_bgr = cv2.cvtColor(quant3, cv2.COLOR_LAB2BGR)
    quant4_bgr = cv2.cvtColor(quant4, cv2.COLOR_LAB2BGR)

    gray0 = cv2.cvtColor(quant0_bgr, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.cvtColor(quant1_bgr, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(quant2_bgr, cv2.COLOR_BGR2GRAY)
    gray3 = cv2.cvtColor(quant3_bgr, cv2.COLOR_BGR2GRAY)
    gray4 = cv2.cvtColor(quant4_bgr, cv2.COLOR_BGR2GRAY)

    #Finds the contours of the output
    img0, contours0, hierarchy0 = cv2.findContours(gray0.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img1, contours1, hierarchy1 = cv2.findContours(gray1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img2, contours2, hierarchy2 = cv2.findContours(gray2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img3, contours3, hierarchy3 = cv2.findContours(gray3.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #print contours

    #Draws all contours onto the quant
    cv2.drawContours(quant4_bgr, contours0, -1, (0,0,255), thickness=1)
    cv2.drawContours(quant4_bgr, contours1, -1, (0,0,255), thickness=1)
    cv2.drawContours(quant4_bgr, contours2, -1, (0,0,255), thickness=1)
    cv2.drawContours(quant4_bgr, contours3, -1, (0,0,255), thickness=1)

    #Resizes the quantified image so that it is easy to see
    quant4_bgr_max = cv2.resize(quant4_bgr, (1150,600))

    #Shows the final product
    cv2.imshow("image", quant4_bgr_max)
    cv2.moveWindow("image", 0, 150)


    cv2.imshow("Find Contours O Image", img0)
    cv2.moveWindow("Find Contours O Image", 0, 0)
    #cv2.moveWindow("BW", 250, 0)
    cv2.imshow("imageG", gray0)
    cv2.moveWindow("imageG", 500, 0)
    cv2.imshow("LAB", quant0)
    cv2.moveWindow("LAB", 750, 0)
    #cv2.imshow("B", b)
    #cv2.moveWindow("B", 1000, 0)


    #Wait for 1 ms if esc pressed break main while loop
    key = cv2.waitKey(1)
    if key == 27:
        break

#Destroys the "Image" window
cv2.destroyWindow("image")
