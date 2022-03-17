import cv2
import numpy as np
from PIL import Image
import time
import pickle
import mysql.connector as ms
import io

MyDB = ms.connect(
    host="localhost",
    database="images",
    user="admin",
    password="burguesllavall19993",
)

MyCursor = MyDB.cursor()

def binary_pixel(img, center, x, y):
    new_value = 0

    try:
        # WE ARE APPLYING THRESHOLD
        # If local neighbourhood pixel
        # value is greater than or equal
        # to center pixel values then
        # set it to 1
        if img[x][y] >= center:
            new_value = 1

    except:
        # Exception is required when
        # neighbourhood value of a center
        # pixel value is null i.e. valuess
        # present at boundaries.
        pass

    return new_value


# Function for calculating LBP
def matrix_LBP(img, x, y):
    center = img[x][y]
    # x = height y= width
    matrixPixels = []
    # we set each value of the matrix ( 0 or 1 )
    # top_left
    matrixPixels.append(binary_pixel(img, center, x - 1, y - 1))

    # top
    matrixPixels.append(binary_pixel(img, center, x - 1, y))

    # top_right
    matrixPixels.append(binary_pixel(img, center, x - 1, y + 1))

    # right
    matrixPixels.append(binary_pixel(img, center, x, y + 1))

    # bottom_right
    matrixPixels.append(binary_pixel(img, center, x + 1, y + 1))

    # bottom
    matrixPixels.append(binary_pixel(img, center, x + 1, y))

    # bottom_left
    matrixPixels.append(binary_pixel(img, center, x + 1, y - 1))

    # left
    matrixPixels.append(binary_pixel(img, center, x, y - 1))

    # CONVERTING BINARY to DECIMAL

    matrixPix = ''.join(map(str, matrixPixels))

    new_value = int(matrixPix, 2)

    # converting central value of matrix ( decimal )
    for i in range(len(matrixPixels)):

        if i == 4:
            matrixPixels[i] = new_value

    return new_value


def Histograms(img):
    """calcualtion of the histogram:

           - transform the image into gray and realise the LBP Operation
           - Save the oeration in a numpy array
           - Perform histogram. Counting how many times a value appear in a single square
           - Append the first numpy array with the values to the following ones until we perform the histogram
           for all the grids
       """
    img = cv2.resize(img, (512, 768))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = img.shape
    img_lbp = np.zeros((height, width),
                       np.uint8)
    # for each position of height-width
    for i in range(0, height):
        for j in range(0, width):
            img_lbp[i, j] = matrix_LBP(img, i, j)

    # split the image into multiple grids
    H = height // 8
    W = width // 8

    HIST = []
    for y in range(0, height, H):
        for x in range(0, width, W):

            tiles = img_lbp[y:y + H, x:x + W]
            hist = np.zeros(256, dtype=int)
            for i in tiles:
                for u in i:
                    hist[u] += 1
            HIST.append(hist)

    return HIST




def retrieveImage():
    """We will have to go over all the images not just one."""

    dic_of_histograms = {}

    SQLStatement = "SELECT * FROM Data_image"
    MyCursor.execute(SQLStatement)
    record = MyCursor.fetchall()
    for row in record:
        img = row[0]
        img = Image.open(io.BytesIO(img))
        arr = np.asarray(img)

        image = Image.fromarray(arr, 'RGB')
        imcv = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        hist = Histograms(imcv)
        dic_of_histograms[row[3]] = hist

        cv2.waitKey(1)

    return dic_of_histograms


if __name__ == '__main__':
    tic = time.perf_counter()

    dict_hist = retrieveImage()

    ## we save model
    filename = 'dictionary'
    outfile = open(filename, 'wb')
    pickle.dump(dict_hist, outfile)
    outfile.close()

    print("LBP Program is finished")
    toc = time.perf_counter()
    # calculate time the program takes to save the model
    print(f"final time {toc - tic:0.4f} seconds")

    # extracting histogram

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
