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
    possible_additions = create_possible_additions(problem)
    links_to_additions = create_links_to_additions(problem)

    while len(possible_additions) > 0:
        best_addition = get_best_additions(problem, possible_additions)
        add_video(problem, solution, best_addition)
        additions_to_remove = get_additions_to_remove(solution, possible_additions, best_addition)
        recalculate_score(problem, possible_additions, links_to_additions, best_addition)

        for id_addition in additions_to_remove:
            del possible_additions[id_addition]
        if best_addition.num_id in possible_additions:
            del possible_additions[best_addition.num_id]

    return solution

"""Create a dict of all possibles additions"""
def create_possible_additions(problem):
    possible_additions = dict()

    for video in problem.videos:
        video_id = video.num_id
        for cache_id in problem.caches_id:
            addition = Addition(video_id, cache_id)
            addition.score = get_video_score(problem, video_id, cache_id)
            possible_additions[(video_id, cache_id)] = addition
    return possible_additions

"""Create a dict assotiating each cache to their connected endpoints"""
def create_cache_to_endpoints_link(problem):
    cache_to_endpoints = dict()
    for endpoint in problem.endpoints:
        connected_caches_id = endpoint.get_connected_caches_id()
        for cache_id in connected_caches_id:
            if cache_id in cache_to_endpoints:
                cache_to_endpoints[cache_id].append(endpoint.num_id)
            else:
                cache_to_endpoints[cache_id] = [endpoint.num_id]
    return cache_to_endpoints


"""Create a dict of dict, allowing to get all additions we should modify for a particular video and a particular cache"""
def create_links_to_additions(problem):
    result = dict()
    cache_to_endpoints = create_cache_to_endpoints_link(problem)


    for video in problem.videos:
        result[video.num_id] = dict()

        for current_cache_id in problem.caches_id:
            connected_caches_id = set()
            connected_endpoints = cache_to_endpoints[current_cache_id]

            for endpoint_id in connected_endpoints:
                new_caches_id = problem.endpoints[endpoint_id].get_connected_caches_id()
                connected_caches_id = connected_caches_id.union(new_caches_id)

            result[video.num_id][current_cache_id] = []
            for cache_id in connected_caches_id:
                addition_id = (video.num_id, cache_id)
                result[video.num_id][current_cache_id].append(addition_id)

    return result

"""Get the score of a video for a particular cache"""
def get_video_score(problem, video_id, cache_id):
    latency_gain = 0
    nb_request = 0
    endpoints_of_cache = create_cache_to_enpoints_link(problem)[cache_id]
    for endpoint_id in endpoints_of_cache: 
        latency _gain+= problem.endpoints[iendpoint_id].dc_latency[cache_id] - problem.endpoints[iendpoint_id].caches_latency[cache_id]
        for requests in problem.requests: 
            if requests.video.num_id == video_id and requests.endpoint.num_id = endpoint_id: 
                nb_request += problem.requests[id_request].nb_request
    return nb_request*latency_gain

"""Return the current best possible additions (max of score/size)"""
def get_best_additions(problem, possible_additions):

    def value_of_addition(addition):
        size = problem.videos[addition.id_video].size
        return addition.score/size

    best_addition = max(possible_additions.values(), key=value_of_addition)

    return best_addition


"""Add a video to the correct cache of the solution"""
def add_video(problem, solution, best_addition):
    pass

""" recalculate the score of all possible additions that require modification"""
def recalculate_score(problem, possible_additions, links_to_additions, best_addition):
    additions_to_change = links_to_additions[best_addition.video_id][best_addition.cache_id]

    for addition_id in additions_to_change:
        (video_id, cache_id) = addition_id
        possible_additions[addition_id].score = get_video_score(problem, video_id, cache_id)

""" Get a list of the id of all the additions to remove (for which the video would surcharge the size of the cache) """
def get_additions_to_remove(solution, possible_additions, best_addition):
    return []

