import cv2 
import numpy as np
import math
def getRect(frame):
    clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
    angle=0
    an=0
    angle_list=[]
    img=cv2.GaussianBlur(frame, (5,5), 0)

    img=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# [55, 250, 211, 255, 255, 255]
    lower=np.array([55, 250, 211],np.uint8)
    upper=np.array([ 255, 255, 255],np.uint8)
    separated=cv2.inRange(img,lower,upper)


    #this bit draws a red rectangle around the detected region
    contours,hierarchy=cv2.findContours(separated,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    
    largest_contour = None
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            largest_contour=contour
            if not largest_contour.all()==None:
                moment = cv2.moments(largest_contour)
                # print(moment)
                if moment["m00"] > 1000:
                    rect = cv2.minAreaRect(largest_contour)
                    # print(rect)
                    rect = cv2.minAreaRect(largest_contour)
                    # angle=math.radians(rect[2]+90)
                    angle_list.append(math.radians(rect[2]-100))
                    angle=sum(angle_list) / len(angle_list) 
                    an = clamp(angle,-1.58, 1.58)
                    rect = ((rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), rect[2])
                    (width,height)=(rect[1][0],rect[1][1])
                    # print (str(width)+" "+str(height))
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    # if(height>0.9*width and height<0.5*width):
                    cv2.drawContours(frame,[box], 0, (0, 0, 255), 2)
    return an