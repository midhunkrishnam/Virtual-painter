import cv2
import mediapipe as mp
import os
import time
import HandTrackingModule as htm
detector = htm.handDetector()
draw_color = (150,150,150)
video = cv2.VideoCapture(0)

while True:
    sucess,frame = video.read()
    frame=cv2.resize(frame,(1280,720))

                                        
    
    #bg
    cv2.rectangle(frame,(10,0),(1270,110),(0,0,0),cv2.FILLED)
    
    
    cv2.rectangle(frame,(20,10),(210,100),(0,0,255),cv2.FILLED)
    cv2.rectangle(frame,(230,10),(450,100),(0,255,0),cv2.FILLED)
    cv2.rectangle(frame,(470,10),(680,100),(255,0,0),cv2.FILLED)
    cv2.rectangle(frame,(700,10),(920,100),(0,255,255),cv2.FILLED)
    cv2.rectangle(frame,(940,10),(1260,100),(255,255,255),cv2.FILLED)

    #TEXT
    cv2.putText(frame,'Eraser',(1050,75),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)
    
    #2. find hand landmarks

    frame = detector.findHands(frame)
    lmlist = detector.findPosition(frame)
    #print(lmlist)

    if len(lmlist)!=0:
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]

        #print(x1,y1)

#3 find whichfinger is up
        fingers = detector.fingersUp()
        print(fingers)

#4 if two fingers is up - selection mode
        if fingers[1] and fingers[2]:
           
           print('selection mode')

           cv2.rectangle(frame,(x1,y1),(x2,y2),draw_color,-3)

#5 if one finger is up drawing mode
        if (fingers[1] and not fingers[2]):


            print('drawing mode')

    cv2.imshow('video',frame)
    if cv2.waitKey(1) & 0xFF ==27:
        break
video.release
cv2.destroyAllWindows()

