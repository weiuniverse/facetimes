# FaceTimes: A website frame for face detection,recognition,landmark localization and modification
## Abstract:
  We design a website for face detection,face recognition,face landmard localization and face modification.

## Introduction
Recent years, computer vision becomes popular. Many companies apply vision techniques into applications about face. The basic applications include face detection,face recognition,face landmark localization.
Therefore, we determined to design a website include these functions.

## Functions
The main functions of our website is shown in the graph.

### Face Detection
The fundamental function of face applications is face detection. Only after we find a face, we can do the following things. Here we use dlib to implement the face detection. It's a very useful tool for face application develop.

### Face Recognition
After we detect the face, we can do face recognition. There is a small dataset for some known people. We didn't put too much people into the dataset due to the limited time and disk space. For recognition, we need to encode the face at first. Here we use face_recognition package to implement the encoder. The For every face, we will get encoded id. To compare the id with the face id in the dataset, we can know who he is if the face is in the dataset.

### Face Attributions
We selected 4 Attributions of face include gender,smile,glasses and head pose. To predict these attributions, we design a convolutional nerual network. In order to train the network, we find a dataset include more than 10,000 images and attributions. To use the dataset, we should first crop all faces in the dataset. However, we found some images have two faces, and we chose the biggest one. When preprocessing the image, we find the cropped face is too large for our task since the four attributions don't need too much details. In order to save the limited computing resource, we decide to scale the images into 64x64 which is enough for our task.

### Face Landmark Localization
We tried to design a deep convolution nerual network framework to do landmark detection, but due to the limit time, we give it up. And we finally chose to use a existed dlib model to implement this.

### Face Modification
Here, we implement face modifcation by swap. Codes partly borrow from https://github.com/QuantumLiu/FaceSwapper. For face swap task, we will have a swap face and model face. Model faces are provided by us. Then we need to get the landmark of two faces and construct an affine matrix with these points. With the affine operation, we can rotate the swap face in order to align to the model face. Then we draw a mask in the swap face and swap the mask on the model face. And we should correct the the picture with guassian filter and get our final result.

## Web Frame
## Acknowledgement
The library we used include keras,opencv,dlib,face_rocognition.
And the code for face swap partly borrow from https://github.com/QuantumLiu/FaceSwapper.
