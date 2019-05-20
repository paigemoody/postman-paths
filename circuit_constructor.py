import networkx as nx 
from graph_constructor_2 import get_eulerian_graph_edges

def make_edges_list(edges_dict):
    """ Given dict of edges and attributes return a list of all edges
    if the edge has num_traversals :2, add to output list twice

    >>> make_edges_list({ ('A','B') : {'num_traversals': 1},('A','D') : {'num_traversals': 1},('B','C') : {'num_traversals': 1},('B','E') : {'num_traversals': 2},('C','E') : {'num_traversals': 2},('C','D') : {'num_traversals': 1}})
    [('A', 'B'), ('A', 'D'), ('B', 'C'), ('B', 'E'), ('B', 'E'), ('C', 'E'), ('C', 'E'), ('C', 'D')]
    """
    all_edges_list = []

    for edge in edges_dict:

        num_traversals = edges_dict[edge]['num_traversals']

        for i in range(num_traversals):
            all_edges_list.append(edge)

    return all_edges_list

def get_bridges(edges_list):
    """Take a list of edges, return a list of all bridges in the graph.
    
    Note: bridges returned are true bridges, meaning that they are bridges
    calculated by networkx without the edges that have multiple traverses 
    remaining. 

    >>> get_bridges([('A', 'B'),('C', 'D'),('D', 'A'),('C', 'A'), ('C', 'A')])
    [('A', 'B')]

    >>> get_bridges([('A', 'B'), ('A', 'B'),('C', 'D'),('D', 'A'),('C', 'A'), ('C', 'A')])
    []

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
        # print()
        if edge in mult_trav_remaining:
            continue
            # print()
            # print(f"bridge {edge} is in {mult_trav_remaining}")
        elif edge[::-1] in mult_trav_remaining: 
            continue
            # print()
            # print(f"bridge {edge} REVERSED is in {mult_trav_remaining}")
        else:
            # print(f"bridge {edge} is NOT in {mult_trav_remaining}")
            
            bridges_reduced.append(edge)
    
    # return a list of true bridges
    return bridges_reduced


def get_all_conn_edges_remaining_in_graph(current_node, remaining_edges, nodes_dict):
    """Takes current node, a list of remaining edges in graph, and a dictionary of nodes
    and their corresponding edges. 
    
    Returns a list of all edges connected to the input node that are still in the graph.
    
    >>> input_current_node = 'A'
    >>> input_remaining_edges = [('A', 'B'), ('A', 'B'),('D', 'C'), ('A', 'D')]
    >>> input_nodes_dict = { 'A': {'connected_edges': [('A', 'B'), ('A', 'D')]}, 'B': {'connected_edges': [('B', 'C'), ('B', 'A')]}}
    >>> output = get_all_conn_edges_remaining_in_graph(input_current_node, input_remaining_edges, input_nodes_dict)
    >>> (((('A', 'D') in output) and (('A', 'B') in output)))
    True
    """
    
    # remove duplicate edges from remaining edges by makeing a set

    remaining_edges_unique_set = set(remaining_edges)

    # print("\nremaining_edges_unique_set:", remaining_edges_unique_set)

    all_conn_edges_in_original_graph_set = set(nodes_dict[current_node]['connected_edges'])

    # print("\nall_conn_edges_in_original_graph_set:", all_conn_edges_in_original_graph_set)

    remaining_edges_conn_to_node = remaining_edges_unique_set.intersection(all_conn_edges_in_original_graph_set)

    # print("\nremaining_edges_conn_to_node:", remaining_edges_conn_to_node)
    

    return list(remaining_edges_conn_to_node)

 
def choose_edge_to_traverse(current_node, possible_next_edges, current_bridges):
    """
    Takes in the current node, a list of possible next edges for node 
    (ie. all connected edges remaining in graph)
    and a list of bridges on the graph.
    
    Returns a tuple of the next edge that should be traversed. 


    >>> current_node = 'A'
    >>> possible_next_edges = [('A','B'), ('A', 'D')]
    >>> current_bridges = [('A','B'), ('B', 'C')]
    >>> choose_edge_to_traverse(current_node,possible_next_edges,current_bridges)
    ('A', 'D')

    """
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


def make_euler_circuit(start_node, updated_graph_instance): 
    """ Given a start node and graph instance (with updated num traversal) 
    attributes in edges_dict, return a list contain the sequence in which
    the graph's nodes should be visited.
    """

    print("Start node:", start_node)

    current_edges_on_graph_list = make_edges_list(updated_graph_instance.edges_dict)

    current_node = start_node 

    node_visit_order = [current_node]


    while len(current_edges_on_graph_list) > 0:
        # while there are still edges on the graph, keep traversing

        current_bridges_on_graph = get_bridges(current_edges_on_graph_list)

        edges_conn_to_current_node = get_all_conn_edges_remaining_in_graph(current_node, 
                                                                           current_edges_on_graph_list, 
                                                                           updated_graph_instance.nodes_dict)

        edge_to_traverse = choose_edge_to_traverse( current_node, 
                                                    edges_conn_to_current_node, 
                                                    current_bridges_on_graph)


        if edge_to_traverse in current_edges_on_graph_list:

            current_edges_on_graph_list.remove(edge_to_traverse)

        else:

            current_edges_on_graph_list.remove(edge_to_traverse[::-1])

        edge_to_traverse_list = list(edge_to_traverse)
        # remove current node from edge to traverse
        edge_to_traverse_list.remove(current_node)
        # update current node to be the only node left in the edge list
        
        current_node = edge_to_traverse_list[0]
        
        # add the new current node to the nodes visit order list 
        node_visit_order.append(current_node)
        
    return node_visit_order

# def make_euler_circuit(start_node, graph):
    
    
    # # print("Start node:", start_node)
    
    # # SET UP EULER GRAPH
    # # get all odd nodes on graph 
    # odd_nodes = get_odd_nodes(graph.nodes_dict)
    
    # print("\nodd nodes:", odd_nodes)
    
    # # get all possible pairings for odd nodes in graph
    # # nodes_dict = make_nodes_dict(G)
    
    # # print("\nnodes dict:", nodes_dict)

    # print("\nnodes dict:", graph.nodes_dict)
    
    # # STARTS GETTING REAL SLOW
    
    # # get list of all possible pairings of odd nodes:
    # possible_pairings_list = get_list_of_all_pairs_lists(odd_nodes)
    
    # print("\npossible_pairings_list:", possible_pairings_list)
    
    # # get the length of each possible pairing of odd nodes 
    # length_pairings_lists_dict = get_dict_length_pairings_lists(possible_pairings_list, graph)
    
    # print("\nlength pairings lists dict:", length_pairings_lists_dict)
    
    # # get the odd nodes pairing that has the shortest distance 
    # optimal_pairing_list_dict = get_optimal_pairing_list_dict(length_pairings_lists_dict)
    
    # print("\noptimal_pairing_list_dict:", optimal_pairing_list_dict)
    
    # # get list of edges that will need to be traversed twice 
    # twice_traversal_list = get_all_double_back_edges(optimal_pairing_list_dict, graph)
    
    # print("\ntwice_traversal_list:", twice_traversal_list)
    
    # # get dict of edges and how many times each needs to be traversed 
    # edge_traversals_dict_eulerian = make_traversal_dict_with_added_edges(twice_traversal_list, graph) 
    
    # print("\nedge_traversals_dict_eulerian:", edge_traversals_dict_eulerian)
    
    # # get list of all edges that need to be traversed, multiple traversal edges are included multiple times
    # all_edges_in_euler_graph = get_list_of_edges_by_traversal_count(edge_traversals_dict_eulerian)

    # print("\nall_edges_in_euler_graph:", all_edges_in_euler_graph)
    
    # # ---- # 
    
    # print("\n\n\n\n\n\n\n\nBUILDING CIRCUIT")
    
    # # GET EULER CIRCUIT 
    
    # # make list of edges currently on graph: 
    # current_edges_on_graph_list = all_edges_in_euler_graph
    
    # # initialize current node 
    # current_node = start_node 
    
    # # initialize a list the contains the order of node visists with the start node
    
    # node_visit_order = [current_node]
    
    # print("--------START-WALKING--------")
    
    # while len(current_edges_on_graph_list) > 0:
        
        # print("Node visit order:", node_visit_order)
        
        # print("\n\nCURRENT NODE:", current_node)
        
        # print edges currently on the graph
        # print("\nedges currently on graph:", current_edges_on_graph_list )

        # get the bridges on the initial graph
        # current_bridges_on_graph = get_bridges(current_edges_on_graph_list)
        # print("\nbridges currently on graph:", current_bridges_on_graph)

        # get all the connected edges in initial graph for the current node 
        # edges_conn_to_current_node = get_all_conn_edges_remaining_in_graph(current_node, 
        #                                                                    current_edges_on_graph_list, 
        #                                                                    nodes_dict)
        # print(f"\ncurrent node: {current_node} is still connected to: {edges_conn_to_current_node}")

        # get the next edge to traverse 
        # edge_to_traverse = choose_edge_to_traverse(current_node, edges_conn_to_current_node, current_bridges_on_graph)
        # print(f"\nedge_to_traverse:", edge_to_traverse)

        # remove edge just traversed from current_edges_on_graph_list
        ## you don't know the order of the nodes in the edge in the current_edges_on_graph_list,
        ## so you have to check both
        
        # print("\nlen of current_edges_on_graph_list BEFORE removing one item:", len(current_edges_on_graph_list))
        
        # if edge_to_traverse in current_edges_on_graph_list:
        #     current_edges_on_graph_list.remove(edge_to_traverse)
        # else:
        #     current_edges_on_graph_list.remove(edge_to_traverse[::-1])
        
        # print("\nlen of current_edges_on_graph_list AFTER removing one item:", len(current_edges_on_graph_list))
        
        # update current node to be node in edge_to_traverse that is not the current node
        ## make edge a list so that you can remove the current node
        
        # print("\ncurrent node BEFORE update:", current_node)
        # edge_to_traverse_list = list(edge_to_traverse)
        ## remove current node from edge to traverse
        # edge_to_traverse_list.remove(current_node)
        ## update current node to be the only node left in the edge list
        
        # current_node = edge_to_traverse_list[0]
        # print("\ncurrent node AFTER update:", current_node)
        
        # add the new current node to the nodes visit order list 
        # node_visit_order.append(current_node)
        
        # print("\n\n\n----------WALKING-----------")

    # return(node_visit_order)

if __name__ == '__main__':

    # import doctest
    # doctest.testmod()

    import time

    start = time.time()

    # test bbox
    NORTH = 37.7599 # max lat 
    SOUTH = 37.7569 # min lat
    EAST = -122.3997 # max lng
    WEST = -122.4023 # min lng  
    SOURCE = "OSM"

    # 1. get start node 
    start_node = 65294616

    # 2. get graph with updated traversals count 
    bbox = [NORTH, SOUTH , EAST, WEST] # min lng 
    updated_graph_inst = get_eulerian_graph_edges(bbox, SOURCE)

    # # 3. calculate euler circuit 
    print("\n\nEuler circuit node order:")
    print(make_euler_circuit(start_node, updated_graph_inst))

    print("\n\nProcess time:", time.time() - start, "seconds")



