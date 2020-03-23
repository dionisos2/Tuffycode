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
    def __init__(self, num_id, id_video, id_cache):
        self.num_id = num_id
        self.id_video = id_video
        self.id_cache = id_cache
        self.score = None


def create_solution(problem):
    solution = Solution()
    possible_additions = create_possible_additions(problem)
    links_to_additions = create_links_to_additions(problem, possible_additions)

    while len(possible_additions) > 0:
        best_addition = get_best_additions(problem, possible_additions)
        add_video(problem, solution, best_addition)
        additions_to_remove = get_additions_to_remove(solution, possible_additions, best_addition)
        recalculate_score(possible_additions, links_to_additions, best_addition)

        for id_addition in additions_to_remove:
            del possible_additions[id_addition]
        if best_addition.num_id in possible_additions:
            del possible_additions[best_addition.num_id]

    return solution

"""Create a dict of all possibles additions"""
def create_possible_additions(problem):
    return dict()

"""Create a dict of dict, allowing to get all additions we should modify for a particular video and a particular cache"""
def create_links_to_additions(problem, possible_additions):
    result = dict()
    #result[id_video] = dict()
    #result[id_video][id_cache] = [id_addition]
    return result

"""Get the score of a video for a particular cache"""
def get_video_score(problem, video, cache):
    return 0

"""Return the current best possible additions (max of score/size)"""
def get_best_additions(problem, possible_additions):
    return possible_additions[1]


"""Add a video to the correct cache of the solution"""
def add_video(problem, solution, best_addition):
    pass

""" recalculate the score of all possible additions that require modification"""
def recalculate_score(possible_additions, links_to_additions, best_addition):
    pass

""" Get a list of the id of all the additions to remove (for which the video would surcharge the size of the cache) """
def get_additions_to_remove(solution, possible_additions, best_addition):
    return []

