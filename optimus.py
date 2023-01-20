#! /Users/abhi17/Work/optimus/optimusdev/bin/python3

"""
Driver program for optimus. 
"""

from random import randint
from optimuslib.optimize.genetic_algorithm import experiment
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--metric",default="latency",help="Application metric that should be optimized through experiments. (eg. QPS, Latency)")
parser.add_argument("-n", "--trials",help="Set the number of iterations that the experiemnt should do")
parser.add_argument("-b", "--bootstrap", default="True", help="provide a boot strap config for the experiments")
parser.add_argument("-p", "--multiproduct", help="Multiproduct")

if __name__ == "__main__":
    args = parser.parse_args()
    optimal = experiment()
    