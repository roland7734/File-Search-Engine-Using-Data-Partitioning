import socket
import sys

from shared.search import search_files

def start_worker(port, directory):
    """
    Starts a worker that listens for queries and searches in the given directory.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)

    print(f"Worker listening on port {port} and searching in '{directory}'")

    while True:
        client_socket, _ = server_socket.accept()
        query = client_socket.recv(1024).decode().strip()

        if query:
            print(f"Worker {port} received query: {query}")
            results = search_files(directory, query)
            response = '\n'.join(results) if results else "No results found."
            client_socket.sendall(response.encode())

        client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: worker.py <port> <directory>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        directory = sys.argv[2]
        start_worker(port, directory)
    except ValueError:
        print("Error: Port number must be an integer.")
        sys.exit(1)
