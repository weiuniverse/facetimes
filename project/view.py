# -*- coding:utf-8 -*-

import json
import base64
import os
import uuid
import numpy as np
from . import face_detection_v3 as fd
from . import utils
from . import tools

from django.conf import settings
from PIL import ImageFile
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import cv2

default_img_list = []

def load_face(image_directory):
    global default_img_list
    name_list = os.listdir(image_directory)
    for name in name_list:
        default_img_list.append({'path':image_directory+name})
    return 0
load_face('./static/pictures/')
augment_btn_list = []

# func is defined as tools.binary2mat
# augment_btn_list.append({'name': 'Alignment', 'func': fd.face.face_align})
augment_btn_list.append({'name': 'To Trump', 'func': fd.face.face_swap_trump})
augment_btn_list.append({'name': 'To CG Style', 'func': fd.face.face_swap_ff})
augment_btn_list.append({'name': 'To Man', 'func': fd.face.face_swap_man})
augment_btn_list.append({'name': 'To Woman', 'func': fd.face.face_swap_woman})


BASE64_HEADER = 'data:image/jpg;base64,'

def display_view(request):
    context = {}
    context['default_img_list'] = default_img_list
    context['aug_btn_list'] = augment_btn_list
    return render(request, 'main.html', context)

def camera_demo(request):
    context = {}
    return render(request, 'basic.html', context)


@csrf_exempt  # Not perform csrf check since complexity
def upload(request):
    print("---- Uploading STARTs ----")

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    file = request.FILES.get("file", None)
    result_list = {}

    (rs, info) = _upload(file)
    result_list['rs'] = 'Success' if rs == 1 else 'Failed'
    result_list['info'] = info
    if rs == 1:
        # Face Dectection
        filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/' + result_list['info']

        img = fd.read_img(filepath)
        facetimes = fd.face()
        rects, faces = facetimes.face_detection(img)

        # Detection Result
        faces_list = rects
        result_list['faces_list'] = []
        for face in faces_list:
            result_list['faces_list'].append({'pt_x': face[0], 'pt_y': face[1], 'width': face[2], 'height': face[3]})

        for i, face in enumerate(faces):
            img = tools.mat2binary(face)
            img_64 = binary2base64(img)
            result_list['faces_list'][i]['base64'] = BASE64_HEADER + img_64
    print("---- Uploading ENDs ----")
    response.write(json.dumps(result_list, ensure_ascii=False))

    return response


def _upload(file):
    '''Image Uploading and Storing'''
    if file:
        path = os.path.join(settings.MEDIA_ROOT, 'static/upload')
        file_name = str(uuid.uuid1()) + ".jpg"
        path_file = os.path.join(path, file_name)

        parser = ImageFile.Parser()
        for chunk in file.chunks():
            parser.feed(chunk)
        try:
            img = parser.close()
        except OSError:
            return 2, 'Not an image.'

        try:
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(path_file, 'jpeg', quality=100)
        except Exception as e:
            print(str(e))
            return 3, 'Cannot save as jpg file.'
        return 1, path_file
    return 4, 'No file attached.'


def upload_default(request):
    print("---- Uploading default STARTs ----")

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    result_list = {}

    if request.POST:
        src = request.POST['src']
    else:
        src = ""

    invalid_src = False
    for i, default_img in enumerate(default_img_list):
        if default_img['path'] == src:
            invalid_src = True
            break

    if invalid_src:
        result_list['rs'] = 'Success'
        result_list['info'] = src
        # TODO: Face Detection
        # filepath = os.path.join(os.path.join(settings.BASE_DIR, 'static/image'),result_list['info'])
        filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + result_list['info']
        img = fd.read_img(filepath)
        facetimes = fd.face()
        rects, faces = facetimes.face_detection(img)

        # Detection Result
        faces_list = rects
        # faces_list = np.array([[0,0,50,50],[20,20,40,50]], dtype=np.float)
        result_list['faces_list'] = []
        for face in faces_list:
            result_list['faces_list'].append(
                {'pt_x': face[0], 'pt_y': face[1], 'width': face[2], 'height': face[3]})

        for i, face in enumerate(faces):
            img = tools.mat2binary(face)
            img_64 = binary2base64(img)
            # print(type(img_64), type(BASE64_HEADER))
            result_list['faces_list'][i]['base64'] = BASE64_HEADER + img_64

    else:
        result_list = {'rs': 'Failed', 'info': 'Not a valid default image'}
    response.write(json.dumps(result_list, ensure_ascii=False))
    print("---- Uploading default ENDs ----")

    return response

def upload_snapshot(request):
    print("---- Uploading snapshot STARTs ----")

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    result_list = {}

    if request.POST:
        src = request.POST['src']
    else:
        src = ""

    path = os.path.join(settings.MEDIA_ROOT, 'static/upload')
    file_name = str(uuid.uuid1()) + ".jpg"
    path_file = os.path.join(path, file_name)

    binary_img = base642binary(src[22:]);

    f = open(path_file, 'wb')
    f.write(binary_img)
    f.close()

    result_list['rs'] = 'Success'
    result_list['info'] = path_file

    # filepath = os.path.join(os.path.join(settings.BASE_DIR, 'static/image'),result_list['info'])
    img = tools.binary2mat(binary_img)
    facetimes = fd.face()
    rects, faces = facetimes.face_detection(img)

    # Detection Result
    faces_list = rects
    # faces_list = np.array([[0,0,50,50],[20,20,40,50]], dtype=np.float)
    result_list['faces_list'] = []
    for face in faces_list:
        result_list['faces_list'].append(
            {'pt_x': face[0], 'pt_y': face[1], 'width': face[2], 'height': face[3]})

    for i, face in enumerate(faces):
        img = tools.mat2binary(face)
        img_64 = binary2base64(img)
        # print(type(img_64), type(BASE64_HEADER))
        result_list['faces_list'][i]['base64'] = BASE64_HEADER + img_64

    response.write(json.dumps(result_list, ensure_ascii=False))
    print("---- Uploading snapshot ENDs ----")

    return response


def landmark(request):
    print("---- Landmarking STARTs ----")

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"

    if request.POST:
        src = request.POST['src']
    else:
        src = ""

    img = base642binary(src[22:])
    img_cv = tools.binary2mat(img)

    # Get landmark by img_cv, result stored in landmark_list(68*[x,y])
    f1=fd.face()
    landmark_list = f1.face_landmark(img_cv).tolist()
    # landmark_list=[[10,10], [20,20],[30,30],[30,40],[20,50],[10,60]]
    gender,smile,glass,pose = f1.face_properties(img_cv)
    pathfile = "./tmp/"+str(uuid.uuid1())+".jpg"
    cv2.imwrite(pathfile,img_cv)
    pname = f1.face_recog(pathfile)
    os.remove(pathfile)
    response.write(json.dumps({'landmark':landmark_list, 'gender':gender, 'name':pname,'smile':smile,'glass':glass,'pose':pose}, ensure_ascii=False))
    print("---- Landmarking ENDs ----")
    return response


def augment(request):
    print("---- Augmenting STARTs ----")

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"

    if request.POST:
        src = request.POST['src']
        type = request.POST['type']
    else:
        src = ""
        type = ""
    # print(src)
    img = base642binary(src[22:])
    img_cv = tools.binary2mat(img)

    # Get augment by img_cv and type, result stored in aug_img(mat formatted image)
    aug_img = None
    for aug in augment_btn_list:
        # print(aug['name'],type[:-2])
        # print(type[-1])
        # print(list(type))
        type_list = type.split('\n')
        # print(type_list)
        type0 = type_list[0]
        # print(type0)
        if aug['name'] == type0:
            if not callable(aug['func']):
                aug_img = img
                # print('sssssssssssssssssssss')
            else:
                f1 = fd.face()
                aug_img_cv = aug['func'](f1, img_cv)
                # print('aaaaaaaaaaaaaaaaa')
                aug_img = tools.mat2binary(aug_img_cv)
            break

    if aug_img is None:
        aug_img = img

    aug_img_64 = BASE64_HEADER + binary2base64(aug_img)

    response.write(json.dumps(aug_img_64, ensure_ascii=False))
    print('---- Augmenting Ends ----')
    return response


def download(request):
    print("---- Downloading STARTs ----")

    if request.POST:
        src = request.POST['src']
    else:
        src = ""
    img = base642binary(src[22:])

    the_file_name = str(uuid.uuid1())+".jpg"
    response = HttpResponse(img)
    response['Content-Type'] = 'image/*'# 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    print("---- Downloading ENDs ----")
    return response


def binary2base64(binary):
    return base64.b64encode(binary).decode('ascii')


def base642binary(str):
    return base64.b64decode(str)
