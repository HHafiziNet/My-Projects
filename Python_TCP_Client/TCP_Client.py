import ipaddress
import socket

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 4444


def get_target_config():
    print("\nConnection Configuration")
    print("1. Use default settings")
    print("2. Enter custom IP and port")
    print("3. Exit")

    choice = input("Choose (1/2/3): ").strip()

    if choice == "1":
        return DEFAULT_HOST, DEFAULT_PORT

    if choice == "2":
        while True:
            host = input(f"IP [{DEFAULT_HOST}]: ").strip() or DEFAULT_HOST
            try:
                ipaddress.ip_address(host)
                break
            except ValueError:
                print("Invalid IP address. Try again.")

        while True:
            port_input = input(f"Port [{DEFAULT_PORT}]: ").strip() or str(DEFAULT_PORT)
            try:
                port = int(port_input)
                if 1 <= port <= 65535:
                    return host, port
            except ValueError:
                pass

            print("Invalid port. Use a number between 1 and 65535.")

    raise SystemExit(0)


def main():
    try:
        target, port = get_target_config()
    except SystemExit:
        return

    print(f"\nConnecting to {target}:{port}...")
    sosmar = None

    try:
        sosmar = socket.create_connection((target, port), timeout=5)
        print(f"Connected to {target}:{port}")

        message = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n".encode("utf-8")
        sosmar.sendall(message)

        print("Message sent. Waiting for response...")
        response = sosmar.recv(4096)
        print("-" * 79)
        print(response.decode("utf-8", errors="ignore"))

    except socket.error as e:
        print(f"Socket error: {e}")
    except KeyboardInterrupt:
        print("User aborted the connection")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if sosmar:
            sosmar.close()
            print("\n" + "-" * 79)
            print("Connection closed")


if __name__ == "__main__":
    main()
