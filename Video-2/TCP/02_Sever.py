import socket
import threading

# Server IP address and Port
SERVER = 'localhost'
PORT = 9999
ADDR = (SERVER, PORT)

# Refer to the image of Client Server Interaction 
# socket() -> bind()  -> listen() -> Accept() -> Interaction -> recv() -> send() -> close # SERVER SIDE
# socket() -> connect() -> send() -> receive() -> close() # CLIENT SIDE

# Creating the server-side socket
SERVER_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_SOCK.bind(ADDR)

DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = 'utf-8'
HEADER = 128

# Listen takes a backlog parameter.
# SERVER_SOCK.listen(5) # 5 connections will be kept waiting if the server is busy.
# If a 6th connection comes, it will be refused to connect.

def Client_Connect(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        # Receive message length (up to 128 bytes based on HEADER)
        msg_length = conn.recv(HEADER).decode(FORMAT)  # A blocking line

        # Check if msg_length is received properly
        if msg_length:
            try:
                # Convert the message length to an integer
                msg_length = int(msg_length)
                
                # Receive the actual message
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f"Client Socket object {conn} with Address:{addr}, received the message: {msg}")
                
                # Check if the client sent a disconnect message
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[DISCONNECT] Client {addr} has disconnected.")
                    break
                
                # Send a response message back to the client
                server_response = input("Enter the Server Message here: ")
                conn.send(server_response.encode(FORMAT))

            except ValueError:
                print(f"Received invalid message length: {msg_length}")
        else:
            print(f"No message received from {addr}")
            break

    conn.close()

def Listen():
    SERVER_SOCK.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # Waiting for a new connection to the server
        print("Server waiting for Connection...")
        Client_Sock, addr = SERVER_SOCK.accept()
        
        # Start a new thread to handle the client connection
        thread = threading.Thread(target=Client_Connect, args=(Client_Sock, addr))
        thread.start()

        # Print the number of active connections (minus the main thread)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# Starting the server
print("Server is Starting:")
Listen()
