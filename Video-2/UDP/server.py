import socket

# Define the server address and port.
# The server listens on this IP address and port for incoming messages.
PORT = 9090
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'  # Character encoding for the messages.

def start_server():
    # Create a UDP socket.
    # AF_INET is the address family for IPv4.
    # SOCK_DGRAM is the socket type for UDP.
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the address and port.
    # This allows the server to listen for incoming messages on this address and port.
    udp_sock.bind(ADDR)
    
    print(f"Server is listening on {ADDR}")

    while True:
        # Receive data from the client.
        # The recvfrom method returns the data and the client's address.
        data, client_addr = udp_sock.recvfrom(8192)  # Buffer size of 8192 bytes.
        print(f"Received message from {client_addr}: {data.decode(FORMAT)}")
        
        # Create a response message to send back to the client.
        response_message = "Hello from UDP Server.".encode(FORMAT)
        
        # Send the response message to the client's address.
        # This address is obtained from the recvfrom call.
        udp_sock.sendto(response_message, client_addr)
        print(f"Response sent to {client_addr}.")

if __name__ == "__main__":
    start_server()
