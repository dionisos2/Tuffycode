class Video:
    """Video class."""
    def __init__(self, num_id, size=1):
        self.num_id = num_id
        self.size = size

    def set_size(self, size):
        self.size = size

    def __repr__(self):
        return "Video({num_id},{size})".format(num_id=self.num_id, size=self.size)


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
    def __init__(self,vid_id,ep_id,nb_request):
        self.vid_id = vid_id
        self.ep_id = ep_id
        self.nb_request = nb_request

    def __repr__(self):
        return "Request({vid_id},{ep_id},{nb_request})".format(vid_id=self.vid_id,
                                                               ep_id=self.ep_id,
                                                               nb_request=self.nb_request)


class Cache:
    def __init__ (self, num_id, size):
        self.num_id = num_id
        self.size = size
        self.videos_dict = set()

    def _add_video(self, video):
        self.videos_dict[video.num_id] = video
