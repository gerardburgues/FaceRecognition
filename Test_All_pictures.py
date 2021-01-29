import mysql.connector as ms
import glob
import os
import cv2
import LBPH_algorithm
import pickle
import FaceDetection as FC

MyDB = ms.connect(
    host="localhost",
    database="images",
    user="admin",
    password="burguesllavall19993",
)
my = MyDB.cursor()


def Compare(hist1, hist2):

    value = sum((p - q) ** 2 for p, q in zip(hist1, hist2)) ** .5
    value = sum(value)
    return value


filename = 'dictionary'
infile = open(filename, 'rb')
new_dict = pickle.load(infile)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

image_dir = os.path.join(BASE_DIR, "Test_images/")


folders = glob.glob(image_dir)
imagenames_list = {}

"""We go all over the images and perform the recognition"""

for file in glob.glob(image_dir):
    imagenames_list[os.path.basename(os.path.normpath(file))] = file

Final_result = []
Values_result = []
for i, values in imagenames_list.items():

    image = FC.DetectFace(values)

    if image == []:
        Final_result.append(("notFound"))
        Values_result.append("-")
        continue
    else:
        print("here")
        x = LBPH_algorithm.Histograms(image)
        final = {}
        for key, ev in new_dict.items():
            final[key] = Compare(x, ev)
        # after doing the euclidean distance we sort the results
        t = {k: v for k, v in sorted(final.items(), key=lambda item: item[1])}
        print(list(t.keys())[0])
        Final_result.append(list(t.keys())[1])
        Values_result.append(values)

""" Here we will be able to see how many results have been correct and how many it wasn't"""
print(Final_result)
result = []
for i, values in imagenames_list.items():
    result.append(i)
print(result)

test_train = dict(zip(Final_result, Values_result))


def calling(folder, index):
    # saving the image that has been recognised in the specific folder
    for i, values in test_train.items():
        if i == index:
            image = cv2.imread(test_train[i])
            cv2.imshow('', image)
            path = "/Users/gerardburgues/Documents/Computer Vision/Projecte_DB/SetDatabase/" + folder
            cv2.imwrite(os.path.join(path, 'prova.jpg'), image)


def SaveinFolder(index):
    # we see what person is the result of the recognition
    if index > 1 and index <= 13:

        txt = input("Type your folder name related to Jordi")
        dir = CreateFolder(txt)
        calling(dir, index)
    elif index >= 14 and index <= 31:
        txt = input("Type your folder name related to Gerard")
        dir = CreateFolder(txt)
        calling(dir, index)
    elif index >= 32 and index <= 43:
        txt = input("Type your folder name related to Nuria")
        dir = CreateFolder(txt)
        calling(dir, index)
    elif index >= 44 and index <= 57:
        txt = input("Type your folder name related to Jordi_Gran")
        dir = CreateFolder(txt)
        calling(dir, index)
    elif index >= 58 and index <= 70:
        txt = input("Type your folder name related to Ramon")
        dir = CreateFolder(txt)
        calling(dir, index)
    elif index >= 71 and index <= 83:
        txt = input("Type your folder name related to Neus")
        dir = CreateFolder(txt)
        calling(dir, index)
    elif index >= 84 and index <= 100:
        txt = input("Type your folder name related to Pepita")
        dir = CreateFolder(txt)
        calling(dir, index)


def CreateFolder(folder):
    #create folder in case is no already created
    print('this is my folder', folder)
    pathh = os.getcwd()
    parent_dir = pathh
    directory = folder
    print(pathh)
    pathh1 = os.path.join(parent_dir, directory)
    if os.path.isdir(folder) == False:
        os.mkdir(pathh1)
        print("directory created", directory)
    return directory


def EndGame(id):
    """we retrieve  with the specific ID and save it in the folder"""
    if id == "notFound":
        print("there is nothing")
    else:
        SQLStatement = ("""SELECT * FROM Data_image
                     WHERE label_id = %s""")
        my.execute(SQLStatement, (id,))

        record = my.fetchall()
        for row in record:
            SaveinFolder(row[3])
            print(row[3])

# for every result we got

for i in Final_result:

    EndGame(i)

infile.close()
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
