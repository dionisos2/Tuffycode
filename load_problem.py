from classes import *
    #dio : lord il faut que tu mettes tous ça dans les objets classes associés.
    # et par contre n’hésite pas à dire si il y a un problème.


def load_videos(file_line):
    """ Return list of Video objects (numId, sz)"""
    return list(map(lambda tup:Video(tup[0],int(tup[1])), enumerate(file_line.split())))

# Test load_videos
doTest = True
if doTest:
    file_line = "50   50   80   30   110"
    vidList = load_videos(file_line)
    print(vidList)
    

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
            iE

    caches = [Cache(1)]
    endpoints = [EndPoint(1)]
    videos = [Video(1)]
    return(caches, endpoints, videos)
