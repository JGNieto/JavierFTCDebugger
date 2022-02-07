from re import X


width = 3657.6
height = 3657.6

def field_to_pixels(point, screen_size):
    """ Transform a point of field coordinates to pixels on a screen """
    field_x, field_y = point
    screen_w, screen_h = screen_size

    screen_x = field_x / width * screen_w
    screen_y = field_y / height * screen_h

    return screen_x, screen_y

def get_robot_size(screen_size):
    """ Compute size of the robot in pixels. """
    robot_size = (337, 433)
    return field_to_pixels(robot_size, screen_size)