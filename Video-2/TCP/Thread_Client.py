import socket
import threading

# Define client parameters
HOST = 'localhost'  # Server IP address
PORT = 8085  # Port to connect to
ADDR = (HOST, PORT)  # Address tuple
FORMAT = 'utf-8'  # Encoding format

def receive_messages(client_socket):
    """
    Function to continuously receive messages from the server and display them.
    """
    while True:
        try:
            # Receive message from the server
            message = client_socket.recv(1024).decode(FORMAT)
            if not message:
                print("Server connection closed.")
                break
            print(f"\nServer says: {message}")
        except socket.error as e:
            print(f"Error receiving message: {e}")
            break

def send_messages(client_socket):
    """
    Function to take user input and send messages to the server.
    """
    while True:
        try:
            # Take user input
            user_input = input("\nEnter message to send (or 'disconnect' to quit): ")
            if user_input.lower() == 'disconnect':
                print("Disconnecting from server...")
                break

            # Send the user input to the server
            client_socket.send(str.encode(user_input, FORMAT))

        except socket.error as e:
            print(f"Error sending message: {e}")
            break

    # Close the socket after disconnect
    client_socket.close()

def connect_to_server():
    """
    Function to connect to the server and start sending and receiving threads.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket

    try:
        client_socket.connect(ADDR)  # Connect to the server
        print(f"Connected to server at IP address: {HOST}, Port: {PORT}")

        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # Handle sending messages from the main thread
        send_messages(client_socket)

    except socket.error as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    connect_to_server()
