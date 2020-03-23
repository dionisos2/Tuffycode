from classes import *
from get_score import get_score
from load_and_save import load_problem, save_solution
from create_solution import *

def test_create_links_to_additions():
    problem_path = "./input/example.txt"
    # problem_path = "./input/me_at_the_zoo.in"

    problem = load_problem(problem_path)

    print(problem)

    cache_to_endpoints = create_cache_to_endpoints_link(problem)

    print(cache_to_endpoints)

    links = create_links_to_additions(problem)
    print(links)

test_create_links_to_additions()
