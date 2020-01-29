# USAGE
# python recognize.py --detector face_detection_model \
#	--embedding-model openface_nn4.small2.v1.t7 \
#	--recognizer output/recognizer.pickle \
#	--le output/le.pickle --image images/adrian.jpg

# import the necessary packages
import numpy as np
import imutils
import pickle
import cv2
import time
import pyodbc

"""
SQL SERVER
"""
server = '192.169.82.62'
database = 'Alike'
username = 'farah'
password = 'S2&7jgo4'
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = conn.cursor()

listUsersIds = []
UsersIds = cursor.execute("SELECT UserID from UsersDataSet")
for row in UsersIds:
    listUsersIds.append(row[0])

dirname = input("Name the Profile Picture: ")
start = time.time()
vecdat = cursor.execute("SELECT ProfilePicData from ProfilePicDataSet where UserId = '"+dirname+"'").fetchval()
vec = pickle.loads(vecdat)
start = time.time()
for j in range(len(listUsersIds)):
    query = cursor.execute("SELECT * FROM UsersDataSet WHERE UserId = '"+listUsersIds[j]+"'").fetchall()
    lble = query[0][2]
    reco = query[0][3]
    # load the actual face recognition model along with the label encoder
    query2 = cursor.execute
    recognizer = pickle.loads(reco)
    le = pickle.loads(lble)
    preds = recognizer.predict_proba(vec)[0]
    j = np.argmax(preds)
    proba = preds[j]
    name = le.classes_[j]
    if name != "unknown" and name != dirname:
        # similarList.append(name)
        cursor.execute("""INSERT INTO SimilarPerson(UserId, SimilarPerson) VALUES(?,?)""", dirname, name)
        cursor.commit()
    # print(proba)
end = time.time()
print(end - start)

