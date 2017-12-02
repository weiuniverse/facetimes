# -*- coding:utf-8 -*-

import json

import os
import uuid
import numpy as np
from . import face_detection_v3 as fd
from . import utils

from django.conf import settings
from PIL import ImageFile
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

default_img_list = []
default_img_list.append({'path': '/static/image/2.jpg'})
default_img_list.append({'path': '/static/image/5.jpg'})
default_img_list.append({'path': '/static/image/IMG_0386.PNG'})
default_img_list.append({'path': '/static/image/input1.jpg'})
default_img_list.append({'path': '/static/image/smile.png'})
default_img_list.append({'path': '/static/image/青い記憶.jpg'})
default_img_list.append({'path': '/static/image/face1.jpg'})

def display_view(request):
    context = {}
    context['hello'] = 'Hello World!'
    athlete = []
    athlete.append({'name': '111'})
    athlete.append({'name': '222'})
    athlete.append({'name': '333'})
    context['athlete_list'] = athlete
    context['response_JSON'] = json.dumps(athlete, ensure_ascii=False)
    context['default_img_list'] = default_img_list
    return render(request, 'main.html', context)


@csrf_exempt  # Not perform csrf check since complexity
def upload(request):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    file = request.FILES.get("file", None)
    result_list = {}

    (rs, info) = _upload(file)
    result_list['rs'] = 'Success' if rs == 1 else 'Failed'
    result_list['info'] = info
    if rs == 1:
        # TODO: Face Dectection
        filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'+result_list['info']
        print('filepath='+filepath)
        img = fd.read_img(filepath)
        facetimes = fd.face()
        rects,faces = facetimes.face_detection(img)

        # Detection Result
        faces_list = rects
        result_list['faces_list'] = []
        for face in faces_list:
            result_list['faces_list'].append({'pt_x':face[0], 'pt_y':face[1], 'width':face[2], 'height':face[3]})

    response.write(json.dumps(result_list, ensure_ascii=False))
    return response


def _upload(file):
    '''Image Uploading and Storing'''
    if file:
        path = os.path.join(settings.MEDIA_ROOT, 'static/upload')
        file_name = str(uuid.uuid1()) + ".jpg"
        path_file = os.path.join(path, file_name)
        print("path="+path)
        print("path_file="+path_file)
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
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    result_list = {}

    if request.POST:
        src = request.POST['src']
    else:
        src = ""
    print('src='+src)
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
        filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+result_list['info']
        print('filepath='+filepath)
        img = fd.read_img(filepath)
        facetimes = fd.face()
        rects,faces = facetimes.face_detection(img)

        # Detection Result
        faces_list = rects
        # faces_list = np.array([[0,0,50,50],[20,20,40,50]], dtype=np.float)
        result_list['faces_list'] = []
        for face in faces_list:
            result_list['faces_list'].append({'pt_x':face[0], 'pt_y':face[1], 'width':face[2], 'height':face[3]})

    else:
        result_list = {'rs': 'Failed', 'info':'Not a valid default image'};
    response.write(json.dumps(result_list, ensure_ascii=False))
    return response
