import cv2
from deepface import DeepFace
import threading
import os

# INSTRUCTIONS

# You need to install Dlib for this to work or change the model in MODEL_NAME
# Press q for a short while to stop (while focused on window), or Control-C (while focused on terminal)

# EDITABLE VARIABLES
RECOGNIZE_EVERY = 30 # find recognizable faces every n frames. this is to minimize lag 
MODEL_NAME = "Dlib" # the ML model we're using for face recognition. see https://github.com/serengil/deepface

# Create a VideoCapture object to capture frames from the webcam
cap = cv2.VideoCapture(0)
v_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
v_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
default_fps = cap.get(cv2.CAP_PROP_FPS)
print("Webcam video capture started")
print(f"Size: {v_width}*{v_height}\n")
print("FPS:", default_fps)

def detect_faces(frame):
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
            print(f"Name: {name}, Accuracy: {accuracy}%", flush=True)

def main():
    frame_count = 0 # number of frames processed

    while True:
        # Read a frame from the webcam
        success, frame = cap.read()
        if success: # if the webcam returns an image frame
            # Perform face recognition on the frame
            if frame_count % RECOGNIZE_EVERY == 0 and frame_count != 0: # only look for recognizable faces once every n frames has passed...
                detection_thread = threading.Thread(target=detect_faces, args=((frame,))) # keep the comma after frame to keep this 
                detection_thread.start()
            # Display the result
            cv2.imshow("Face Recognition", frame)

            frame_count+=1
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the VideoCapture object and close the windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
