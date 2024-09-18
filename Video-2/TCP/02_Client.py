import socket

SERVER = 'localhost'  # Server Address
PORT = 9999
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 128  # The fixed length header to send message length

# Creating the client socket and connecting to the server
CLIENT_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# This method takes a two-item tuple object as argument. The two items are IP address and port number of the server.

CLIENT_SOCK.connect(ADDR)

# Function to send messages with length
def send_message(message):
    # Encode the message
    message_encoded = message.encode(FORMAT)
    
    # Calculate the message length
    msg_length = len(message_encoded)
    
    # Convert the length to string and encode it
    length_encoded = str(msg_length).encode(FORMAT)
    
    # Pad the length to match the fixed header size (HEADER)
    length_encoded += b' ' * (HEADER - len(length_encoded))
    
    # First, send the padded length
    CLIENT_SOCK.send(length_encoded)
    
    # Then, send the actual message
    CLIENT_SOCK.send(message_encoded)

# Send the initial message
payload = "Hey_Server"
send_message(payload)

try:
    while True:
        # Receive the server's response
        data = CLIENT_SOCK.recv(1024).decode(FORMAT)
        print(f"Server: {data}")
        
        # Prompt the user for additional input
        more = input("Enter more to send (or press Enter to continue): ")
        if len(more) == 0:
            payload = input("Enter your message: ")
        else:
            # Send the new message to the server
            send_message(more)
            break

except KeyboardInterrupt:
    print("Exited by User")

# Send the disconnect message
send_message("!DISCONNECT")

# Close the client socket
CLIENT_SOCK.close()
