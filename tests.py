from classes import *
from get_score import get_score
from load_and_save import load_problem, save_solution
from create_solution import *

def test_create_links_to_additions():
    problem_path = "./input/example.txt"
    # problem_path = "./input/me_at_the_zoo.in"

    problem = load_problem(problem_path)

    print(problem)

    links = create_links_to_additions(problem)
    print(links)

    possible_additions = create_possible_additions(problem)
    print(possible_additions)

    possible_additions[(2,1)].score = 3

    plop = get_best_additions(problem, possible_additions)
    print(plop)


test_create_links_to_additions()
