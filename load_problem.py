from classes import *
    #dio : lord il faut que tu mettes tous ça dans les objets classes associés.
    # et par contre n’hésite pas à dire si il y a un problème.

# Generic function
def line_to_int_list(line):
    """Read file line into a list of int."""
    return list(map(lambda x:int(x), line.split()))

## == LOAD VIDEOS ==

def load_videos(file_line):
    """ Return list of Video objects (numId, sz)"""
    return list(map(lambda tup:Video(tup[0],tup[1]), enumerate(line_to_int_list(file_line))))

# Test load_videos
do_test_load_videos = False
if do_test_load_videos:
    file_line = "50   50   80   30   110"
    vid_list = load_videos(file_line)
    print(vid_list)


## == LOAD ENDPOINT ==

def load_endpoint(file,num_endpoint):
    """Return Endpoint object"""
    # Create endpoint with data_center_latency
    first_line = file.readline()
    dc_lat, n_cache = line_to_int_list(first_line)
    endpoint = EndPoint(num_endpoint,dc_lat)
    # Add all linked caches, add latency
    for _ in range(n_cache):
        cur_line = file.readline()
        cache_id, latency = line_to_int_list(cur_line)
        endpoint.add_cache_latency(cache_id,latency)
    return endpoint

# Test load_endpoint
do_test_load_endpoint = False
if do_test_load_endpoint:
    file_name = "test_load_endpoint.txt"
    with open(file_name, "r+") as file:
        # First endpoint
        endpoint = load_endpoint(file,1)
        print(endpoint)
        # 2nd endpoint
        endpoint2 = load_endpoint(file,2)
        print(endpoint2)


## == LOAD REQUEST ==

def load_request(file_line):
    """Return Request object"""
    vid_id,ep_id,nb_request = line_to_int_list(file_line)
    return Request(vid_id,ep_id,nb_request)

# Test load_request
do_test_load_request = False
if do_test_load_request: 
    file_line = "3   0   1500 "
    request = load_request(file_line)
    print(request)


## == LOAD PROBLEM ==

def load_problem(problem,problem_path):
    """Load a problem file."""
    # Generic parameters
    # V: nbr of videos
    # E: nbr of endpoints
    # R: nbr of requests
    # C: nbr of cache
    # X: size of cache
    var = ["V","E","R","C","X"]
    
    with open(problem_path, "r+") as f:
        datas = f.readline()
        # First line: problem description/inputs
        datas = list(map(lambda x:int(x), datas.split()))
        problem.infos = {var[i] : datas[i] for i in range(len(var))}
        # Second line: videos (sizes)
        videos_list = load_videos(f.readline())
        problem.videos = videos_list
        # Next lines: endpoints (latency of DC and cache)
        endpoints_list = []
        for iE in range(problem.infos["E"]):
            endpoints_list.append(load_endpoint(f,iE))
        problem.endpoints = endpoints_list
        # Next lines: requests
        requests_list = []
        for _ in range(problem.infos["R"]):
            requests_list.append(load_request(f.readline()))
        problem.requests = requests_list

#    caches = [Cache(1)]
#    endpoints = [EndPoint(1)]
#    videos = [Video(1)]
#    return (videos_list, endpoints_list, requests_list) #self.inputs, 

#do_test_load_problem = False
#if do_test_load_problem:
#    problem = Problem()
#    print(problem)
#    problem_path = "test_load_problem"
#    load_problem(problem,problem_path)
#    print(problem)
    
