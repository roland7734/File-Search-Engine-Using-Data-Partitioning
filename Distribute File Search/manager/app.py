import socket
import multiprocessing

WORKERS = [
    ("127.0.0.1", 5001),
    ("127.0.0.1", 5002)
]

def worker_process(task_queue, result_queue):
    while True:
        task = task_queue.get()
        if task is None:
            break

        ip, port, query = task
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

                results = data.decode().splitlines()
                result_queue.put(results)

        except socket.timeout:
            print(f"Timeout: Worker {ip}:{port} did not respond in time.")
            result_queue.put([])
        except ConnectionRefusedError:
            print(f"Error: Cannot connect to worker {ip}:{port}. Is it running?")
            result_queue.put([])
        except Exception as e:
            print(f"Unexpected error with worker {ip}:{port}: {e}")
            result_queue.put([])

def main():
    print("Distributed File Search Engine")

    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    processes = []
    for _ in WORKERS:
        p = multiprocessing.Process(target=worker_process, args=(task_queue, result_queue))
        p.start()
        processes.append(p)

    while True:
        query = input("Enter the query to search (or 'exit' to quit): ").strip()

        if query.lower() == "exit":
            print("Exiting search engine.")
            break
        elif not query:
            print("Query cannot be empty. Please enter a valid search term.")
            continue

        for ip, port in WORKERS:
            task_queue.put((ip, port, query))

        all_results = []

        for _ in WORKERS:
            result = result_queue.get()
            all_results.extend(result)

        print("\nSearch Results:")
        if all_results:
            for result in all_results:
                print(result)
        else:
            print("No results found.")

        print("\n")


    for _ in processes:
        task_queue.put(None)
    for p in processes:
        p.join()

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    main()
