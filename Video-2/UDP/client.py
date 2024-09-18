import socket

# Define the server address and port.
# The client will send messages to this address and port.
PORT = 9090
SERVER = 'localhost'
ADDR = (SERVER, PORT)# this addr corresponds to server and not client (client needs address of server so as to send data to server)
FORMAT = 'utf-8'  # Character encoding for the messages.

def send_message():
    # Create a UDP socket.
    # AF_INET is the address family for IPv4.
    # SOCK_DGRAM is the socket type for UDP.
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Create a message to send to the server.
    msg = "Hello UDP Server"
    
    # Send the message to the server.
    # The server's address and port are specified in ADDR.
    udp_sock.sendto(msg.encode(FORMAT), ADDR)
    print("Message sent to server.")
    
    # Receive the response from the server.
    # The recvfrom method returns the data and the server's address.
    data, server_addr = udp_sock.recvfrom(8192)  # Buffer size of 8192 bytes.
    print("Server says:")
    print(data.decode(FORMAT))  # Decode the response to a string
    
    # Close the socket.
    udp_sock.close()

if __name__ == "__main__":
    send_message()
