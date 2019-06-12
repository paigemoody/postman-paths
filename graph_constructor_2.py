from networkx import shortest_path

from classes import OSMGraph

import json
import time

def get_bbox_from_geojson(geojson_dictionary):
    """From feature collection geojson of a bounding box
    return bbox list --> [north, south, east, west]
    """
    geojson_dictionary = json.loads(geojson_dictionary)
    all_lats = []
    all_lngs = []
    
    feature = geojson_dictionary['features'][0]
    coordinates = feature['geometry']['coordinates'][0]

    for coord in coordinates:

        # [lng, lat]
        lng = coord[0]
        lat = coord[1]
        all_lats.append(lat)
        all_lngs.append(lng)

    max_lat = max(all_lats)  # north
    min_lat = min(all_lats) # south

    max_lng = max(all_lngs) # east 
    min_lng = min(all_lngs) # west

    bbox = [max_lat, min_lat, max_lng, min_lng]
    print("\n\n\nCALCULATED bbox:", bbox)
    return bbox

def get_odd_nodes(nodes_dict):
    """ Given a nodes dictionary return 
    list of odd nodes -- nodes that have 'is_odd = True'.
    """
    odd_nodes_list = []

    for node in nodes_dict:
        if nodes_dict[node]['is_odd'] == True:
            odd_nodes_list.append(node)

    print("\n\n\n\nLEN ODD NODES",len(odd_nodes_list))
    return odd_nodes_list

def get_list_of_all_pairs_lists(input_lst):
    """
    Takes in a list of items and returns a list of 
    lists, each containing tuples that represent 
    pairings of list items. Each item can appear only
    once in a list of pairs.  

    >>> alpha_list = ['A','B','C','D']
    >>> get_list_of_all_pairs_lists(alpha_list)
    [[('A', 'B'), ('C', 'D')], [('A', 'C'), ('B', 'D')], [('A', 'D'), ('B', 'C')]]
    """
    # handle possible case of empty list input 
    if len(input_lst) == 0:
        return [[]]
    
    # base case - if list is two items long
    elif len(input_lst) == 2:
        return [[(input_lst[0], input_lst[1])]]
    
    else: 
        combos = []
        first_item = input_lst[0] # first item in list 
        
        # look at all items after first item - pair each with first item
        for i in range(1,len(input_lst)):
            
            pair = (first_item,input_lst[i])
            other_items_list = input_lst[1:i] + input_lst[i+1:]
            
            for rest in get_list_of_all_pairs_lists(other_items_list):
                
                combos.append([pair] + rest)
                
    return combos


def get_list_of_all_pairs_lists_short(odd_nodes):
    """Given list of nodes, output a list of three basic pairing options:

    1. neighbors, starting at index 0
    2. neighbors, starting at index 1
    3. pairs starting from (first, last) then (second, second to last)
    """

    print("\n\n\n\n\n\n ODD NODE COUNT:", len(odd_nodes))

    all_pairs_list = [] 
    
    pair_list = [] 

    all_nodes = odd_nodes


    pairing_options = [] 
    
    # do twice - to get immediate neighbors start at 0 and then 1 
    # list1 = slice by neighbors
    # list2 = slice by neighbors - shifted 1 -> to pair up first and last 
    for k in range(0,2):  
        
        curr_list = [] 
        total_nodes = len(all_nodes)

        i = k
        while i < total_nodes: # there will be len/2 pairs in each option 

            pair_first = all_nodes[i]

            next_index = (i + 1) % len(all_nodes) # get the remainder
            pair_second = all_nodes[next_index]

            pair = (pair_first, pair_second)
            
            curr_list.append(pair)

            i += 2

        pairing_options.append(curr_list)
        
    # get pairs moving in from the outside - in (eg first pairs with last, second pairs with second to last)
    curr_list = [] 
    first = 0 
    last = -1 
    
    mid_point = (len(all_nodes) / 2)
    
    while first < mid_point:
        pair_first = all_nodes[first]
        pair_second = all_nodes[last]
        
        pair = (pair_first, pair_second) 
                
        curr_list.append(pair)
        
        first += 1 
        last -= 1
    pairing_options.append(curr_list)   
       
    return pairing_options 


def get_shortest_route_two_nodes(start_node, end_node, graph_instance):
    """ Given a start and end node, 
    return sequenced list of nodes included in shortest route
    between the nodes.
    """
    route = shortest_path(graph_instance.ox_graph, start_node, end_node, weight='length')
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

# def get_route_length(route_edges_list, graph_instance):
def get_route_length(route_edges_list, edges_dict):
    """
    Given a list of edges in a route, and a dictionary
    which includes those edges 
    return the total length of the route 
    (sum of the lengths of all edges in list).
    """
    total_edges_length = 0

    for edge in route_edges_list:
        edge = edge 

        # handle edge keys that are reversed 
        if edge not in edges_dict:

            edge = edge[::-1]
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
    
    #>>> get_dict_pairings_lists_lengths([[(65294615, 65320193), (65313455, 65320188)], [(65294615, 65313455), (65320193, 65320188)], [(65294615, 65320188), (65320193, 65313455)]], ORIG_GRAPH)
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
            total_route_length = get_route_length(shortest_route_edges, graph_instance.edges_dict)
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

    return  graph_instance

## over-arching function that takes a bounding box and returns 
## a dict with twice traversal edges marked 

def get_eulerian_graph_edges(bbox, source):
    """Given a bounding box list [north,south,east,west],
    return a dictionary of edges with metadata and traversal count.
    """
    osm_graph = OSMGraph(bbox, source)
    # input all nodes  and get odd nodes, update node attributes
    odd_nodes = get_odd_nodes(osm_graph.nodes_dict)

    # initialize all_pairs_list
    all_pairs_list = [] 

    # if there are 6 or fewer odd nodes look for all possible options,
    # otherwise look for just three basic pairing options 

    if len(odd_nodes) <= 10:
        print("ROBUST PAIRING FUNCTION")
        all_pairs_list = get_list_of_all_pairs_lists(odd_nodes)

    else:
        print("CHEAP PAIRING FUNCTION")
        all_pairs_list = get_list_of_all_pairs_lists_short(odd_nodes)
    
    for item in all_pairs_list:
        print("\n\nPair option:", item)
        print("Pair option len:", len(item))

    dict_pairings_lists_lengths = get_dict_pairings_lists_lengths(all_pairs_list, osm_graph)
    twice_traversals_edges = get_twice_traversals_edges(dict_pairings_lists_lengths)
    updated_graph_instance = update_twice_traversal_edges(twice_traversals_edges, osm_graph)
    return updated_graph_instance


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # NORTH = 37.7599 # max lat 
    # SOUTH = 37.7569 # min lat
    # EAST = -122.3997 # max lng
    # WEST = -122.4023 # min lng 
    # SOURCE = "OSM"

    # bbox = [NORTH, SOUTH , EAST, WEST] # min lng 

    # bbox = get_bbox_from_geojson('test_bbox_input.geojson')

    # osm_graph = OSMGraph(bbox, source)

    # print("bbox")

    # updated_graph_inst = get_eulerian_graph_edges(bbox, "OSM")

    # for edge in updated_graph_inst.edges_dict:
    #     print()
    #     print(edge, "\n", updated_graph_inst.edges_dict[edge])





