from classes import *
from load_and_save import load_problem, save_solution, load_solution

def get_score(problem_path, solution_path):
    problem = load_problem(problem_path)
    solution = load_solution(solution_path)

    check_validity(problem, solution)
    score = 0
    for request in problem.requests:
        score += get_request_score(problem, solution, request)

    score /= sum(request.nb_request for request in problem.requests)
    return int(score * 1000)


def check_validity(problem, solution):
    for cache in solution.caches.values():
        videos_size = sum(video.size for video in problem.videos if video.num_id in cache.videos_id)
        if videos_size > problem.infos["X"]:
            raise ValueError(f"cache {cache} surcharged")

def get_request_score(problem, solution, request):
    best_cache_latency = get_best_cache_latency(problem, solution, request)

    dc_latency = problem.endpoints[request.ep_id].dc_latency

    if best_cache_latency < dc_latency:
        return (dc_latency - best_cache_latency) * request.nb_request
    else:
        return 0


def get_best_cache_latency(problem, solution, request):
    best_latency = float("inf")

    endpoint = problem.endpoints[request.ep_id]
    for caches_id, cache_latency in endpoint.caches_latency.items():
        if request.vid_id in solution.caches[caches_id].videos_id:
            best_latency = min(best_latency, cache_latency)

    return best_latency
