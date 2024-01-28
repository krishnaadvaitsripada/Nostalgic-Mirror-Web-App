import pygame
import cv2
from deepface import DeepFace
import threading
import os
import pygame_functions
import time

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

# Initialize Pygame
pygame.init()

# Get screen info
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

print(f"Screen size: {screen_width}x{screen_height}")

# Pygame
pygame.font.init()

SMALL_LABEL_FONT = pygame.font.SysFont('assets/Roboto-Regular.ttf', 30)
LABEL_FONT = pygame.font.Font('assets/Roboto-Medium.ttf', 40) 
TITLE_FONT = pygame.font.Font('assets/Roboto-Medium.ttf', 60) # same font type as LABEL but bigger

# colours
LIGHT_GRAY = (160, 166, 176)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# create display, set window size, start clock
pygame.mixer.init()
pygame.display.set_caption("Nostalgic Mirror")
main_screen = pygame.display.set_mode([screen_width, screen_height], pygame.SCALED) # pygame.SCALED makes the display fill the screen
pygame.display.toggle_fullscreen()
clock = pygame.time.Clock()

main_screen.fill(RED)

# Create a VideoCapture object to capture frames from the webcam
cap = cv2.VideoCapture(0)
v_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
v_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
default_fps = cap.get(cv2.CAP_PROP_FPS)

print("Webcam video capture started")
print(f"Size: {v_width}*{v_height}\n")
print("FPS:", default_fps)

pygame_fps = default_fps
running = True # whether this program is running
start = time.time() # when this program started

def display_menu(fps=0):
    """Draws stuff on the mirror screen, text info like FPS and other image icons"""
    if fps > 0: # if fps was given
        fps_text = SMALL_LABEL_FONT.render(f'FPS: {fps}', False, WHITE)
        main_screen.blit(fps_text, (20, screen_height - fps_text.get_height() - 20))

    some_text = SMALL_LABEL_FONT.render('Welcome', False, WHITE)
    main_screen.blit(
        some_text, 
            (screen_width - some_text.get_width() - 20, 
            screen_height - some_text.get_height() - 20))

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
    global running

    frame_count = 0 # number of frames processed
    fps = 0 # calculated fps

    while cap.isOpened() and running:
        clock.tick(pygame_fps) # tick the clock...
        # Read a frame from the webcam
        
        success, frame = cap.read()

        # Perform face recognition on the frame
        if frame_count % RECOGNIZE_EVERY == 0 and frame_count != 0: # only look for recognizable faces once every n frames has passed...
            detection_thread = threading.Thread(target=detect_faces, args=((frame,))) # keep the comma after frame to keep this 
            detection_thread.start()
        
        # Display the result
        background_pygame_img = pygame_functions.array_img_to_pygame(frame, v_width, v_height)
        main_screen.blit(background_pygame_img, (0,0)) # insert the background image, starting from the top left so it fills the whole screen

        # update display, render menu
        end = time.time()

        if SHOW_FPS:
            fps = round(clock.get_fps(), 1)
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
