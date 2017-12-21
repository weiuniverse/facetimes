temp_path = './template_images/'
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()

def landmark_templ(temp_path):
    global predictor
    name_list = os.listdir(temp_path)
    for name in name_list:
        landmark = face_landmark_background(image)
        if type(landmark)==str:
            continue
        f = open(temp_path+name[:-4]+'.json','w')
        f.write(json.dumps(landmark, ensure_ascii=False))
        f.close()

    return name

def face_landmark_background(image_name):
    global detector
    global predictor
    image = cv.imread(image_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 2)
    for (i, rect) in enumerate(rects):
        if i>=1:
            print(image_name+"more than one face,skip it")
            return "skip"
        pts = predictor(gray, rect)
        pts = face_utils.shape_to_np(pts)
        (x, y, w, h) = face_utils.rect_to_bb(rect)
    return pts
