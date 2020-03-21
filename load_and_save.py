from classes import *

# Generic function
def line_to_int_list(line):
    """Read file line into a list of int."""
    return list(map(lambda x:int(x), line.split()))

## == LOAD VIDEOS ==

def load_videos(file_line):
    """ Return list of Video objects (numId, sz)"""
    return list(map(lambda tup:Video(tup[0],tup[1]), enumerate(line_to_int_list(file_line))))

def test_load_videos():
    do_test_load_videos = False
    if do_test_load_videos:
        file_line = "50   50   80   30   110"
        vid_list = load_videos(file_line)
        print(vid_list)

## == LOAD ENDPOINT ==

def load_endpoint(problem_file, num_endpoint):
    """Return Endpoint object"""
    # Create endpoint with data_center_latency
    first_line = problem_file.readline()
    dc_lat, n_cache = line_to_int_list(first_line)
    endpoint = EndPoint(num_endpoint,dc_lat)
    # Add all linked caches, add latency
    for _ in range(n_cache):
        cur_line = problem_file.readline()
        cache_id, latency = line_to_int_list(cur_line)
        endpoint.add_cache_latency(cache_id,latency)
    return endpoint

def test_load_endpoint():
    do_test_load_endpoint = False
    if do_test_load_endpoint:
        file_name = "input/example.txt"
        with open(file_name, "r") as problem_file:
            # First endpoint
            endpoint = load_endpoint(problem_file,1)
            print(endpoint)
            # 2nd endpoint
            endpoint2 = load_endpoint(problem_file,2)
            print(endpoint2)


## == LOAD REQUEST ==

def load_request(file_line):
    """Return Request object"""
    vid_id,ep_id,nb_request = line_to_int_list(file_line)
    return Request(vid_id,ep_id,nb_request)

def test_load_request():
    do_test_load_request = False
    if do_test_load_request:
        file_line = "3   0   1500 "
        request = load_request(file_line)
        print(request)


## == LOAD PROBLEM ==

def load_problem(problem_path):
    """Load a problem file."""

    problem = Problem()

    # Generic parameters
    # V: nbr of videos
    # E: nbr of endpoints
    # R: nbr of requests
    # C: nbr of cache
    # X: size of cache
    var = ["V", "E", "R", "C", "X"]

    with open(problem_path, "r") as problem_file:
        datas = problem_file.readline()
        # First line: problem description/inputs
        datas = list(map(int, datas.split()))
        problem.set_infos({var[i] : datas[i] for i in range(len(var))})
        # Second line: videos (sizes)
        videos_list = load_videos(problem_file.readline())
        problem.set_videos(videos_list)
        # Next lines: endpoints (latency of DC and cache)
        endpoints_list = []
        for iE in range(problem.infos["E"]):
            endpoints_list.append(load_endpoint(problem_file, iE))
        problem.set_endpoints(endpoints_list)
        # Next lines: requests
        requests_list = []
        for _ in range(problem.infos["R"]):
            requests_list.append(load_request(problem_file.readline()))
        problem.set_requests(requests_list)


    return problem


def save_solution(solution, file_path):
    caches = sorted(solution.caches.values(), key=lambda cache:cache.num_id)
    with open(file_path, "w") as solution_file:
        solution_file.write(str(len(caches)) + "\n")
        for cache in caches:
            line = str(cache.num_id) + " " + " ".join(map(str, sorted(cache.videos_id)))
            solution_file.write(line + "\n")

def load_solution(file_path):
    solution = Solution()
    with open(file_path, "r") as solution_file:
        cache_nbr = int(solution_file.readline())
        for _ in range(cache_nbr):
            # Set each cache configuration (videos to store)
            params = list(map(int, solution_file.readline().split()))
            cache_id = params[0]
            cache = Cache(cache_id)
            for video_id in params[1:]:
                cache.videos_id.add(video_id)

            solution.caches[cache_id] = cache

    return solution
