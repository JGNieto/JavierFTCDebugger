# Hide pygame message.
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from field import get_robot_size, field_to_pixels

robot_position = (0, 0, 0)
needs_update = True # Initialize to True to guarantee first paint.

screen_width = 600
screen_height = 600

screen_size = screen_width, screen_height

def init_pygame(screen_size):
    """ Initializes pygame and creates a window. """
    global screen, field_img, robot_img

    # Open screen and set caption.
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Javier's Debugging #11468") # 11468 is the FTC team number.

    # Get image for field background.
    field_img_raw = pygame.image.load("field-cropped.png")

    # Scale the image to the size of the screen.
    # We can afford smoothscale since this is a one-off computation.
    field_img = pygame.transform.smoothscale(field_img_raw, screen_size)

    # Get robot sprite.
    robot_img_raw = pygame.image.load("robot.png")

    # Grab robot size.
    robot_size = get_robot_size(screen_size)

    # Resize robot sprite to its correct dimensions.
    # Again, we can afford smoothscale.
    robot_img = pygame.transform.smoothscale(robot_img_raw, robot_size)

def pygame_loop():
    """ To be called every iteration. Updates the screen. """
    global needs_update

    # Go through events to check whether user has quit.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # To indicate quitting, we raise a KeyboardInterrupt.
            raise KeyboardInterrupt
    
    """
    To avoid wasting resources painting the same image, we only
    update if there has been a change in the robot's position.
    """
    if not needs_update: return
    needs_update = False

    # Paint background first.
    screen.blit(field_img, (0,0))

    # Then, paint robot.
    screen.blit(robot_img, (screen_height // 2, screen_height // 2))

    pygame.display.flip()

def set_robot_position(new_position):
    """ Changes the robot's position. Provide a tuple with values (x, y, heading). """
    global robot_position, needs_update
    robot_position = new_position
    needs_update = True