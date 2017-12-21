# -*- coding:utf-8 -*-
import numpy as np
import cv2
from imutils import face_utils
import imutils
import dlib
import uuid
from . import utils
import json
# from . import utils
# import project.utils
import keras
import face_recognition
import os
# load the model

print("=======Loading Model=========")
detector = dlib.get_frontal_face_detector()
model_prop = keras.models.load_model('model.h5')
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
print("=======Finish Loading Model=========")

def load_known():
    known_path = './known_people_encode/'
    file = open(known_path+"encode_list.json")
    pre_encoding_list = json.loads(file.read())
    file.close()
    encoding_list = []
    for encode in pre_encoding_list:
        encoding_list.append(np.array(encode))
    file2 = open(known_path+"name_list.json")
    name_list = json.loads(file2.read())
    file2.close()
    return encoding_list,name_list

encoding_list,name_list = load_known()

FACE_SCALE = 1.2
class face:
# face detection
    def face_detection(self,image):
        global detector
        img = image.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = detector(gray,2)
        rect_list = []
        faces = []
        for rect in rects:
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            rect_list.append([x, y, w, h])
            face = img[y:y+h, x:x+w].copy()
            faces.append(face)
        return rect_list,faces

# facial landmark localization
    def face_landmark(self,image):
        global predictor
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        w,h,d = image.shape
        rect = dlib.rectangle(0,0,w,h)
        pts = predictor(gray, rect)
        pts = face_utils.shape_to_np(pts)
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        img = image.copy()
        return pts


    def face_landmark_background(self,image):
        global predictor
        global detector
        # detector = dlib.get_frontal_face_detector()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 2)
        for (i, rect) in enumerate(rects):
            pts = predictor(gray, rect)
            pts = face_utils.shape_to_np(pts)
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            img_copy = image.copy()
        return pts

# face alignment
    def face_alignment(self,face,std_image):
        face = cv2.resize(face,(100,100))
        pts = self.face_landmark(face)

        std_rects,std_faces = self.face_detection(std_image)
        std_face = std_faces[0]
        std_face = cv2.resize(std_face,(100,100))
        std_pts = self.face_landmark(std_face)

        affine_mat = utils.transformation_from_points(pts, std_pts)
        output_im = utils.warp_image(face,affine_mat,std_face.shape)
        return output_im
# face_swap
    def face_swap(self,face,std_image):

        face = cv2.resize(face,(100,100))
        pts = self.face_landmark(face)

        std_rects,std_faces = self.face_detection(std_image)
        std_face = std_faces[0]
        std_face = cv2.resize(std_face,(100,100))
        std_pts = self.face_landmark(std_face)

        affine_mat = utils.transformation_from_points(std_pts,pts)

        mask = utils.get_face_mask(face,pts)
        warped_mask = utils.warp_image(mask,affine_mat,std_face.shape)
        combined_mask = np.max([utils.get_face_mask(std_face,std_pts),warped_mask],axis=0)

        warp_face = utils.warp_image(face,affine_mat,std_face.shape)
        warped_corrected = utils.correct_colours(std_face,warp_face,std_pts)
        syn_face= std_face * (1.0 - combined_mask) + warped_corrected * combined_mask
        return syn_face

    def face_swap_background(self,face,std_image,method):
        '''
        swap the face to another face with background
        '''
        face = cv2.resize(face,(100,100))
        pts = self.face_landmark(face)
        temp_path = './template_images/'
        # read the pts for template_images
        file = open(temp_path+method+'.json','r')
        std_pts = json.loads(file.read())
        std_pts = np.array(std_pts)
        file.close()
        # compute the affine_mat
        affine_mat = utils.transformation_from_points(std_pts,pts)
        # get the mask
        mask = utils.get_face_mask(face,pts)
        warped_mask = utils.warp_image(mask,affine_mat,std_image.shape)
        combined_mask = np.max([utils.get_face_mask(std_image,std_pts),warped_mask],axis=0)

        warp_face = utils.warp_image(face,affine_mat,std_image.shape)
        warped_corrected = utils.correct_colours(std_image,warp_face,std_pts)
        syn_face= std_image * (1.0 - combined_mask) + warped_corrected * combined_mask
        return syn_face

    def face_swap_trump(self,face):
        std_img = cv2.imread('./template_images/trump.jpg')
        syn_face = self.face_swap_background(face,std_img,'trump')
        return syn_face

    def face_swap_ff(self,face):
        std_img = cv2.imread('./template_images/ff1.jpg')
        syn_face = self.face_swap_background(face,std_img,'ff1')
        return syn_face

    def face_swap_man(self,face):
        std_img = cv2.imread('./template_images/face1.jpg')
        syn_face = self.face_swap_background(face,std_img,'face1')
        return syn_face

    def face_swap_woman(self,face):
        std_img = cv2.imread('./template_images/Gaoyuanyuan.jpg')
        syn_face = self.face_swap_background(face,std_img,'Gaoyuanyuan')
        return syn_face

    # def face_align(self,face):
    #     std_img = cv2.imread('./template_images/chuanpu.jpg')
    #     output = self.face_alignment(face,std_img)
    #     return output

    def face_properties(slef,face):
        face = cv2.resize(face,(64,64))
        face = np.reshape(face,(1,64,64,3))
        results = model_prop.predict(face)
        print('result',results)
        predicted_genders = results[0][0]
        predicted_smile = results[0][1]
        predicted_glass = results[0][2]
        predicted_pose = results[0][3]

        gender = "No Result"
        smile = "No Result"
        glass = "No Result"
        pose = "No Result"

        # we found there are two much male in the dataset,which make it unbalance
        # so we manually set a parameter by test image
        if predicted_genders<1.71:
            gender = 'Male'
        else:
            gender = "Female"

        if predicted_smile<1.5:
            smile = 'Smile'
        else:
            smile = "No Smile"

        if predicted_glass<1.5:
            glass = 'Wearing glasses'
            # since more man wear glasses in the dataset
            if predicted_genders>1.4:
                gender = "Female"
        else:
            glass = 'No glasses'

        pose_angle = int((predicted_pose-1)*180/4)
        if pose_angle<85:
            pose = "Left: "+str(90-pose_angle)+" degrees"
        elif 85<=pose_angle and pose_angle<=95:
            pose = "Frontal"
        else:
            pose = "Right: "+str(pose_angle-90)+" degrees"

        return gender,smile,glass,pose

    def face_recog(self,face_path):
        global encoding_list
        global name_list
        name = "Unknown"
        unknown_image = face_recognition.load_image_file(face_path)
        try:
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        except Exception:
            return name

        known_faces = encoding_list
        results = face_recognition.compare_faces(known_faces, unknown_face_encoding,tolerance=0.5)
        print(results)
        for i in range(len(name_list)):
            if results[i]:
                name = name_list[i][:-4]
                return name
        return name

def read_img(filepath):
    image = cv2.imread(filepath)
    return image

def load_the_kerasmodel():
    print("==========Loading Keras_model==========")
    img = cv2.imread('./static/pictures/facess.jpg')
    face_pre = face()
    rects,faces = face_pre.face_detection(img)
    face1 = faces[0]
    face2 = face1.copy()
    result = face_pre.face_properties(face1)
    print("======Finish Loading Keras_model========")

    return 0

load_the_kerasmodel()
