#arrumar direcoes
import cv2
import mediapipe as mp
from pynput.keyboard import Key,Controller
import pyautogui

block = False
keyboard = Controller()
state = None
capture = cv2.VideoCapture(0)
WebCamWidth = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
WebCamHeight = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
mphands = mp.solutions.hands
mpdraw = mp.solutions.drawing_utils
hands = mphands.Hands(min_detection_confidence = 0.7,min_tracking_confidence = 0.5)
topIds = [4,8,12,16,20]

def drawHands(frame,landmarks):
    if(landmarks):
        for(landmark) in landmarks:
            mpdraw.draw_landmarks(frame,landmark,mphands.HAND_CONNECTIONS)

def countFingers(frame,landmarks,handNo=0):
    global state
    if(landmarks):
        handlandmark = landmarks[handNo].landmark
        fingerCount = []
        for(index) in topIds:
            fingerTopY = handlandmark[index].y
            fingerBottomY = handlandmark[index-2].y
            fingerTopX = handlandmark[index].x
            fingerBottomX = handlandmark[index-2].x
            if(index != 4):
                if(fingerTopY < fingerBottomY):
                    fingerCount.append(1)
                if(fingerTopY > fingerBottomY):
                    fingerCount.append(0)
            elif(not block):
                if(fingerTopX < fingerBottomX):
                    fingerCount.append(1)
                if(fingerTopX > fingerBottomX):
                    fingerCount.append(0)

        totalFingers = fingerCount.count(1)
        cv2.putText(frame,str(totalFingers),(500,120),cv2.FONT_HERSHEY_COMPLEX,5,(50,125,1),10)
        if(totalFingers == 4):
            state = "play"
        if(totalFingers == 0 and state == "play"):
            keyboard.press("k")
            state = "pause"
        indicatorX = (handlandmark[8].x) * WebCamWidth
        if(totalFingers == 3):
            keyboard.press("f")
        if(totalFingers == 2):
            keyboard.press(Key.alt)
            keyboard.press(Key.f4)
        if(totalFingers == 1 and handlandmark[8].y < handlandmark[6].y):
            if(indicatorX > 450):
                keyboard.press(Key.right)
            elif(indicatorX < 250):
                keyboard.press(Key.left)

while True:
    ret, frame = capture.read()

    frame = cv2.flip(frame,1)
    result = hands.process(frame)
    landmarks = result.multi_hand_landmarks
    drawHands(frame,landmarks)
    countFingers(frame,landmarks)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == 32:
        cv2.destroyAllWindows()       
        break
cv2.destroyAllWindows()