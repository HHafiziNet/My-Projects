import socket
import datetime
from urllib.parse import urlparse
from tqdm import tqdm


def resolve_host(target):
    parsed = urlparse(target if "://" in target else f"http://{target}")
    host = parsed.hostname or target
    try:
        return socket.gethostbyname(host)
    except socket.gaierror as e:
        raise ValueError(f"Unable to resolve host '{target}': {e}") from e


def Scanner(target, S_Port=1, E_Port=1023, timeout=0.1):
    open_ports = []
    start_time = datetime.datetime.now()
    total_ports = E_Port - S_Port + 1
    resolved_ip = resolve_host(target)

    print("=" * 60)
    print("PORT SCANNER")
    print("=" * 60)
    print(f"Target        : {target}")
    print(f"Resolved IP   : {resolved_ip}")
    print(f"Port range    : {S_Port} - {E_Port} ({total_ports} ports)")
    print(f"Start time    : {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    for port in tqdm(range(S_Port, E_Port + 1), desc="Scanning ports", unit="port"):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                if sock.connect_ex((resolved_ip, port)) == 0:
                    open_ports.append(port)
        except socket.timeout:
            continue
        except socket.error as e:
            tqdm.write(f"Error while checking port {port}: {e}")
        except KeyboardInterrupt:
            tqdm.write("\nScan stopped by user")
            break

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print()
    print("-" * 60)
    print(f"Scan completed in {duration.total_seconds():.2f} seconds")
    print(f"Open ports   : {len(open_ports)} / {total_ports}")
    if open_ports:
        print("Open port(s) : " + ", ".join(str(p) for p in open_ports))
    else:
        print("Open port(s) : None found")
    print("-" * 60)

    return open_ports


def main():
    target = input("Enter IP address or URL to scan: ").strip()
    try:
        print("\n" + "-" * 50)
        print("Port Range Selection")
        print("-" * 50)
        print("Default range: 1 - 1024\n")

        start_port_input = input("Enter start port (default 1): ").strip()
        start_port = int(start_port_input) if start_port_input else 1

        end_port_input = input("Enter end port (default 1024): ").strip()
        end_port = int(end_port_input) if end_port_input else 1024

        print()
        res = Scanner(target, start_port, end_port)

        if res:
            print("\nDetailed open ports:")
            for port in res:
                print(f"  - Port {port} is open")
        else:
            print("\nNo open ports were detected.")
    except ValueError as e:
        print(e)
    except KeyboardInterrupt:
        print("\nProgram stopped by user")


if __name__ == "__main__":
    main()