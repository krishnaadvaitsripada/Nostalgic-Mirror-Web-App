import random
import pygame
import cv2
from deepface import DeepFace
import threading
import os
import pygame_functions
import time
from imutils import paths
import numpy as np

# TODO:
"""
- make the image display not stretch

- for now, just one photo appears of that person or group of people that move in front 
  of the camera. a cool scale-out affect as a reccoended photo appears

- extra: search up how to make sparkles or cool effects pop out in pygame
  
- playsound() when new person recognized. 5 s tolerance so that someone cant come 
  in front of the mirror, leave, then come again really fast to spam the noise and effects

- GET request to fetch a list of photos of name of person from Flask server.
- only request one photo at a time to display; try not to download them but mkae
  pygame display an image from a URL

"""

# INSTRUCTIONS

# You need to install Dlib for this to work or change the model in MODEL_NAME
# Press q for a short while to stop (while focused on window), or Control-C (while focused on terminal)

# EDITABLE VARIABLES
RECOGNIZE_EVERY = 30 # find recognizable faces every n frames. this is to minimize lag 
MODEL_NAME = "Dlib" # the ML model we're using for face recognition. see https://github.com/serengil/deepface
SHOW_FPS = True
IMAGE_DISPLAY_TIME = 4 # how long the image stays between zooming out, and disappearing (seconds)
ANIMATION_FREQUENCY_L = 2 # a new album image will appear at random intervals between _L and _H seconds
ANIMATION_FREQUENCY_H = 4
ZOOM_OUT_DURATION = 4 # the length of the zooming out animation in seconds.
PORTRAIT_BORDER_SIZE = 20 # border size around displayed image in pixels
MAX_MIRROR_USERS = 1 # max number of users that can influence the mirror at once
# MAX_IMAGES_DISPLAYED = 1 # max number of album images that can be shown on the screen at one time 


# Initialize Pygame
pygame.init()

# Get screen info
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

print(f"Screen size: {screen_width}x{screen_height}")

PARENT_DIR = "/Users/baget/Desktop/Developing/mirror/"

# Pygame
pygame.font.init()
SMALL_LABEL_FONT = pygame.font.SysFont(PARENT_DIR+'Mirror Display/assets/Roboto-Regular.ttf', 30)
LABEL_FONT = pygame.font.Font(PARENT_DIR+'Mirror Display/assets/Roboto-Medium.ttf', 40) 
TITLE_FONT = pygame.font.Font(PARENT_DIR+'Mirror Display/assets/Roboto-Medium.ttf', 60) # same font type as LABEL but bigger

# colours
LIGHT_GRAY = (160, 166, 176)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0,80,240)

# filepath constants
SELFIES_FOLDER = PARENT_DIR+"Mirror Display/face-images" # path to the directory of solo selfie images with name of person

# create display, set window size, start clock
pygame.mixer.init()
pygame.display.set_caption("Nostalgic Mirror")
main_screen = pygame.display.set_mode([screen_width, screen_height]) # pygame.SCALED makes the display fill the screen
pygame.display.toggle_fullscreen()
clock = pygame.time.Clock()

main_screen.fill(BLUE)

# Create a VideoCapture object to capture frames from the webcam
cap = cv2.VideoCapture(0)
v_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
v_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
default_fps = cap.get(cv2.CAP_PROP_FPS)

print("Webcam video capture started")
print(f"Size: {v_width}*{v_height}\n")
print("FPS:", default_fps)
pygame_fps = default_fps
running = True # whether this program is running
current_users = [] # names of the users standing in front of the camera right now
landscape_img = cv2.imread("landscape.jpg")

def find_person_in_db(frame: np.ndarray, album_db: str):
    """Returns a set of assigned names of people from the image frame, using a path
     to a folder of other images.
    frame: image containing one face
    album_db: path to folder containing images to search"""
    
    # TODO: if someone is there but is not recognized, add "unknown" to the list
    
    faces = DeepFace.find(
        frame, 
        db_path=album_db, 
        enforce_detection=False,
        silent=True,
        model_name="Dlib",
        detector_backend="dlib",
        distance_metric="euclidean"
    )

    people_in_mirror = set() # names of people detected in front of the camera
    for face in faces: # loop through every recognized face in the image
        if not face.empty: # if this is a face
            name = os.path.basename(str(face["identity"]).split("/")[-1]).split(".")[0] # name of the person
            # distance = float(str(face["distance"]).split("\n")[0].split('0 ')[-1].strip())  # accuracy 0 to 1 but 0 is best and 1 is worst
            # accuracy = round((1-distance)*100,1)
            # print(f"Name: {name}, Accuracy: {accuracy}%", flush=True)
            people_in_mirror.add(name)
    return people_in_mirror
# --------------------------------------------------
# initialize uploaded photos from the test album
print("Reading offline test photos..")
test_album_paths = list(paths.list_images(PARENT_DIR+"Mirror Display/test-album")) # list of paths to each test photo
selfies_paths = list(paths.list_images(SELFIES_FOLDER)) # list of paths to each test photo

test_album_images = {} # dictionary of numpy array test images with a set of names of people in the image {"filename": ('name1','name2')}

# loop through each selfie face
for photo_path in test_album_paths:
    photo_filename = photo_path.split("/")[-1]
    photo_img = cv2.imread(photo_path)
    people_names = find_person_in_db(photo_img, SELFIES_FOLDER)
    test_album_images[photo_filename] = people_names
# --------------------------------------------------
    
def find_person_in_db_async(frame, album_db):    
    """Used for multithreading purposes to detect faces asynchronously.
    Automatically updates the global current users for other function to
    access during execution."""
    global current_users
    current_users = find_person_in_db(frame, album_db) # reassign the global current_users array

def get_image(users: [str]):
    """Fetch an image stored in the webserver to display based on
    the given user names. Atm, if there are more than one users, then
    it will randomly choose any photo form anyone."""
    possible_images = [] # list of filenames of images that could be possibly elected to be displayed
    for i,name in enumerate(users):
        if i+1 <= MAX_MIRROR_USERS: # make sure we keep less than or equal to the number of max users for the mirror
            for test_album_img_filename in test_album_images:
                if name in test_album_images[test_album_img_filename]: # if this image includes the user's name
                    possible_images.append(test_album_img_filename)
    if len(possible_images) > 0:
        random_img = possible_images[random.randint(0,len(possible_images)-1)] # select a random image. this is temporary until we're hooked up to the flask side.
        return cv2.imread(random_img)
    else:
        return landscape_img

def display_menu(fps=0):
    """Draws stuff on the mirror screen, text info like FPS and other image icons"""
    if fps > 0: # if fps was given
        fps_text = SMALL_LABEL_FONT.render(f'FPS: {fps}', False, WHITE)
        main_screen.blit(fps_text, (20, screen_height - fps_text.get_height() - 20))

    some_text = LABEL_FONT.render('Welcome, '+', '.join(current_users) + "!", False, WHITE)
    main_screen.blit(
        some_text, 
            (screen_width - some_text.get_width() - 20, 
            screen_height - some_text.get_height() - 20))

def main():
    global running
    global image_to_display_py

    frame_count = 0 # number of frames passed since start of program (frames)
    # next_photo_appearance = 0 # when the next photo of the user standing in front of the mirror should appear (frames passed) 
    fps = 0 # initialize fps (will be calculated later below)
    animation_start = 0 # when the photo animation will start (time.time()). if there is no current animation, then this value (along with _dur) is 0
    
    # TODO:
    # make photo zoom out from random points on the screen. random 1-2 seconds between each reappearance of a photo.
    # change frame background. use an image somehow without distorting it
    
    # GET request to flask web will ask for a photo in that person's album.
    # later, try to match those two people

    while cap.isOpened() and running:
        clock.tick(pygame_fps) # tick the clock...
        # Read a frame from the webcam
        
        success, frame = cap.read()
        if not success: # if we did not receive a valid frame
            continue
        # Perform face recognition on the frame
        if frame_count % RECOGNIZE_EVERY == 0 and frame_count != 0: # only look for recognizable faces once every n frames has passed...
            detection_thread = threading.Thread(target=find_person_in_db_async, args=((frame,SELFIES_FOLDER,))) # keep the comma after frame to keep this 
            detection_thread.start()
        
        # Display the result
        try:
            background_pygame_img = pygame_functions.array_img_to_pygame(frame, v_width, v_height)
            main_screen.blit(background_pygame_img, (0,0)) # insert the background image, starting from the top left so it fills the whole screen
        except:
            print("Cv2 error! cant draw background")
            print(type(frame))
            print(frame)

        if animation_start > 0 and time.time() - animation_start > ZOOM_OUT_DURATION: # once the animation has ended
            animation_start = 0 # reset it
        elif animation_start > 0:
            pygame.draw.rect(main_screen,WHITE,(200,150,100,50))
            i_width, i_height = image_to_display_py.get_size()
            left = screen_width / 2 - i_width
            top = screen_height / 2 - i_height
            portrait = pygame.Surface((i_width+PORTRAIT_BORDER_SIZE, i_height+PORTRAIT_BORDER_SIZE))
            main_screen.blit(portrait, (left-PORTRAIT_BORDER_SIZE, top-PORTRAIT_BORDER_SIZE))
            main_screen.blit(image_to_display_py, (left, top))

        if SHOW_FPS: # update FPS
            fps = round(clock.get_fps(), 1)
    
        if len(current_users) > 0 and current_users != ["unknown"]: # if there are recognized users in front of the mirror
            if animation_start == 0: # if no current animation playing or is planned
                wait_duration = random.randint(ANIMATION_FREQUENCY_L, ANIMATION_FREQUENCY_H)
                image_to_display_py = pygame_functions.array_img_to_pygame(get_image(current_users), v_width, v_height)
                animation_start = time.time() + wait_duration # this is when the animation should start
        display_menu( # draw the display menu on the main screen
            fps=fps,
        )
        pygame.display.update() # update the display. must be called continuously every frame.

        # keyboard press events
        keys_pressed = pygame.key.get_pressed()

        # escape key is used to close game
        if keys_pressed[pygame.K_ESCAPE]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        # pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # quit pygame window, stop game loop
                running = False

            frame_count+=1
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                break
    # Release the VideoCapture object and close the windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
