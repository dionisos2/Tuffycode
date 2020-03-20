from get_score import get_score
from load_problem import load_problem
from classes import *

class Problem:
    def __init__(self):
        self.result_path = None
        self.endpoints = {}
        self.videos = {}
        self.caches = {}

        """ Load a problem file """
    def load_problem(self, problem_path):
        result = load_problem(problem_path)
        self.caches, self.endpoints, self.videos = result

    """ Create a solution from the current problem and save it in a file"""
    def save_solution(self, result_path):
        self.result_path = result_path
        pass


problem = Problem()
problem.load_problem("./qualification_round_2017.in/me_at_the_zoo.in")

problem.save_solution("result.txt")

print(get_score(problem, "result.txt"))
