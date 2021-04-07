import cv2 as cv
import numpy as np
import serial
import time



img2=cv.imread("red.jpg")
img3=cv.imread(("green.jpg"))
img4=cv.imread("yellow.jpg")
img3=cv.resize(img3, (200, 200))
img2=cv.resize(img2,(200, 200))
img4=cv.resize(img4,(200, 200))
cascadeCar='cars.xml'
ard_srl = serial.Serial('com6', 9600)



def CheckEntranceLineCrossing(y, x):

    if (abs(x) < abs(y)):
        return 1
    else:
        return 0



def detectCount(vid):
    img =cv.VideoCapture(vid) #"tf0.mp4"
    carCas=cv.CascadeClassifier(cascadeCar)


    kernalOp2 = np.ones((5,5),np.uint8)
    kernalCl = np.ones((11,11),np.uint8)

    fgbg = cv.createBackgroundSubtractorMOG2(varThreshold=90, detectShadows=False, history=200)
    width = 0

    carCnt=0




    while(img.isOpened()):
        ret, frame = img.read()



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


            for (x1, y1, w1, h1) in carsFilter:
                cv.rectangle(frame1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 255), 2)

            CoorYEntranceLine = 355

            cv.line(frame1, (0, CoorYEntranceLine), (width, CoorYEntranceLine), (0, 0xFF, 0), 5)

            contours,_ = cv.findContours(mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)



            for contour in contours:

                area = cv.contourArea(contour)
                if area > 5000:

                    (x, y, w, h) = cv.boundingRect(contour)

                    cx = (x+x+w)//2
                    cy = (y+y+h)//2
                    estimatedCenter=(cx,cy)

                    cv.circle(frame1, estimatedCenter, 1, (0, 0, 255), 2)

                    if (CheckEntranceLineCrossing(cy, CoorYEntranceLine)):

                       carCnt += 1




            countNum = 'Total vehicle: ' + str(carCnt)

            cv.putText(frame1, countNum, (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)




            cv.imshow('Objects Detected', frame1)
            cv.imshow('Objects Detected2', mask2)




            if (carCnt >= 0 and carCnt <= 5):
                    ard_srl.write('0')
                    cv.destroyWindow('REDsignal')
                    cv.imshow('GREENsignal', img3)
            elif (carCnt >= 6 and carCnt <= 9):
                    ard_srl.write('1')
                    cv.destroyWindow('GREENsignal')
                    cv.imshow('YELLOWsignal', img4)
            elif (carCnt == 10):
                    ard_srl.write('2')
                    cv.destroyWindow('YELLOWsignal')
                    cv.imshow('REDsignal', img2)

            elif (carCnt > 10):
                time.sleep(5)
                carCnt = 0






            if cv.waitKey(10) & 0xFF == ord('q'):
                break
    sbb="Total counted car: "



    print sbb,carCnt
    img.release() # destroys capture object
    cv.destroyAllWindows() # destroys all windows