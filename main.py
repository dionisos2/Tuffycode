from get_score import get_score

class Problem:
    def __init__(self):
        self.x=10
        self.result_path = None

        """ Load a problem file """
    def load_problem(self, problem_path):
        pass


    """ Create a solution from the current problem and save it in a file"""
    def save_solution(self, result_path):
        self.result_path = result_path
        pass


    def get_score(self):
        return get_score(self.result_path)


problem = Problem()
problem.load_problem("./qualification_round_2017.in/me_at_the_zoo.in")

problem.save_solution("result.txt")

problem.get_score()
