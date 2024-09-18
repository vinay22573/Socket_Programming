import socket
import threading

# Server parameters
HOST = 'localhost'  # Server IP address
PORT = 8085  # Port to listen on
ADDR = (HOST, PORT)  # Address tuple
FORMAT = 'utf-8'  # Encoding format
MAX_CONNECTIONS = 5  # Maximum number of queued connections

# List to keep track of all connected clients
clients = []

def handle_client_connection(client_socket):
    """
    Handle the client connection. Receives data from client,
    processes it, and sends a response back.
    """
    welcome_message = f"Welcome to the Server with IP Addr: {HOST}, PORT: {PORT}"
    client_socket.send(str.encode(welcome_message, FORMAT))  # Send welcome message
    print(f"Sent welcome message to {client_socket.getpeername()}")

    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(2048)
            if not data:
                # No data received, client has closed the connection
                break

            # Process the received data
            received_message = data.decode(FORMAT)
            response_message = f"Server: This is what was received: {received_message}"
            client_socket.sendall(str.encode(response_message, FORMAT))
            print(f"Received and responded to {client_socket.getpeername()}: {received_message}")

        except socket.error as e:
            print(f"Socket error: {e}")
            break

    # Close the connection
    close_client_connection(client_socket)

def close_client_connection(client_socket):
    """
    Close the connection with a client and remove it from the client list.
    """
    client_socket.close()
    clients.remove(client_socket)
    print(f"Connection with {client_socket.getpeername()} closed")

def accept_connections(server_socket):
    """
    Accept new client connections and start a thread to handle each client.
    """
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)  # Add new client to the list
        print(f"New connection from {client_address}")

        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_thread.start()

        print(f"Active threads: {threading.active_count() - 1}")

def broadcast_message(message):
    """
    Broadcast a message to all connected clients.
    """
    for client_socket in clients:
        try:
            client_socket.send(str.encode(message, FORMAT))
        except socket.error as e:
            print(f"Error sending to client {client_socket.getpeername()}: {e}")

def start_server():
    """
    Set up and start the server, then handle client connections and server-side input.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP socket

    try:
        server_socket.bind(ADDR)  # Bind the socket to the address
        print(f"Server started on {HOST}:{PORT}")
    except socket.error as e:
        print(f"Socket binding error: {e}")
        return

    server_socket.listen(MAX_CONNECTIONS)  # Start listening for connections
    print(f"Server is listening for connections (Max {MAX_CONNECTIONS})...")

    # Start a thread to accept client connections
    accept_thread = threading.Thread(target=accept_connections, args=(server_socket,))
    accept_thread.start()

    # Main thread handles server-side input
    while True:
        try:
            user_input = input("Enter a message to broadcast to all clients (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                print("Server shutting down...")
                break
            
            # Broadcast the input message to all connected clients
            broadcast_message(user_input)

        except KeyboardInterrupt:
            print("\nServer interrupted by user")
            break

    # Close all client connections and the server socket
    for client_socket in clients:
        close_client_connection(client_socket)
    server_socket.close()
    print("Server closed")

if __name__ == "__main__":
    start_server()
