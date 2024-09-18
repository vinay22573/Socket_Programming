import socket
# Always remember that you have to start the server first
HEADER  = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.43.42"
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  # Proper padding with spaces
    # First, send the length of the message
    client.send(send_length)
    # Then, send the actual message
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    


send("Hello Everyone")
input()
# send("I am Vinay")
# send("Who are you?")
# input()
# send("let's Disconnect")
# input()
# send("Bye")
# send(DISCONNECT_MESSAGE)