import cv2
import numpy as np
import face_recognition
import os
from flask import Flask, jsonify
from threading import Thread, Lock
import time
import pickle

app = Flask(__name__)

lock = Lock()  # Verrou pour gérer l'accès aux ressources partagées

chemin_fichier = "donnees_encodee.pkl"
path = 'persons'
images = []
classNames = []
foundNames = []
foundNamesClean = []
personsList = os.listdir(path)


def encoding():
    global encodeListKnown

    if not os.path.exists(chemin_fichier):
        for cl in personsList:
            curPersonn = cv2.imread(f'{path}/{cl}')
            images.append(curPersonn)
            classNames.append(os.path.splitext(cl)[0])

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
            print("fichier crée avec succès")

    with open(chemin_fichier, "rb") as f:
        for cl in personsList:
            curPersonn = cv2.imread(f'{path}/{cl}')
            images.append(curPersonn)
            classNames.append(os.path.splitext(cl)[0])
        donnees_charge = pickle.load(f)
        encodeListKnown = donnees_charge
        print("donnees chargees avec succès : ")

    print(encodeListKnown)
    print(len(encodeListKnown))
    print('Encoding Complete.')


@app.route('/')
def get_names():
    return jsonify(foundNamesClean)


@app.route('/encode')
def reEncode():
    with lock:
        classNames.clear()
        encodeListKnown.clear()
        images.clear()
        print(len(encodeListKnown))
        if os.path.exists(chemin_fichier):
            os.remove(chemin_fichier)
            print("file removed")

        encoding()
        print(len(encodeList))
    return "encoding success"


def scan_task():
    global foundNames
    global foundNamesClean

    foundNames.clear()
    foundNamesClean.clear()

    cap = cv2.VideoCapture(0)
    timeout = time.time() + 10
    while time.time() < timeout:
        _, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
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

    cap.release()
    foundNamesClean = list(set(foundNames))


@app.route('/scan')
def scan():
    thread = Thread(target=scan_task)
    thread.start()
    return "Scanning in progress..."


if __name__ == "__main__":
    encoding()
    app.run()
