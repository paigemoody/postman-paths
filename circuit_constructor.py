# contains all functions needed to build an euler circuit 
# takes in euler graph constructor function from graph constructor.py


import numpy as np # seems to slow down a bit
import osmnx as ox # really slows down file run?
import networkx as nx
import itertools
from random import choice
import math

from graph_constructor import make_nodes_dict
from graph_constructor import get_odd_nodes
from graph_constructor import get_list_of_all_pairs_lists
from graph_constructor import get_shortest_path_route_two_nodes
from graph_constructor import get_route_edges_from_shortest_path
from graph_constructor import get_total_length_shortest_path
from graph_constructor import get_dict_length_pairings_lists
from graph_constructor import get_optimal_pairing_list_dict
from graph_constructor import get_all_double_back_edges
from graph_constructor import make_traversal_dict_with_added_edges



def get_bridges(edges_list):
    
    """
    Takes a list of edges, returns a list of all bridges in the graph.
    
    Note: bridges returned are true bridges, meaning that they are bridges
    calculated by networkx without the edges that have multiple traverses 
    remaining. 
    """
    
    # make a temporary graph 
    temp_G = nx.Graph()
    
    # add all current edges to the graph
    for edge in edges_list:
            edge_node_1, edge_node_2 = edge
            temp_G.add_edge(edge_node_1, edge_node_2)
    
    # get all_bridges in temp graph 
    bridges_all = list(nx.bridges(temp_G))
    
    # get set of edges with two traversals left (only want one of each, so use set)
    mult_trav_remaining = set([])
    
    for edge in edges_list:
        
        num_trav_remaining = edges_list.count(edge)
        
        if num_trav_remaining > 1:
            
            mult_trav_remaining.add(edge)
    
    mult_trav_remaining = list(mult_trav_remaining)
    
    # remove mult traversal edges from bridges list 
    
    # print("bridges_ all:", bridges_all)
    # print("\nmult_trav_remaining:", mult_trav_remaining)
    
    # make a new bridges list that contains only edges that don't have mult traversals left
    
    bridges_reduced = []
    
    for edge in bridges_all:
        # print("\n\nedge:", edge)
        print()
        if edge in mult_trav_remaining:
            print()
            # print(f"bridge {edge} is in {mult_trav_remaining}")
        elif edge[::-1] in mult_trav_remaining: 
            print()
            # print(f"bridge {edge} REVERSED is in {mult_trav_remaining}")
        else:
            # print(f"bridge {edge} is NOT in {mult_trav_remaining}")
            
            bridges_reduced.append(edge)
    
    # return a list of true bridges
    return bridges_reduced

def get_all_conn_edges_remaining_in_graph(current_node, remaining_edges, nodes_dict):
    
    """
    Takes current node, a list of remaining edges in graph, and a dictionary of nodes
    and their corresponding edges. 
    
    Returns a list of all edges connected to the input node that are still in the graph.
    
    """
    
    # print("\ncurrent_node:", current_node)
    # print("\nremaining_edges:", remaining_edges)

    
    # get list of all edges that contain the current node -- in the original graph
    all_conn_edges_in_original_graph = list(nodes_dict[current_node])
    
    # print(f"\nnodes_dict at {current_node}", all_conn_edges_in_original_graph)
    
    
    # remove duplicate edges from remaining edges by makeing a set, then making that set into a list
    
    remaining_edges_unique = list(set(remaining_edges))
    
    # loop remaining edges set
    # find edges that correspond to an edge in the nodes dict OR the reversed edge order is in the nodes dict
    
    possible_next_edges = []
    
    for remaining_edge in remaining_edges_unique:
        # print("\nremaining edge:", remaining_edge)
        
        # check if remaining edge is connected to current node:
        
        if current_node in remaining_edge:
            # print(f"{current_node} IS IN {remaining_edge}")
            
            possible_next_edges.append(remaining_edge)
        
        elif current_node not in remaining_edge:
            # print((f"{current_node} is NOT in {remaining_edge}"))
            pass
    
    # print("\n\npossible_next_edges:", possible_next_edges)
    
    return possible_next_edges

def choose_edge_to_traverse(current_node, possible_next_edges, current_bridges):
    """
    Takes in the current node, a list of possible next edges for node 
    (ie. all connected edges remaining in graph)
    and a list of bridges on the graph.
    
    Returns a tuple of the next edge that should be traversed.  
    """
    # print("\ncurrent_node_for_test:", current_node)
    # print("\npossible_next_edges:", possible_next_edges)
    # print("\nbridges:",current_bridges )
    
    non_bridge_next_edges_options = []
    bridge_next_edge_options = []
    
    # find all possible next edges that are not in current bridges list 
    
    for possible_next_edge in possible_next_edges:
        
        # print(f"\n\nREVIEWING: {possible_next_edge}:")
        
        if possible_next_edge in current_bridges or possible_next_edge[::-1] in current_bridges:
            # print(f" {possible_next_edge} or {possible_next_edge[::-1]} in current_bridges")
            bridge_next_edge_options.append(possible_next_edge)
        else: 
            #print(f" {possible_next_edge} AND {possible_next_edge[::-1]} NOT in current_bridges")                               
            non_bridge_next_edges_options.append(possible_next_edge)
    
    # print("\n\nnon_bridge_next_edges_options:", non_bridge_next_edges_options)
    # print("bridge_next_edge_options:", bridge_next_edge_options)
    
    
    # if non_bridge_next_edges is not empty, return the first item in non_bridges 
    if len(non_bridge_next_edges_options) > 0:
        return non_bridge_next_edges_options[0]
    
    # if non_bridge_next_edges is empty, return the first item in bridges 
    else:
        return bridge_next_edge_options[0]


def get_list_of_edges_by_traversal_count(edge_traversals_dict):
    """
    Given edge traversals dict, return a list of edges. 
    If the edge needs twice traversal it will appear twice in the 
    output list.
    """
    
    edges_list = []
    
    # look at each key (edge) in edge traversals dict
    for edge in edge_traversals_dict:
        
        # make var for number of traversals for current edge
        traversals = edge_traversals_dict[edge]
        
        # add the edge to the edges list as many times as it needs to be traversed
        for i in range(traversals):
        
            edges_list.append(edge)

    return edges_list


def make_euler_circuit(start_node, graph):
    
    
    print("Start node:", start_node)
    
    # SET UP EULER GRAPH
    # get all odd nodes on graph 
    odd_nodes = get_odd_nodes(graph)
    
    print("\nodd nodes:", odd_nodes)
    
    # get all possible pairings for odd nodes in graph
    nodes_dict = make_nodes_dict(G)
    
    print("\nnodes dict:", nodes_dict)
    
    # STARTS GETTING REAL SLOW
    
    # get list of all possible pairings of odd nodes:
    possible_pairings_list = get_list_of_all_pairs_lists(odd_nodes)
    
    print("\npossible_pairings_list:", possible_pairings_list)
    
    # get the length of each possible pairing of odd nodes 
    length_pairings_lists_dict = get_dict_length_pairings_lists(possible_pairings_list, graph)
    
    print("\nlength pairings lists dict:", length_pairings_lists_dict)
    
    # get the odd nodes pairing that has the shortest distance 
    optimal_pairing_list_dict = get_optimal_pairing_list_dict(length_pairings_lists_dict)
    
    print("\noptimal_pairing_list_dict:", optimal_pairing_list_dict)
    
    # get list of edges that will need to be traversed twice 
    twice_traversal_list = get_all_double_back_edges(optimal_pairing_list_dict, graph)
    
    print("\ntwice_traversal_list:", twice_traversal_list)
    
    # get dict of edges and how many times each needs to be traversed 
    edge_traversals_dict_eulerian = make_traversal_dict_with_added_edges(twice_traversal_list, graph) 
    
    print("\nedge_traversals_dict_eulerian:", edge_traversals_dict_eulerian)
    
    # get list of all edges that need to be traversed, multiple traversal edges are included multiple times
    all_edges_in_euler_graph = get_list_of_edges_by_traversal_count(edge_traversals_dict_eulerian)

    print("\nall_edges_in_euler_graph:", all_edges_in_euler_graph)
    
    # ---- # 
    
    print("\n\n\n\n\n\n\n\nBUILDING CIRCUIT")
    
    # GET EULER CIRCUIT 
    
    # make list of edges currently on graph: 
    current_edges_on_graph_list = all_edges_in_euler_graph
    
    # initialize current node 
    current_node = start_node 
    
    # initialize a list the contains the order of node visists with the start node
    
    node_visit_order = [current_node]
    
    print("--------START-WALKING--------")
    
    while len(current_edges_on_graph_list) > 0:
        
        print("Node visit order:", node_visit_order)
        
        print("\n\nCURRENT NODE:", current_node)
        
        # print edges currently on the graph
        print("\nedges currently on graph:", current_edges_on_graph_list )

        # get the bridges on the initial graph
        current_bridges_on_graph = get_bridges(current_edges_on_graph_list)
        print("\nbridges currently on graph:", current_bridges_on_graph)

        # get all the connected edges in initial graph for the current node 
        edges_conn_to_current_node = get_all_conn_edges_remaining_in_graph(current_node, 
                                                                           current_edges_on_graph_list, 
                                                                           nodes_dict)
        print(f"\ncurrent node: {current_node} is still connected to: {edges_conn_to_current_node}")

        # get the next edge to traverse 
        edge_to_traverse = choose_edge_to_traverse(current_node, edges_conn_to_current_node, current_bridges_on_graph)
        print(f"\nedge_to_traverse:", edge_to_traverse)

        # remove edge just traversed from current_edges_on_graph_list
        ## you don't know the order of the nodes in the edge in the current_edges_on_graph_list,
        ## so you have to check both
        
        print("\nlen of current_edges_on_graph_list BEFORE removing one item:", len(current_edges_on_graph_list))
        
        if edge_to_traverse in current_edges_on_graph_list:
            current_edges_on_graph_list.remove(edge_to_traverse)
        else:
            current_edges_on_graph_list.remove(edge_to_traverse[::-1])
        print("\nlen of current_edges_on_graph_list AFTER removing one item:", len(current_edges_on_graph_list))
        
        # update current node to be node in edge_to_traverse that is not the current node
        ## make edge a list so that you can remove the current node
        
        print("\ncurrent node BEFORE update:", current_node)
        edge_to_traverse_list = list(edge_to_traverse)
        ## remove current node from edge to traverse
        edge_to_traverse_list.remove(current_node)
        ## update current node to be the only node left in the edge list
        
        current_node = edge_to_traverse_list[0]
        print("\ncurrent node AFTER update:", current_node)
        
        # add the new current node to the nodes visit order list 
        node_visit_order.append(current_node)
        
        print("\n\n\n----------WALKING-----------")

    return(node_visit_order)

if __name__ == '__main__':

    # default bbox
    NORTH = 37.7599 # max lat 
    SOUTH = 37.7569 # min lat
    EAST = -122.3997 # max lng
    WEST = -122.4023 # min lng 

        
    G = ox.graph_from_bbox(NORTH,SOUTH, EAST, WEST, network_type='walk') ## FLAG

    start_node = choice(list(G.nodes))

    print(make_euler_circuit(start_node, G))



