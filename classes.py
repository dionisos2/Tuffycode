

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
        return f"EndPoint({self.num_id},{self.dc_latency},{self.caches_latency})"


class Request:
    """Video request."""
    def __init__(self, video, endpoint, nb_request):
        self.video = video
        self.endpoint = endpoint
        self.nb_request = nb_request
        # 
        self.best_latency = endpoint.dc_latency

    def __repr__(self):
        return f"Request({self.video},{self.endpoint},{self.nb_request})"


class Cache:
    def __init__(self, num_id):
        self.num_id = num_id
        self.videos = set() # or dict(). L'inconvenient de set sera si l'on souhaite modifier un cache pour le retrouver.

    def add_video(self, video):
        self.videos.add(video)
#        # si videos est dict()
#        self.videos[video.num_id] = video
    
    def get_size(self):
        return sum(video.size for video in self.videos)

    def __repr__(self):
        return f"Cache({self.num_id}, {self.videos})"


class Solution:
    """Dict of caches (and their configuration)."""
    def __init__(self):
        self.caches = dict() # or set(). Dict() permet surtout d'avoir indexation.

    # Set solutions
    def set_cache(self, cache):
        """Directly set cache configuration."""
        self.caches[cache.num_id] = cache
    
    def set_copystore(self, problem, copystore): 
        """Add a video to the correct cache of the solution."""
        video = problem.videos[copystore.video_id]
        cache_id = copystore.cache_id
    
        self.caches[cache_id].add_video(video)
        
        # Update request best latency
        for request in problem.get_requests_of_video(copystore.video_id):
            if cache_id in request.endpoint.caches_latency:
                cache_latency = request.endpoint.caches_latency[cache_id]
                request.best_latency = min(request.best_latency,cache_latency)

    
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
        # Attached solution
        self._solution = None        
        # >> Constructed look-up table <<
        # Between: endpoints <-> cache
        #   | ep -> cache is straightforward
        #   | cache -> ep is not
        self._endpoints_of_caches_link = dict()
        # Between: request <-> endpoints
        #   | req -> ep is straightforward
        #   | ep -> req is not
        self._requests_of_endpoints_link = dict()
        # Between: request <-> videos/caches ?
        self._requests_of_videos_link = dict() # in particular for video scoring ?

    # Links: endpoints <- cache
    def get_endpoints_of_cache(self, cache_id):
        """ Return endPoints connected to the cache identified by cache_id."""
        if len(self._endpoints_of_caches_link) == 0:
            self._create_endpoints_of_caches_link()

        return self._endpoints_of_caches_link[cache_id]

    def _create_endpoints_of_caches_link(self):
        """Create a dictionary associating each cache to their connected endPoints."""
        if len(self._endpoints_of_caches_link) > 0:
            raise RuntimeError("create_endpoints_of_caches_link should be call only one time")

        for endpoint in self.endpoints:
            connected_caches_id = endpoint.get_connected_caches_id()
            for cache_id in connected_caches_id:
                if cache_id in self._endpoints_of_caches_link:
                    self._endpoints_of_caches_link[cache_id].append(endpoint.num_id)
                else:
                    self._endpoints_of_caches_link[cache_id] = [endpoint.num_id]
                                      
    # Links: requests <- endpoint
    def get_requests_of_endpoint(self, endpoint_id):
        """ Return requests called from endpoint identified by endpoint_id."""
        if len(self._requests_of_endpoints_link) == 0:
            self._create_requests_of_endpoints_link()

        return self._requests_of_endpoints_link[endpoint_id]
    
    def _create_requests_of_endpoints_link(self):
        """Create a dictionary associating each endpoint to their connected requests."""
        if len(self._requests_of_endpoints_link) > 0:
            raise RuntimeError("create_requests_of_endpoints_link should be call only one time")
        
        # Peut-etre reprendre le code de _create_endpoints_of_caches_link ?
        request_dict  = dict()
        for iE in range (self._infos["E"]):
            request_dict[iE] = []
        for request in self._requests :
            request_dict[request.endpoint.num_id].append(request)
            
    # Links: requests <- video
    def get_requests_of_video(self, video_id):
        """ Return requests calling video identified by video_id."""
        if len(self._requests_of_videos_link) == 0:
            self._create_requests_of_videos_link()
        
        return self._requests_of_videos_link[video_id]
    
    def _create_requests_of_videos_link(self):
        """Create a dictionary associating each video to their connected requests."""
        if len(self._requests_of_videos_link) > 0:
            raise RuntimeError("create_requests_of_videos_link should be call only one time.")
        
        # Initiate all videos with empty set (some video may not be requested)
        for video in self._videos:
            self._requests_of_videos_link[video.num_id] = set()
        
        for request in self._requests:
            video_id = request.video.num_id
            self._requests_of_videos_link[video_id].add(request)
                

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

    # Solution
    @property
    def solution(self):
        return self._solution
    def set_solution(self, solution):
        self._solution = solution
    

    def __str__(self):
        result_path = "Result path: " + str(self.result_path) + "\n"
        str_infos = "Infos: " + str(self.infos) + "\n"
        str_vid = "Videos: " + str(self.videos) + "\n"
        str_endpoints = "EndPoints: " + str(self.endpoints) + "\n"
        str_requests = "Requests: " + str(self.requests) + "\n"
        str_all = result_path + str_infos + str_vid + str_endpoints + str_requests
        return str_all
