
# contains all functions that are needed to create a list of edges for an Euler 
# graph 

import numpy as np # seems to slow down a bit
import osmnx as ox # really slows down file run?
import networkx as nx
import itertools
from random import choice
import math


def make_nodes_dict(graph):
    """ 
    Given a graph, make dict where:
    key is each node,  
    value is set of all edges that contain node.
    """
    nodes_dict = {}

    # loop over graph's node object
    for node in graph.nodes:
        # make a key for the node 
        # initialize the key's valuse as a set, so that only one "version"
        # of each edge can be added -- context: osmnx makes a directed 
        # graph so edge (A,B) is distinct from (B,A). We want these edges to be
        # considered identical. Thus, we use a set. 
        nodes_dict[node] = set() 
        
    # Confirm that the dict has the expected number of nodes 
    # expected_node_count = basic_stats['n']
    # actual_node_count = len(nodes_dict.keys())
    # print("Confirmed node count:", expected_node_count == actual_node_count)

     
    # if expected_node_count == actual_node_count:
        # If the node count matches expectation, move on to add edges to set.
        
        # WIP - check edge count: 
            # Expected edge count is half of what's 
            # reported from basic_stats because we are using an undirected graph.
            # expected_edge_count = basic_stats['m'] 
            # edge_counter = 0

        # loop over each edge in graph's edge object, see which edges contain current node
    # for edge in G.edges:
    for edge in graph.edges:

        # Note: each edge is a three item tuple: (start,end,weight) 
        # the stored weight in the edge is defaulted to 0 and 
        # is superfluous, so it will be ignored moving forward

        start_node = edge[0]
        end_node = edge[1]

        # name edge by start and end node 
        edge_identifier = (start_node, end_node)

        # add edge tuple to the node's value set 
        # NOTE: not naming edge by wayid because osm wayids are not unique to a particular edge
        # in osm a 'way' often contains several edges

        nodes_dict[start_node].add(edge_identifier)

    return nodes_dict





