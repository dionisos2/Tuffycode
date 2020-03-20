from get_score import get_score
from load_problem import load_problem
from classes import *

class Problem:
    def __init__(self):
        self.result_path = None
        self.infos = None
        self.videos = list()
        self.endpoints = list()
        self.requests = list()
        self.caches = {}
        
    def __str__(self):
        result_path = "Result path: "+str(self.result_path)+"\n"
        str_infos = "Infos: "+str(self.infos)+"\n"
        str_vid = "Videos: "+str(self.videos)+"\n"
        str_endpoints = "EndPoints: "+str(self.endpoints)+"\n"
        str_requests = "Requests: "+str(self.requests)+"\n"
        str_all = result_path+str_infos+str_vid+str_endpoints+str_requests
        return str_all

    def load_problem(self, problem_path):
        """ Load a problem file """
        result = load_problem(problem_path)
        self.caches, self.endpoints, self.videos = result

    def save_solution(self, result_path):
        """ Create a solution from the current problem and save it in a file"""
        self.result_path = result_path
        pass
    
    


problem = Problem()
print(problem)
problem_path_test = "test_load_problem.txt"
problem_path = "./qualification_round_2017.in/me_at_the_zoo.in"
load_problem(problem,problem_path_test)
print(problem)


#problem.save_solution("result.txt")
#
#print(get_score(problem, "result.txt"))
