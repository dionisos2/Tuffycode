from classes import *
from load_and_save import load_problem, save_solution, load_solution

def get_score(problem_path, solution_path):
    problem = load_problem(problem_path)
    solution = load_solution(solution_path)


    score = 0
    for request in problem.requests:
        score += get_request_score(problem, solution, request)

    score /= sum(request.nb_request for request in problem.requests)
    return int(score * 1000)


def get_request_score(problem, solution, request):
    possible_caches = get_possible_caches(problem, solution, request)
    if len(possible_caches) == 0:
        return 0

    best_cache_latency = min(possible_caches, key=lambda cache: cache.latency)
    dc_latency = problem.endpoints[request.ep_id].dc_latency

    if best_cache_latency < dc_latency:
        return (dc_latency - best_cache_latency) * request.nb_request
    else:
        return 0


def get_possible_caches(problem, solution, request):
    """ Pour 1 video et 1 endpoint, trouve les caches en commun.
    Entre la cfg solution (videos-caches) et les liaisons endpoints-caches."""
    connected_caches = set(problem.endpoints[request.ep_id].caches_latency.keys())
    caches_with_video = set(cache for cache in solution.caches if request.vid_id in cache.videos)

    return connected_caches.intersection(caches_with_video)
