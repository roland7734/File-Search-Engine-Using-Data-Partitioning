import socket
import multiprocessing
import os
from cache import Cache

def send_query(port, query, result_queue):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('localhost', port))
            sock.sendall(query.encode())
            response = sock.recv(1024).decode().strip()
            result_queue.put(response.split('\n') if response else [])
    except socket.timeout:
        print(f"[Timeout] Worker {port} did not respond.")
    except ConnectionRefusedError:
        print(f"[Error] Cannot connect to worker {port}. Is it running?")
    except Exception as e:
        print(f"[Error] Worker {port} encountered error: {e}")
        result_queue.put([])

def rank_results(results):
    return sorted(results, key=lambda path: path.count(os.sep))

def main():
    ports = [5001, 5002]
    cache = Cache()

    while True:
        query = input("Enter search query (or type 'exit' to quit): ").strip()
        if not query:
            continue
        if query.lower() == 'exit':
            break

        if cache.exists(query):
            print("Cache hit.")
            results = cache.get(query)
        else:
            print("Cache miss.")
            print("Sending query to workers...")
            result_queue = multiprocessing.Queue()
            processes = []

            for port in ports:
                p = multiprocessing.Process(target=send_query, args=(port, query, result_queue))
                processes.append(p)
                p.start()

            all_results = []
            for _ in ports:
                all_results.extend(result_queue.get())

            for p in processes:
                p.join()

            combined_results = list(set(all_results))
            results = rank_results(combined_results)
            cache.store(query, results)

        print("\nRanked Results:")
        for path in results:
            print(path)
        print()

if __name__ == "__main__":
    main()
