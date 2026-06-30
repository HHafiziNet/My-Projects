import argparse
import concurrent.futures
import errno
import socket
import datetime
from urllib.parse import urlparse
from tqdm import tqdm

KNOWN_SERVICES = {
    20: "ftp-data",
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "domain",
    67: "dhcp",
    68: "dhcp",
    80: "http",
    110: "pop3",
    123: "ntp",
    143: "imap",
    161: "snmp",
    194: "irc",
    443: "https",
    465: "smtps",
    587: "smtp",
    993: "imaps",
    995: "pop3s",
    3306: "mysql",
    3389: "rdp",
    5432: "postgresql",
    5900: "vnc",
    6379: "redis",
    8080: "http-alt",
}


def resolve_host(target):
    parsed = urlparse(target if "://" in target else f"http://{target}")
    host = parsed.hostname or target
    try:
        return socket.gethostbyname(host)
    except socket.gaierror as e:
        raise ValueError(f"Unable to resolve host '{target}': {e}") from e


def resolve_service(port, protocol="tcp"):
    try:
        return socket.getservbyport(port, protocol)
    except OSError:
        return KNOWN_SERVICES.get(port)


def validate_port(value):
    port = int(value)
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("Port must be between 1 and 65535")
    return port


def scan_port(resolved_ip, port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)

        result = sock.connect_ex((resolved_ip, port))

        if result == 0:
            return port, "open"
        else:
            return port, "closed"


def Scanner(target, S_Port=1, E_Port=1023, timeout=1, max_workers=100):
    if S_Port < 1 or E_Port < 1 or S_Port > 65535 or E_Port > 65535:
        raise ValueError("Port range must be between 1 and 65535")
    if S_Port > E_Port:
        raise ValueError("Start port must be less than or equal to end port")

    open_ports = []
    closed_ports = []
    start_time = datetime.datetime.now()
    total_ports = E_Port - S_Port + 1
    resolved_ip = resolve_host(target)
    workers = min(max_workers, total_ports)

    print("=" * 60)
    print("PORT SCANNER")
    print("=" * 60)
    print(f"Target        : {target}")
    print(f"Resolved IP   : {resolved_ip}")
    print(f"Port range    : {S_Port} - {E_Port} ({total_ports} ports)")
    print(f"Threads       : {workers}")
    print(f"Timeout       : {timeout:.2f} seconds")
    print(f"Start time    : {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    futures = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for port in range(S_Port, E_Port + 1):
            futures[executor.submit(scan_port, resolved_ip, port, timeout)] = port

        try:
            for future in tqdm(concurrent.futures.as_completed(futures), total=total_ports, desc="Scanning ports", unit="port"):
                port = futures[future]
                try:
                    result_port, status = future.result()
                    if status == "open":
                        open_ports.append(result_port)
                    else:
                        closed_ports.append(result_port)
                except socket.error as e:
                    tqdm.write(f"Error while checking port {port}: {e}")
        except KeyboardInterrupt:
            tqdm.write("\nScan stopped by user")
            for future in futures:
                future.cancel()

    open_ports.sort()
    closed_ports.sort()
    end_time = datetime.datetime.now()
    duration = end_time - start_time

    print()
    print("-" * 60)
    print(f"Scan completed in {duration.total_seconds():.2f} seconds")
    print(f"Open ports   : {len(open_ports)} / {total_ports}")
    print(f"Closed ports : {len(closed_ports)} / {total_ports}")
    print("-" * 60)

    return open_ports


def parse_arguments():
    parser = argparse.ArgumentParser(description="Multi-threaded TCP port scanner")
    parser.add_argument("target", nargs="?", help="IP address or URL to scan")
    parser.add_argument("-s", "--start", type=validate_port, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=validate_port, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--timeout", type=float, default=1, help="Socket timeout in seconds (default: 1)")
    parser.add_argument("-w", "--workers", type=int, default=100, help="Number of concurrent worker threads (default: 100)")
    return parser.parse_args()


def main():
    args = parse_arguments()

    if not args.target:
        target = input("Enter IP address or URL to scan: ").strip()
    else:
        target = args.target.strip()

    try:
        print("\n" + "-" * 50)
        print("Port Range Selection")
        print("-" * 50)
        print("Default range: 1 - 1024\n")

        start_port = args.start
        end_port = args.end

        if not args.target:
            start_port_input = input(f"Enter start port (default {start_port}): ").strip()
            start_port = int(start_port_input) if start_port_input else start_port
            end_port_input = input(f"Enter end port (default {end_port}): ").strip()
            end_port = int(end_port_input) if end_port_input else end_port

        print()
        res = Scanner(target, start_port, end_port, timeout=args.timeout, max_workers=args.workers)

        if res:
            print("\nDetailed open ports:")
            for port in res:
                service = resolve_service(port) or None
                if service:
                    print(f"  - Port {port} ({service}) is open")
                else:
                    print(f"  - Port {port} is open")
        else:
            print("\nNo open ports were detected.")
    except ValueError as e:
        print(e)
    except KeyboardInterrupt:
        print("\nProgram stopped by user")


if __name__ == "__main__":
    main()
