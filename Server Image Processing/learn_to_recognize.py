import os
import cv2 
import face_recognition

# Tutorial used to make this: https://medium.com/staple-ai/album-organizer-using-face-recognition-with-deep-learning-f763e41ec65c

def recognize_faces(image_paths): 
    """Trains the program to recognize people. Accepts a list of image file paths"""
    known_people = {} # {"person_name": encoding}

    # loop over all the images and extract the face encodings
    for imagepath in image_paths:
        # get the friend's name from the image path
        image_name = imagepath.split("/")[-1]
        person_name = image_name.split(".")[0] # name of person in selfie

        # read the image and convert it to RGB scale
        image = cv2.imread(imagepath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # get all the bounding boxes of each face in this image 
        bboxes = face_recognition.face_locations(image, model='hog') # use "cnn" for better accuracy, but longer processing time

        # construct the encoding of the face within the bounding box
        encodings = face_recognition.face_encodings(image, bboxes)

        # store the face encoding and their respective name to the lists of encodings and names respectively,
        for encoding in encodings:
            known_people[person_name] = encoding
    return known_people