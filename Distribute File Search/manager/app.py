import socket

WORKERS = [
    ("127.0.0.1", 5001),
    ("127.0.0.1", 5002)
]

def fetch_results_from_worker(ip, port, query):
    """
    Sends a search query to a worker and retrieves results.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((ip, int(port)))
            s.sendall(query.encode())

            data = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                data += chunk

            return data.decode().splitlines()

    except socket.timeout:
        print(f"Timeout: Worker {ip}:{port} did not respond in time.")
    except ConnectionRefusedError:
        print(f"Error: Cannot connect to worker {ip}:{port}. Is it running?")
    except Exception as e:
        print(f"Unexpected error with worker {ip}:{port}: {e}")

    return []


def main():
    print("Distributed File Search Engine")

    while True:
        query = input("Enter the query to search (or 'exit' to quit): ").strip()

        if query.lower() == "exit":
            print("Exiting search engine.")
            break
        elif not query:
            print("Query cannot be empty. Please enter a valid search term.")
            continue

        all_results = []

        for worker_ip, worker_port in WORKERS:
            results = fetch_results_from_worker(worker_ip, worker_port, query)
            all_results.extend(results)

        print("\nSearch Results:")
        if all_results:
            for result in all_results:
                print(result)
        else:
            print("No results found.")

        print("\n")


if __name__ == "__main__":
    main()
