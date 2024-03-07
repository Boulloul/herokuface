
# FaceRecognition_absence

Le projet vise à développer un système de suivi des absences des étudiants basé sur la technologie de reconnaissance faciale. Ce système permettra d'automatiser le processus de suivi de la présence des étudiants dans les salles de classe.


## Technologie utilisé

**Environnement:** ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
**langage:** ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
**Server:** ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
**Librairie:** 
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) ![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)face-recognition 1.3.0


## Documentation

**Import des bibliothèques**

Le code commence par importer les bibliothèques nécessaires telles que cv2, numpy, face_recognition, os, Flask, time et pickle.

**Lancement du serveur Flask**

Une instance de l'application Flask est créée pour gérer les routes et la technologie de reconnaissance faciale.

**Les routes**

***Route '/'*** : Cette route renvoie les noms des étudiants dont les visages ont été détectés.

***Route '/encode'*** : Cette route ré-encode les visages en cas de besoin.

***Route '/scan'*** : Cette route effectue la détection des visages en temps réel à partir de la webcam et renvoie les noms des étudiants détectés.

**Les fonctions utilisé**

***Fonction encoding***

Cette fonction réalise l'encodage des visages des étudiants à partir des images stockées dans un répertoire spécifié (persons). Les encodages sont enregistrés dans un fichier .pkl pour éviter de recalculer les encodages à chaque exécution du programme.

***Fonction scaan***

Cette fonction capture des images de la webcam, détecte les visages et compare les encodages des visages détectés avec ceux stockés dans le fichier .pkl. Si une correspondance est trouvée, le nom de l'étudiant est ajouté à la liste foundNames.

***Fonction reencode***

Cette fonction supprime le fichier qui contient l'encodage des visages des étudiants et re réalise l'encodage à partir des images stockées dans le répertoire persons. Les encodages sont réenregistrés dans le meme fichier .pkl .

**Exécution de l'Application**

La fonction encoding() est appelée pour encoder les visages au démarrage de l'application.
Ensuite, l'application Flask est exécutée avec app.run().

Le fichier .pkl est utilisé pour stocker les encodages des visages afin de réduire le temps de traitement lors des exécutions ultérieures.

La détection des visages et la comparaison des encodages sont effectuées en temps réel à l'aide de la webcam.

Le résultat de la détection est renvoyé sous forme de liste de noms d'étudiants détectés.
## Contact
El mahdi boulloul - boulloul.123@gmail.com