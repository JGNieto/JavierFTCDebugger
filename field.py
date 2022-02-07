from re import X


width = 3657.6
height = 3657.6

def field_to_pixels(point, screen_size):
    """ Transform a point of field coordinates to pixels on a screen """
    field_x, field_y = point
    screen_w, screen_h = screen_size

    # x and y are flipped
    screen_x = field_y / width * screen_w
    screen_y = field_x / height * screen_h

    # Account for pygame's weird axes.
    screen_x = - screen_x + screen_w // 2
    screen_y = - screen_y + screen_h // 2

    return screen_x, screen_y

def get_robot_size(screen_size):
    """ Compute size of the robot in pixels. """
    robot_w, robot_h = 337, 433
    screen_w, screen_h = screen_size

    screen_x = robot_w / width * screen_w
    screen_y = robot_h / height * screen_h
    return screen_x, screen_y