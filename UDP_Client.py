import socket
#import subprocess
#import os
#import threading

target = "localhost"
port = 80

try : 
    sosmar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("sosmar created")
    sosmar.connect((target,port))
    print("sosmar connected")
    sosmar.sendto("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n".encode(),(target,port))
    print("sosmar is sending")
    response, addr = sosmar.recvfrom(4086)
    print("Waiting for response ...\n\n")
    print(response.decode() + f"from {addr}")
except socket.error :
    print("Socket error occurred")
finally :
    if 'sosmar' in locals() and sosmar:
        sosmar.close()
        print("Sosmar closed")

