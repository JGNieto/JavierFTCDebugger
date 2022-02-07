from email.policy import strict
import socket
from tkinter import E
from screen import set_robot_position

HOST = "127.0.0.1"
PORT = 11468

# The version of our little debugging protocol that we support.
# For now, only one version exists.
VERSION = 1

connection_counter = 0 # Keep track of how many connections have occurred.

def open_socket():
    global my_socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((HOST, PORT))
    my_socket.listen()
    my_socket.setblocking(0)

def wait_for_connection():
    """ This function sees if the client has sent new position information. """
    global connection_counter
    try:
        conn, addr = my_socket.accept()
    except: return
    connection_counter += 1
    with conn:
        print("Received connection", connection_counter, "from addr", addr)
        total_data = ""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                data = data.decode(encoding="UTF-8", errors="strict")
                total_data += data
                if data.endswith(";"): break
            except UnicodeError:
                print("Unicode error on connection", connection_counter)
                return

        # Process and interpret data
        if len(total_data.split(";")) != 2:
            print("Data does not end with semicolon", connection_counter, total_data)
            return

        try:
            version = int(total_data.split("v", 1)[0])
            if version > VERSION:
                print("Usupported version", version)
                return

            data = total_data.split("v", 1)[1]
            numbers = data.split(",", 2)

            x = int(numbers[0])
            y = int(numbers[1])
            heading = int(numbers[2].split(";", 1)[0]) # The semicolon allows us to cleanly remove the garbage from the end of the message.

            robot_position = x, y, heading
            print("New robot position", robot_position)

            set_robot_position(robot_position)
        except Exception as e:
            print("Error processing", connection_counter, e)

def close_socket():
    """ This function closes the socket connection. Very important. """
    my_socket.close()