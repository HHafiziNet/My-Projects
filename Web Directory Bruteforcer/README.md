


# Directory Discovery Tool (Web Path Brute-Forcer)



## Features

- Single-file implementation – easy to deploy and modify.
- Customizable wordlist support (any text file with one directory name per line).
- Configurable delay between requests to avoid triggering rate-limiting firewalls.
- Saves discovered directories to an output file for later analysis.
- Clean console output with a simple ASCII banner.
- Graceful interruption support (CTRL+C).

## Project Structure
```
Directory brute-forcer.py   # single-file directory discovery tool
README.md
```

## Dependencies

| Dependency | Type | Installation Command |
| :--- | :--- | :--- |
| Python 3.8+ | Runtime | N/A |
| `requests` | External Library | `pip install requests` |

*All other modules (`argparse`, `time`) are part of Python's standard library.*

## How It Works

### Scan Mode
1. The tool reads a wordlist file (one potential directory name per line).
2. For each word, it constructs a full URL: `{target_url}/{word}`.
3. It sends an HTTP `GET` request with a 10-second timeout.
4. If the server responds with an HTTP `200 OK` status, the directory/file is considered discovered and added to the results list.
5. If a `--delay` is set, the tool waits the specified number of seconds between requests.
6. Once scanning finishes, it prints all discovered directories to the console and (optionally) writes them to an output file.

### Output Mode
- Discovered directories are printed to the console by default.
- If `--output` is specified, results are saved to a text file (one directory per line).

## Usage

### Install the required dependency
```bash
pip install requests
```

### Start a scan
```bash
python "Directory brute-forcer.py" -u <TARGET_URL> -w <WORDLIST_PATH> [OPTIONS]
```

### Save output to a file
```bash
python "Directory brute-forcer.py" -u http://example.com -w wordlist.txt -o found.txt
```

### Run with a delay between requests
```bash
python "Directory brute-forcer.py" -u http://example.com -w wordlist.txt -d 0.5
```

### Example Output Instance
```
====================================
|                                  |
|   DIRECTORY DISCOVERY TOOL       |
|                                  |
====================================
Discovering directories for http://192.168.1.100...
[!] Request failed for http://192.168.1.100/phpmyadmin: 404 Client Error: Not Found for url
Discovered directories saved to 'found.txt'.

Discovered Directories:
admin
backup
images
css
secret
robots.txt
```

## Notes

* The tool currently only detects **HTTP 200 OK** responses. Valid directories that return `301`, `302`, or `403` are ignored.
* Requests are sent sequentially (single-threaded) to avoid overwhelming the target server.
* Network timeouts and connection errors are caught and printed without crashing the scan.
* If you interrupt the scan with `CTRL+C`, the tool exits immediately without saving partial results.

## Limitations

* No authentication support (cookies, tokens, or basic auth).
* No encryption or TLS certificate validation beyond what `requests` provides.
* No multi-threading – scanning large wordlists can be slow.
* No User-Agent rotation or IP spoofing – easily blocked by basic WAFs.
* Only checks for `200` status; does not handle redirects or forbidden responses.
* Does not differentiate between files and directories (both are treated the same).

## Safety Warning

Do not use this tool against any website or server without **explicit written permission** from the owner. This tool generates a significant amount of traffic and may:
- Trigger intrusion detection systems (IDS/IPS).
- Get your IP address banned.
- Violate computer fraud and abuse laws (e.g., CFAA in the US, Computer Misuse Act in the UK).

Use responsibly and only in isolated lab environments, CTF competitions, or on systems you own.

## Learning Goals

* Interacting with web servers via the HTTP protocol in Python.
* Using the `requests` library to send GET requests and handle status codes.
* Parsing command-line arguments with `argparse`.
* Basic file I/O (reading wordlists, writing output files).
* Implementing request throttling with `time.sleep()`.
* Handling exceptions and keyboard interrupts gracefully.

⚠️ **Disclaimer:**  
This project is for educational purposes and authorized security testing only. Unauthorized scanning of websites or servers is illegal. You must have explicit permission from the system owner before using this tool.

## License

Educational use only. No warranty. Provided "as is" without any guarantees.