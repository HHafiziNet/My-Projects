# TCP Client – Socket Testing Tool

A lightweight, interactive TCP client for testing and debugging socket-based services. Connects to any TCP server, sends a raw HTTP/1.1 GET request, and displays the server's response.

## Features

- Interactive configuration menu for connection settings.
- IP address validation using `ipaddress` module.
- Port validation (1-65535).
- Uses `socket.create_connection()` with configurable timeout (5 seconds).
- Sends a pre-formatted HTTP/1.1 GET request.
- Displays server response with proper decoding.
- Comprehensive error handling for network issues and user interruptions.
- Automatically closes the socket upon completion or error.

## Project Structure
```
TCP_Client.py   # single-file TCP client tool
README.md
```

## Dependencies

| Dependency | Type | Installation Command |
| :--- | :--- | :--- |
| Python 3.6+ | Runtime | N/A |

*All modules (`ipaddress`, `socket`) are part of Python's standard library.*

## How It Works

### Configuration Menu
1. The tool presents three options to the user:
   - **Option 1:** Use default settings (`127.0.0.1:4444`).
   - **Option 2:** Enter custom IP and port (with validation).
   - **Option 3:** Exit the program.
2. If a custom IP is entered, the tool validates it using `ipaddress.ip_address()`.
3. If a custom port is entered, the tool validates it is between 1 and 65535.

### Connection and Request
1. The tool establishes a TCP connection using `socket.create_connection()` with a 5-second timeout.
2. It sends a pre-formatted HTTP/1.1 GET request:
   ```
   GET / HTTP/1.1
   Host: localhost

   ```
3. It waits for the server response and reads up to 4096 bytes.
4. The response is decoded (UTF-8) and displayed to the user.

### Cleanup
- The socket is closed in the `finally` block regardless of success or failure.

## Usage

### Start the client
```bash
python TCP_Client.py
```

### Example Session – Using Default Settings
```
Connection Configuration
1. Use default settings
2. Enter custom IP and port
3. Exit
Choose (1/2/3): 1

Connecting to 127.0.0.1:4444...
Connected to 127.0.0.1:4444
Message sent. Waiting for response...
-------------------------------------------------------------------------------
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1024

<html>
<head><title>Test Server</title></head>
<body>
<h1>Hello from Test Server</h1>
</body>
</html>
-------------------------------------------------------------------------------
Connection closed
```

### Example Session – Custom Configuration
```
Connection Configuration
1. Use default settings
2. Enter custom IP and port
3. Exit
Choose (1/2/3): 2
IP [127.0.0.1]: 192.168.1.100
Port [4444]: 8080

Connecting to 192.168.1.100:8080...
Connected to 192.168.1.100:8080
Message sent. Waiting for response...
-------------------------------------------------------------------------------
[Server response displayed here...]
-------------------------------------------------------------------------------
Connection closed
```

### Command-Line Arguments (None)
This tool uses an interactive menu system and does not accept command-line arguments.

## Notes

* The tool sends a **fixed** HTTP/1.1 GET request to the root path (`/`) with `Host: localhost`. For servers expecting a different Host header, modify the `message` variable in the code.
* The client uses `socket.create_connection()` with a **5-second timeout** to prevent hanging indefinitely.
* The response is decoded using UTF-8 with `errors="ignore"`, meaning invalid characters are skipped.
* Only **4096 bytes** of the response are read. For larger responses, the data will be truncated.
* This client is designed for **plain TCP** communication. For TLS/SSL (HTTPS), use `ssl.wrap_socket()` or the `requests` library.

## Limitations

* **Hardcoded HTTP Request:** The client always sends the same GET request to `/` with `Host: localhost`. It cannot send custom requests or commands.
* **Single Request Only:** The client sends one request and closes the connection. It does not support persistent connections or multiple requests.
* **Response Truncation:** `recv(4096)` reads only the first 4KB of the response. Large responses will be truncated.
* **No TLS/SSL Support:** Cannot connect to HTTPS or other encrypted services without modification.
* **No Payload Sending:** The client cannot send custom data beyond the hardcoded HTTP request.
* **Limited Error Messages:** Generic "Socket error" messages may not provide enough detail for debugging.
* **No Keep-Alive:** Connection is closed immediately after receiving the response.

## Learning Goals

* Understanding TCP/IP socket programming in Python.
* Using `socket.create_connection()` for simplified client connections.
* Implementing input validation for IP addresses and ports.
* Building interactive command-line menus with user input.
* Handling socket errors, timeouts, and connection issues.
* Proper resource management with `try/finally` for socket cleanup.
* Sending and receiving raw data over TCP.
* Decoding byte data to readable text.

## Disclaimer

⚠️ **This tool is for educational purposes and authorized network testing only.**  
Unauthorized use of this tool against networks, systems, or devices without explicit written permission from the owner is illegal and violates computer fraud and abuse laws (e.g., CFAA in the US, Computer Misuse Act in the UK). The developer assumes **zero liability** for any misuse or damage caused by this script. Use responsibly and only in isolated lab environments or on systems you own.

## License

Educational use only. No warranty. Provided "as is" without any guarantees.