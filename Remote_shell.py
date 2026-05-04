import socket
import threading
import argparse
import subprocess


def client_handler(client_socket, args): # Handling Coming sockets.  
    with client_socket as client:
        client.send(b"Welcome\n-h for help\n>>>: ")
        if args.execute :
            result = subprocess.run([args.execute], capture_output=True, text=True)
            print(result.stdout)
            client.send(result.stdout.encode())

        with client :
            while True :
                    message = client.recv(1024).decode()
                    #print(message.decode())
                    if message.strip() == "out":
                        print("Client closing the connection")
                        break
            client.send("Good bye. Hope to see y ou soon".encode())
            client.close()
            print("client closed")


def main(): 
    # Creating list of arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", nargs='?', default='0.0.0.0', help="IP address of the server")
    parser.add_argument('-p', '--port', type=int, default=4444, help="Specifying the port address. Default is 4444")
    parser.add_argument('-l', '--listen', action="store_true", help="Enable listening mod")
    parser.add_argument('-c', '--command', help="Enter the command you want to run after connection")
    parser.add_argument('-e', '--execute', help="The execute after connection")  
        
    args = parser.parse_args()
    try:
        sosmar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("sosmar is born")
        sosmar.bind((args.ip,args.port)) # Binding IP and port.
        print("sosmar is now binded")

        if args.listen :                     #Verifying the server mode
            sosmar.listen()                 #Initiate the listening
            print("sosmar waiting for connection")
            while True:
                conn, addr = sosmar.accept()
                print(f"Sosmar caught {addr[0]:{addr[1]}}")
                client_thread = threading.Thread(target=client_handler, args=(conn,args))
                client_thread.start()

        elif not args.listen:
            sosmar.connect((ip,port))
            # Connect to the server and pass the options and commands.
        else: 
            print(args.h)
    except NameError as e:
        print("wrong parameters enterd. use -h to see a help page")
    except socket.error as e:
        print(f"A socket error occurred : {e}")
    except KeyboardInterrupt as e:
        print(f"Sosmar stoped. {e}")
    finally:
        if 'sosmar' in locals() and sosmar:
            sosmar.close()
            print("sosmar is closed")

    
if __name__ == '__main__':
    main()


