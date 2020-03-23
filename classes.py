class Video:
    """Video class."""
    def __init__(self, num_id, size=1):
        self.num_id = num_id
        self.size = size

    def set_size(self, size):
        self.size = size

    def __repr__(self):
        return "Video({num_id},{size})".format(num_id=self.num_id, size=self.size)

    def __lt__(self,vid2):
        if type(vid2)==Video:
            return self.num_id < vid2.num_id


class EndPoint:
    """EndPoint e.g. neighborhood."""
    def __init__(self, num_id, dc_latency):
        self.num_id = num_id
        self.dc_latency = dc_latency
        self.caches_latency = dict()

    def get_connected_caches_id(self):
        return list(self.caches_latency.keys())

    def add_cache_latency(self, cache_id, latency):
        self.caches_latency[cache_id] = latency

    def get_cache_latency(self, cache_id):
        return self.caches_latency[cache_id]

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
        self.videos = set() # or dict(). L'inconvenient de set sera si l'on souhaite modifier un cache pour le retrouver.

    def add_video(self, video):
        self.videos.add(video)
#        # si videos est dict()
#        self.videos[video.num_id] = video

    def __repr__(self):
        return f"Cache({self.num_id}, {self.videos})"


class Solution:
    """Sets of caches (and their configuration)."""
    def __init__(self):
        self.caches = dict() # or set(). Dict() permet surtout d'avoir indexation.

    def add_cache(self, cache):
        self.caches[cache.num_id] = cache

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
        self._requests = set()
        self._endpoints_of_cache = dict()

    """ Return the endpoints connected to the cache identified by id_cache"""
    def get_endpoints_of_cache(self, id_cache):
        if len(self._endpoints_of_cache) == 0:
            self._create_cache_to_endpoints_link()

        return self._endpoints_of_cache[id_cache]

    """Create a dict assotiating each cache to their connected endpoints"""
    def _create_cache_to_endpoints_link(self):
        if len(self._endpoints_of_cache) > 0:
            raise RuntimeError("create_cache_to_endpoints_link should be call only one time")

        for endpoint in self.endpoints:
            connected_caches_id = endpoint.get_connected_caches_id()
            for id_cache in connected_caches_id:
                if id_cache in self._endpoints_of_cache:
                    self._endpoints_of_cache[id_cache].append(endpoint.num_id)
                else:
                    self._endpoints_of_cache[id_cache] = [endpoint.num_id]


    @property
    def caches_id(self):
        """Subset of caches linked to endpoints."""
        # a priori un set proche de range(self._infos['C']) sauf s'il y a des caches isoles
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
    # Expand infos into attributes
    @property
    def nb_videos(self):
        return self._infos["V"]
    @property
    def nb_endpoints(self):
        return self._infos["E"]
    @property
    def nb_requests(self):
        return self._infos["R"]
    @property
    def nb_caches(self):
        return self._infos["C"]
    @property
    def caches_size(self):
        return self._infos["X"]

    # Videos
    @property
    def videos(self):
        return self._videos
    @videos.setter
    def videos(self, videos):
        self._videos = videos
    def set_videos(self, videos):
        self._videos = videos

    def get_video(self, video_id):
        return self._videos[video_id]

    # Endpoints
    @property
    def endpoints(self):
        return self._endpoints
    @endpoints.setter
    def endpoints(self, endpoints):
        self._endpoints = endpoints
    def set_endpoints(self, endpoints):
        self._endpoints = endpoints

    def get_endpoint(self, endpoint_id):
        return self._endpoints[endpoint_id]

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
