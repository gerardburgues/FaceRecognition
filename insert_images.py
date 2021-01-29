import mysql.connector as ms
import os
import numpy as np
import io
import glob
import cv2
from PIL import Image
import random
from datetime import datetime
from datetime import timedelta
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

def random_date(start_date,end_date):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)

    return random_date

def insertBlobl(FilePath):

    """We will isnert the image in the DB depending on each main and Id"""
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 5, 1)

    for File1 in glob.glob(FilePath):
        with open(File1,"rb") as File:
            BinaryData = File.read()

        y = random_date(start_date, end_date)
        SQLStatement = "insert into Data_image (label_id,img,email,day_pic) Values (7,%s, 'Pepita@gmail.com',%s)"

        result = MyCursor.execute(SQLStatement, (BinaryData,y))
        #MyCursor.execute("insert into Data_image values(5,%s,'Ramon@gmail.com',%s)",(BinaryData,y))

        MyDB.commit()
        print("this is my result",  result)



def retrieveImage():
    """To prove we inserted the Image here is program to retrieve it. """
    SQLStatement = "SELECT * FROM Data_image where label_id=36"
    MyCursor.execute(SQLStatement)
    record = MyCursor.fetchall()
    for row in record:
        img = row[0]
        img = Image.open(io.BytesIO(img))
        arr = np.asarray(img)
        print(arr)
        image = Image.fromarray(arr, 'RGB')
        imcv = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        cv2.imshow('', imcv)
        cv2.waitKey(0 )






insertBlobl("training_images/Pepita/*.*")
retrieveImage()



cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
