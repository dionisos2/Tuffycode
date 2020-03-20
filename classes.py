class Video:
    """Video class."""
    def __init__(self, numId, size):
        self.numId = numId
        self.size = size
        self.requests = {}

    def add_request(self, endpoint_id, nbr):
        self.requests[endpoint_id] = nbr

    def __repr__(self):
        return "Video({numId},{size})".format(numId=self.numId,size=self.size)

class EndPoint:
    """EndPoint e.g. neighborhood."""
    def __init__(self, numId, data_center_latency):
        self.numId = numId
        self.data_center_latency = data_center_latency
        self.cache_latency = {}

    def add_cache(self, cache_id, latency):
        self.cache_latency[cache_id] = latency


class Request:
    """Video request."""
    def __init__(self):
        pass


class Cache:
    def __init__ (self, numId, size):
        self.numId = numId
        self.size = size
        self.videosDict = set()
        
    def _add_video(self, video):
        self.videosDict[video.numId] = video



