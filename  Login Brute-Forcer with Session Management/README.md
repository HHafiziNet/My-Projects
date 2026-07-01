# Login Brute-Forcer with Session Management

A Python-based credential brute-forcing tool that uses a persistent session to handle cookies and authentication flows. Designed for testing login forms that do **not** require CSRF tokens.

## Features

- Supports both single credentials and file-based wordlists for usernames and passwords.
- Uses `requests.Session()` for automatic cookie handling and session persistence.
- Configurable delay between requests to avoid rate-limiting or account lockout.
- Saves successfully discovered credentials to an output file.
- Robust error handling for network issues, file I/O, and user interruptions.
- Clean console output with a simple ASCII banner.

## Project Structure
```
Login_Brute-Forcer_with_Session_Management.py   # single-file brute-force tool
README.md
```

## Dependencies

| Dependency | Type | Installation Command |
| :--- | :--- | :--- |
| Python 3.6+ | Runtime | N/A |
| `requests` | External Library | `pip install requests` |

*All other modules (`argparse`, `os`, `time`) are part of Python's standard library.*

## How It Works

### Session Management
1. A `requests.Session()` object is created to persist cookies across requests.
2. The session automatically handles any cookies set by the server (e.g., session IDs).

### Brute-Force Attack
1. The tool iterates through each password (outer loop) and each username (inner loop).
2. For each combination, it constructs a payload containing `username` and `password`.
3. It sends a `POST` request to the target URL using the persistent session.
4. If the server responds with an **HTTP 302 redirect**, the credentials are considered valid and saved.
5. A configurable delay is applied between requests to avoid detection.

### Output
- Found credentials are printed to the console in `username:password` format.
- If `--output` is specified, they are also saved to a file (one per line).

## Usage

### Install the required dependency
```bash
pip install requests
```

### Basic scan with single username and password list
```bash
python "Login_Brute-Forcer_with_Session_Management.py" -t http://example.com/login -u admin -p passwords.txt
```

### Scan with username and password wordlists
```bash
python "Login_Brute-Forcer_with_Session_Management.py" -t http://example.com/login -u usernames.txt -p passwords.txt
```

### Scan with delay to avoid rate limiting
```bash
python "Login_Brute-Forcer_with_Session_Management.py" -t http://example.com/login -u usernames.txt -p passwords.txt -d 0.5
```

### Save found credentials to a file
```bash
python "Login_Brute-Forcer_with_Session_Management.py" -t http://example.com/login -u admin -p passwords.txt -o found.txt
```

### Command-Line Arguments

| Argument | Short | Required | Description |
| :--- | :--- | :--- | :--- |
| `--target` | `-t` | **Yes** | Target login URL (e.g., `http://example.com/login`). |
| `--username` | `-u` | No | Single username or path to username wordlist file. |
| `--password` | `-p` | No | Single password or path to password wordlist file. |
| `--delay` | `-d` | No | Delay in seconds between requests (default: `0`). |
| `--output` | `-o` | No | File to save discovered credentials (`username:password` format). |

### Example Output Instance
```
====================================
|                                  |
|   FORM SUBMITTER TOOL            |
|                                  |
====================================
Submitting form data to example/login.com...
Found valid credentials: admin:password123
Found valid credentials: admin:letmein
Found valid credentials: root:toor
Results saved to found.txt
```

**Contents of `found.txt` (saved output):**
```
admin:password123
admin:letmein
root:toor
```

## Notes

* The tool detects successful logins by checking for an **HTTP 302 redirect**. This assumes the application redirects users after a successful authentication.
* A `requests.Session()` is used to maintain cookies and session state across requests.
* Both `-u` and `-p` accept either a single value or a file path. If a file path is provided, the tool reads one entry per line.
* If no credentials are found, the tool exits silently (no output printed).
* The tool prints error messages for network failures (timeouts, connection errors) and continues the scan.

## Limitations

* **No CSRF Handling:** This version does **not** extract or submit CSRF tokens. 
* **Success Detection:** Only detects `302` redirects. 
* **No Multi-Threading:** The scan is single-threaded and can be slow for large wordlists.
* **No TLS Verification Bypass:** Does not bypass self-signed or invalid SSL certificates (add `verify=False` to `requests` calls for testing).
* **No Authentication Headers:** Does not support Bearer tokens, API keys, or custom authentication headers beyond the POST payload.
* **Empty Credentials Warning:** If you run the tool without providing a username or password, it will exit silently without warning. Ensure you provide at least one of each.
* **Argparse Error Handling:** On invalid arguments, the script prints argparse's error and an additional "Unexpected error" message due to the broad exception catch. This is cosmetic and does not affect functionality.

## Learning Goals

* Understanding HTTP form submission and session handling in Python.
* Using `requests.Session()` to persist cookies and manage sessions.
* Implementing a basic brute-force attack pattern with nested loops.
* Using `argparse` to build a flexible command-line interface.
* Handling file I/O for wordlists and output.
* Implementing robust error handling for network, file, and user interruptions.
* Understanding the difference between CSRF-protected and unprotected forms.

## Disclaimer

⚠️ **This tool is for educational purposes and authorized security testing only.**  
Unauthorized use of this tool against websites, applications, or systems without explicit written permission from the owner is illegal and violates computer fraud and abuse laws (e.g., CFAA in the US, Computer Misuse Act in the UK). The developer assumes **zero liability** for any misuse or damage caused by this script. Use responsibly and only in isolated lab environments, CTF competitions, or on systems you own.

## License

Educational use only. No warranty. Provided "as is" without any guarantees.