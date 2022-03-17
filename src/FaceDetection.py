import cv2
import glob
import numpy as np
import os
face_cascade = cv2.CascadeClassifier('harcascade/haarcascade_frontalface_alt.xml')
face_cascade_lateral = cv2.CascadeClassifier('harcascade/haarcascade_profileface.xml')

"""Using Haarcascade we are detecting a picture (Profile Face and Frontal Face)
    When is detected we save it in the training_images folder of the current person.
"""

def DetectFace(File):
    """Face Detection. With a given image we use Haarcascade and calculate the points of the face in the image"""
    it= 0
    for file in glob.glob(File):
        end_cord_y1,x, end_cord_y,end_cord_x,end_cord_x1 = 0,0,0,0,0
        y = 0
        x1 = 0
        y1 = 0
        file = cv2.imread(file)

        cv2.imshow('', file) # Showing image we want to detect
        file = cv2.resize(file, (600,450))
        face_gray = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)# Transforming image to color gray
        faces = face_cascade.detectMultiScale(face_gray) #FrontalFace
        faces_lateral = face_cascade_lateral.detectMultiScale(face_gray ,1.06, 6,flags=cv2.CASCADE_SCALE_IMAGE)#Lateral Detection

        #All pixels in face image

        if faces == () and faces_lateral == ():
            print("no face found") # the face haven't been found, we return nothing
            return []
        """We calculate coordenates in image where there is lateral face and we show it in the image"""
        for (x1,y1,w1,h1) in faces_lateral:
            lateral = face_gray[y1:y1 + h1, x1:x1 + w1]
            color1 = (20, 20, 193 )  # BGR 0-255
            stroke1 = 2
            end_cord_x1 = x1 + w1
            end_cord_y1= y1 + h1
            frame1 = cv2.rectangle(face_gray, (x1, y1), (end_cord_x1, end_cord_y1), color1, stroke1)
            #cv2.imshow('frame1', frame1)# in case we want to show the image
        """We calculate coordenates in image where there is frontal face and we show it in the image"""
        for (x,y,w,h) in faces:
            center = face_gray[y:y+ h, x:x+w]

            color = (255, 0, 0)  # BGR 0-255
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            frame = cv2.rectangle(face_gray, (x, y), (end_cord_x, end_cord_y), color, stroke)
            # cv2.imshow('frame', frame)# in case we want to show the image
            ## Here will do lateral face
        if faces != () or faces_lateral != ():

            c1= calcular_coordenades((x1, y1),(x, y),(end_cord_x,end_cord_y),(end_cord_x1,end_cord_y1))
            it+=1
            #here we show the image that will be saved or used
            cv2.imshow('Capture - Face de tection', save_image(c1, file))
            return save_image(c1,file)



        cv2.waitKey(0)


def calcular_coordenades(xy1,xy, endxy,endxy1):
    """We calculate coordenates based on how many dectectors we use.
    In case two detectors detect a face in image the program we calculate the
    middle "square" between the two detections"""
    if not all(xy1) and not all(xy):
        return (0,0)
    if not all(xy1) and xy[:] != 0:
        return (xy,endxy)
    if not all(xy)and  xy1[:] != 0:
        return (xy1,endxy1)
    if xy1[:]!=0 and xy[:] !=0:
        #print(endxy1[0])
        endx =endxy1[0] + endxy[0]
        endy = endxy1[1] + endxy[1]
        end = (int(endx/2),int (endy/2))
        startx = xy1[0]+xy[0]
        starty = xy1[1] + xy[1]
        start = (int(startx/2),int(starty/2))

        return (start,end)


def save_image(points, image):

    """in case we are saving the images in training folder we will write the in the specific folder using
        #filename = "/Users/gerardburgues/Documents/Computer Vision/Projecte/SetDatabase/training_images/Pepita/Pepita_im%d.jpg"%i
        #cv2.imwrite(filename, frame)
    """
    path = '/Users/gerardburgues/Documents/Computer Vision/Projecte/SetDatabase/training_images'


    #print('my points', points)

    frame = image[points[0][1]:points[1][1], points[0][0]: points[1][0]] #We retur the frame of the picture

    return frame










cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)