import cv2
import numpy as np
import face_recognition
import os
import json
from datetime import datetime
class FaceRecognize(path = "Train_image"):
    def __init__(self):
        # read the json for existing encodings
        self.encodedDataFile = open(f'{path}/encodedImages.json','w+')
        # self.encodedData = json.load(self.encodedDataFile)
        self.encodedData = {}

    def readJson(self):
        encodedDataJson = json.load(self.encodedDataFile)
        for k,v in encodedDataJson:
            self.encodedData[k] = np.array(v)

    def writeJson(self, name, encodedImage):
        encodedImageList = encodedImage.tolist()


    # for all the images in the given path encode and store
    def EncodeAll(self):
        # remove all existing encodings
        self.encodedDataFile.truncate()
        images = []
        names = []
        myList = os.listdir((path))
        print(myList)

        for cl in myList:
            curImg = cv2.imread((f'{path}/{cl}'))
            images.append(curImg)
            names.append(os.path.splitext(cl)[0])

        print(names)
        encodedImages = Encode(images)
        print("Encoding Complete")
    def Encode(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imageEncoding = face_recognition.face_encodings(image)[0]
        return imageEncoding
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgEncode = face_recognition.face_encodings(img)[0]
            encodeList.append(imgEncode)
        return encodeList
    def updateEncodings(self,image, name):
        encodedImage = self.Encode(image)
        self.encodedData[name] = encodedImage
    def markAttendance(name):
        with open('attendance.csv','r+') as f:
            dataList = f.readlines()
            nameList = []
            for line in dataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dateString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dateString}')

path = "Train_image"
images = []
names  = []
myList = os.listdir((path))
print(myList)

for cl in myList:
    curImg = cv2.imread((f'{path}/{cl}'))
    images.append(curImg)
    names.append(os.path.splitext(cl)[0])

print(names)
encodedImages = Encode(images)
print("Encoding Complete")
imgElon = face_recognition.load_image_file("Train_image/elonMuskf.jpeg")
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
faceLoc = face_recognition.face_locations(imgElon)
encodeElon = face_recognition.face_encodings(imgElon)
for encodeFace, faceLoc in zip(encodeElon, faceLoc):
            matches = face_recognition.compare_faces(encodedImages, encodeFace)
            faceDis = face_recognition.face_distance(encodedImages, encodeFace)
            print(matches, faceDis)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = names[matchIndex]
                print(name)
                markAttendance(name)

# for camera capture
# cap = cv2.VideoCapture("0")
# print(cap)
# while True:
#     print ("inside loop")
#     try:
#         success, img = cap.read()
#         print(success,img)
#         # imgS = cv2.resize(img, (0,0),None,0.25,0.25)
#         # imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
#         # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         cv2.imshow('Video', img)
#
#         # facesCurFrame = face_recognition.face_locations(imgS)
#         # encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
#
#         # for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
#         #     matches = face_recognition.compare_faces(encodedImages, encodeFace)
#         #     faceDis = face_recognition.face_distance(encodedImages, encodeFace)
#         #     print(faceDis)
#                 print(matches, faceDis)
#                 matchIndex = np.argmin(faceDis)
#                 if matches[matchIndex]:
#                     name = names[matchIndex]
#                     print(name)
#                     y1,x2,y2,x1 = faceLoc
#                     # #multiply by 4 as downscaled
#                     y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1 * 4
#                     cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
#                     cv2.rectangle(img,(x1,y1-35),(x2-y2),(0,255,0),cv2.FILLED)
#                     cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,1(255,255,255),2)
#         cv2.imshow('webcam',img)
#         cv2.waitKey(1)
#     except Exception as e:
#         print(e)
