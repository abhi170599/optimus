"""
Implementation of genetic algorithm for config optimization
"""

import numpy as np
import copy

from typing import Any, Callable, List
from random import randint, random, choice

def get_inititial_population_space(bootstrap_solution: List[Any], steps: List[Any], step_constant_limits: List[int], n: int):
    """
    Create an initial solution space for the genetic algorithm.
    """
    initial_solution_space = [bootstrap_solution]
    while len(initial_solution_space)<n:
        generator = choice(initial_solution_space)
        base = copy.deepcopy(generator)

        print(f"base : {base}")
        for i in range(len(base)):
            change_direction = 1
            chnage_magnitude = randint(0, step_constant_limits[i]*steps[i])
            change = change_direction*chnage_magnitude
            base[i] += change
        initial_solution_space.append(base)

        for i in range(len(base)):
            change_direction = -1
            chnage_magnitude = randint(0, step_constant_limits[i]*steps[i])
            change = change_direction*chnage_magnitude
            base[i] += change

        f=False 
        for i in range(len(base)):
            if base[i] < 0:
                f = True
                break
        if not f:        
            initial_solution_space.append(base)  

        print(initial_solution_space)      

    return initial_solution_space

def get_top_k_parents(solution_space: List[List[Any]], fitness_function: Callable, k: int) -> List[List[Any]]:
    """
    Select top K solutions that can server as parents for the next generation.
    """
    fitness_scores = [fitness_function(solution_space[i]) for i in range(len(solution_space))]
    sorted_score_indices = np.argsort(fitness_scores)
    parent_indices = sorted_score_indices[0:k]
    parents = [solution_space[i] for i in parent_indices]
    return parents

def perform_crossover(parent1: List[Any], parent2: List[Any]) -> List[Any]:
    """
    Generate an offspring from two fit parents.
    """
    new_solution = []
    last = 1
    for i in range(len(parent1)):
        p = choice([1,2])
        if p == 1:
            new_attribute = parent1[i]
        else:
            new_attribute = parent2[i]    
        new_solution.append(new_attribute)
        last = (last + 1)%2

    return new_solution            
        
def create_new_generation(solution_space: List[List[Any]], n: int) -> List[List[Any]]:
    """
    Generate new solutions from the existing fit solution space
    """
    new_generation_solutions = []
    while len(new_generation_solutions)<n:
        parent1 = choice(solution_space)
        parent2 = choice(solution_space)
        offspring = perform_crossover(parent1, parent2)
        new_generation_solutions.append(offspring)

    return new_generation_solutions

def run_genetic_algorithm(
    bootstrap_solution: List[Any],
    iterations: int, 
    solution_size: int,
    fitness_function: Callable
    ) -> List[List[Any]]:
    """
    Run the genetic algorithm
    """
    initial_solution_space = get_inititial_population_space(bootstrap_solution,[5,10,1],[5,5,4],100)
    print(f"initial space: {initial_solution_space}")
    optimal_solution = []
    solution_space = initial_solution_space
    for i in range(iterations):
        print(f"******* iteration {i+1} *******")
        parents = get_top_k_parents(solution_space,fitness_function,10)
        print(f"fittest parents : {parents}")
        print(f"fitness scores: {[fitness_function(parent) for parent in parents]}")
        new_generation = create_new_generation(parents, solution_size)
        print(f"new generation: {new_generation}")
        solution_space = new_generation

    return solution_space    
        
def fitness_function(solution: List[Any]) -> int:
    """
    TODO: replace this with k8s steps, i.e running
    load generator for the deployed app and
    calculating average latency 
    """
    
    score = solution[0]*5 + solution[1]*1 + solution[2]*2
    return score



    





