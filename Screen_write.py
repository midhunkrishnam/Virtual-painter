import cv2
import HandTrackingModule as htm
import numpy as np
import mediapipe as mp
import time 

detector=htm.handDetector()
draw_color=(0,0,0)
brush_size=20
eraser_size=50
p_time=0 


img_canvas=np.zeros((720,1280,3),np.uint8)


#1.import image 
cam = cv2.VideoCapture(0)
while True:
    sucess,img=cam.read()
    img=cv2.flip(img,1)
    img=cv2.resize(img,(1280,720))
    

    rect=cv2.rectangle(img,pt1=(0,0),pt2=(1280,110),color=(0,0,0),thickness=-3)
    
    rect1=cv2.rectangle(img,pt1=(20,10),pt2=(210,100),color=(0,0,255),thickness=-3)
    
    rect2=cv2.rectangle(img,pt1=(230,10),pt2=(450,100),color=(255,0,0),thickness=-3)
    
    rect3=cv2.rectangle(img,pt1=(470,10),pt2=(680,100),color=(0,255,0),thickness=-3)
    
    rect4=cv2.rectangle(img,pt1=(700,10),pt2=(920,100),color=(0,255,255),thickness=-3)
    
    rect5=cv2.rectangle(img,pt1=(940,10),pt2=(1260,100),color=(255,255,255),thickness=-3)

    text=cv2.putText(rect4,text='Eraser',org=(1040,60),fontFace=cv2.FONT_HERSHEY_SCRIPT_COMPLEX,fontScale=1,color=(0,0,0),thickness=3)
    
   
     
    
    
    #2.finding handlandmarks

    img=detector.findHands(img)
    lmlist=detector.findPosition(img)
    print(lmlist)

    if len(lmlist)!=0:
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
        print(x1,y1)

    #3.find which finger is up

        fingers=detector.fingersUp()
        print(fingers)

    #4.if two finger is up--selection mode
        if fingers[1] and fingers[2]:
            print('selection mode')
            xp ,yp = 0 ,0

            if y1<130:
              if 20<x1<210:
                    draw_color=(0,0,255)
              elif 230<x1<450:
                    draw_color=(255,0,0)
              elif 470<x1<680:
                    draw_color=(0,255,0)
              elif  700<x1<920:
                    draw_color=(0,255,255)
              elif 940<x1<1260:
                   draw_color=(0,0,0) 
            

            cv2.rectangle(img,(x1,y1),(x2,y2),draw_color,-3)

    #5.if one finger is up--drawing mode
        if (fingers[1] and not fingers[2]):
            print("Drawing mode")
            cv2.circle(img,(x1,y1),15,draw_color,-3)


            if xp==0 and yp ==0:
                xp=y1
                yp=y1
            if draw_color==(0,0,0):
                  cv2.line(img,(xp,yp),(x1,y1),draw_color,thickness=eraser_size)
                  cv2.line(img_canvas,(xp,yp),(x1,y1),draw_color,thickness=eraser_size)
            else:
                  cv2.line(img,(xp,yp),(x1,y1),draw_color,thickness=brush_size)
                  cv2.line(img_canvas,(xp,yp),(x1,y1),draw_color,thickness=brush_size)
        
            xp,yp=x1,y1
            
    img_gray=cv2.cvtColor(img_canvas,cv2.COLOR_BGR2GRAY)
    _,img_inv=cv2.threshold(img_gray,20,255,cv2.THRESH_BINARY_INV)
    img_inv=cv2.cvtColor(img_inv,cv2.COLOR_BAYER_BG2BGR)

    img=cv2.bitwise_and(img,img_inv)
    img=cv2.bitwise_or(img,img_canvas)

    img=cv2.addWeighted(img,1,img_canvas,0.5,0)

    #FPS DISPLAY
    c_time=time.time()
    fps=1/(c_time - p_time)
    p_time=c_time
    cv2.putText(img,str(int(fps)),(50,250),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)

    img=cv2.addWeighted(img,1,img_canvas,0,5,0)

    cv2.imshow('camera',img)
    #cv2.imshow('canvas',img_canvas)
    if cv2.waitKey(1) & 0XFF==27:
        break
cam.release
cv2.destroyAllWindows()



