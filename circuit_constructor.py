import networkx as nx 
from graph_constructor_2 import get_eulerian_graph_edges, get_bbox_from_geojson
from random import choice



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

    current_edges_on_graph_list = make_edges_list(updated_graph_instance.edges_dict)

    current_node = start_node 

    node_visit_order = [current_node]
    edge_visit_order = []


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
        
        # update edge traveral list with edge just traversed
        edge_traversed = (current_node, edge_to_traverse_list[0])

        edge_visit_order.append(edge_traversed)

        current_node = edge_to_traverse_list[0]
        
        # add the new current node to the nodes visit order list 
        node_visit_order.append(current_node)
        
    return {
            "node_visit_order": node_visit_order, 
            "edge_visit_order": edge_visit_order
            }


if __name__ == '__main__':

    # import doctest
    # doctest.testmod()

    import time

    start = time.time()

    # test bbox
    # NORTH = 37.7599 # max lat 
    # SOUTH = 37.7569 # min lat
    # EAST = -122.3997 # max lng
    # WEST = -122.4023 # min lng  
    SOURCE = "OSM"

    

    # 3. get graph with updated traversals count 
    # bbox = [NORTH, SOUTH , EAST, WEST] # min lng 

    bbox = get_bbox_from_geojson('test_bbox_input.geojson')


    SOURCE = "OSM"
    updated_graph_inst = get_eulerian_graph_edges(bbox, SOURCE)

    # 2. get start node 
    start_node = choice(list(updated_graph_inst.nodes_dict.keys()))

    # # 3. calculate euler circuit 

    euler_circuit_output = make_euler_circuit(start_node, updated_graph_inst)

    print("\n\nEuler circuit node order:")
    print("node_visit_order:", euler_circuit_output["node_visit_order"])
    print("edge_visit_order:", euler_circuit_output["edge_visit_order"])

    print("\n\nroads order:")

    for edge in euler_circuit_output["edge_visit_order"]:
        print("\n\n")
        print(edge, ": ")
        if edge in updated_graph_inst.edges_dict:
            print(updated_graph_inst.edges_dict[edge]['name'])
        else:
            edge = edge[::-1]
            print(updated_graph_inst.edges_dict[edge]['name'])



    print("\n\nProcess time:", time.time() - start, "seconds")



