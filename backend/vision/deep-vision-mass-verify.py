from imutils import paths
import os
import cv2
import numpy as np
from deepface import DeepFace

identified_faces_dir = "backend/vision/face-images"
unknown_images_dir = "backend/vision/album-data"
main_dir = os.getcwd()

# list of paths of all the solo selfie pictures

selfies_list = list(paths.list_images(identified_faces_dir)) # list of paths to each selfie
photos_list = list(paths.list_images(unknown_images_dir)) # list of paths to each photo 

def detect_faces(frame: np.ndarray, selfie_db: str):
    """Detect all the faces from selfie_db in the given photo frame. Returns a face_dictionary "selfie image filename": accuracy_float_to this frame
    frame: image containing a photo
    selfie_db: path to folder containing selfie images"""
    faces = DeepFace.find(
        frame,
        db_path=selfie_db, 
        enforce_detection=False,
        distance_metric="euclidean",
        silent=True,
        model_name="Facenet512",
        detector_backend="dlib"
    )
    face_dictionary = {}
    for face in faces: # loop through every recognized face in the image
        if not face.empty: # if this is a face
            name = os.path.basename(str(face["identity"]).split("/")[-1]).split(".")[0] # name of the person
            distance = float(str(face["distance"]).split("\n")[0].split('0 ')[-1].strip())  # accuracy 0 to 1 but 0 is best and 1 is worst
            accuracy = round((1-distance)*100,1)
            face_dictionary[name] = accuracy

    return face_dictionary

for photo_path in photos_list:
    photo_filename = photo_path.split("/")[-1]
    photoImg = cv2.imread(photo_path)
    faces = detect_faces(photoImg, identified_faces_dir)
    print("Photo: {}, People: {}".format(photo_filename, str(list(faces.keys()))))