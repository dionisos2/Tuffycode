import random
from classes import *

def create_solution(problem):
    return Solution()


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
