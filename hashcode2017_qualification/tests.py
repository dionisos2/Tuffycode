from classes import *
from get_score import get_score
from load_and_save import load_problem, save_solution
from create_solution import *

def test_create_links_to_copystores():
    problem_path = "./input/example.txt"
    # problem_path = "./input/me_at_the_zoo.in"

    problem = load_problem(problem_path)
    solution = Solution()

    print(problem)

    links = create_links_to_copystores(problem)
    print(links)

    possible_copystores = create_possible_copystores(problem, solution)
    print(possible_copystores)

    possible_copystores[(2,1)].score = 3

    plop = get_best_copystores(problem, possible_copystores)
    print(plop)


test_create_links_to_copystores()
