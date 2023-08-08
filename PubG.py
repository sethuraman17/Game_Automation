import cv2
from cvzone.PoseModule import PoseDetector
from cvzone.HandTrackingModule import HandDetector
import pyautogui

pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = PoseDetector()
detector1 = HandDetector(detectionCon=0.8, maxHands=2)

d_down = False
a_down = False
w_down = False
s_down = False
j_down = False
p_down = False
b_down = False
r_down = False
f_down = False
space_down = False

while True:
    success, img = cap.read()

    hands, img = detector1.findHands(img)
    lmList, bbox = detector1.findPosition(img)

    if hands:
        for hand in hands:
            handType = hand["type"]
            lmlist = hand["lmList"]
            fingers = detector1.fingersUp(hand)

            if handType == "Left" and fingers[1] == 1 and fingers[2] == 1:  # Check if index and middle fingers are up
                x, y = lmList[8][1], lmList[8][2]

                if fingers[0] == 1:
                    pyautogui.rightClick()

                x_screen = int(x)
                y_screen = int(y)

                pyautogui.moveTo(x_screen, y_screen, duration=0.1)

            elif handType == "Right":
                if lmlist[0][1] > lmlist[17][1]:
                    if fingers == [1, 1, 1, 1, 1]:
                        cv2.putText(img, "FORWARD", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if not w_down:
                            pyautogui.keyDown("w")
                            w_down = True
                    else:
                        if w_down:
                            pyautogui.keyUp("w")
                            w_down = False

                    if fingers == [1, 0, 0, 0, 0]:
                        cv2.putText(img, "BACKWARD", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if not s_down:
                            pyautogui.keyDown("s")
                            s_down = True
                    else:
                        if s_down:
                            pyautogui.keyUp("s")
                            s_down = False

                    if fingers == [0, 1, 0, 0, 0]:
                        cv2.putText(img, "RUN", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if not j_down:
                            pyautogui.keyDown("j")
                            j_down = True

                    else:
                        if j_down:
                            pyautogui.keyUp("j")
                            j_down = False

                    if fingers == [0, 1, 1, 0, 0]:
                        cv2.putText(img, "SHOOT", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if not p_down:
                            pyautogui.keyDown("p")
                            p_down = True

                    else:
                        if p_down:
                            pyautogui.keyUp("p")
                            p_down = False

                    if fingers == [0, 1, 0, 0, 1]:
                        cv2.putText(img, "SCOPE", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if not b_down:
                            pyautogui.keyDown("b")
                            b_down = True

                    else:
                        if b_down:
                            pyautogui.keyUp("b")
                            b_down = False

                    if fingers == [0, 0, 0, 0, 1]:
                        cv2.putText(img, "JUMP", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if not space_down:
                            pyautogui.keyDown("Space")
                            space_down = True

                    else:
                        if space_down:
                            pyautogui.keyUp("Space")
                            space_down = False

                    if fingers == [1, 0, 0, 0, 1]:
                        cv2.putText(img, "PICK UP", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if not f_down:
                            pyautogui.keyDown("f")
                            f_down = True

                    else:
                        if f_down:
                            pyautogui.keyUp("f")
                            f_down = False

    img = detector.findPose(img)

    lmList, bbox = detector.findPosition(img, draw=False)

    if lmList:
        lm11 = lmList[11]
        lm12 = lmList[12]
        lm20 = lmList[20]

        # Get the x-coordinate of lm11 and lm12
        lm11_x = lm11[1]
        lm12_x = lm12[1]
        lm20_x = lm20[1]

        # Draw the left line
        cv2.line(img, (195, 0), (195, 720), (0, 255, 255), 4)  # left

        # Draw the right line
        cv2.line(img, (1080, 0), (1080, 720), (0, 255, 255), 4)  # right

        # Check if both hands are inside the threshold lines
        if 195 < lm11_x < 1080 and 195 < lm12_x < 1080 and 195 < lm20_x < 1080:
            if d_down:
                pyautogui.keyUp("a")
                d_down = False
            if a_down:
                pyautogui.keyUp("d")
                a_down = False
            if r_down:
                pyautogui.keyUp("r")
                r_down = False
        else:
            # Check if lm11 crosses the right line
            if lm11_x > 1080:
                cv2.putText(img, "LEFT", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if not d_down:
                    pyautogui.keyDown("a")
                    d_down = True

            # Check if lm12 crosses the left line
            elif lm12_x < 195:
                cv2.putText(img, "RIGHT", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if not a_down:
                    pyautogui.keyDown("d")
                    a_down = True

            elif lm20_x < 195:
                cv2.putText(img, "RELOAD", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if not r_down:
                    pyautogui.keyDown("r")
                    r_down = True

    cv2.imshow("Images", img)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
