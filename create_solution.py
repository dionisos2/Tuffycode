import random
from classes import *

def create_solution(problem):
    return Solution()


def create_random_solution(problem):
    cache_size = problem.infos["X"]

    solution = Solution()

    for cache_id in problem.caches_id:
        cache = Cache(cache_id)
        video = random.choice(problem.videos)
        current_size = video.size
        while current_size < cache_size:
            cache.videos.add(video)
            video = random.choice(problem.videos)
            current_size += video.size
        solution.caches[cache_id] = cache

    return solution
