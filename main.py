from get_score import get_score
from load_problem import load_problem
from classes import *

class Problem:
    def __init__(self):
        self.result_path = None
        self._infos = None
        self._videos = list()
        self._endpoints = list()
        self._requests = list()
        self.caches = {}

    # Infos
    @property
    def infos(self):
        return self._infos
    @infos.setter
    def infos(self, infos):
        self._infos = infos
    def set_infos(self, infos):
        self._infos = infos

    # Videos
    @property
    def videos(self):
        return self._videos
    @videos.setter
    def videos(self, videos):
        self._videos = videos
    def set_videos(self, videos):
        self._videos = videos

    # Endpoints
    @property
    def endpoints(self):
        return self._endpoints
    @endpoints.setter
    def endpoints(self, endpoints):
        self._endpoints = endpoints
    def set_endpoints(self, endpoints):
        self._endpoints = endpoints

    # Requests
    @property
    def requests(self):
        return self._requests
    @requests.setter
    def requests(self, requests):
        self._requests = requests
    def set_requests(self, requests):
        self._requests = requests


    def __str__(self):
        result_path = "Result path: " + str(self.result_path) + "\n"
        str_infos = "Infos: " + str(self.infos) + "\n"
        str_vid = "Videos: " + str(self.videos) + "\n"
        str_endpoints = "EndPoints: " + str(self.endpoints) + "\n"
        str_requests = "Requests: " + str(self.requests) + "\n"
        str_all = result_path + str_infos + str_vid + str_endpoints + str_requests
        return str_all


    def save_solution(self, result_path):
        """ Create a solution from the current problem and save it in a file"""
        self.result_path = result_path
        pass




problem = Problem()
print(problem)
problem_path_test = "test_load_problem.txt"
problem_path = "./qualification_round_2017.in/me_at_the_zoo.in"
load_problem(problem, problem_path_test)
print(problem)


#problem.save_solution("result.txt")
#
#print(get_score(problem, "result.txt"))
