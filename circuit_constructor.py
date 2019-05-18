# contains all functions needed to build an euler circuit 
# takes in euler graph constructor function from graph constructor.py


import numpy as np
import osmnx as ox
import networkx as nx
import itertools
from random import choice
import math

from graph_constructor import print_hi




# BUILD GRAPH & GET STATS
def build_graph(north,south, east, west):

    """
    From boox constraints, construct graph

    Return graph

    Print summary stats about graph.
    """
    # set bbox bounds: (will eventually come from drawing)
     
    # create graph
    G = ox.graph_from_bbox(north, south, east, west, network_type='walk')

    # display graph
    # ox.plot_graph(G, node_size=60)

    # Get graph info 
    basic_stats = ox.basic_stats(G)
        
    print("\n n (number of nodes in the graph):", basic_stats['n'])
    print("\n m (number of edges in the graph):", basic_stats['m']/2) # for undirected graph
    print("\n street_length_total (sum in meters):", basic_stats['street_length_total']/2)

    return G


def make_euler_circuit(start_node, graph):
    print(start_node, graph.nodes)

if __name__ == '__main__':

    # default bbox
    NORTH = 37.7599 # max lat 
    SOUTH = 37.7569 # min lat
    EAST = -122.3997 # max lng
    WEST = -122.4023 # min lng 

        
    # G = build_graph(NORTH,SOUTH, EAST, WEST) ## FLAG

    # start_node = choice(list(G.nodes))

    # make_euler_circuit(start_node, G)

    print_hi()


