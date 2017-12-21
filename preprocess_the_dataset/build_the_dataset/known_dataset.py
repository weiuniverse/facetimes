import face_recognition
import os
import json

def know_dataset(path):
    name_list = os.listdir(path)
    image_list= []
    encoding_list=[]
    encoding_dict = {}
    for name in name_list:
        print('Loading',name)
        image = (face_recognition.load_image_file(path+name))
        image_list.append(image)
        face_encoding = face_recognition.face_encodings(image)[0]
        encoding_list.append(face_encoding.tolist())

    f = open("E:\\cse527\\facetimes\\facetimes\\preprocess_the_dataset\\known_people\\encode_list.json",'w')
    f.write(json.dumps(encoding_list, ensure_ascii=False))
    f.close()
    f = open("E:\\cse527\\facetimes\\facetimes\\preprocess_the_dataset\\known_people\\name_list.json",'w')
    f.write(json.dumps(name_list, ensure_ascii=False))
    f.close()
    return name

# know_dataset("../known_people/")
know_dataset("E:\\cse527\\facetimes\\facetimes\\preprocess_the_dataset\\known_people\\")
