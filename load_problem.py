from classes import *
    #dio : lord il faut que tu mettes tous ça dans les objets classes associés.
    # et par contre n’hésite pas à dire si il y a un problème.

def line_to_int_list(line):
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
do_test_load_endpoint = True
if do_test_load_endpoint:
    file_name = "test_load_endpoint.txt"
    with open(file_name, "r+") as file:
        # First endpoint
        endpoint = load_endpoint(file,1)
        print(endpoint)
        # 2nd endpoint
        endpoint2 = load_endpoint(file,2)
        print(endpoint2)

## == LOAD PROBLEM ==

def load_problem(problem_path):
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
        self.inputs = {var[i] : datas[i] for i in range(len(var))}
        # Second line: videos (sizes)
        self.videos = load_videos(f.readline())
        # Next lines: endpoints (latency of DC and cache)
        for iE in range(self.inputs["E"]):
            self.endpoints.append(load_endpoint(f,iE))
        # Next lines: 

    caches = [Cache(1)]
    endpoints = [EndPoint(1)]
    videos = [Video(1)]
    return(caches, endpoints, videos)
