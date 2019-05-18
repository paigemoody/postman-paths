
# contains all functions that are needed to create a list of edges for an Euler 
# graph 

import numpy as np # seems to slow down a bit
import osmnx as ox # really slows down file run?
import networkx as nx
import itertools
from random import choice
import math

def print_hi():

    print("hi")