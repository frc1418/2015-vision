from sklearn.cluster import MiniBatchKMeans
import numpy as np
import cv2

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
    '''Code I dont fully understand'''
    clt = MiniBatchKMeans(n_clusters = 5)
    labels = clt.fit_predict(image)
    quant0 = clt.cluster_centers_.astype("uint8")[labels]

    #Reshapes the output back into a three demisional array
    quant0 = quant0.reshape((h, w, 3))

    #Converts from LAB to BGR
    #Contverts from BGR to gray-scale for findingcontours
    quant1 = cv2.cvtColor(quant0, cv2.COLOR_LAB2BGR)
    imgGray = cv2.cvtColor(quant1, cv2.COLOR_BGR2GRAY)

    #Finds the contours of the output
    img, contours, hierarchy = cv2.findContours(imgGray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print contours

    #Draws all contours onto the quant
    cv2.drawContours(quant1, contours, -1, (0,0,255), thickness=2)

    #Resizes the quantified image so that it is easy to see
    quant2 = cv2.resize(quant1, (1150,600))

    #Shows the final product
    cv2.imshow("Find Contours O Image", img)
    cv2.imshow("imageG", imgGray)
    cv2.imshow("LAB", quant0)
    cv2.imshow("image", quant2)

    #Wait for 1 ms if esc pressed break main while loop
    key = cv2.waitKey(1)
    if key == 27:
        break

#Destroys the "Image" window
cv2.destroyWindow("image")
