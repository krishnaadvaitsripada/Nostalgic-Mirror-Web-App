import numpy as np
import cv2
import pygame

def array_img_to_pygame(img, width, height):
    # image needs to be rotated in pygame (weird bug)
    img = np.rot90(img)
    
    # CV2 uses BGR colors and PyGame needs RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (height, width), interpolation=cv2.INTER_LINEAR)
    pygame_img = pygame.surfarray.make_surface(img)
    return pygame_img

def play_sound(file, volume=1):
    sound = pygame.mixer.Sound(file)
    sound.set_volume(volume)
    sound.play()
    return sound