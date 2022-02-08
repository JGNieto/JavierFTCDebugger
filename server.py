import logging
import socket
from screen import set_robot_position, set_message

# Local IP Address within the robot's network. 
# Make sure you manually set your computer to have this IP Address.
HOST = "192.168.43.97" # CHANGE THIS
PORT = 11468 # Port used for TCP. 11468 is the OHM Raiders' FTC team number.

# The version of our little debugging protocol that we support.
# For now, only one version exists.
VERSION = 1

connection_counter = 0 # Keep track of how many connections have occurred.

def open_socket():
    """ This function opens the socket for the robot to connect to. """
    global my_socket, HOST, PORT
    try: # Attempt to open socket.
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.bind((HOST, PORT))
        my_socket.listen()

        # Disable blocking for my_socket.accept()
        my_socket.setblocking(False)

        print("Server open")
    except OSError:
        print("Could not open server. Are you connected to the robot's wifi?")
        set_message("Could not open server. Check WiFi?")

def wait_for_connection():
    """ This function sees if the client has sent new position information. """
    global connection_counter

    # Attempt to accept connection. If there is not one, an exception is thrown and we return.
    try:
        conn, addr = my_socket.accept()
    except: return

    # Increment connection counter.
    connection_counter += 1

    # Use "with" to autmatically handle closing the connection.
    with conn:
        logging.debug("Received connection", connection_counter, "from addr", addr)

        # Initialize variable to aggregate data.
        total_data = ""

        # Get data until there is no more and we break.
        while True:
            try:
                # Try to get more data. If has not got through yet, python will throw an exception.
                data = conn.recv(1024)

                # If the data is empty, it means the connection has been terminated by the client. Exit loop.
                if not data:
                    break

                # Try to decode data.
                try:
                    data = data.decode(encoding="UTF-8", errors="strict")
                    total_data += data
                except UnicodeError:
                    # If decode fails, the data has been corrupted, so we return.
                    print("Unicode error on connection", connection_counter)
                    return
            except: pass

        # Ensure there is one and only one semicolon (checks integrity).
        if len(total_data.split(";")) != 2:
            print("Data does not end with semicolon", connection_counter, total_data)
            return

        # Try to process the data.
        try:
            # This version of the server only accepts version 1 data. There may be more code here in future versions.
            version = int(total_data.split("v", 1)[0])

            # If client has higher version number, there is nothing we can do.
            if version > VERSION:
                set_message("Unsupported client version", version)
                print("Usupported version", version)
                return

            # Remove the version.
            data = total_data.split("v", 1)[1]

            # Separate each number
            numbers = data.split(",", 2)

            # Process the numbers.
            x = int(numbers[0])
            y = int(numbers[1])
            heading = int(numbers[2].split(";", 1)[0]) # The semicolon allows us to cleanly remove the garbage from the end of the message.

            # Make tuple with robot position.
            robot_position = x, y, heading
            logging.debug("New robot position", robot_position)

            # Update robot position to the screen.
            set_robot_position(robot_position)
        except Exception as e:
            # Unexpected errors.
            print("Error processing", connection_counter, e)

def close_socket():
    """ This function closes the socket connection. Very important. """
    my_socket.close()