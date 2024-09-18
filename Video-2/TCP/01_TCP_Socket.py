import socket
import sys
# s = socket.socket(family=AF_INET,type=SOCK_DGRAM) for UDP
# s = socket.socket(family=AF_INET,type=SOCK_STREAM) #for TCP

#Errors can occur so it is a good idea to do some error handling or proper network bound communication
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("Failed to Create the Socket.")
    print("Reason"+str(err))
    sys.exit()
print("Socket Create")
HOST = input("Enter the target host name to connect:")
PORT = input("Enter the target port:")
ADDR  = (HOST , int(PORT))
try:
    sock.connect((HOST,int(PORT)))
    print(f"Socket Connected to {HOST} on Port#: {PORT}")
    sock.shutdown(2)
except socket.error as err:
    print("Failed to Connect to " +HOST+ PORT)
    print(f"Error: {err}")
    sys.exit()
    