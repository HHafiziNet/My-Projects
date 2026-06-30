
# Remote Command Execution Tool (Client/Server Socket Tool)

A simple Python-based client/server socket program that allows remote command execution over a TCP connection.

⚠️ **Disclaimer:**  
This project is for educational purposes only. Do not expose it to untrusted networks.

## Features

- TCP client/server communication
- Multi-client support using threading
- Command execution on server side
- Timeout handling for socket operations
- Basic line-based protocol (`\n` terminated commands)
- Subprocess-based command execution


## Project Structure
PyCat.py   # single-file implementation (client + server)
README.md



## Dependencies
All the modules used are python built-in modules.

## How It Works

### Server Mode
- Listens on a specified IP and port
- Accepts multiple clients using threads
- Receives commands terminated by `\n`
- Executes commands using `subprocess`
- Sends output back to client

### Client Mode
- Connects to server IP and port
- Sends user input as commands
- Receives and prints responses
- Uses timeout to prevent infinite blocking



## Usage

### Start Server
```bash
python PyCat.py -l -t 0.0.0.0 -p 4444
````

### Start Client

```bash
python PyCat.py -t 127.0.0.1 -p 4444
```

### Run Initial Command (optional)

```bash
python PyCat.py -l -t 0.0.0.0 -p 4444 -c "whoami"
```

---

## Notes

* Commands executed via `subprocess.check_output`
* Communication is line-based (`\n`)
* Each client runs in its own thread
* Output is raw bytes sent over TCP


## Limitations

* No authentication
* No encryption
* Minimal error handling
* Not production safe
* Depends on system shell behavior


## Safety Warning

Do not expose this tool to public or untrusted networks.


## Learning Goals

* Socket programming in Python
* Threaded server architecture
* Basic remote execution model
* Process management with subprocess
* Simple custom TCP protocol design


## License

Educational use only. No warranty.

```
If you want the next level upgrade, I can turn this into a proper repo layout (multiple files, config, logging, clean CLI). Right now it’s a working prototype wearing a README like a cheap suit.
```
