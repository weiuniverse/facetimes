import os
import cv2
import uuid


def mat2binary(mat_img):
    filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static/upload/' + str(
        uuid.uuid1()) + '.jpg'

    cv2.imwrite(filepath, mat_img)

    f = open(filepath, 'rb')
    content = f.read()
    f.close()

    os.remove(filepath)
    return content


def binary2mat(binary_img):
    filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static/upload/' + str(
        uuid.uuid1()) + '.jpg'

    f = open(filepath, 'wb')
    f.write(binary_img)
    f.close()

    content = cv2.imread(filepath)

    os.remove(filepath)
    return content