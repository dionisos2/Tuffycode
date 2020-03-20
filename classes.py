class Video:
    """Video class."""
    def __init__(self, num_id, size=1):
        self.num_id = num_id
        self.size = size
#        self.requests = {}
#
#    def add_request(self, endpoint_id, nbr):
#        self.requests[endpoint_id] = nbr
        
    def set_size(self, size):
        self.size = size
    
    def __repr__(self):
        return "Video({num_id},{size})".format(num_id=self.num_id,size=self.size)


class EndPoint:
    """EndPoint e.g. neighborhood."""
    def __init__(self, num_id, dc_latency):
        self.num_id = num_id
        self.dc_latency = dc_latency
        self.caches_latency = dict()

    def add_cache_latency(self, cache_id, latency):
        self.caches_latency[cache_id] = latency

    def __repr__(self):
        return "EndPoint({num_id},{dc_latency},{c_latency})".format(\
                                                num_id=self.num_id,\
                                                dc_latency=self.dc_latency,\
                                                c_latency=self.caches_latency)


class Request:
    """Video request."""
    def __init__(self):
        pass


class Cache:
    def __init__ (self, num_id, size):
        self.num_id = num_id
        self.size = size
        self.videosDict = set()
        
    def _add_video(self, video):
        self.videosDict[video.num_id] = video



