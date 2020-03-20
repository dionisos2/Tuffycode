from get_score import get_score

class Problem:
    def __init__(self):
        self.result_path = None

        """ Load a problem file """
    def load_problem(self, problem_path):
        var = ["V","E","R","C","X"]
        with open(problem_path, "r+") as f:
            datas = f.readline()
            datas = list(map(lambda x:int(x), datas.split()))
            self.inputs = {var[i] : datas[i] for i in range(len(var))}
            self.taille_videos = list(map(lambda x:int(x), f.readline().split()))
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
