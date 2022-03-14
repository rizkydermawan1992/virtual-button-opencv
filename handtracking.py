import cv2
import pyfirmata
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
#Set size screen
ws, hs = 1280, 720
cap.set(3, ws)
cap.set(4, hs)

if not cap.isOpened():
    print("Camera couldn't Access")
    exit()

detector  = HandDetector(detectionCon=0.7)

port = "COM7"
board = pyfirmata.Arduino(port)
servo_pinX = board.get_pin('d:5:s') #pin 5 Arduino
servo_pinY = board.get_pin('d:6:s') #pin 6 Arduino


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    if lmList :

        fx, fy = lmList[9][0], lmList[9][1]
        posFinger = [fx, fy]
        # convert coordinat to servo degree
        servoX = np.interp(fx, [0, ws], [0, 180])
        servoY = np.interp(fy, [0, hs], [0, 180])


        cv2.circle(img, (fx-20, fy+50), 15, (0, 0, 255), cv2.FILLED)  # draw circle on center of hand
        cv2.putText(img, str(posFinger), (fx-10, fy+40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
        cv2.line(img, (0, fy+50), (ws, fy+50), (0,0,0), 2) # x line
        cv2.line(img, (fx-20, hs), (fx-20, 0), (0, 0, 0), 2)# y line
        cv2.putText(img, f'Servo X: {int(servoX)} deg', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(img, f'Servo Y: {int(servoY)} deg', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        servo_pinX.write(servoX)
        servo_pinY.write(servoY)


    cv2.imshow("Image", img)
    cv2.waitKey(1)

