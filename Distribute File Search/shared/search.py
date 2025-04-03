import os

def search_files(directory, query):
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if query.lower() in file.lower():
                results.append(os.path.join(root, file))
    return results
