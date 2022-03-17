import os
import cv2
import LBPH_algorithm
import pickle
import numpy as np
import FaceDetection as FC
import scipy.spatial.distance as p
def Compare(hist1, hist2):
    """Calculate euclidean distance"""
    value = sum((p - q) ** 2 for p, q in zip(hist1, hist2)) ** .5
    value = sum(value)
    print("this is value", value)
    return value




filename = 'dictionary'
infile = open(filename, 'rb')
new_dict = pickle.load(infile)

# print(new_dict)

path = 'Test_images/Papa_2.jpeg'
image = FC.DetectFace(path)
#image =cv2.imread(path) ---  In case we try with an already detected face AKA training image
x = LBPH_algorithm.Histograms(image)



final = {}
for key, values in new_dict.items():
    print("-------------------------------------------------------------------------")
    print('This is kye ',key, values)
    final[key] = Compare(x,values)

# sort the result and show it
x = {k: v for k, v in sorted(final.items(), key=lambda item: item[1])}
print(x)


infile.close()

print("LBP Program is finished")

# extracting histogram


cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)