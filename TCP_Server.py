import socket
import threading

def thread_handler(client):
    response = client.recv(4089)
    client.send("ACK".encode())
    print(response.encode())
    client.close()

IP = '192.168.0.20'
port = 4444


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP,port))
print(f"{IP}:{port} binded to the server")
server.listen()
print("server is listening")
while True: 
    client, addr = server.accept()
    print(f"{addr} connected to the server.")
    client_thread = threading.Thread(target=thread_handler, args=(client,))
    client_thread.start()
