# Multi-Thread Port Scanner

A fast and efficient TCP port scanner written in Python using multi-threading. Scan multiple ports simultaneously on a target host to identify open services.

## Features

- **Multi-threaded scanning** - Scan multiple ports in parallel for faster results
- **Host resolution** - Accepts both IP addresses and domain names
- **Service identification** - Identifies common services running on open ports
- **Progress tracking** - Real-time progress bar showing scan status
- **Customizable parameters** - Control thread count, timeout, and port range
- **Cross-platform** - Works on Windows, Linux, and macOS
- **Error handling** - Graceful handling of network errors and interruptions

## Dependencies

- **Python 3.6+**
- **tqdm** - Progress bar library

### Install Dependencies

```bash
pip install tqdm
```

Or install from requirements file:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run with default settings (scans ports 1-1024):

```bash
python multi_thread_port_scanner.py 192.168.1.1
```

Or scan a domain name:

```bash
python multi_thread_port_scanner.py google.com
```

### Command-Line Arguments

```bash
python multi_thread_port_scanner.py TARGET [OPTIONS]
```

**Arguments:**

- `TARGET` - IP address or URL to scan (optional - will prompt if not provided)

**Options:**

- `-s, --start PORT` - Start port number (default: 1)
- `-e, --end PORT` - End port number (default: 1024)
- `-t, --timeout SECONDS` - Socket timeout in seconds (default: 1)
- `-w, --workers COUNT` - Number of concurrent worker threads (default: 100)

### Examples

**Scan ports 1-1024 on localhost:**
```bash
python multi_thread_port_scanner.py 127.0.0.1
```

**Scan specific port range (80-443):**
```bash
python multi_thread_port_scanner.py 192.168.1.1 -s 80 -e 443
```

**Scan with custom timeout and fewer threads:**
```bash
python multi_thread_port_scanner.py example.com -t 2 -w 50
```

**Scan common services (1-65535 - not recommended without adjusting timeout):**
```bash
python multi_thread_port_scanner.py 192.168.1.1 -s 1 -e 65535 -t 0.5 -w 200
```

**Interactive mode (no command-line arguments):**
```bash
python multi_thread_port_scanner.py
```

## Output Example

```
==============================================================
PORT SCANNER
==============================================================
Target        : google.com
Resolved IP   : 142.250.185.46
Port range    : 1 - 1024 (1024 ports)
Threads       : 100
Timeout       : 1.00 seconds
Start time    : 2026-06-30 10:15:23
==============================================================

Scanning ports: 100%|████████████████| 1024/1024 [00:12<00:00, 85.33port/s]

------------------------------------------------------------
Scan completed in 12.04 seconds
Open ports   : 3 / 1024
Closed ports : 1021 / 1024
------------------------------------------------------------

Detailed open ports:
  - Port 80 (http) is open
  - Port 443 (https) is open
  - Port 8080 (http-alt) is open
```

## Performance Tips

1. **Adjust Thread Count** - More threads = faster scanning (but more system load)
   - Default (100) is good for most cases
   - Increase to 200-300 for faster scanning
   - Decrease for systems with limited resources

2. **Adjust Timeout** - Lower timeout = faster scanning (but may miss slow services)
   - Default (1 second) is balanced
   - Use 0.5 seconds for quick scans
   - Use 2-3 seconds for unreliable networks

3. **Port Range** - Scanning fewer ports is faster
   - Common ports (1-1024) - ~10 seconds
   - All ports (1-65535) - ~10+ minutes depending on settings

## Port Status Definitions

- **Open** - The port is accepting connections and a service is listening
- **Closed** - The port is not accepting connections (connection refused)

## Common Port Numbers

| Port | Service |
|------|---------|
| 21 | FTP |
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 3389 | Remote Desktop |
| 6379 | Redis |

## Supported Services (Fallback List)

The scanner includes a built-in list of ~25 common services including FTP, SSH, SMTP, DNS, HTTP, HTTPS, MySQL, PostgreSQL, Redis, VNC, and more.

## Limitations

- TCP only (no UDP scanning)
- Requires network connectivity to the target
- Some firewalls may block or rate-limit scanning
- Scanning without permission may be illegal - always get authorization first

## Error Handling

- **Host resolution errors** - Invalid domain names will show an error message
- **Connection errors** - Network errors are caught and reported per-port
- **Keyboard interrupt** - Press `Ctrl+C` to stop the scan gracefully

## System Requirements

- **RAM** - 50-100 MB
- **Network bandwidth** - Depends on timeout and thread settings
- **Permissions** - May need elevated privileges on some systems for certain ports

## License

This project is provided as-is for educational and authorized testing purposes.

## Warning

Port scanning without authorization is illegal in many jurisdictions. Always:
- Get explicit written permission before scanning any network or host
- Use only on systems you own or have authorization to test
- Understand local laws regarding network scanning

## Troubleshooting

**Q: "Unable to resolve host" error**
- Check your internet connection
- Verify the hostname or IP address is correct

**Q: Scan is too slow**
- Increase the number of workers (`-w` flag)
- Decrease the timeout (`-t` flag)
- Scan a smaller port range

**Q: Few open ports detected**
- Some hosts may have a firewall blocking scans
- Increase the timeout to allow slow services to respond
- Try scanning specific known ports

**Q: ModuleNotFoundError: No module named 'tqdm'**
- Install tqdm: `pip install tqdm`

## Contributing

Feel free to modify and improve the scanner for your needs.
