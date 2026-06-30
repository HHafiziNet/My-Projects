# TCP Server

A simple multithreaded TCP server written in Python that listens for client connections, receives data, and sends acknowledgment responses.

## Features

- Configurable host IP and port
- Support for both IPv4 and IPv6 addresses
- Multithreaded client handling
- Input validation for IP addresses and ports
- Graceful shutdown with Ctrl+C

## Dependencies

All dependencies are part of Python's standard library:
- `ipaddress` - IP address validation
- `socket` - TCP socket communication
- `threading` - Multithreaded client handling

**Python Version**: 3.6+

## Installation

1. Clone or download this project
2. No additional packages required (uses only Python standard library)

## How to Run

### Option 1: Use Default Settings
```bash
python TCP_Server.py
```
Then select option `1` when prompted. The server will start on `0.0.0.0:4444`.

### Option 2: Use Custom IP and Port
```bash
python TCP_Server.py
```
Then select option `2` when prompted and enter:
- **IP Address**: Any valid IPv4 (e.g., `127.0.0.1`, `192.168.1.100`) or IPv6 address
- **Port**: A number between 1 and 65535 (e.g., `5000`)

### Option 3: Exit
Select option `3` to exit without starting the server.

## Example Output

```
Server Configuration
1. Use default settings
2. Enter custom IP and port
3. Exit
Choose (1/2/3): 1
Listening on 0.0.0.0:4444
Server is listening...
('127.0.0.1', 54321) connected
Hello from client
Server shutting down...
```

## Usage

### Starting the Server
```bash
python TCP_Server.py
```

### Connecting a Client
Using `telnet`:
```bash
telnet 127.0.0.1 4444
```

Using Python socket client:
```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 4444))
client.sendall(b"Hello Server")
response = client.recv(1024)
print(response.decode())  # Output: ACK
client.close()
```

Using `netcat` (nc):
```bash
echo "Hello from client" | nc 127.0.0.1 4444
```

## Configuration

Default settings can be modified by editing the constants at the top of `TCP_Server.py`:

```python
DEFAULT_HOST = "0.0.0.0"   # Listen on all interfaces
DEFAULT_PORT = 4444         # Port number
```

## How It Works

1. **Configuration**: Server prompts user to choose between default or custom settings
2. **Binding**: Server binds to the specified host and port
3. **Listening**: Server listens for incoming client connections
4. **Accepting Connections**: Accepts client connections in the main loop
5. **Handling Clients**: Each client is handled in a separate daemon thread
6. **Client Handler**: Receives data, prints it, and sends back an "ACK" response
7. **Shutdown**: Press Ctrl+C to gracefully shut down the server

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Address already in use" | Wait a moment or change the port number |
| "Invalid IP address" | Enter a valid IPv4 (e.g., 127.0.0.1) or IPv6 address |
| "Invalid port" | Enter a port number between 1 and 65535 |
| Clients disconnecting | Ensure the network connection is stable |

## License

This project is provided as-is for educational purposes.
