import cv2 as cv
import numpy as np
import serial
import tkinter as tk
#from matplotlib import pyplot as plt
from collections import deque

img2=cv.imread("red.jpg")
img3=cv.imread(("green.jpg"))
img4=cv.imread("yellow.jpg")
img3=cv.resize(img3, (200, 200))
img2=cv.resize(img2,(200, 200))
img4=cv.resize(img4,(200, 200))
cascadeCar='cars.xml'
ard_srl = serial.Serial('com6', 9600)

def CheckEntranceLineCrossing(y, x):
    # absDistance = abs(y - x)

    if (abs(x) < abs(y)):
        return 1
    else:
        return 0


def detectCount(vid):
    img =cv.VideoCapture(vid)#"tf0.mp4"
    carCas=cv.CascadeClassifier(cascadeCar)

    #kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
    #kernalOp = np.ones((3,3),np.uint8)
    kernalOp2 = np.ones((5,5),np.uint8)
    kernalCl = np.ones((11,11),np.uint8)
    fgbg = cv.createBackgroundSubtractorMOG2(varThreshold=90, detectShadows=False, history=200)
    width = 0
    #height = 0
    carCnt=0
    #OffsetRefLines = 150


    #ret, frame2 = img.read()

    while(img.isOpened()):
        ret, frame = img.read()


        #height = frame1.shape[0]
        #width = frame1.shape[1]

        #height = np.size(frame1, 0)

        if ret==False:
            print ('No Video Found!!')
            break
        else:
            frame1 = cv.resize(frame, (900, 400))
            try:
                width = np.size(frame1, 1)
            except IndexError:
                pass

            carsFilter = carCas.detectMultiScale(frame1,1.1,1)
            fgmask = fgbg.apply(frame1)

            _, thres = cv.threshold(fgmask, 200, 255, cv.THRESH_BINARY)
            mask1 = cv.morphologyEx(thres, cv.MORPH_OPEN, kernalOp2)
            mask2= cv.morphologyEx(mask1, cv.MORPH_CLOSE, kernalCl)

            #hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            #cv.imshow('HSV Image', hsv)
            #cv.waitKey(0)

            #hue, saturation, value = cv.split(hsv)
            #cv.imshow('Saturation Image', saturation)
            #cv.waitKey(0)

            #retval, thresholded = cv.threshold(saturation, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
            #cv.imshow('Thresholded Image', thresholded)
            #cv.waitKey(0)

            #medianFiltered = cv.medianBlur(thresholded, 5)
            #cv.imshow('Median Filtered Image', medianFiltered)
            #cv.waitKey(0)


            #diff=cv.absdiff(frame1,frame2)
            #medianFiltered = cv.medianBlur(diff, 5)
            #gray=cv.cvtColor(medianFiltered,cv.COLOR_BGR2GRAY)
            #blur=cv.GaussianBlur(gray,(5,5),0)

            #medianFiltered2 = cv.medianBlur(thres, 5)

            #cv.fastNlMeansDenoising(thres,thres,3,7,21)

            #dilated=cv.dilate(medianFiltered2,kernel ,iterations=20)
            #blur = cv.GaussianBlur(dilated, (5, 5), 0)

            for (x1, y1, w1, h1) in carsFilter:
                cv.rectangle(frame1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 255), 2)
            #fgmask = cv.morphologyEx(blur, cv.MORPH_OPEN, kernel)"""
            CoorYEntranceLine = 355    #(height // 2)+100
           # CoorYExitLine = (height // 2) - OffsetRefLines

            cv.line(frame1, (0, CoorYEntranceLine), (width, CoorYEntranceLine), (0, 0xFF, 0), 5)

            contours,_ = cv.findContours(mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)



            for contour in contours:

                area = cv.contourArea(contour)
                if area > 5000:
                    #contour_list.append(contour)
                    (x, y, w, h) = cv.boundingRect(contour)
                    #m = cv.moments(contour)
                    cx = (x+x+w)//2                         #int(m['m10'] / m['m00'])
                    cy = (y+y+h)//2                         #int(m['m01'] / m['m00'])
                    estimatedCenter=(cx,cy)

                    cv.circle(frame1, estimatedCenter, 1, (0, 0, 255), 2)

                    if (CheckEntranceLineCrossing(cy, CoorYEntranceLine)):
                    #if(abs(cy-CoorYEntranceLine)<=2):
                       carCnt += 1
                    #for ax in range(0, 960):
                     #   if (cx > ax) & (cy > 270):
                      #      carCnt =carCnt+1
                            #continue
                    #continue

                #cv.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #cv.drawContours(frame, contour_list, 3, (255, 0, 0), 2)



            countNum = 'Total vehicle: ' + str(carCnt)

            cv.putText(frame1, countNum, (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)

           # print((0, int(height / 2)), (int(width), int(height / 2)))
        #print(height)


        #return iigg


            cv.imshow('Objects Detected', frame1)
            cv.imshow('Objects Detected2', mask2)

        #def trafficControl(carCnt):


            #print ard_srl.readline()
            #print ("Enter 1 to ON and 0 to OFF")



            if (carCnt >= 0 and carCnt <= 5):
                    ard_srl.write('0')
                    cv.imshow('GREENsignal', img3)
            elif (carCnt >= 6 and carCnt <= 9):
                    ard_srl.write('1')
                    cv.destroyWindow('GREENsignal')
                    cv.imshow('YELLOWsignal', img4)
            elif (carCnt >= 10):
                    ard_srl.write('2')
                    cv.destroyWindow('YELLOWsignal')
                    cv.imshow('REDsignal', img2)


               # print(intHorizontalLinePosition)
                #frame1=frame2
                #ret,frame2=img.read()




                #cv.imshow("cars_detector",frame)
                #cv.imshow("mask",fgmask)
            if cv.waitKey(10) & 0xFF == ord('q'):
                break
    sbb="Total counted car: "

    print sbb,carCnt
    img.release() # Destroys the capture object
    cv.destroyAllWindows() # Destroys all the windows"""