# Usage: python3 recognize.py -i <path_to_test_image_dir> -o <path_to_output_dir>
import os
import cv2 
import face_recognition
from deepface import DeepFace

# Tutorial used to make this: https://medium.com/staple-ai/album-organizer-using-face-recognition-with-deep-learning-f763e41ec65c

def find_people(known_people: dict, test_dir: str):
    """Using the dictionary known_people that contains people's name and their encodings, 
    the model will identify who's in each photo from the folder of image files test_dir.
    Will return an image_categories dictionary which-for each image's filename- 
    provides a set of identified peoples' names."""
    known_encodings = list(known_people.values()) # as of Python 3.7, dictionary keys are ordered
    names = list(known_people.keys())
    print(names)
    image_categories = {} # {"image file name": 
                            # {"people": (set of names of identified peoples' names, including "unknown"), #comment: ('unknown' if at least 1 face is unrecognizable)
                            #  "face_count": len(matches)}
                            # } 

    # loop over all the images in the test directory
    for image in os.listdir(test_dir):
        print("Image name:",image)
        people_in_this_image = set() # set of names of people in this image

        imagepath = os.path.join(test_dir, image)
        filename = imagepath.split(os.path.sep)[-1] # image filename

        # load the image
        testimage = cv2.imread(imagepath)
        #DeepFace.verify(img1_path=testimage, img2_path=)

        bboxes = face_recognition.face_locations(testimage, model='hog') # detect bboxes of random faces in the image
        encodings_of_faces = face_recognition.face_encodings(testimage, bboxes) # match each bbox with an encoding of any face on the image
        print("Bounding boxes:")
        print(bboxes)
        # loop over the known_encodings of each person and comparing it to the encodings in the database
        for i,someones_encoding in enumerate(known_encodings):
            # a list of True/False values for each of the known_face_encodings, stating whether the face_encoding_to_check is the same person in 
            matches = face_recognition.compare_faces(known_face_encodings=encodings_of_faces, face_encoding_to_check=someones_encoding)
            
            if True in matches: # if there's at least one match of the same face
                # extract a list of indices in encodings_of_faces where a face encoding match was found
                matchedIdxs = [i for (i, b) in enumerate(matches) if b] # there should probably only be one

                # extract the corresponding names of the matched indices and get a vote count for each matched face name 
                print(matchedIdxs)
                for i in matchedIdxs: # truthfully, this list should only be of size 1
                    if i >= len(names): # skip this person because they don't belong to a name (unknown)
                        continue
                    print(i)
                    person_name = names[i]
                    print(person_name)
                    people_in_this_image.add(person_name)
        if len(encodings_of_faces) > len(people_in_this_image): # there are more faces/matches than names we recognize, so there's at least one unknown individual
            people_in_this_image.add("unknown")
        image_data = {"face_count": len(encodings_of_faces), "people": people_in_this_image}
        image_categories[filename] = image_data # add this image to image_categories dictionary

    return image_categories # return the dictionary of ALL the images in test_dir