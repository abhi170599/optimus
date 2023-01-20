"""
Implementation of genetic algorithm for config optimization
"""

import numpy as np
import copy

from time import sleep
from typing import Any, Callable, List, Tuple
from random import randint, random, choice
from optimuslib.k8s.k8s_controller import get_fibonacci_deployment, update_deployment_spec, is_deployment_ready
from optimuslib.load.load_generator import LoadGenerator, ApacheLoadGenerator

SERVICE_URL = "http://20.237.37.65/fibonacci"
LOAD_SIZE = 10
APACHE_SERVICE_URL = 'http://20.242.152.46/'

def get_load_inputs_for_fibonacci():
    load = []
    for i in range(LOAD_SIZE):
        random_load = randint(1,38)
        load.append(random_load)

    return load

load_generator = LoadGenerator(service_url=SERVICE_URL,load_inputs=get_load_inputs_for_fibonacci())
apacheLoad = ApacheLoadGenerator(url=APACHE_SERVICE_URL,time=10)

def all_greater_than_zero(solution):
    for s in solution:
        if s<=0:
            return False 
    return True        

def get_inititial_population_space(bootstrap_solution: List[Any], steps: List[Any], step_constant_limits: List[int], n: int):
    """
    Create an initial solution space for the genetic algorithm.
    """
    initial_solution_space = [bootstrap_solution]
    while len(initial_solution_space)<n:
        generator = choice(initial_solution_space)
        base = copy.deepcopy(generator)
        for i in range(len(base)):
            change_direction = 1
            chnage_magnitude = randint(0, step_constant_limits[i]*steps[i])
            change = change_direction*chnage_magnitude
            base[i] += change
        
        if base[0]<base[1] and base[2]<base[3] and all_greater_than_zero(base):     
            initial_solution_space.append(base)
        
        base = copy.deepcopy(generator)
        for i in range(len(base)):
            change_direction = -1
            chnage_magnitude = randint(0, step_constant_limits[i]*steps[i])
            change = change_direction*chnage_magnitude
            base[i] += change
        
        if base[0]<base[1] and base[2]<base[3] and all_greater_than_zero(base):     
            initial_solution_space.append(base)    

    return initial_solution_space

def get_top_k_parents(solution_space: List[List[Any]], fitness_function: Callable, k: int) -> Tuple[List[List[Any]],int]:
    """
    Select top K solutions that can server as parents for the next generation.
    """
    fitness_scores = [fitness_function(solution_space[i]) for i in range(len(solution_space))]
    sorted_score_indices = np.argsort(fitness_scores)
    parent_indices = sorted_score_indices[0:k]
    highest_fitness_score = fitness_scores[sorted_score_indices[0]]
    parents = [solution_space[i] for i in parent_indices]
    return parents, highest_fitness_score

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
        if offspring[0]<offspring[1] and offspring[2]<offspring[3]:
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
    initial_solution_space = get_inititial_population_space(bootstrap_solution,[5,10,10,20,1],[10,10,10,10,1],20)
    print(f"generated initial solution space: {initial_solution_space}")
    optimal_solution = []
    solution_space = initial_solution_space
    for i in range(iterations):
        print(f"******* iteration {i+1} *******")
        parents, highest_score = get_top_k_parents(solution_space,fitness_function,10)
        print(f"fittest parents : {parents}")
        print(f"highest fitness scores: {highest_score}")
        new_generation = create_new_generation(parents, solution_size)
        print(f"new generation: {new_generation}")
        solution_space = new_generation

    return solution_space[0:2]    
        
def fitness_function(solution: List[Any]) -> int:
    
    try:
        resource_spec = {
            "cpu_req": solution[0],
            "cpu_lim": solution[1],
            "mem_req": solution[2],
            "mem_lim": solution[3],
            "replicas": solution[4]
        }
        deployment = get_fibonacci_deployment()
        update_deployment_spec(deployment, resource_spec)

        while not is_deployment_ready():
            sleep(1)

        latency = apacheLoad.get_average_latency()
        cost_of_deploying = resource_spec["cpu_lim"] + resource_spec["mem_lim"]

        fitness_score = latency + cost_of_deploying

        return fitness_score
    except Exception as e:
        print(e)
        return 99999    


def experiment():

    bootstrap_solution = [200, 300, 150, 200, 1] 
    print(f"Initiating OPTIMUS Experiments with bootstrap the config {bootstrap_solution}")
    optimal = run_genetic_algorithm(bootstrap_solution, 4, 5, fitness_function)
    return optimal



    





