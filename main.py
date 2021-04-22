# Taken and adapter from https://github.com/dbaldwin/DroneBlocks-Tello-Python/blob/master/lesson4-box-mission/TelloBoxMission.ipynb
# This example script demonstrates how use Python to fly Tello in a box mission
# This script is part of our course on Tello drone programming
# https://learn.droneblocks.io/p/tello-drone-programming-with-python/

# Import the necessary modules
import socket
import threading
import time
import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy as sp
import Code.waypoint_class
import matplotlib.pyplot as plt

# EDIT HERE
def main_function(waypoints, sock):

    # Insert your functions here. If you want to import additional functions that you've created, feel free to do so. However, make sure the
    # file paths still

    # Set up 3 axies chart
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # XYZ data to be graphed
    X=[0, 0,-60,-60,0,0,  60,60,0,0,   104,334,230,0,  -104,-334,-230,0]
    Y=[0, 0,104,334,230,0,  -104,-334,-230,0,   60,60,0,0,  -60,-60,0,0]
    Z=[0, 20,20,20,20,20,  20,20,20,20,   20,20,20,20,  20,20,20,20]

    # Make 3D plot of origonal XYZ data
    ax.plot3D(X,Y,Z,'*-')

    # Show 3d plot
    plt.show()

    # Put Tello into command mode
    send("command", 3)

    # Send the takeoff command
    send("takeoff", 10)

    # 4 leaf clover
    send("curve " + str(60) + " " + str(104) + " " + str(0) + " " + str(0) + " " + str(230) + " " + str(0) + " " + str(60), 5)
    send("curve " + str(-60) + " " + str(-104) + " " + str(0) + " " + str(0) + " " +  str(-230) + " " + str(0) + " " + str(60), 5)
    send("curve " + str(60) + " " + str(-104) + " " + str(0) + " " + str(0) + " " + str(-230) + " " + str(0) + " " + str(60), 5)
    send("curve " + str(-60) + " " + str(104) + " " + str(0) + " " + str(0) + " " +  str(230) + " " + str(0) + " " + str(60), 5)
    send("curve " + str(104) + " " + str(60) + " " + str(0) + " " + str(230) + " " + str(0) + " " + str(0) + " " + str(60), 5)
    send("curve " + str(-104) + " " + str(-60) + " " + str(0) + " " + str(-230) + " " + str(0) + " " + str(0) + " " + str(60), 5)
    send("curve " + str(-104) + " " + str(-60) + " " + str(0) + " " + str(-230) + " " + str(0) + " " + str(0) + " " + str(60), 5)
    send("curve " + str(104) + " " + str(60) + " " + str(0) + " " + str(230) + " " + str(0) + " " + str(0) + " " + str(60), 5)

    # Land
    send("land", 5)

    # Print message
    print("Mission completed successfully!")

    return

##############################################
# DO NOT EDIT ANYTHING BELOW HERE
##############################################

def ex_main_function(waypoints, sock):

    ##################
    # DRAW plot first
    ##################
    plt.figure()
    plt.plot([0,0,100,100,0],[0,100,100,0,0,0],'*-')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

    ####################
    # Now run drone code
    ####################

    # Each leg of the box will be 100 cm. Tello uses cm units by default.
    box_leg_distance = 100

    # Yaw 90 degrees
    yaw_angle = 90

    # Yaw clockwise (right)
    #yaw_direction = "cw"

    # Put Tello into command mode
    send("command", 3)

    # Send the takeoff command
    send("takeoff", 5)

    # Fly forward
    send("forward " + str(box_leg_distance), 4)

    # Yaw right
    send("cw " + str(yaw_angle), 3)

    # Fly forward
    send("forward " + str(box_leg_distance), 4)

    # Yaw right
    send("cw " + str(yaw_angle), 3)

    # Fly forward
    send("forward " + str(box_leg_distance), 4)

    # Yaw right
    send("cw " + str(yaw_angle), 3)

    # Fly forward
    send("forward " + str(box_leg_distance), 4)

    # Yaw right
    send("cw " + str(yaw_angle), 3)

    # Land
    send("land", 5)

    # Print message
    print("Mission completed successfully!")

    return

# IP and port of Tello
tello_address = ('192.168.10.1', 8889)

# IP and port of local computer
local_address = ('', 9000)

# Create a UDP connection that we'll send the command to
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the local address and port
sock.bind(local_address)

# Send the message to Tello and allow for a delay in seconds
def send(message, delay):
# Try to send the message otherwise print the exception
    try:
        sock.sendto(message.encode(), tello_address)
        print("Sending message: " + message)
    except Exception as e:
        print("Error sending: " + str(e))

    # Delay for a user-defined period of time
    time.sleep(delay)

# Receive the message from Tello
def receive():
    # Continuously loop and listen for incoming messages
    while True:
        # Try to receive the message otherwise print the exception
        try:
            response, ip_address = sock.recvfrom(128)
            print("Received message: " + response.decode(encoding='utf-8'))
        except Exception as e:
            # If there's an error close the socket and break out of the loop
            sock.close()
            print("Error receiving: " + str(e))
            break

if __name__ == "__main__":

    # Create and start a listening thread that runs in the background
    # This utilizes our receive functions and will continuously monitor for incoming messages
    receiveThread = threading.Thread(target=receive)
    receiveThread.daemon = True
    receiveThread.start()

    waypoints = [] # This will contain an array of Waypoint class objects

    # Execute the actual algorithm
    #ex_main_function(waypoints, sock)
    main_function(waypoints, sock)



    # Close the socket
    sock.close()