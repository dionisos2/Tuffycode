from classes import *
from get_score import get_score
from load_and_save import load_problem, save_solution
from create_solution import create_solution, create_random_solution


def main(problem_name, random_solution = False):
    problem_path = f"./input/{problem_name}"
    solution_path = f"./output/{problem_name}"

    problem = load_problem(problem_path)
    if random_solution:
        solution = create_random_solution(problem)
    else:
        solution = create_solution(problem)
    save_solution(solution, solution_path)

    score = get_score(problem_path, solution_path)
    print(score)

def test_example():
    problem_path = "./input/example.txt"
    solution_path = "./output/example.txt"
    score = get_score(problem_path, solution_path)
    print(score)
    print(score == 462500)

test_example()

def random_and_main(name):
    print("random solution")
    main(name, True)
    print("talos solution")
    main(name)


name = "me_at_the_zoo.in" #kittens.in.txt"
random_and_main(name)
