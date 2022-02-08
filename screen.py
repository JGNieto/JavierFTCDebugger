# Hide pygame message.
from email import message
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from field import get_robot_size, field_to_pixels

robot_position = None
message = None
needs_update = True

screen_width = 600
screen_height = 600

screen_size = screen_width, screen_height

def init_pygame(screen_size = screen_size):
    """ Initializes pygame and creates a window. """
    global screen, field_img, robot_img, font

    # Open screen and set caption.
    screen = pygame.display.set_mode(screen_size)
    icon = pygame.image.load("assets/icon.png");
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Javier's Debugging #11468") # 11468 is the FTC team number.

    # Init font module
    pygame.font.init()
    font = pygame.font.Font("assets/UbuntuMono-Regular.ttf", 30)

    # Get image for field background.
    field_img_raw = pygame.image.load("assets/field-cropped.png")

    # Scale the image to the size of the screen.
    # We can afford smoothscale since this is a one-off computation.
    field_img = pygame.transform.smoothscale(field_img_raw, screen_size)

    # Get robot sprite.
    robot_img_raw = pygame.image.load("assets/robot.png")

    # Grab robot size.
    robot_size = get_robot_size(screen_size)

    # Resize robot sprite to its correct dimensions.
    # Again, we can afford smoothscale.
    robot_img = pygame.transform.smoothscale(robot_img_raw, robot_size)

def pygame_loop():
    """ To be called every iteration. Updates the screen if needed. """
    global needs_update, message, robot_position

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

    if message != None:
        # Show error message.
        screen.fill((255, 255, 255))
        font_surface = font.render(message, True, (0, 0, 0))
        font_coordinates = (screen_width - font_surface.get_width()) // 2, (screen_height - font_surface.get_height()) // 2
        screen.blit(font_surface, font_coordinates)
    elif robot_position == None:
        # Show "No connection message" when waiting for connection.
        screen.fill((255, 255, 255))
        font_surface = font.render("Waiting for connection...", True, (0, 0, 0))
        font_coordinates = (screen_width - font_surface.get_width()) // 2, (screen_height - font_surface.get_height()) // 2
        screen.blit(font_surface, font_coordinates)
    else:
        # Paint background first.
        screen.blit(field_img, (0,0))

        """ Robot painting. """
        # Destructure robot position
        robot_x, robot_y, robot_heading = robot_position

        # Rotate robot to correct heading.
        robot_rotated = pygame.transform.rotate(robot_img, robot_heading)

        # Compute robot's position on the screen.
        robot_screen_x, robot_screen_y = field_to_pixels((robot_x, robot_y), screen_size)

        # Retrieve width and height of the robot sprite after rotation
        robot_w, robot_h = robot_rotated.get_size()

        # Compute the coordinates we need to give pycharm.
        robot_pycharm_x = robot_screen_x - robot_w // 2
        robot_pycharm_y = robot_screen_y - robot_h // 2

        screen.blit(robot_rotated, (robot_pycharm_x, robot_pycharm_y))

    pygame.display.flip()
    needs_update = False

def set_robot_position(new_position):
    """ Changes the robot's position. Provide a tuple with values (x, y, heading). """
    global robot_position, needs_update
    needs_update = True
    robot_position = new_position

def set_message(new_message):
    """ Paints a message to the screen. It stays there until set_message(None) is called. """
    global message, needs_update
    needs_update = True
    message = new_message