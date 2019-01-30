import cv2
import numpy as np
import os
import time
import random
#img = cv2.resize(img,(360,640))
img = 0
color = 225
gray = 0

def isBlack(coo):
    if img[coo[1]][coo[0]][0]<70 and img[coo[1]][coo[0]][1]<70 and img[coo[1]][coo[0]][2]<70:
        return True
    else:
        return False
def isInRegion(coo):
    if coo[1]>1800 or coo[1]<400 or coo[0]>980 or coo[0]<100:
        return False
    return True
while True: 
    penguin = [0,0]
    point = [[[0,0]],[[0,0]],[[0,0]],[[0,0]]]

    os.system("adb shell screencap -p /sdcard/game.png")
    os.system("adb pull /sdcard/game.png")
    radious = 0
    img = cv2.imread("./game.png");
    dw = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2.0, 20,param1=100, param2=65, minRadius=12, maxRadius=100)
    for i in circles[0]:
        x = int(i[0])
        y = int(i[1])
        r = int(i[2])
        if isInRegion(i) and isBlack([x,y]) and (isBlack([x+r-15,y]) or isBlack([x-r+15,y])) and isBlack([x,y+r-10]) and isBlack([x,y-r+15]) :
            if i[2] >= radious:
                radious = i[2]
                penguin = [i[0],i[1]]
    if penguin[0] == 0:
        continue
    dw = cv2.circle(dw, (int(penguin[0]), int(penguin[1])), int(radious), (255, 255, 0), 4)
    print("source:",penguin,i[2])
    thre = cv2.threshold(gray ,color,255,cv2.THRESH_BINARY)
    contours = cv2.findContours(thre[1],1,2)
    #dw = cv2.drawContours(dw,contours[1],-1,(255,0,0),5)
    
    pmax = 0;
    cnt = 0;
    savecnt = 0;
    for i in contours[1]:
        cnt+=1
        approx = cv2.approxPolyDP(i,0.1*cv2.arcLength(i,True),True)
        if len(approx)==4:
            p = (approx.sum(axis=0)/4)[0]
            if isInRegion(p) and img[int(p[1])][int(p[0])][2] > 252 and img[int(p[1])][int(p[0])][0] < 100 and img[int(p[1])][int(p[0])][1] < 100 and p[1]<penguin[1] and max(approx[1][0][0],approx[2][0][0],approx[3][0][0],approx[0][0][0])>pmax :
                xmin = min(approx[1][0][0],approx[2][0][0],approx[3][0][0],approx[0][0][0])
                xmax = max(approx[1][0][0],approx[2][0][0],approx[3][0][0],approx[0][0][0])
                scale = xmax-xmin
                if img[int(p[1])][int(p[0]-3*scale/8)][1] > 200:
                    pmax = max(approx[1][0][0],approx[2][0][0],approx[3][0][0],approx[0][0][0])
                    point = approx
                    savecnt = cnt
    if point[0][0][0] == 0: 
        if color==225:
            color = 205;
            continue
        else:
            break;

    dw = cv2.drawContours(dw,[contours[1][savecnt-1]],-1,(255,255,0),5)
    print("goal:",(point.sum(axis=0)/4)[0])
    distance = abs((point.sum(axis=0)/4)[0][0]-penguin[0])*1.152865
    xmin = min(point[1][0][0],point[2][0][0],point[3][0][0],point[0][0][0])
    xmax = max(point[1][0][0],point[2][0][0],point[3][0][0],point[0][0][0])
    scale = xmax-xmin

    if scale < 110:
        scale -= 10
    ptime = int(1.2556*distance*191/scale)
    print("distance:",distance)
    print("scale:",scale)
    print("time =",ptime)

    dw = cv2.resize(dw,(360,640))
    cv2.imshow("hel",dw)
    right = 13;
    putx = str(random.random()*500 + 300)+" "
    puty = str(random.random()*300 + 500)+" "
    cv2.waitKey(100)
    if right == 13 :
        print("===========waiting===========")
        os.system("adb shell input swipe "+putx+puty+putx+puty+str(ptime))
        color = 225
    elif right == 110 :
        break
    else:
        continue
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
        #os.system("adb shell input swipe 320 410 320 410 "+str(int(1.2556*distance*191/scale)))
       # dw = cv2.drgawContours(img,[i],0,(0,255,0),-1)
