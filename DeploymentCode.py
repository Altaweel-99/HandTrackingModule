import cv2
import os
import sys

import pyfirmata2
import time
port = 'COM3'

board = pyfirmata2.Arduino(port)

OpenHandLED= board.get_pin("d:3:o")
ClosedHandLED = board.get_pin("d:4:o")
IndexFingerUPLED= board.get_pin("d:5:o")
IndexAndMiddleUPLED= board.get_pin("d:6:o")
NoneOfThemLED = board.get_pin("d:7:o")

import sys
print (sys.version)
print (sys.path)


import HandTrackingModule as htm
wCam, hCam = 640, 480


cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pTime = 0

detector = htm.handDetector (detectionCon=0)



while True:

    success, img = cap.read()

    img = detector.findHands(img)

    lmList = detector.findPosition( img, draw = False)


    if len(lmList) != 0:


     if (lmList[8][2] < lmList[7][2] and lmList[12][2] < lmList[11][2] and lmList[16][2] < lmList[15][2] and lmList[20][2] < lmList[19][2] and lmList[4][2] < lmList[3][2]):
        print('Open Hand')
        OpenHandLED.write (1)
        ClosedHandLED.write(0)
        IndexFingerUPLED.write(0)
        IndexAndMiddleUPLED.write(0)
        NoneOfThemLED.write(0)


     else:

        if (lmList[8][2] < lmList[7][2] and lmList[12][2] >= lmList[10][2] and lmList[16][2] >= lmList[14][2] and
                 lmList[20][2] >= lmList[18][2]):
            print('Index Finger Up')
            OpenHandLED.write(0)
            ClosedHandLED.write(0)
            IndexFingerUPLED.write(1)
            IndexAndMiddleUPLED.write(0)
            NoneOfThemLED.write(0)
        else:

            if (lmList[8][2] < lmList[7][2] and lmList[12][2] <= lmList[11][2] and lmList[16][2] >= lmList[14][2] and
                lmList[20][2] >= lmList[18][2]):
                print('Index Finger and Middle Finger Up')
                OpenHandLED.write(0)
                ClosedHandLED.write(0)
                IndexFingerUPLED.write(0)
                IndexAndMiddleUPLED.write(1)
                NoneOfThemLED.write(0)
            else:
                if(lmList[8][2]  >= lmList[7][2] and lmList[12][2] >= lmList[10][2] and lmList[16][2] >= lmList[14][2] and lmList[20][2] >= lmList[18][2]):
                    print('Closed Hand')
                    OpenHandLED.write(0)
                    ClosedHandLED.write(1)
                    IndexFingerUPLED.write(0)
                    IndexAndMiddleUPLED.write(0)
                    NoneOfThemLED.write(0)
                else:
                    print('Hand Gesture Not Recognized')
                    OpenHandLED.write(0)
                    ClosedHandLED.write(0)
                    IndexFingerUPLED.write(0)
                    IndexAndMiddleUPLED.write(0)
                    NoneOfThemLED.write(1)





            #else:

               # print('hands not fully open nor fully closed')




     cTime = time.time()
     fps = 1/(cTime - pTime )
     pTime = cTime

     cv2.putText(img, f'FPS:{int (fps) }',(400,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0 ,0),3)

     cv2.imshow("Image", img)

     cv2.waitKey(1)
