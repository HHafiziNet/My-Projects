import requests
import argparse
import time

def directory_discovery(url : str, wordlist : list, delay: float = 0) -> list:
    discovered_directories = []
    print(f"Discovering directories for {url}...")
    for word in wordlist:
        try:
            res = requests.get(f"{url}/{word}", timeout=10)
            if res.status_code == 200:
                discovered_directories.append(word)
        except requests.RequestException as e:
            print(f"[!] Request failed for {url}/{word}: {e}")
            continue
        if delay > 0:
            time.sleep(delay)
    return discovered_directories


def parser():
    try : 
        parser = argparse.ArgumentParser(description="Directory Discovery Tool", epilog="Example usage: python3 dir_discovery.py -u http://example.com -w wordlist.txt")
        parser.add_argument("-u", "--url", nargs='?', required=True, help="Target URL")
        parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
        parser.add_argument("-o", "--output", help="Output file to save discovered directories")
        parser.add_argument("-d", "--delay", type=float, default=0, help="Delay between requests in seconds (default: 0)")
        return parser.parse_args()
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        return None

def main():
    print('=' * 36)
    print('|' + ' ' * 34 + '|')
    print('|' + ' DIRECTORY DISCOVERY TOOL '.center(34) + '|')
    print('|' + ' ' * 34 + '|')
    print('=' * 36)
   
    args = parser()
    if not args:
        return
    url = args.url
    wordlist_path = args.wordlist
    output_file = args.output
    delay = args.delay
    try:
        with open(wordlist_path, 'r') as f:
            wordlist = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Wordlist file '{wordlist_path}' not found.")
        return

    try:
        discovered_directories = directory_discovery(url, wordlist, delay)
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
        return

    if output_file:
        with open(output_file, 'w') as file:
            for directory in discovered_directories:
                file.write(f"{directory}\n")
        print(f"Discovered directories saved to '{output_file}'.")

    print("Discovered Directories:")
    for directory in discovered_directories:
        print(directory)

if __name__ == "__main__":
    main()
