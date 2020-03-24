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
        solution.add_cache(cache)

    return solution


# %% Optimized solution

class Addition:
    def __init__(self, video_id, cache_id):
        self.couple_id = (video_id, cache_id)
        self.video_id = video_id
        self.cache_id = cache_id
        self.score = None

    def __repr__(self):
        return f"Addition({self.video_id}, {self.cache_id}, {self.score})"


def create_solution(problem):
    solution = Solution()

    for cache_id in range(problem.nb_caches):
        solution.add_cache(Cache(cache_id))

    possible_additions = create_possible_additions(problem, solution)
    links_to_additions = create_links_to_additions(problem)

    while len(possible_additions) > 0:
        best_addition = get_best_additions(problem, possible_additions)
        add_video(problem, solution, best_addition)
        additions_to_remove = get_additions_to_remove(problem, solution, possible_additions, best_addition)
        recalculate_score(problem, solution, possible_additions, links_to_additions, best_addition)

        for addition_id in additions_to_remove:
            del possible_additions[addition_id]

        if best_addition.couple_id in possible_additions:
            del possible_additions[best_addition.couple_id]

    return solution

# %% Prepare struture for additions manipulation

"""Create a dict of all possibles additions"""
# Initiate and compute additions' score.
def create_possible_additions(problem, solution):
    possible_additions = dict()

    for video in problem.videos:
        video_id = video.num_id
        for cache_id in problem.caches_id:
            addition = Addition(video_id, cache_id)
            addition.score = get_video_score(problem, solution, video_id, cache_id)
            possible_additions[addition.couple_id] = addition
    return possible_additions


"""Create a dict of dict, allowing to get all additions we should modify for a particular video and a particular cache.
Double dict indexed by a video and a cache (i.e. an addition).
Each value is a set of caches that are linked to this cache.
"""
def create_links_to_additions(problem):
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
            current_addition_id = (video.num_id, current_cache_id)

            connected_caches_id = linked_caches[current_cache_id]
            connected_additions_id = [(video.num_id, cache_id) for cache_id in connected_caches_id]
            result[current_addition_id] = connected_additions_id

    return result

# %% Score functions

def get_video_score(problem, solution, video_id, cache_id):
    """Get the score of a video for a particular cache."""
    video = problem.videos[video_id]
    score = 0

    for endpoint_id in problem.get_endpoints_of_cache(cache_id):
        endpoint = problem.endpoints[endpoint_id]
        possible_latencies = [endpoint.dc_latency]

        for cache in solution.caches.values():
            if video in cache.videos:
                possible_latencies.append(endpoint.caches_latency[cache_id])

        best_latency = min(possible_latencies)
        latency_gain = max(0, best_latency - endpoint.caches_latency[cache_id])

        for request in problem.get_requests_of_endpoint(endpoint_id):
            if request.video.num_id == video_id:
                score += latency_gain * request.nb_request

    return score

# %% Optimization iteration functions

"""Return the current best possible additions (max of score/size)"""
def get_best_additions(problem, possible_additions):

    def value_of_addition(addition):
        size = problem.videos[addition.video_id].size
        return addition.score/size

    best_addition = max(possible_additions.values(), key=value_of_addition)

    return best_addition


"""Add a video to the correct cache of the solution"""
def add_video(problem, solution, best_addition):
    video_id = best_addition.video_id
    video = problem.videos[video_id]
    cache_id = best_addition.cache_id

    solution.caches[cache_id].add_video(video)

""" recalculate the score of all possible additions that require modification"""
def recalculate_score(problem, solution, possible_additions, links_to_additions, best_addition):
    additions_to_change = links_to_additions[best_addition.couple_id]

    for addition_id in additions_to_change:
        (video_id, cache_id) = addition_id
        if addition_id in possible_additions:
            possible_additions[addition_id].score = get_video_score(problem, solution, video_id, cache_id)

""" Get a list of the id of all the additions to remove (for which the video would surcharge the size of the cache) """
def get_additions_to_remove(problem, solution, possible_additions, best_addition):
    addition_to_remove = []
    max_size = problem.caches_size

    for addition_id in possible_additions.keys():
        video_id, cache_id = addition_id
        video_size = problem.videos[video_id].size
        current_size = sum(video.size for video in solution.caches[cache_id].videos)
        if current_size + video_size > max_size:
            addition_to_remove.append(addition_id)

    return addition_to_remove
