"""
Driver program for optimus. 
"""

from random import randint
from load.load_generator import LoadGenerator


SERVICE_URL = "http://20.237.37.65/fibonacci"
LOAD_SIZE = 10

def get_load_inputs_for_fibonacci():
    load = []
    for i in range(LOAD_SIZE):
        random_load = randint(1,38)
        load.append(random_load)

    return load    

if __name__ == "__main__":
    
    load_generator = LoadGenerator(service_url=SERVICE_URL,load_inputs=get_load_inputs_for_fibonacci())
    print(load_generator.get_average_latency())