#!/usr/bin/env python3
from field import field_to_pixels
from screen import init_pygame, pygame_loop, screen_size

def main():
    init_pygame(screen_size)

    try:
        while True:
            pygame_loop()
    except KeyboardInterrupt:
        print("Closing...")

if __name__ == "__main__":
    main()