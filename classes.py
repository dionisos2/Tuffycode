class Cache:
    def __init__ (self, size):
        self.size = size
        self.videos = set()



class EndPoint:
    def __init__ (self, data_center_latency):
        self.data_center_latency = data_center_latency
        self.cache_latency = {}

    def add_cache(self, cache_id, latency):
        self.cache_latency[cache_id] = latency


class Video:
    def __init__ (self, size):
        self.size = size
        self.requests = {}

    def add_request(self, endpoint_id, nbr):
        self.requests[endpoint_id] = nbr
