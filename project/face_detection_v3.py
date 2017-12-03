import numpy as np
import cv2
# import tensorflow as tf
from imutils import face_utils
# import argparse
import imutils
import dlib
# from FaceSwapper.faceswapper import Faceswapper
from . import utils

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

def read_img(filepath):
    image = cv2.imread(filepath)
    return image
'''

img = cv2.imread('./images/face1.jpg')
f1 = face()
rects,faces = f1.face_detection(img)
face = faces[0]
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
