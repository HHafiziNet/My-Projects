import ipaddress
import socket
import threading

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 4444


def handle_client(client):
    try:
        data = client.recv(4096)
        if data:
            print(data.decode("utf-8", errors="ignore"))
            client.sendall(b"ACK")
    except Exception as exc:
        print(f"Client error: {exc}")
    finally:
        client.close()


def get_server_config():
    print("\nServer Configuration")
    print("1. Use default settings")
    print("2. Enter custom IP and port")
    print("3. Exit")

    choice = input("Choose (1/2/3): ").strip()

    if choice == "1":
        return DEFAULT_HOST, DEFAULT_PORT

    if choice == "2":
        host = input(f"IP [{DEFAULT_HOST}]: ").strip() or DEFAULT_HOST

        while True:
            try:
                ipaddress.ip_address(host)
                break
            except ValueError:
                print("Invalid IP address.")
                host = input("IP: ").strip() or DEFAULT_HOST

        while True:
            port_input = input(f"Port [{DEFAULT_PORT}]: ").strip() or str(DEFAULT_PORT)
            try:
                port = int(port_input)
                if 1 <= port <= 65535:
                    return host, port
            except ValueError:
                pass

            print("Invalid port. Use a number from 1 to 65535.")

    raise SystemExit(0)


def main():
    try:
        host, port = get_server_config()
    except SystemExit:
        return

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((host, port))
        server.listen(5)
        print(f"Listening on {host}:{port}")

        while True:
            client, addr = server.accept()
            print(f"{addr} connected")
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()

    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server.close()


if __name__ == "__main__":
    main()

