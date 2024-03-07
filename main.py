import cv2
import numpy as np
import face_recognition
import os
from flask import Flask,jsonify,request
import time
from typing import List

import pickle

app = Flask(__name__)

chemin_fichier = "donnees_encodee.pkl"
path = 'persons'
images = []
classNames = []
foundNames = []
foundNamesClean=[]
personsList = os.listdir(path)

def encoding():
    global encodeListKnown
    

    #had la variable khassni nssiftha lfichier json (encodeListKnow)
    # ndir wahd lfichier nstocker fih l'encodages o ndir wahd lconditions bach iqra men lfichier directement bla maydouz idir encodages ila deja kayn lfichier si nn ila makanch lfichier idir l'encodage o istocker
    #encodeListKnown = findEncodeings(images)
    #ma_variable_pkl = pickle.dump(encodeListKnown)
    if not os.path.exists(chemin_fichier):

        for cl in personsList:
            curPersonn = cv2.imread(f'{path}/{cl}')
            images.append(curPersonn)
            classNames.append(os.path.splitext(cl)[0])
        print(classNames)

        def findEncodeings(image):
            global encodeList
            global encode
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList
        encodeListKnown = findEncodeings(images)



        with open(chemin_fichier, "wb") as f:
            pickle.dump(encodeListKnown, f)
            print("fichier creer avec succes")
    
    with open(chemin_fichier, "rb") as f:
            for cl in personsList:
                curPersonn = cv2.imread(f'{path}/{cl}')
                images.append(curPersonn)
                classNames.append(os.path.splitext(cl)[0])
            print(classNames)
            
            donnees_charge = pickle.load(f)
            encodeListKnown= donnees_charge
            print(donnees_charge)
            print("donnees charge avec succees : ")

    print(encodeListKnown)
    print(len(encodeListKnown))
    print('Encoding Complete.')

@app.route('/')
def get_names():
    return foundNamesClean

@app.route('/encode')
def reEncode():
    classNames.clear()
    encodeListKnown.clear()
    #encodeList.clear()
    images.clear()
    print(len(encodeListKnown))
    if os.path.exists(chemin_fichier):
        os.remove(chemin_fichier)
        #with open(chemin_fichier, "rb") as f:
            
         #   donnees_charge = pickle.load(f)
         #   encodeListKnown= donnees_charge
          #  print("donnees charge avec succees : "+ donnees_charge)
        print("file removed")
            
        encoding()
        print(len(encodeList))

    
    return "encoding success"

@app.route('/scan')
def scaan():
        global foundNames
        global foundNamesClean
        
        
        foundNames.clear()
        foundNamesClean.clear()

        # for cl in personsList:
        #     curPersonn = cv2.imread(f'{path}/{cl}')
        #     images.append(curPersonn)
        #     classNames.append(os.path.splitext(cl)[0])
        # print(classNames)

        # def findEncodeings(image):
        #     encodeList = []
        #     for img in images:
        #         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #         encode = face_recognition.face_encodings(img)[0]
        #         encodeList.append(encode)
        #     return encodeList

        # encodeListKnown = findEncodeings(images)
        # print(encodeListKnown)
        # print('Encoding Complete.')

        cap = cv2.VideoCapture(0)
        timeout = time.time() + 10
        while time.time() < timeout :
            print(time.time())

            _, img = cap.read()

            imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faceCurentFrame = face_recognition.face_locations(imgS)
            encodeCurentFrame = face_recognition.face_encodings(imgS, faceCurentFrame)

            for encodeface, faceLoc in zip(encodeCurentFrame, faceCurentFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeface)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeface)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    print(name)
                    if name not in foundNames:
                        foundNames.append(name)
                    # y1, x2, y2, x1 = faceLoc
                    # y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    # cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)
                    # cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,0,255), cv2.FILLED)
                    # cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

            # print('mon test ' + name)
            
            #cv2.imshow('Face Recogntion', img)
            if cv2.waitKey(1) and time.time() > timeout:
                cap.release()
                break
        print("foundNames: ", foundNames)
        foundNamesClean = list(set(foundNames))
        

        return foundNamesClean

        
    
    
if __name__ == "__main__":
    #global foundNames
    # for cl in personsList:
    #     curPersonn = cv2.imread(f'{path}/{cl}')
    #     images.append(curPersonn)
    #     classNames.append(os.path.splitext(cl)[0])
    # print(classNames)

    # def findEncodeings(image):
    #     encodeList = []
    #     for img in images:
    #         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #         encode = face_recognition.face_encodings(img)[0]
    #         encodeList.append(encode)
    #     return encodeList

    # encodeListKnown = findEncodeings(images)
    # print(encodeListKnown)
    # print('Encoding Complete.')
    encoding()
    app.run()
    