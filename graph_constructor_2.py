# import numpy as np # seems to slow down a bit
# import osmnx as ox # really slows down file run?
# import networkx as nx

from networkx import shortest_path
# import itertools
# from random import choice
# import math

from classes import OSMGraph
from classes import DIYGraph
# from class_experimentation import make_edges_dict
# from class_experimentation import make_nodes_dict


# save these for testing 
NORTH = 37.7599 # max lat 
SOUTH = 37.7569 # min lat
EAST = -122.3997 # max lng
WEST = -122.4023 # min lng 

ORIG_GRAPH = OSMGraph(NORTH, SOUTH, EAST, WEST)
ABCD_graph = DIYGraph([('A','B'), ('B', 'C'), ('C', 'D'), ('D','A'), ('A', 'C'), ('B', 'D')])

def get_odd_nodes(graph_instance):
    """ Given graph instance return 
    list of odd nodes.
    """
    odd_nodes_dict = []

    # nodes_dict = make_nodes_dict(graph_instance)

    nodes_dict = graph_instance.nodes_dict

    for node in nodes_dict:
        if nodes_dict[node]['is_odd'] == True:
            odd_nodes_dict.append(node)

    return odd_nodes_dict

def get_all_pairing_options(lst):
    """ Given list of items
    return a list of lists, each containing
    tuples of item pairs.

    THIS FUNCTION IS NOT MINE:
    it is from: 
    https://stackoverflow.com/questions/5360220/how-to-split-a-list-into-pairs-in-all-possible-ways
    """

    if len(lst) < 2:
        # if there are zero items or just one return (yield?) an empty list
        # basically used exclusively for when you get to the
        # last item in the input list so no more pairs can be made
        yield []
        return
    
    if len(lst) % 2 == 1:
        # Handle odd length list
        for i in range(len(lst)):
            
            # items from 0 to i 
            items_to_left_ = lst[:i]    

            # items right of i to end of list
            items_to_right_ = lst[i+1:]
            
            for result in get_all_pairing_options(items_to_left_ + items_to_right_):
                yield result
    else:
        cur_first_item = lst[0]
        
        for i in range(1,len(lst)):
            
            next_item = lst[i]
            
            pair = (cur_first_item, next_item)
            
            items_to_left_of_pair = lst[1:i]
            items_to_right_of_pair = lst[i+1:]
            
            for rest in get_all_pairing_options(items_to_left_of_pair + items_to_right_of_pair):
                yield [pair] + rest

def get_list_of_all_pairs_lists(lst):
    """
    Takes in a list of items and returns a list of 
    lists, each containing tuples that represent 
    pairings of odd nodes.   

    (Calls the function I didn't write, returns a list)
    """
    
    list_of_possible_pairs_lists = []
    
    # get the all pairs  generator
    all_pairs_object = get_all_pairing_options(lst)
    
    for pairs_list in all_pairs_object: 
        list_of_possible_pairs_lists.append(pairs_list)
    
    return list_of_possible_pairs_lists

def get_shortest_route_two_nodes(start_node, end_node, graph_instance):
    """ Given a start and end node, 
    return sequenced list of nodes included in shortest route
    between the nodes.
    """
    route = shortest_path(graph_instance.ox_graph, start_node, end_node, weight='length')
    # route = nx.shortest_path(graph_instance.ox_graph, start_node, end_node, weight='length')
    return route

def get_route_edges_from_route(route):
    """Given a sequenced list of nodes (route)
    return all edges in route.

    >>> get_route_edges_from_route(['A', 'B', 'C', 'D','E'])
    [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')]

    """

    edges_in_route = []
    
    for i in range(0, len(route)-1):

        edge = route[i], route[i+1]

        edges_in_route.append(edge)

    return edges_in_route

def get_route_length(route_edges_list, graph_instance):
    """
    Given a list of edges in a route, 
    return the total length of the route 
    (sum of the lengths of all edges in list).

    >>> get_route_length([(65294615, 65294613), (65294613, 65320188)], ORIG_GRAPH)
    228.606
    """

    edges_dict = graph_instance.edges_dict
    # edges_dict = make_edges_dict(graph_instance)

    total_edges_length = 0

    for edge in route_edges_list:
        # check for both order of the edge tuple in the dict
        if edge in edges_dict:

            total_edges_length += edges_dict[edge]['length']

        elif edge[::-1] in edges_dict:

            edge = edge[::-1]
            total_edges_length += edges_dict[edge]['length']

    return total_edges_length

def get_dict_pairings_lists_lengths(list_of_possible_pairs_lists, graph_instance):
    """Given list of list of possible 
    odd node pairings , return a dictionary of the length 
    of each pairing.
    
    >>> get_dict_pairings_lists_lengths([[(65294615, 65320193), (65313455, 65320188)], [(65294615, 65313455), (65320193, 65320188)], [(65294615, 65320188), (65320193, 65313455)]], ORIG_GRAPH)
    {((65294615, 65320193), (65313455, 65320188)): 506.546, ((65294615, 65313455), (65320193, 65320188)): 506.546, ((65294615, 65320188), (65320193, 65313455)): 330.56899999999996}

    """
    pairings_lengths_dict = {}


    for possible_pairing_list in list_of_possible_pairs_lists:

        pairings_list_length = 0 

        pairings_lengths_dict[tuple(possible_pairing_list)] = pairings_list_length

        for pair in possible_pairing_list:

            start_node = pair[0]
            end_node = pair[1]

            shortest_route_nodes_list = get_shortest_route_two_nodes(start_node, end_node, graph_instance)

            shortest_route_edges = get_route_edges_from_route(shortest_route_nodes_list)

            total_route_length = get_route_length(shortest_route_edges, graph_instance)

            pairings_list_length += total_route_length

        pairings_lengths_dict[tuple(possible_pairing_list)] = pairings_list_length

    return pairings_lengths_dict

def get_twice_traversals_edges(pairings_lengths_dict):
    """Given dict of pairings and lengths, 
    return list of edges to traverse twice. 

    >>> get_twice_traversals_edges({(('A', 'B'), ('B', 'C')): 1, (('A', 'C'), ('B', 'C')): 6, (('D', 'C'), ('B', 'A')): 10})
    [('A', 'B'), ('B', 'C')]
    """
    
    optimal_pairing = None
    shortest_length = float('inf') 

    for pairing in pairings_lengths_dict:
        if pairings_lengths_dict[pairing] < shortest_length:
            optimal_pairing = pairing
            shortest_length = pairings_lengths_dict[pairing]

    return list(optimal_pairing)

def update_twice_traversal_edges(list_twice_trav_edges, graph_instance):
    """ 
    Update num_traversals attribute in edges_dict for 
    for edges that will be traversed twice.

    Return edges dict for graph instance 
    """
    
    edges_dict = graph_instance.edges_dict
    # edges_dict = make_edges_dict(graph_instance)

    for node_pair in list_twice_trav_edges:

        # get all edges that are needed for shortest path between nodes

        route = get_shortest_route_two_nodes(node_pair[0], node_pair[1], graph_instance)
        route_edges = get_route_edges_from_route(route)

        for edge in route_edges:

            if edge in edges_dict:

                edges_dict[edge]['num_traversals'] += 1 


            elif edge[::-1] in edges_dict: 

                edge = edge[::-1]

                edges_dict[edge]['num_traversals'] += 1 

            else: 

                print(f"{edge} not in {edges_dict}.")

    graph_instance.edges_dict = edges_dict 

    # return updated graph_instance?
    return  graph_instance



## over-arching function that takes a bounding box and returns 
## a dict with twice traversal edges marked 

def get_eulerian_graph_edges(bbox):
    """Given a bounding box list [north,south,east,west],
    return a dictionary of edges with metadata and traversal count.
    """
    north, south, east, west = bbox

    print(north,south,east,west)

    osm_graph = OSMGraph(north,south,east,west)

    odd_nodes = get_odd_nodes(osm_graph)

    print("\nodd_nodes",odd_nodes)

    all_pairs_list = get_list_of_all_pairs_lists(odd_nodes)

    print("\nall_pairs_list",all_pairs_list)

    dict_pairings_lists_lengths = get_dict_pairings_lists_lengths(all_pairs_list, osm_graph)

    print("\ndict_pairings_lists_lengths", dict_pairings_lists_lengths)

    twice_traversals_edges = get_twice_traversals_edges(dict_pairings_lists_lengths)

    print("\ntwice_traversals_edges",twice_traversals_edges)

    updated_dict = update_twice_traversal_edges(twice_traversals_edges, osm_graph)
    
    return updated_dict


bbox = [37.7599,37.7569 ,-122.3997,-122.4023] # min lng 
updated_graph_inst = get_eulerian_graph_edges(bbox)

for edge in updated_graph_inst.edges_dict:
    print()
    print(edge, "\n", updated_graph_inst.edges_dict[edge])




# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()


# twice_traversals_edges = [(65294615, 65320188), (65320193, 65313455)]
# print(update_twice_traversal_edges(twice_traversals_edges, ORIG_GRAPH))







