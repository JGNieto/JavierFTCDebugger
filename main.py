#!/usr/bin/env python3
from screen import init_pygame, pygame_loop
from server import open_socket, close_socket, wait_for_connection

def main():
    # Open socket to clients
    open_socket()

    # Open a window and initialize.
    init_pygame()

    try:
        """
        Run continuously until a KeyboardInterrupt is either raised by pygame_loop()
        or by the user actually pressing Ctrl+C.
        """
        while True:
            # See whether there is a socket connection.
            wait_for_connection()

            # Execute the update to the pygame screen.
            pygame_loop()
    except KeyboardInterrupt:
        print("Closing...")
    except Exception as e:
        # Unexpected.
        print(e)
    finally:
        # It is VERY important that the socket is closed.
        close_socket()

if __name__ == "__main__":
    main()