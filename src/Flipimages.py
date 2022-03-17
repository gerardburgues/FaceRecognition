###TRANSFORM pictures mirror efect
import numpy as np
import glob
import cv2
path  ="training_images/Gerard/*.*"

"""We flip evere training image folder so we have more data in the database"""
i=0
for file in glob.glob(path):
    image = cv2.imread(file)
    cv2.resize(image,(250,300))
    image_show = cv2.flip(image, 1)
    cv2.imwrite("training_images/Gerard/Gerard_transform%i.jpg"%i,image_show)
    cv2.imshow("image", image)
    cv2.imshow("image mirror",image_show)
    i+=1




cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
