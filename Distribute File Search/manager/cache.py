class Cache:
    def __init__(self):
        self.cache = {}

    def exists(self, query):
        return query in self.cache

    def get(self, query):
        return self.cache.get(query, [])

    def store(self, query, results):
        self.cache[query] = results
