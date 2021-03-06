import socket
import threading
 
PORT = 5000
SERVER = "0.0.0.0"
 
# Address is stored as a tuple
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
 
# Lists that will contains
# all the clients connected to
# the server and their names.
clients, names = [], []
 
# Create a new socket for
# the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# bind the address of the
# server to the socket
server.bind(ADDRESS)
 
# function to start the connection
def startChat():
   
    print("Servidor funcionando em " + SERVER)
     
    # listening for connections
    server.listen()
     
    while True:
       
        # accept connections and returns
        # a new connection to the client
        #  and  the address bound to it
        conn, addr =  server.accept()
        conn.send("NAME".encode(FORMAT))
         
        # 1024 represents the max amount
        # of data that can be received (bytes)
        name = conn.recv(1024).decode(FORMAT)
         
        # append the name and client
        # to the respective list
        names.append(name)
        clients.append(conn)
         
        print(f"Nome: {name}")
         
        # broadcast message
        broadcastMessage(f"{name} está no chat!".encode(FORMAT))
        conn.send('Conexão bem sucedida!'.encode(FORMAT))
         
        # Start the handling thread
        thread = threading.Thread(target = handle, args = (conn, addr))
        thread.start()
         
        # no. of clients connected
        # to the server
        print(f"conexões ativas {threading.active_count()-1}")
 
# method to handle the
# incoming messages
def handle(conn, addr):
   
    print(f"Nova conexão: {addr}")
    connected = True
     
    while connected:
          # receive message
        message = conn.recv(1024)
         
        # broadcast message
        broadcastMessage(message)
     
    # close the connection
    conn.close()
 
def broadcastMessage(message):
    for client in clients:
        client.send(message)
 
startChat()