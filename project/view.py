# -*- coding:utf-8 -*-

import json
import base64
import os
import uuid
from . import face_detection_v3 as fd
from . import utils
from . import tools

from django.conf import settings
from PIL import ImageFile
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

default_img_list = []
default_img_list.append({'path': u'/static/image/face1.jpg'})
default_img_list.append({'path': u'/static/image/chuanpu.jpg'})
default_img_list.append({'path': u'/static/image/ff.jpeg'})
default_img_list.append({'path': u'/static/image/jojo.jpeg'})
default_img_list.append({'path': u'/static/image/waifu2.jpg'})
default_img_list.append({'path': u'/static/image/aoi_kioku.jpg'})
default_img_list.append({'path': u'/static/image/suzukaze_aoiba.jpeg'})

augment_btn_list = []
# func is defined as tools.binary2mat
augment_btn_list.append({'name': 'Aug1', 'func': None})
augment_btn_list.append({'name': 'Aug2', 'func': None})
augment_btn_list.append({'name': 'Aug3', 'func': None})
augment_btn_list.append({'name': 'Aug4', 'func': None})

BASE64_HEADER = 'data:image/jpg;base64,'

def display_view(request):
    context = {}
    context['default_img_list'] = default_img_list
    context['aug_btn_list'] = augment_btn_list
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
        filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/' + result_list['info']
        print('filepath=' + filepath)
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

    response.write(json.dumps(result_list, ensure_ascii=False))
    return response


def _upload(file):
    '''Image Uploading and Storing'''
    if file:
        path = os.path.join(settings.MEDIA_ROOT, 'static/upload')
        file_name = str(uuid.uuid1()) + ".jpg"
        path_file = os.path.join(path, file_name)
        print("path=" + path)
        print("path_file=" + path_file)
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

    invalid_src = False
    print("unquote filename = "+src)
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
        print('filepath=' + filepath)
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
            result_list['faces_list'][i]['base64'] = BASE64_HEADER + img_64

    else:
        result_list = {'rs': 'Failed', 'info': 'Not a valid default image'}
    response.write(json.dumps(result_list, ensure_ascii=False))
    return response


def landmark(request):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"

    if request.POST:
        src = request.POST['src']
    else:
        src = ""

    img = base642binary(src[22:])
    img_cv = tools.binary2mat(img)

    # TODO: Get landmark by img_cv, result stored in landmark_list(68*[x,y])
    landmark_list=[[10,10], [20,20],[30,30],[30,40],[20,50],[10,60]]

    response.write(json.dumps(landmark_list, ensure_ascii=False))
    return response


def augment(request):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"

    if request.POST:
        src = request.POST['src']
        type = request.POST['type']
    else:
        src = ""
        type = ""

    img = base642binary(src[22:])
    img_cv = tools.binary2mat(img)

    print("aug type = "+type+" src= "+src)
    # TODO: Get augment by img_cv and type, result stored in aug_img(mat formatted image)
    aug_img = None
    for aug in augment_btn_list:
        if aug['name'] == type:
            if not callable(aug['func']):
                aug_img = img
            else:
                aug_img_cv = aug['func'](img_cv)
                aug_img = tools.mat2binary(aug_img_cv)
            break

    if aug_img is None:
        aug_img = img

    aug_img_64 = BASE64_HEADER + binary2base64(aug_img)

    response.write(json.dumps(aug_img_64, ensure_ascii=False))
    print('Augment Ends')
    return response


def download(request):
    the_file_name = str(uuid.uuid1())+".jpg"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)


def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def binary2base64(binary):
    return base64.b64encode(binary)


def base642binary(str):
    return base64.b64decode(str)

