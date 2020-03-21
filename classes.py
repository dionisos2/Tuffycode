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
    def __init__(self, video, endpoint, nb_request):
        self.video = video
        self.endpoint = endpoint
        self.nb_request = nb_request

    def __repr__(self):
        return "Request({video},{endpoint},{nb_request})".format(video=self.video,
                                                               endpoint=self.endpoint,
                                                               nb_request=self.nb_request)


class Cache:
    def __init__(self, num_id):
        self.num_id = num_id
        self.videos = set()

    def __repr__(self):
        return f"Cache({self.num_id}, {self.videos})"


class Solution:
    def __init__(self):
        self.caches = dict()

    def __str__(self):
        string = "---Solution---\n"
        string += f"Caches: {self.caches}"
        return string


class Problem:
    def __init__(self):
        self.result_path = None
        self._infos = None
        self._videos = list()
        self._endpoints = list()
        self._requests = list()

    @property
    def caches_id(self):
        result = set()
        for endpoint in self.endpoints:
            result = result.union(endpoint.caches_latency.keys())
        return result

    # Infos
    @property
    def infos(self):
        return self._infos
    @infos.setter
    def infos(self, infos):
        self._infos = infos
    def set_infos(self, infos):
        self._infos = infos

    # Videos
    @property
    def videos(self):
        return self._videos
    @videos.setter
    def videos(self, videos):
        self._videos = videos
    def set_videos(self, videos):
        self._videos = videos

    # Endpoints
    @property
    def endpoints(self):
        return self._endpoints
    @endpoints.setter
    def endpoints(self, endpoints):
        self._endpoints = endpoints
    def set_endpoints(self, endpoints):
        self._endpoints = endpoints

    # Requests
    @property
    def requests(self):
        return self._requests
    @requests.setter
    def requests(self, requests):
        self._requests = requests
    def set_requests(self, requests):
        self._requests = requests


    def __str__(self):
        result_path = "Result path: " + str(self.result_path) + "\n"
        str_infos = "Infos: " + str(self.infos) + "\n"
        str_vid = "Videos: " + str(self.videos) + "\n"
        str_endpoints = "EndPoints: " + str(self.endpoints) + "\n"
        str_requests = "Requests: " + str(self.requests) + "\n"
        str_all = result_path + str_infos + str_vid + str_endpoints + str_requests
        return str_all
