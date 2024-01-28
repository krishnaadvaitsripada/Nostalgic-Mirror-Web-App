from imutils import paths
import os
import cv2
import numpy as np
from deepface import DeepFace

unknown_images_dir = "Server Image Processing/friends-data"
identified_faces_dir = "Server Image Processing/face-images"
main_dir = os.getcwd()
identities_dir = os.path.join(main_dir, identified_faces_dir)
unknown_dir = os.path.join(main_dir, unknown_images_dir)

# list of paths of all the solo selfie pictures
identified_faces_path_list = list(paths.list_images(identities_dir))
unknown_faces_path_list = list(paths.list_images(unknown_dir))

def detect_faces(frame: np.ndarray, selfie_db: str):
    """frame: image containing one face
    selfie_db: path to folder containing images to search"""
    faces = DeepFace.find(
        frame, 
        db_path="face-images", 
        enforce_detection=False,
        silent=True,
        model_name="Dlib",
    )
    for face in faces: # loop through every recognized face in the image
        if not face.empty: # if this is a face
            name = os.path.basename(str(face["identity"]).split("/")[-1]).split(".")[0] # name of the person
            distance = float(str(face["distance"]).split("\n")[0].split('0 ')[-1].strip())  # accuracy 0 to 1 but 0 is best and 1 is worst
            accuracy = round((1-distance)*100,1)

for selfiefile_path in unknown_faces_path_list:
    selfieImg = cv2.imread(selfiefile_path)
    #cv2.imshow("Selfie Img", selfieImg)
    for albumImg_path in identified_faces_path_list:
        albumImg = cv2.imread(albumImg_path)
        #cv2.imshow("Album Img", albumImg)

        print(f"\nSelfie img: {selfiefile_path.split('/')[-1]}, Album img: {albumImg_path.split('/')[-1]}")
        result = DeepFace.verify(img1_path=selfieImg, img2_path=albumImg, enforce_detection=False, model_name="Dlib")
        print(result)

cv2.destroyAllWindows()