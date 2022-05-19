import cv2
import numpy as np
import face_recognition
import os
import json
from datetime import datetime
class FaceRecognize():
    def __init__(self,path = "Train_image"):
        self.path = path
        # read the json for existing encodings
        self.encodedDataFile = open('encodedImages.json', 'r+')
        self.encodedImages = []
        self.names = []
        try:
            self.readJson()
        except:
            print("could not read json, starting encoding")
        finally:
            self.EncodeAll()

    def readJson(self):
        self.encodedDataFile.seek(0)
        encodedDataJson = json.loads(self.encodedDataFile.read())
        for k,v in encodedDataJson.items():
            self.names.append(k)
            self.encodedImages.append(np.array(v))

    def writeJson(self):
        encodedDataJson = {}
        for name, encodedImage in zip(self.names, self.encodedImages):
            encodedDataJson[name] = encodedImage.tolist()
        self.encodedDataFile.truncate(0)
        json.dump(encodedDataJson, self.encodedDataFile)


    # for all the images in the given path encode and store
    def EncodeAll(self):
        images = []
        names = []
        myList = os.listdir((self.path))
        print(myList)
        for cl in myList:
            curImg = cv2.imread((f'{self.path}/{cl}'))
            images.append(curImg)
            names.append(os.path.splitext(cl)[0])
        print(names)
        encodedImages = self.Encode(images)
        self.names = names
        self.encodedImages = encodedImages
        print("Encoding Complete")
        self.writeJson()

    # Encode list of images and returns list of encoded images
    def Encode(self, images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgEncode = face_recognition.face_encodings(img)[0]
            encodeList.append(imgEncode)
        return encodeList

    # Given image with single face and name, update encoding dict and write to JSON file
    def updateEncodings(self, imagePath, name):
        image = face_recognition.load_image_file(f"{imagePath}")
        encodedImage = self.Encode([image])[0]
        self.names.append(name)
        self.encodedImages.append(encodedImage)
        self.writeJson()

    # Given the stored image(can have multiple faces so encode accordingly) path returns name
    def findName(self, imagePath):
        img = face_recognition.load_image_file(f"{imagePath}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodedFaces = face_recognition.face_encodings(img)
        foundNames = []
        for encodedFace in encodedFaces:
            matches = face_recognition.compare_faces(self.encodedImages, encodedFace)
            faceDis = face_recognition.face_distance(self.encodedImages, encodedFace)
            print(matches, faceDis)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = self.names[matchIndex]
                foundNames.append(name)
                print(name)
        return foundNames

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

