import os
from imutils import paths
from learn_to_recognize import recognize_faces
from recognize_friends import find_people

# face-images: solo selfies with name identified
# friends-data: photos with any number of people (or none), who are yet to be indentified in each image
unknown_images_dir = "Server Image Processing/friends-data"
identified_faces_dir = "Server Image Processing/face-images"

# define the main directory and directory with your friends' data
main_dir = os.getcwd()
data_dir = os.path.join(main_dir, identified_faces_dir)

# list of paths of all the solo selfie pictures
datapaths = list(paths.list_images(data_dir))

# get the encodings for your friends's faces
print("Registering identities from solo images...")
identified_people = recognize_faces(image_paths=datapaths)
print(identified_people)
print("Searching for known people in the album...")
image_catalog = find_people(known_people=identified_people, test_dir=unknown_images_dir) # search for familiar faces in every image file in test_dir
print(image_catalog)

