import mysql.connector as ms
import os
import numpy as np
import io
import cv2
from PIL import Image
#connecting to db
#We have to change this
MyDB = ms.connect(
    host="localhost",
    database="images",
    user="admin",
    password="burguesllavall19993",
    )

MyCursor = MyDB.cursor()

#creating cursor


def insertBlobl(FilePath):
    with open(FilePath,"rb") as File:
        BinaryData = File.read()
    SQLStatement = "insert into table_images (image) Values (%s)"
    MyCursor.execute(SQLStatement, (BinaryData,))
    MyDB.commit()
def retrieveImage(ID):
    SQLStatement = "SELECT * FROM table_images"
    MyCursor.execute(SQLStatement.format(str(ID)))
    MyResult = MyCursor.fetchone()[2]

    StoreFilePath = "img{0}.png".format(str(ID))
    print(StoreFilePath)
    #with open(StoreFilePath,"wb") as File:
     #     File.write(MyResult)
      #    File.close()
    img = Image.open(io.BytesIO(MyResult))
    arr =np.asarray(img)
    print(arr)
    image = Image.fromarray(arr,'RGB')
    imcv = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
    cv2.imshow('',imcv)



#load images into an array
def load_images(folder):

	images = []
	for filename in os.listdir(folder):
		img = cv2.imread(os.path.join(folder,filename))
		if img is not None:
			images.append(img)
	return images

""""
x = load_images("images/emilia-clarke")
#we are setting images into the sql
for foto in x:
    # cur.execute(sql %  foto)
    cv2.imshow("picture", foto)
    cv2.waitKey(0)
"""

# insertBlobl('images/Gerard/1.jpg')
retrieveImage(4)



cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
