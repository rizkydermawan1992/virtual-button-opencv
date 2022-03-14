import cv2
import pyfirmata
from cvzone.HandTrackingModule import HandDetector
from cvzone.FPS import FPS

cap = cv2.VideoCapture(0)
#Set size screen
x_max, y_max = 1280, 720
cap.set(3, x_max)
cap.set(4, y_max)

if not cap.isOpened():
    print("Camera couldn't Access")
    exit()

fpsReader = FPS()
fps = fpsReader.update()

detector  = HandDetector(detectionCon=0.7)
pinR, pinY, pinG = 2, 3, 4
port = 'COM7' #Select your COM
board = pyfirmata.Arduino(port)

counter_R, counter_Y, counter_G = 0, 0, 0
R_on, Y_on, G_on = False, False, False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    fps, img = fpsReader.update(img)
    lmList, bboxInfo = detector.findPosition(img)

    if lmList :
        x, y = 100, 100
        w, h = 225, 225
        X, Y = 120, 190

        fx, fy = lmList[8][0], lmList[8][1] #index fingertip
        posFinger = [fx, fy]
        cv2.circle(img, (fx, fy), 15, (255, 0, 255), cv2.FILLED) #draw circle on index fingertip
        cv2.putText(img, str(posFinger), (fx+10, fy-10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
        # cv2.line(img, (0, fy), (x_max, fy), (255,255,0), 2) # x line
        # cv2.line(img, (fx, y_max), (fx, 0), (255, 255, 0), 2)# y line


        if x < fx < x + w - 95 and y < fy < y + h - 95:
            counter_R += 1
            cv2.rectangle(img, (x, y), (w, h), (255, 255, 0), cv2.FILLED)
            if counter_R == 1:
                R_on = not R_on
        else :
            counter_R = 0
            if R_on:
                R_val = 1
                cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, "ON", (X, Y), cv2.FONT_HERSHEY_PLAIN,
                            4, (255, 255, 255), 5)
            else:
                R_val = 0
                cv2.rectangle(img, (x, y), (w, h), (150, 150, 150), cv2.FILLED)
                cv2.putText(img, "OFF", (X-15, Y), cv2.FONT_HERSHEY_PLAIN,
                            4, (0, 0, 255), 5)

        if x + 250 < fx < x + 155 + w and y < fy < y + h - 95: #155 = 250 - 95
            counter_Y += 1
            cv2.rectangle(img, (x + 250, y), (w + 250, h), (255, 255, 0), cv2.FILLED)
            if counter_Y == 1:
                Y_on = not Y_on
        else:
            counter_Y = 0
            if Y_on:
                Y_val = 1
                cv2.rectangle(img, (x+250, y), (w+250, h), (0, 255, 255), cv2.FILLED)
                cv2.putText(img, "ON", (X+250, Y), cv2.FONT_HERSHEY_PLAIN,
                            4, (255, 255, 255), 5)
            else:
                Y_val = 0
                cv2.rectangle(img, (x + 250, y), (w + 250, h), (150, 150, 150), cv2.FILLED)
                cv2.putText(img, "OFF", (X-15 + 250, Y), cv2.FONT_HERSHEY_PLAIN,
                            4, (0, 255, 255), 5)

        if x + 500 < fx < x + 405 + w and y < fy < y + h - 95: #500 - 95 = 405
            counter_G += 1
            cv2.rectangle(img, (x + 500, y), (w + 500, h), (255, 255, 0), cv2.FILLED)
            if counter_G == 1:
                G_on = not G_on

        else:
            counter_G = 0
            if G_on:
                G_val = 1
                cv2.rectangle(img, (x + 500, y), (w + 500, h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "ON", (X + 500, Y), cv2.FONT_HERSHEY_PLAIN,
                            4, (255, 255, 255), 5)
            else:
                G_val = 0
                cv2.rectangle(img, (x + 500, y), (w + 500, h), (150, 150, 150), cv2.FILLED)
                cv2.putText(img, "OFF", (X-15 + 500, Y), cv2.FONT_HERSHEY_PLAIN,
                            4, (0, 255, 0), 5)

        board.digital[pinR].write(R_val)
        board.digital[pinY].write(Y_val)
        board.digital[pinG].write(G_val)


    cv2.imshow("Image", img)
    cv2.waitKey(1)

