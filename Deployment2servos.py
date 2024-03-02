import cv2
import os
import sys

from pyfirmata2 import Arduino
import time
port = 'COM5'
from pyfirmata2 import SERVO
board = Arduino('COM5')
board.digital[11].mode = SERVO
board.digital[10].mode = SERVO
board.digital[9].mode = SERVO
board.digital[6].mode = SERVO
board.digital[5].mode = SERVO
board.digital[3].mode = SERVO



board.digital[10].write(110)
board.digital[9].write(110)
board.digital[3].write(200)
time.sleep(5)














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
        board.digital[10].write(110)
        board.digital[9].write(110)
        board.digital[3].write(140)
        print('Servo Angel = 140')
        time.sleep(1)



     else:

        if (lmList[8][2] < lmList[7][2] and lmList[12][2] >= lmList[10][2] and lmList[16][2] >= lmList[14][2] and
                 lmList[20][2] >= lmList[18][2]):
            print('Index Finger Up')
            board.digital[10].write(110)
            board.digital[9].write(110)
            board.digital[5].write(60)
            print('Servo Angel = 60')
            time.sleep(1)

        else:

            if (lmList[8][2] < lmList[7][2] and lmList[12][2] <= lmList[11][2] and lmList[16][2] >= lmList[14][2] and
                lmList[20][2] >= lmList[18][2]):
                print('Index Finger and Middle Finger Up')
                board.digital[10].write(30)
                board.digital[9].write(30)
                board.digital[5].write(170)
                print('170')
                time.sleep(1)

            else:
                if(lmList[8][2]  >= lmList[7][2] and lmList[12][2] >= lmList[10][2] and lmList[16][2] >= lmList[14][2] and lmList[20][2] >= lmList[18][2]):
                    print('Closed Hand')
                    board.digital[10].write(110)
                    board.digital[9].write(110)
                    board.digital[3].write(200)
                    print('Servo Angel = 200')
                    time.sleep(1)

                else:
                    print('Hand Gesture Not Recognized')
                    board.digital[10].write(110)
                    board.digital[9].write(110)
                    #board.digital[11].write(0)

                    time.sleep(0.9)
                    board.digital[11].write(55)
                    time.sleep(1)

            #else:

               # print('hands not fully open nor fully closed')




     cTime = time.time()
     fps = 1/(cTime - pTime )
     pTime = cTime

     cv2.putText(img, f'FPS:{int (fps) }',(400,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0 ,0),3)

     cv2.imshow("Image", img)

     cv2.waitKey(1)
