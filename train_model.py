# USAGE
# python train_model.py --embeddings output/embeddings.pickle \
#	--recognizer output/recognizer.pickle --le output/le.pickle

# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle
import pyodbc
def trainModel(dirname, data):

    # load the face embeddings
    print("[INFO] loading face embeddings...")

    # encode the labels
    print("[INFO] encoding labels...")
    le = LabelEncoder()
    labels = le.fit_transform(data["names"])
    # train the model used to accept the 128-d embeddings of the face and
    # then produce the actual face recognition
    print("[INFO] training model...")
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(data["embeddings"], labels)

    """
    SQL SERVER
    """
    server = '192.169.82.62'
    database = 'Alike'
    username = 'farah'
    password = 'S2&7jgo4'
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    cursor = conn.cursor()
    cursor.execute("""INSERT INTO UsersDataSet(UserId, Embeddings, LabelEncoder, Recognizer) VALUES(?,?,?,?)""",dirname, pickle.dumps(data['embeddings']), pickle.dumps(le), pickle.dumps(recognizer))
    cursor.commit()
    return 0