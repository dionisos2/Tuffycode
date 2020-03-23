import random
from classes import *


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



class Addition:
    def __init__(self, id_video, id_cache):
        self.couple_id = (id_video, id_cache)
        self.id_video = id_video
        self.id_cache = id_cache
        self.score = None

    def __repr__(self):
        return f"Addition({self.id_video}, {self.id_cache}, {self.score})"


def create_solution(problem):
    solution = Solution()
    possible_additions = create_possible_additions(problem, solution)
    links_to_additions = create_links_to_additions(problem)

    while len(possible_additions) > 0:
        best_addition = get_best_additions(problem, possible_additions)
        add_video(problem, solution, best_addition)
        additions_to_remove = get_additions_to_remove(problem, solution, possible_additions, best_addition)
        recalculate_score(problem, solution, possible_additions, links_to_additions, best_addition)

        for id_addition in additions_to_remove:
            del possible_additions[id_addition]
        if best_addition.num_id in possible_additions:
            del possible_additions[best_addition.num_id]

    return solution

"""Create a dict of all possibles additions"""
# Initiate and compute additions' score.
def create_possible_additions(problem, solution):
    possible_additions = dict()

    for video in problem.videos:
        id_video = video.num_id
        for id_cache in problem.caches_id:
            addition = Addition(id_video, id_cache)
            addition.score = get_video_score(problem, solution, id_video, id_cache)
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

"""Get the score of a video for a particular cache"""
def get_video_score(problem, solution, id_video, id_cache):
    video = problem.videos[id_video]
    score = 0

    for endpoint_id in problem.get_endpoints_of_cache(id_cache):
        endpoint = problem.endpoints[endpoint_id]
        possible_latencies = [endpoint.dc_latency]

        for cache in solution.caches:
            if video in cache.videos:
                possible_latencies.append(problem.caches_latency[id_cache])

        best_latency = min(possible_latencies)
        latency_gain = max(0, best_latency - endpoint.caches_latency[id_cache])

        for request in problem.requests:
            if request.video.num_id == id_video and request.endpoint.num_id == endpoint_id:
                score += latency_gain * request.nb_request

    return score


"""Return the current best possible additions (max of score/size)"""
def get_best_additions(problem, possible_additions):

    def value_of_addition(addition):
        size = problem.videos[addition.id_video].size
        return addition.score/size

    best_addition = max(possible_additions.values(), key=value_of_addition)

    return best_addition


"""Add a video to the correct cache of the solution"""
def add_video(problem, solution, best_addition):
    id_video = best_addition.id_video
    video = problem.videos[id_video]
    id_cache = best_addition.id_cache

    if id_cache in solution.caches:
        solution.caches[id_cache].add_video(video)
    else:
        cache = Cache(id_cache)
        cache.add_video(video)
        solution.caches[id_cache] = cache

""" recalculate the score of all possible additions that require modification"""
def recalculate_score(problem, solution, possible_additions, links_to_additions, best_addition):
    additions_to_change = links_to_additions[best_addition.id_video][best_addition.id_cache]

    for addition_id in additions_to_change:
        (id_video, id_cache) = addition_id
        possible_additions[addition_id].score = get_video_score(problem, solution, id_video, id_cache)

""" Get a list of the id of all the additions to remove (for which the video would surcharge the size of the cache) """
def get_additions_to_remove(problem, solution, possible_additions, best_addition):
    addition_to_remove = []
    max_size = problem.caches_size

    for addition_id in possible_additions.keys():
        id_video, id_cache = addition_id
        video_size = problem.videos[id_video].size
        current_size = sum(video.size for video in solution.caches[id_cache].videos)
        if current_size + video_size > max_size:
            addition_to_remove.append(addition_id)

    return addition_to_remove
