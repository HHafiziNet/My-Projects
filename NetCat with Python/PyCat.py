import sys
import shlex
import argparse
import socket
import threading
import subprocess


def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s


# ---------------- CLIENT ----------------
def run(sock, args):
    try:
        sock.settimeout(1)
        sock.connect((args.target, args.port))
        sock.settimeout(1)

        while True:
            # receive
            try:
                response = b''

                while b'\n' not in response:
                    try:
                        data = sock.recv(4096)

                        if not data:
                            print("[!] Server closed connection")
                            return

                        response += data

                    except socket.timeout:
                        break

                if response:
                    print(response.decode(errors="ignore"))

            except Exception as e:
                print(f"[recv error] {e}")

            # send
            buffer = input(">>> ").strip()
            if buffer:
                sock.sendall((buffer + "\n").encode())

    except KeyboardInterrupt:
        print("\n[!] Client stopped")

    except Exception as e:
        print(f"[!] Error: {e}")

    finally:
        sock.close()
        sys.exit()


# ---------------- SERVER ----------------
def listen(sock, args):
    sock.bind((args.target, args.port))
    sock.listen(5)

    print("-" * 30)
    print(f"[*] Listening on {args.port}")

    try:
        while True:
            client_socket, addr = sock.accept()
            print(f"[+] Connection from {addr}")

            thread = threading.Thread(
                target=handler,
                args=(client_socket, args),
                daemon=True
            )
            thread.start()

    except KeyboardInterrupt:
        print("\n[!] Stopping server")

    finally:
        sock.close()
        sys.exit()


# ---------------- HANDLER ----------------
def handler(client_socket, args):
    client_socket.send(b"welcome\n")

    if args.command:
        client_socket.send(execute(args.command))

    try:
        while True:
            buffer = b''

            while b'\n' not in buffer:
                data = client_socket.recv(4096)

                if not data:
                    return

                buffer += data

            command = buffer.decode(errors="ignore").strip()
            output = execute(command)

            client_socket.send(output)

    except Exception:
        pass

    finally:
        client_socket.close()


# ---------------- EXECUTOR ----------------
def execute(command):
    command = command.strip()

    try:
        output = subprocess.check_output(
            shlex.split(command),
            stderr=subprocess.STDOUT
        )
        return output

    except FileNotFoundError:
        return b"!Command not found\n"

    except subprocess.CalledProcessError as e:
        return e.output

    except Exception as e:
        return str(e).encode()


# ---------------- MAIN ----------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target')
    parser.add_argument('-p', '--port', type=int)
    parser.add_argument('-l', '--listen', action='store_true')
    parser.add_argument('-c', '--command')

    args = parser.parse_args()

    sock = create_socket()

    try:
        if args.listen:
            listen(sock, args)
        else:
            run(sock, args)

    except KeyboardInterrupt:
        print("\n[!] Interrupted")

    finally:
        sock.close()
        sys.exit()


if __name__ == "__main__":
    main()