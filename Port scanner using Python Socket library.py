scapyimport socket
import datetime
from tqdm import tqdm



def Scanner(IP , S_Port=1, E_Port=1023, timeout = 0.1):

    open_ports = []
    start_time = datetime.datetime.now()
    total_ports = E_Port - S_Port + 1
    scan_count = 0

    print('-' * 50)
    print(f"Starting scan on {IP}",)
    print(f"Port range {S_Port} {E_Port} ")
    print(f"Start time {start_time.strftime("%Y-%m-%d %H:%M:%S")}")
    print('\n')

    for port in tqdm(range(S_Port, E_Port + 1), desc=f"Scan progress"):

        scan_count += 1

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                if sock.connect_ex((IP, port)) == 0 :
                    #print(f"Port {port} is open\n")
                    open_ports.append(port)
        except socket.timeout:
            continue
        except socket.error as e:
            tqdm.write(f"Error while checking port {port} : {e}")
        except KeyboardInterrupt:
            tqdm.write("\n\nScan stopped by user")
            break

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"Scan completed in {duration.total_seconds():.2f} seconds")
    print(f"Open ports : {len(open_ports)} out of {total_ports}")
    return open_ports


IP = "127.0.0.1"
try:
    res = Scanner(IP, int(input("Start port: ")), int(input("End port ")))
    for i in res:
        print(f"Port {i} is open")
except ValueError:
    print("Wrong parameters")
except KeyboardInterrupt :
    print("Program stopped by user")




