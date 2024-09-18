import socket
import threading

PORT = 9999
HEADER = 64
# if the message is not 64 bytes then we will pad the rest of the message this technique is very common in CN
# SERVER  = "192.168.150.1" # Rather than doing this doing for you what we can do is 
SERVER  = socket.gethostbyname(socket.gethostname())# we are doing stuff on the same router/Lan based network but to do it on the interent just change this line and you are good to go.

# print(SERVER)
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_Client(conn , addr):# this function would be running in parallel(concurrently)
    print(f"[NEW CONNECTION] {addr} connected.")
    connected  = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)# a blocking line 
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
            if msg==DISCONNECT_MESSAGE:# We want a protocol such that we can handle to close the connection when someone leaves otherwise they would disconnect but when they will be willing to connect later then they might run into the problem that the server has already them connected
                # when you try to connect it might say hey you can't connect because on our end you are connected
                connected = False
            
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on--- {SERVER}")
    while True:
        conn, addr = server.accept()# This line waits for a new connection to the server # when a new connection occurs store the ipaddr, port it came from 
        thread = threading.Thread(target=handle_Client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()- 1}")
        # -1 because one thread is running always and that is this start thread.
        
        




print("[STARTING] server is starting....")
start()