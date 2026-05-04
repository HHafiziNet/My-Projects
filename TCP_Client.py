import socket
target = '192.168.0.20'
port = 4444
print("HI")
try : 
    sosmar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("sosmar is hunting ...")
    sosmar.bind(("192.168.0.20",2222))
    sosmar.connect((target, port))
    print(sosmar.getsockname())
    print(f"Sosmar hunted {target}:{port}" if sosmar else "Not connect")
    sosmar.send("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n".encode())
    print("sosmar sent message\nWaiting for response ...")
    response = sosmar.recv(4096)
    print("-"*79)
    print(response.decode())
except socket.error as e: 
    print(f"A socket errror occurred : {e}")
except Exception : 
    print("Error occured. Connection refused!!!" + str(e))
except KeyboardInterrupt :
    print("User aborted the sosmar")
finally : 
    if "sosmar" in locals() and sosmar: 
        sosmar.close()
        print("\n\n" + "-" * 79 )
        print("Sosmar is closed")
