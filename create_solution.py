import random
from classes import *

# %% Random solution

def create_random_solution(problem):
    solution = Solution()

    for cache_id in problem.caches_id:
        cache = Cache(cache_id)
        video = random.choice(problem.videos)
        current_size = video.size
        while current_size < problem.caches_size:
            cache.add_video(video)
            video = random.choice(problem.videos)
            current_size += video.size
        solution.set_cache(cache)
        
    # Overwrite potentiel existing solution
    problem.set_solution(solution)

    return solution


# %% Optimized solution

class Copystore:
    def __init__(self, video_id, cache_id):
        self.couple_id = (video_id, cache_id)
        self.video_id = video_id
        self.cache_id = cache_id
        self.score = None

    def __repr__(self):
        return f"Copystore({self.video_id}, {self.cache_id}, {self.score})"


def create_solution(problem):
    if problem.solution == None:
        solution = Solution()
    
        for cache_id in range(problem.nb_caches):
            solution.set_cache(Cache(cache_id))
    else:
        solution = problem.solution

    possible_copystores = create_possible_copystores(problem, solution)
    links_to_copystores = create_links_to_copystores(problem)

    while len(possible_copystores) > 0:
        best_copystore = get_best_copystores(problem, possible_copystores)
        solution.set_copystore(problem, best_copystore)
        copystores_to_remove = get_copystores_to_remove(problem, solution, possible_copystores, best_copystore)
        recalculate_score(problem, solution, possible_copystores, links_to_copystores, best_copystore)

        for copystore_id in copystores_to_remove:
            del possible_copystores[copystore_id]

        if best_copystore.couple_id in possible_copystores:
            del possible_copystores[best_copystore.couple_id]

    return solution

# %% Prepare struture for copystores manipulation

"""Create a dict of all possibles copystores"""
# Initiate and compute copystores' score.
def create_possible_copystores(problem, solution):
    possible_copystores = dict()

    for video in problem.videos:
        video_id = video.num_id
        for cache_id in problem.caches_id:
            copystore = Copystore(video_id, cache_id)
            copystore.score = get_video_score(problem, solution, video_id, cache_id)
            possible_copystores[copystore.couple_id] = copystore
    return possible_copystores


"""Create a dict of dict, allowing to get all copystores we should modify for a particular video and a particular cache.
Double dict indexed by a video and a cache (i.e. an copystore).
Each value is a set of caches that are linked to this cache.
"""
def create_links_to_copystores(problem):
    # Dans cette construction, les caches lies ne sont pas video-dependant.

    linked_caches = dict()
    for current_cache_id in problem.caches_id:
        connected_caches_id = set()

        # current_cache (1) -> linked_endpoints (n) -> linked_caches(m>n)
        connected_endpoints = problem.get_endpoints_of_cache(current_cache_id)
        for endpoint_id in connected_endpoints:
            new_caches_id = problem.get_endpoint(endpoint_id).get_connected_caches_id()
            connected_caches_id = connected_caches_id.union(new_caches_id)

        linked_caches[current_cache_id] = connected_caches_id

    result = dict()
    for video in problem.videos:
        result[video.num_id] = dict()
        for current_cache_id in problem.caches_id:
            current_copystore_id = (video.num_id, current_cache_id)

            connected_caches_id = linked_caches[current_cache_id]
            connected_copystores_id = [(video.num_id, cache_id) for cache_id in connected_caches_id]
            result[current_copystore_id] = connected_copystores_id

    return result

# %% Score functions

# Eventuellement a mettre en methode de Copystore
def get_video_score(problem, solution, video_id, cache_id):
    """Get the score of a video for a particular cache."""
    score = 0
    for request in problem.get_requests_of_video(video_id):
        if cache_id in request.endpoint.caches_latency:
            cache_latency = request.endpoint.get_cache_latency(cache_id)
            latency_gain = max(0,request.best_latency-cache_latency)
            score += latency_gain * request.nb_request
    
    return score

# %% Optimization iteration functions

"""Return the current best possible copystores (max of score/size)"""
def get_best_copystores(problem, possible_copystores):

    def value_of_copystore(copystore):
        size = problem.videos[copystore.video_id].size
        return copystore.score/size

    best_copystore = max(possible_copystores.values(), key=value_of_copystore)

    return best_copystore

""" recalculate the score of all possible copystores that require modification"""
def recalculate_score(problem, solution, possible_copystores, links_to_copystores, best_copystore):
    copystores_to_change = links_to_copystores[best_copystore.couple_id]

    for copystore_id in copystores_to_change:
        (video_id, cache_id) = copystore_id
        if copystore_id in possible_copystores:
            possible_copystores[copystore_id].score = get_video_score(problem, solution, video_id, cache_id)

""" Get a list of the id of all the copystores to remove (for which the video would surcharge the size of the cache) """
def get_copystores_to_remove(problem, solution, possible_copystores, best_copystore):
    copystore_to_remove = []
    max_size = problem.caches_size

    for copystore_id in possible_copystores.keys():
        video_id, cache_id = copystore_id
        video_size = problem.videos[video_id].size
        current_size = sum(video.size for video in solution.caches[cache_id].videos)
        if current_size + video_size > max_size:
            copystore_to_remove.append(copystore_id)

    return copystore_to_remove
