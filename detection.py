import cv2
import mediapipe  as mp
import numpy as np
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)
locations = []
if not cap.isOpened():
    print("Error opening video stream or file")
while True:
    ret, frame = cap.read()
    newFrame = np.copy(frame)
    h, w = frame.shape[:2]
    imrgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(imrgb)
    if results.multi_hand_landmarks:
        for hand_mark in results.multi_hand_landmarks:
            mpdraw.draw_landmarks(frame, hand_mark,mpHands.HAND_CONNECTIONS)
            for id_,lm in enumerate(hand_mark.landmark):
                cx, cy = int(lm.x*w), int(lm.y*h)
                locations.append((id_, cx,cy))
                thumb,first,second,third,last = np.array_split(locations,5)
                thumb = thumb[1:]
        num = 0
        if(thumb[1][1] < last[1][1]): #LEFT HAND
            if((thumb[0][2] - thumb[3][2] > 50 and thumb[2][1] > thumb[3][1]) or thumb[0][2] - thumb[3][2] > 115):
                num+= 1
        else: #RIGHT HAND
            if((thumb[0][2] - thumb[3][2] > 50 and thumb[2][1] < thumb[3][1]) or thumb[0][2] - thumb[3][2] > 115):
                num+= 1
            elif(thumb[0][1] - thumb[3][1] < -70 or thumb[0][1] - thumb[3][1] > 70):
                num+= 1
        if(first[0][2] - first[3][2] > 50):
            num+= 1
        elif(first[0][1] - first[3][1] < -50 or first[0][1] - first[3][1] > 50):
            num+= 1
        if(second[0][2] - second[3][2] > 50):
            num+= 1
        elif(second[0][1] - second[3][1] < -50 or second[0][1] - second[3][1] > 50):
            num+= 1
        if(third[0][2] - third[3][2] > 50):
            num+= 1
        elif(third[0][1] - third[3][1] < -50 or third[0][1] - third[3][1] > 50):
            num+= 1
        if(last[0][2] - last[3][2] > 50):
            num+= 1
        elif(last[0][1] - last[3][1] < -50 or last[0][1] - last[3][1] > 50):
            num+= 1
        cv2.putText(newFrame,str(num),(50,50),cv2.FONT_HERSHEY_DUPLEX,2,(0,0,255),2)
        locations = []
    if ret:
        cv2.imshow('Frame', frame)
        cv2.imshow("Normal", newFrame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
