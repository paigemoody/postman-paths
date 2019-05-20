
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
     #key is each node,  
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

    # loop over each edge in graph's edge object, see which edges contain current node
    # for edge in G.edges:
    for edge in graph.edges:

        # Note: each edge is a three item tuple: (start,end,weight) 
        # the stored weight in the edge is defaulted to 0 and is superfluous, so is ignored
        start_node = edge[0]
        end_node = edge[1]
        # name edge by start and end node 
        edge_identifier = (start_node, end_node)

        # add edge tuple to the node's value set 
        # NOTE: not naming edge by wayid because osm wayids are not unique to a particular edge
        # in osm a 'way' often contains several edges
        nodes_dict[start_node].add(edge_identifier)

    return nodes_dict

def get_odd_nodes(graph):
    """
    Take in a graph, 
    return list of nodes with odd order.
    """
    
    # initialize empy list for odd nodes
    odd_nodes = []

    # get dict of nodes and associated edges from make_nodes_dict function
    nodes_dict = make_nodes_dict(graph) 

    # loop over nodes (keys) in ndoes dict 
    for node in nodes_dict:

        # get the count of edges (length of edges set) for the current node
        all_edges = nodes_dict[node]
        edge_count = len(all_edges)

        
        if edge_count % 2 != 0:
            # if the edge count is odd, add node to the odd_nodes list
            odd_nodes.append(node)

    return odd_nodes    

def all_pairs(lst):
    
    """ 
    THIS FUNCTION IS NOT MINE: it is from: 
    https://stackoverflow.com/questions/5360220/how-to-split-a-list-into-pairs-in-all-possible-ways
    
    Takes a list of items, returns a generator which (I think)
    contains lists which are each a way to create pairs from
    the input list.
    
    !! I need to work more on this to refactor (see 'list_of_pairs' notebook)
    """
    
    if len(lst) < 2:
        
        # if there are zero items or just one 
        # return (yield?) an empty list
        # basically used exclusively for when you get to the
        # last item in the input list so no more pairs can be made
        # confirm ^^
        
        yield []
        return
    
    if len(lst) % 2 == 1:
        # Handle odd length list
        for i in range(len(lst)):
            
            # items from 0 to i 
            items_to_left_ = lst[:i]    

            # items right of i to end of list
            items_to_right_ = lst[i+1:]
            
            for result in all_pairs(items_to_left_ + items_to_right_):
                yield result
    else:
        cur_first_item = lst[0]
        
        for i in range(1,len(lst)):
            
            next_item = lst[i]
            
            pair = (cur_first_item, next_item)
            
            items_to_left_of_pair = lst[1:i]
            items_to_right_of_pair = lst[i+1:]
            
            for rest in all_pairs(items_to_left_of_pair + items_to_right_of_pair):
                yield [pair] + rest

def get_list_of_all_pairs_lists(lst):
    """
    Takes in a generator and returns a list of 
    lists, each containing tuples that represent 
    pairings of odd nodes.   
    """
    
    list_of_possible_pairs_lists = []
    
    all_pairs_object = all_pairs(lst)
    
    for pairs_list in all_pairs_object: 
        list_of_possible_pairs_lists.append(pairs_list)
    
    return list_of_possible_pairs_lists

def get_shortest_path_route_two_nodes(start_node, end_node, graph): 
    
    """
    Given a start and end node, 
    return sequenced list of nodes included in shortest route
    between the nodes.
    
    NOTE: basically wraps the osmnx's shortest path function for 
    documentation's sake.
    
    # ref: https://automating-gis-processes.github.io/2017/lessons/L7/network-analysis.html
    # ox.plot_graph_route(G, route, fig_height=10, fig_width=10)
    """

    route = nx.shortest_path(graph, start_node, end_node, weight='length')
    return route

def get_route_edges_from_shortest_path(route):
    
    """ 
    Given a route (sequenced list of nodes), 
    return all edges needed to build the route.
    
    NOTE TO CHECK: I belive the returned route list will always 
    have an odd length.

    ^ maybe not, if the route is just A to B with no waypoints
    """
    
    # print("route nodes sequence:", route)
    # print()
    
    # make sure route is longer than one node:
    
    if len(route) > 1:
        # set the start and end nodes to usable variables
        start_node = route[0]
        end_node = route[-1]

        # initialize list to add each edge to 
        involved_edges_list = []

        # loop over indicies in route list
        for index in range(len(route)): 


            if index < (len(route)-1):
                # if the index is not of the last item, make an edge from slicing the route list
                curr_edge = tuple(route[index:index+2]) # note: add two because indexing is non-inclusive
                # add edge to involved edges list 
                involved_edges_list.append(curr_edge)

        return involved_edges_list
    else: 
        # if the route is just one node, return an empty list -- there are no edges. 
        return []

def get_total_length_shortest_path(edges_list, graph):
    
    """

    Given a list of edges in a route, 
    return the length of the route 
    (sum of the lengths of all edges in list).
    
    """
    # get nodes and edges dataframes
    nodes, edges = ox.graph_to_gdfs(graph)

    # print(edges)
    
    # intialized length to zero
    total_length = 0
    
    for edge in edges_list:

        # print("\n\nedge:", edge)
        
        # get var for start and end node of edge 
        start_node = edge[0]
        end_node = edge[1]
        
        # get dataframe object for edge defined by two nodes
        curr_edge = edges.loc[(edges['u'] == start_node) & (edges['v'] == end_node)]
        
        # try the opposite order?
        curr_edge = edges.loc[(edges['v'] == start_node) & (edges['u'] == end_node)]

        # There is something funky with getting length 
        # (maybe a built-in name as well as a edges df column name?)
        # -- this is why I had to get length from 
        # curr_edge in a more verbose way
        
        # print("curr_edge:", curr_edge)

        # print("\ncurr_edge:", curr_edge['v'].values, curr_edge['u'].values)
        
        # print("\ncurr_edge['length']:", curr_edge['length'])
        
        # print("\ncurr_edge['length'].values[0]", curr_edge['length'].values[0])
        
        edge_length = curr_edge['length'].values[0]
        
        # print("\nedge:", edge)
        # print("\nlength:", edge_length)
        
        # add edge's length to the total length
        total_length = total_length + edge_length
        
    return total_length

def get_dict_length_pairings_lists(possible_pairings_list, graph):
    
    """ 
    Given a possible pairings list, 
    return dict of pairing list 
    and total distance of pairs in list
    
    example input: 
    [
    [(65294615, 65320193), (65313455, 65320188)], 
    [(65294615, 65313455), (65320193, 65320188)], 
    [(65294615, 65320188), (65320193, 65313455)]
    ]
    
    example ouput:
    {
    ((65294615, 65320193), (65313455, 65320188)): 506.546, 
    # expected to be equal because they contain the same edges
    ((65294615, 65313455), (65320193, 65320188)): 506.546, 
    ((65294615, 65320188), (65320193, 65313455)): 330.56899999999996
    }
    
    """
    # initialize dict for pairing list and total length
    pairings_lengths_dict = {}
    
    # look at each possible pairing list
    for possible_pairing_list in possible_pairings_list:
        
        # make possible pairing list into a tuple, so it can be a dict key
        possible_pairings_tuple = tuple(possible_pairing_list)

        # initialize total length of parings in list to 0
        total_pairing_length = 0

        for pair in possible_pairings_tuple:
            
        # look at each pair in current possible pairings tuple 
        
            # print("  current pair:", pair)

            # get shortest path distance for pair of nodes: 
            
            # make var for start and end node for pair
            start_node = pair[0]
            end_node = pair[1]

            # get the shortest route between the two nodes
            route = get_shortest_path_route_two_nodes(start_node, end_node, graph)
            # print("\n   route:", route)

            # get all edges in shortest route (because route alone is a list of nodes)
            route_edges_list = get_route_edges_from_shortest_path(route)
            # print("   route edges:", route_edges_list)

            # get total route length
            total_route_length = get_total_length_shortest_path(route_edges_list, graph)
            # print("   total route length:", total_route_length)

            # get total added length for pairings_list
            total_pairing_length = total_pairing_length + total_route_length
        
            # print("\n\nTOTAL PAIRING ADDED LENGTH:", total_pairing_length)
            # print("\n-----------\n")
        
        pairings_lengths_dict[possible_pairings_tuple] = total_pairing_length
        
    return pairings_lengths_dict

def get_optimal_pairing_list_dict(length_pairings_lists_dict):
    
    """ 
    Take a list of odd nodes pairing options (a list of lists), 
    return optimal pairing list. 
    """
    
    # initialized optimal dist to infinity 
    
    current_optimal_pairings_list = []
    current_optimal_dist = math.inf 
    
    # look at the added distance for each pairings list
    for pairing in length_pairings_lists_dict:
        
        # update the current optimal dist if the dist for the parings list is less than current optimal dist
        if length_pairings_lists_dict[pairing] < current_optimal_dist:
        
            # if the added distance for the current pairings is less than the current optimal dist,
            # replace the current optimal vars 
            
            # print(pairing, length_pairings_lists_dict[pairing])
            
            current_optimal_dist = length_pairings_lists_dict[pairing]
            current_optimal_pairings_list = pairing
            
    
    # confirm that the current_optimal_pairings_list goes with current_optimal_dist
    
    calc_op_dist = current_optimal_dist
    assoc_op_dist = length_pairings_lists_dict[current_optimal_pairings_list]
    
    # print("TEST: \n  optimal distance is assoc. with optimal pairing:", calc_op_dist == assoc_op_dist)
    
    if calc_op_dist == assoc_op_dist:
    
        return {'optimal_pairing' : current_optimal_pairings_list, 

                'optimal_added_distance' : length_pairings_lists_dict[current_optimal_pairings_list]

    #             ,'twice_traverse_edges' : None # get a list of edges involved in the pairings
               }
    else:
        return None

def get_all_double_back_edges(optimal_pairing_list_dict, graph):
    """ 
    POSSIBLE DUPLICATE FUNCTION

    Given dictionary for optimal pairing and the length of the pairing, 
    return list of edges in the optimal pairing (ie. the edges that will
    need to be traversed twice.)
    
    The returned list contains all edges that are included in the
    routes betwen each odd node - the edges that make the odd nodes
    even.
    
    """
    
    # get tuple which contains start/end tuples for optimal pairing 
    optimal_pairing_pairs = optimal_pairing_list_dict['optimal_pairing']

    # initialize list of edges that will need to be traversed twice
    twice_traversal_edges = []
    
    # for each pair in optimal pairings, get all the edges involved in the shorted path between the 
    # nodes
    for pair in optimal_pairing_pairs:
        # print()
        # print("pair:", pair)
        
        route = get_shortest_path_route_two_nodes(pair[0], pair[1], graph)
        
        # print("route:", route)
        # get all edges in shortest route
        route_edges_list = get_route_edges_from_shortest_path(route)
        
        # print("edges in route:", route_edges_list)
        
        twice_traversal_edges = twice_traversal_edges + route_edges_list

    # print("\n\nTwice traversal edges:", twice_traversal_edges, "\n\n")
    
    return twice_traversal_edges

def make_traversal_dict_with_added_edges(twice_traversal_list, graph):
    """
    Given a list of edges that need to be traversed twice and a graph,
    
    Return a dictionary with each edge and the count of times it 
    will need to be traversed. 
    
    """
    
    # print("twice traversal list:", twice_traversal_list)
    
    # get default dictionary of edges and traversal counts 
    
    # edge_traversals_dict_eulerian = make_dict_of_edge_traversals(get_edges_list(graph))
    
    # make a default dictionary of edges and one traversal
    edge_traversals_dict_eulerian = {}
    
    for edge in list (graph.edges):
        
        # the default graph G will have consider the same edge two time
        # ie. A,B and B,A will both be in the edges list 
        
        # if the reversed order edge is not already in the dict add the edge
        if edge[0:2][::-1] not in edge_traversals_dict_eulerian:
        
            edge_traversals_dict_eulerian[edge[0:2]] = 1
    
    # for each edge in list of edges that will need to be traversed twice...
    for edge in twice_traversal_list:
        
        # get the alternative id for the edge -- ie. the tuple in reversed order
        reversed_edge_order = edge[::-1]
        
        # if og edge name is a key in the edge traversals dict, increment the traversals count
        #if edge in edge_traversals_dict:

        if edge in edge_traversals_dict_eulerian:
                
            edge_traversals_dict_eulerian[edge] += 1
        
        # if the reversed edge id is a key in the edge traversals dict, increment the traversals count
        # elif reversed_edge_order in edge_traversals_dict:

        elif reversed_edge_order in edge_traversals_dict_eulerian:
            
            edge_traversals_dict_eulerian[reversed_edge_order] += 1
            
        else:
            print(f"EDGE NOT IN DICT: {edge} is not in {edge_traversals_dict_eulerian}")
    
    # return a dict where the twice traversal edges have '2' as their values
    return edge_traversals_dict_eulerian
