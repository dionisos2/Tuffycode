from classes import *


def get_score(problem, solution_path):
    caches = {}

    with open(solution_path, "r+") as f:
        cache_nbr = int(f.readline())
        for _ in range(cache_nbr):
            params = f.readline().split()

            for video_id in params[2:]:
                problem.caches[params[1]].videos.add(video_id)

    score = 0

    for video_id, video in problem.videos.items():
        score += get_video_score(problem, video_id, video)


def get_video_score(problem, video_id, video):
    best_score = 0
    if len(videos.requests) == 0:
        return 0
    else:
        for endpoint_id, request_nbr in videos.requests.items():
            possible_caches = get_possible_cache(problem, video_id, endpoint_id)
            best_cache_latency = min(possible_caches, key=lambda cache: cache.latency)
            latency_diff = abs(problem.endpoints[endpoint_id].data_center_latency-cache.lantency)
            best_score = max(latency_diff, best_score)
    return best_score


def possible_caches(problem, video_id, endpoint_id):
    possible_caches = set()
    for cache in problem.caches:
        if video_id in cache.videoDict and cache in problem.endpoints.caches_latency:
            possible_caches.add(cache)

    return possible_caches

