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

dirname = input("Name the Profile Picture: ")
image_prototype1 = 'profile_' + dirname + "/current.jpg"

probability = 0.7

print("[INFO] loading face detector...")
protoPath = "face_detection_model/deploy.prototxt"
modelPath = "face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch("openface_nn4.small2.v1.t7")
image = cv2.imread(str(image_prototype1))
image = imutils.resize(image, width=600)
(h, w) = image.shape[:2]
# construct a blob from the image
imageBlob = cv2.dnn.blobFromImage(
    cv2.resize(image, (300, 300)), 1.0, (300, 300),
    (104.0, 177.0, 123.0), swapRB=False, crop=False)
# apply OpenCV's deep learning-based face detector to localize
# faces in the input image
detector.setInput(imageBlob)
detections = detector.forward()
# loop over the detections
# extract the confidence (i.e., probability) associated with the
# prediction
confidence = detections[0, 0, 1, 2]
# filter out weak detections
# compute the (x, y)-coordinates of the bounding box for the
# face
box = detections[0, 0, 1, 3:7] * np.array([w, h, w, h])
(startX, startY, endX, endY) = box.astype("int")
face = image[startY:endY, startX:endX]
(fH, fW) = face.shape[:2]
for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        # filter out weak detections
        if confidence > probability:
            # compute the (x, y)-coordinates of the bounding box for the
            # face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # extract the face ROI
            face = image[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
                continue

            # construct a blob for the face ROI, then pass the blob
            # through our face embedding model to obtain the 128-d
            # quantification of the face
            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                                             (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()
            cursor.execute("""INSERT INTO ProfilePicDataSet(UserId, ProfilePicData) VALUES(?,?)""", dirname, pickle.dumps(vec))
            cursor.commit()