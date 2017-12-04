# -*- coding:utf-8 -*-

import numpy as np
import cv2
from imutils import face_utils
import imutils
import dlib
import uuid
from . import utils
from project.wide_resnet import WideResNet
import face_recognition
import os

FACE_SCALE = 1.2
class face:
# face detection
    def face_detection(self,image):
        detector = dlib.get_frontal_face_detector()
        img = image.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = detector(gray,2)
        rect_list = []
        faces = []
        for rect in rects:
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            rect_list.append([x, y, w, h])
            face = img[y:y+h, x:x+w].copy()
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            faces.append(face)

        return rect_list,faces

# facial landmark localization
    def face_landmark(self,image):
        # detector = dlib.get_frontal_face_detector()
        # image = imutils.resize(image, width=500)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        # rects = detector(gray, 2)
        w,h,d = image.shape
        print(w,h)
    	# determine the facial landmarks for the face region, then
    	# convert the facial landmark (x, y)-coordinates to a np
    	# array
        rect = dlib.rectangle(0,0,w,h)
        pts = predictor(gray, rect)
        pts = face_utils.shape_to_np(pts)
    	# convert dlib's rectangle to a OpenCV-style bounding box
    	# [i.e., (x, y, w, h)], then draw the face bounding box
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        img = image.copy()

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    	# show the face number
        cv2.putText(img, "Face #{}".format(1), (x - 10, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    	# loop over the (x, y)-coordinates for the facial landmarks
    	# and draw them on the image
        for (x, y) in pts:
    	    cv2.circle(img, (x, y), 1, (0, 0, 255), -1)

        # cv2.imshow("std_face",img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # pts = pts.tolist()
        return pts

    def face_landmark_background(self,image):
        detector = dlib.get_frontal_face_detector()
        # image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        # rects = int(rects)
        rects = detector(gray, 2)
        for (i, rect) in enumerate(rects):
        	# determine the facial landmarks for the face region, then
        	# convert the facial landmark (x, y)-coordinates to a np
        	# array
            pts = predictor(gray, rect)
            pts = face_utils.shape_to_np(pts)
        	# convert dlib's rectangle to a OpenCV-style bounding box
        	# [i.e., (x, y, w, h)], then draw the face bounding box
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            img_copy = image.copy()
            cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

        	# show the face number
            cv2.putText(img_copy, "Face #{}".format(i + 1), (x - 10, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        	# loop over the (x, y)-coordinates for the facial landmarks
        	# and draw them on the image
            for (x, y) in pts:
        	    cv2.circle(img_copy, (x, y), 1, (0, 0, 255), -1)
        # pts = pts.tolist()
        # print(type(pts))
        return pts

# face alignment
    def face_alignment(self,face,std_image):
        face = cv2.resize(face,(100,100))
        pts = self.face_landmark(face)

        std_rects,std_faces = self.face_detection(std_image)
        std_face = std_faces[0]
        std_face = cv2.resize(std_face,(100,100))
        std_pts = self.face_landmark(std_face)

        cv2.imshow("std_face",std_face)

        affine_mat = utils.transformation_from_points(pts, std_pts)
        output_im = utils.warp_image(face,affine_mat,std_face.shape)
        cv2.imshow("out",output_im)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return output_im

    def face_swap(self,face,std_image):

        face = cv2.resize(face,(100,100))
        # face = face * (1/255.0)
        pts = self.face_landmark(face)

        std_rects,std_faces = self.face_detection(std_image)
        std_face = std_faces[0]
        # std_face = std_face *(1/255.0)
        std_face = cv2.resize(std_face,(100,100))
        std_pts = self.face_landmark(std_face)

        affine_mat = utils.transformation_from_points(std_pts,pts)

        mask = utils.get_face_mask(face,pts)
        warped_mask = utils.warp_image(mask,affine_mat,std_face.shape)
        # cv2.imshow("warpmask",warped_mask)
        combined_mask = np.max([utils.get_face_mask(std_face,std_pts),warped_mask],axis=0)

        warp_face = utils.warp_image(face,affine_mat,std_face.shape)
        warped_corrected = utils.correct_colours(std_face,warp_face,std_pts)
        syn_face= std_face * (1.0 - combined_mask) + warped_corrected * combined_mask

        # cv2.imshow("11",std_face * (1.0 - combined_mask))
        # cv2.imshow("mask",warped_corrected*combined_mask)
        # cv2.imshow("out",syn_face)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return syn_face

    def face_swap_background(self,face,std_image):

        face = cv2.resize(face,(100,100))
        # face = face * (1/255.0)
        pts = self.face_landmark(face)

        # std_rects,std_faces = self.face_detection(std_image)
        # std_face = std_faces[0]
        # std_face = std_face *(1/255.0)
        # std_face = cv2.resize(std_face,(100,100))
        std_pts = self.face_landmark_background(std_image)

        affine_mat = utils.transformation_from_points(std_pts,pts)

        mask = utils.get_face_mask(face,pts)
        warped_mask = utils.warp_image(mask,affine_mat,std_image.shape)
        # cv2.imshow("warpmask",warped_mask)
        combined_mask = np.max([utils.get_face_mask(std_image,std_pts),warped_mask],axis=0)

        warp_face = utils.warp_image(face,affine_mat,std_image.shape)
        warped_corrected = utils.correct_colours(std_image,warp_face,std_pts)
        syn_face= std_image * (1.0 - combined_mask) + warped_corrected * combined_mask

        # cv2.imshow("11",std_image * (1.0 - combined_mask))
        # cv2.imshow("mask",warped_corrected*combined_mask)
        # cv2.imshow("out",syn_face)
        # cv2.waitKey(0)

        return syn_face

    def face_swap_chuangpu(self,face):
        std_img = cv2.imread('./template_images/chuanpu.jpg')
        syn_face = self.face_swap_background(face,std_img)
        return syn_face

    def face_swap_ff(self,face):
        std_img = cv2.imread('./template_images/ff1.jpg')
        syn_face = self.face_swap_background(face,std_img)
        return syn_face

    def face_swap_man(self,face):
        std_img = cv2.imread('./template_images/face1.jpg')
        syn_face = self.face_swap_background(face,std_img)
        return syn_face

    def face_swap_woman(self,face):
        std_img = cv2.imread('./template_images/images.jpg')
        syn_face = self.face_swap_background(face,std_img)
        return syn_face

    def face_age_gender(self,face):
        # w,h,c = faces[0].shape
        # print(w)
        # img_size = w
        face = cv2.resize(face,(64,64))
        face = np.reshape(face,(1,64,64,3))
        results = model.predict(face)
        predicted_genders = results[0]
        ages = np.arange(0, 101).reshape(101, 1)
        predicted_genders = results[0]
        gender = "No Result"
        if predicted_genders[0][0]<0.5:
            gender = 'Male'
        else:
            gender = "Female"
        predicted_ages = results[1].dot(ages).flatten()
        predicted_ages = int(predicted_ages)
        print(gender)
        print(predicted_ages)
        return predicted_ages,gender

    def face_recog(self,face_path):
        #  将jpg文件加载到numpy数组中
        unknown_image = face_recognition.load_image_file(face_path)
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

        name_list = os.listdir("./known_people/")
        # print(name_list)
        image_list= []
        enconding_list=[]
        for name in name_list:
            image = (face_recognition.load_image_file("./known_people/"+name))
            image_list.append(image)
            face_encoding = face_recognition.face_encodings(image)[0]
            enconding_list.append(face_encoding)
        known_faces = enconding_list

        # 获取每个图像文件中每个面部的面部编码
        # 由于每个图像中可能有多个面，所以返回一个编码列表。
        # 但是由于我知道每个图像只有一个脸，我只关心每个图像中的第一个编码，所以我取索引0。
        # 结果是True/false的数组，未知面孔known_faces阵列中的任何人相匹配的结果

        results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
        name = "Unknown"
        for i in range(len(name_list)):
            if results[i]:
                name = name_list[i][:-4]
        # if results[0]:
            # name = "baby"
        # elif results[1]:
            # name = "chenglong"
        # else:
            # name = "Unknown"
        return name

def read_img(filepath):
    image = cv2.imread(filepath)
    return image


'''
std_img = cv2.imread('./images/ff1.jpg')
# f1.face_landmark(std_img)
# f1.face_alignment(face,std_img)
syn_face = f1.face_swap_ff(face)
cv2.imwrite("out.jpg",syn_face)
out = cv2.imread('out.jpg')
cv2.imshow("out",out)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
img_size = 64
depth = 16
k = 8
weight_file = "weights.18-4.06.hdf5"
model = WideResNet(img_size, depth=depth, k=k)()
model.load_weights(weight_file)


img = cv2.imread('./static/image/facess.jpg')
f2 = face()
rects,faces = f2.face_detection(img)
face1 = faces[0]
face2 = face1.copy()

face1 = cv2.resize(face1,(64,64))
face1 = np.reshape(face1,(1,64,64,3))
resultss = model.predict(face1)
# cv2.imshow("face1")

# face2 = face2.astype(np.uint8)
'''
pathfile = "./tmp/"+str(uuid.uuid1())+".jpg"
cv2.imwrite(pathfile,face2)
result_name = f2.face_recog(pathfile)
print(result_name)
# print(resultss)
'''
