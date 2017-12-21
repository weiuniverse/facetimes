# import tensorflow as tf
import numpy as np
from skimage import io
import dlib
from imutils import face_utils
import cv2
import pickle
import os

def face_detection(image):
    detector = dlib.get_frontal_face_detector()
    img = image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector(gray,2)
    max = 100
    face = np.zeros((64,64,3))
    flag = 0
    for rect in rects:
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        if w*h>max and x>=0and y>=0:
            flag = 1
            max = w*h
            face = img[y:y+h, x:x+w,:].copy()
            # print(x,y,w,h)
            # print(face)
            # cv2.imshow("face",face)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
    if flag == 1:
        face = cv2.resize(face,(64,64),interpolation = cv2.INTER_CUBIC)

    return face,flag


def processed_data():
    train_root = 'E:\\face_detection\\gender_age\\dataset\\MTFL\\'
    file_root =  'E:\\face_detection\\gender_age\\dataset\\MTFL\\training.txt'
    f = open(file_root,'r')
    file = list()
    num = 0
    for line in open(file_root):
        line = f.readline()
        file.append(line)
        num = num + 1
        if(num==50000):
            break
    f.close()
    # data_points = np.zeros([num,4])
    data_points = []
    data_images = []
    label = open("../dataset/processed/label.txt","w")
    for i,unit in enumerate(file):
        print(i)
        unit = unit.split()
        image_path = train_root + unit[0]
        img = cv2.imread(image_path)
        img,flag = face_detection(img)
        if flag == 0:
            continue
        data_images.append(img)
        data_points.append(unit[11:])

        cv2.imwrite("../dataset/processed/faces/"+str(i)+".jpg",img)
        label.write(str(unit[11:])+'\n')
    label.close()
    data_images = np.array(data_images)
    data_points = np.array(data_points)
    return(data_images,data_points)

def fix_image():
    os.list_dir

def read_data():
    print("reading data")
    train_root = '.\\data\\faces\\'
    file_root =  '.\\data\\label.txt'
    file = open(file_root,'r')
    lines = file.readlines()
    # print(len(lines))
    image_list = os.listdir(train_root)
    images = []
    for image_name in image_list:
        image_name = image_name[:-4]
        # print(image_name)
        images.append(int(image_name))
    images.sort()
    # print(images)
    data = []
    # for i  in range(len(images)):
    labels = []
    # for i in range(10):
    for i  in range(len(images)):
        # print(train_root+str(images)+'.jpg')
        print(i)
        img = cv2.imread(train_root+str(images[i])+'.jpg')
        # cv2.imshow("1",img)
        # cv2.waitKey(0)
        data.append(img)
        line = lines[i]
        label = [int(line[2]),int(line[7]),int(line[12]),int(line[17])]
        labels.append(label)

    # labels = []
    # for line in lines:
    # for line in lines[0:100]
        # label = [line[2],line[7],line[12],line[17]]
        # labels.append(label)
        # print(label)
        # i = i+1
    print("finish reading")
    return data,labels

# image,label = read_data()
# images = np.array(image)
# print(label[0])
# print(type(images))
# processed_data()
# data_images,data_points = read_data()
# data,labels = read_data()
# print(data[0])
# print(data[0].shape)
# images = pickle.dumps(data_images)
# points = pickle.dumps(data_points)

# with open("images.pkl", "wb") as f:
    # pickle.dump(images, f)

# def save_face(data_images):

# with open("data.pkl") as f:
    # images = pickle.load(f)

# cv2.imshow(images[0])
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# pickle.dump(images,open("images.pkl", "wb"))
# pickle.dump(points,open("points.pkl", "w"))
# file_root =  'E:\\face_detection\\gender_age\\dataset\\MTFL\\training.txt'
# file = open(file_root,'r')
