import networkx as nx 
from graph_constructor_2 import get_eulerian_graph_edges, get_bbox_from_geojson
from random import choice
from shapely.geometry import shape
import json



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

    # print("all edges:", edges_list)
    
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
    # print("\n\n\n\ncurrent_node:", current_node)
    # print("possible next edges: ", possible_next_edges)


    for possible_next_edge in possible_next_edges:
        
        # print(f"\n\nREVIEWING: {possible_next_edge}:")
    
        if possible_next_edge in current_bridges or possible_next_edge[::-1] in current_bridges:
            # print(f" {possible_next_edge} or {possible_next_edge[::-1]} in current_bridges")
            bridge_next_edge_options.append(possible_next_edge)
        else: 
            #print(f" {possible_next_edge} AND {possible_next_edge[::-1]} NOT in current_bridges")                               
            non_bridge_next_edges_options.append(possible_next_edge)
    
    # print("\nnon_bridge_next_edges_options:", non_bridge_next_edges_options)
    # print("bridge_next_edge_options:", bridge_next_edge_options)
    
    
    # if non_bridge_next_edges is not empty, return the first item in non_bridges 
    if len(non_bridge_next_edges_options) > 0:
        return non_bridge_next_edges_options[0]
    
    # if non_bridge_next_edges is empty, return the first item in bridges 
    else:
        return bridge_next_edge_options[0]


def make_node_geojson(graph_instance):
    """
    Input: graph instance with node visit order attribute

    Output: geojson feature collection of node points with 
    all node metadata as properties.
    """

    # add visit order to nodes_dict properties, so that each node can
    # be a single feature in the feature collection 

    node_visit_order =  graph_instance.node_visit_order

    # make a dict of nodes and their visits order as a list 
    node_visit_dict = {} 

    curr_order_num = 1 

    for node in node_visit_order:

        if node not in node_visit_dict:

            node_visit_dict[node] = [curr_order_num]
        else: 
            node_visit_dict[node].append(curr_order_num)

        curr_order_num += 1

    # print("\n\n\nnode_visit_dict:", node_visit_dict, "\n\n\n")

    node_features_list = [] 

    for node in graph_instance.node_visit_order:
        # get node attributes from nodes dict 

        # check if node is the start node
        # use string in order to enable 
        # data-driven styling in the map - for start node

        if node == node_visit_order[0]:
            start_node = 'true'
        else:
            start_node = 'false'

        

        node_attributes = graph_instance.nodes_dict[node]

        if node_attributes["is_odd"] == True:
            was_odd = 'true'

        else:
            was_odd = 'false'
        # print("\n\nnode_attributes:",node_attributes)

        # make list of point coords from shapely geometry
        point_shapely = node_attributes['geometry']
        point_coords_list = [ list(coord_tuple) for coord_tuple in list(shape(point_shapely).coords)]

        # build edge feature dict from graph attributes 
        node_feature = {
                          "type": "Feature",
                          "properties": {
                            # node identifier is the osmid
                            "osmid" : float(node),
                            "connected_edges" : node_attributes['connected_edges'],
                            "visit_order": node_visit_dict[node],
                            # "was_odd" : node_attributes["is_odd"],
                            "was_odd" : was_odd,
                            "start_node": start_node
                          },
                          "geometry": {
                            "type": "Point",
                            "coordinates": point_coords_list[0]
                          }
                        }


        node_features_list.append(node_feature)

    nodes_feature_collection = {
                                "type": "FeatureCollection",
                                "features": node_features_list
                                }
    # transform dict into valid json                            
    return json.dumps(nodes_feature_collection)

def make_edge_geojson(graph_instance):
    """ 
    Input: updated graph instance - has edge visit order attribute

    Output: geojson feature collection of edge linestrings with 
    all edge metadata as properties.  
    """

    edges_dict = graph_instance.edges_dict

    edge_visit_order =  graph_instance.edge_visit_order


    # make a dict of nodes and their visits order as a list 
    # to be added as a visit order property of each edge feature
    edge_visit_dict = {} 

    curr_order_num = 1 

    for edge in edge_visit_order:

        # align the order of the tuple so it 
        # matches up with a tuples in edge_visit_order 

        if edge not in edge_visit_dict:

            edge_visit_dict[edge] = [curr_order_num]
        else: 

            edge_visit_dict[edge].append(curr_order_num)

        curr_order_num += 1


    # loop over unique edges, add each as a feature in the feature collection

    edge_features_list = [] 
    for edge in list(edge_visit_dict.keys()):

        # check both original edge order and reversed edge order
        # order could have been rearranged in earlier computation
        edge_attributes = None

        if edge not in edges_dict: 
            edge_attributes = graph_instance.edges_dict[edge[::-1]]
        
        else:
            edge_attributes = graph_instance.edges_dict[edge]
        
        # edge_attributes = graph_instance.edges_dict[edge]

        # transform the shapely object into a list of coordinate lists 
        line_shapely = edge_attributes['geometry']
        # shpely coords comes back as a list of tuples, 
        # so we transform each tuple into a list to creata list of lists:
        line_coords_list = [ list(coord_tuple) for coord_tuple in list(shape(line_shapely).coords)]


        # some ways (edges) have more than one osmid because they are 
        # part of more than one way - to handle this while also handling
        # the conversion of numpy 64 ints to regular ints
        # I do something different for wayids that are lists and 
        # way ids that are numpy64 ints 

        converted_osm_id = ""

        if type(edge_attributes['osmid']) is list:
            # if osmid is a list, keep as list but make each item a regular
            # python int rather than numpy64

            converted_osm_id = []

            for osmid in edge_attributes['osmid']: 

                converted_osm_id.append(float(osmid))

        else: 

            # print("edge_attributes['osmid']", edge_attributes['osmid'])
            # print("type(edge_attributes['osmid'])",type(edge_attributes['osmid']) )
            # if osmid is not a list just convert the numpy64 int into
            # a regular int 
            converted_osm_id = float(edge_attributes['osmid'])




        # print("\n\n\n\n\nLOOKING AT EDGE OSMID TYPE")

        # print("\nOG type:", edge_attributes['osmid'])

        # print("\n made to string type:", str(edge_attributes['osmid']))
        # build edge feature dict from graph attributes 
        edge_feature = {
                          "type": "Feature",
                          "properties": {
                            "num_traversals": edge_attributes['num_traversals'],
                            "length" : edge_attributes['length'], 
                            "hwy_type" : edge_attributes['hwy_type'], 
                            "road_name" : edge_attributes['name'], #road name
                            # need to transform numpy.int64 into str?
                            "osmid" : converted_osm_id,    
                            "visit_order" : edge_visit_dict[edge],     

                            # add dict of node information - add coordinates proprety for
                            # each connected node  

                            "nodes": {
                                        edge[0] : [list(coord_tuple) for coord_tuple in (list(shape(graph_instance.nodes_dict[edge[0]]['geometry']).coords))], 

                                        edge[1] : [list(coord_tuple) for coord_tuple in (list(shape(graph_instance.nodes_dict[edge[1]]['geometry']).coords))] 
                            }
                                    
                          },
                          "geometry": {
                            "type": "LineString",
                            "coordinates": line_coords_list
                          }
                        }

        # add feature dict to list of features 
        edge_features_list.append(edge_feature)

    # onces all features (edge linestrings) have been added to the features list,
    # add feature list to edges_feature collection

    edges_feature_collection = {
                                "type": "FeatureCollection",
                                "features": edge_features_list
                                }
    # transform dict into valid json                            
    return json.dumps(edges_feature_collection)


def make_route_geojson(graph_instance):
    """ 
    Input: updated graph instance - has edge visit order 
    and node visit order attributes.

    Output: geojson Feature collection with one LineString feature
    which contains all coordinates in graph, order by visit order. 
    """

    # # instantiate list of coordinates 
    coordinates = [] 

    # # instantiate counter for route length
    # # to be added when each edge is "traversed"
    route_length = 0 

    node_visit_order = graph_instance.node_visit_order
    edge_visit_order = graph_instance.edge_visit_order

    edges_dict = graph_instance.edges_dict
    nodes_dict = graph_instance.nodes_dict

    edge_num = 0 

    print("node_visit_order:", node_visit_order)

    for edge in edge_visit_order:



        # print("edges_dict[edge]",edges_dict[edge])

        first_node = node_visit_order[edge_num]
        first_node_geometry = nodes_dict[first_node]['geometry']
        first_node_coords = [list(coord_tuple) for coord_tuple in list(shape(first_node_geometry).coords)]

        # edge id might be reversed - so cheeck for that in order to
        # do the look-up with the correct key
        # if the edge in current order is not in the edges dict, reverse the 
        # tuple order, then reset edge to that id
        if edge not in edges_dict:
            edge = edge[::-1]
        else: 
            edge = edge 

        edge_geometry = edges_dict[edge]['geometry']
        edge_geometry_coords = [ list(coord_tuple) for coord_tuple in list(shape(edge_geometry).coords) ]

        edge_len = edges_dict[edge]['length']

        route_length += edge_len

        # check if first node is first in edge coord, if not , reverse
        # the order of the points in the line so that 
        # the first node is first 
        if edge_geometry_coords[0] != first_node_coords[0]:

            print(".......reverse coords!")

            print("og coords:",edge_geometry_coords )

            edge_geometry_coords.reverse()

            print("rev coords:",edge_geometry_coords )


        print("\n\n\nfirst node:", first_node)
        print("\nfirst node coords:", first_node_coords)
        print("\nedge_geometry_coords", edge_geometry_coords)

        # if there are just two coords in edge line, add the
        # coordinates of the first node 
        if len(edge_geometry_coords) == 2: 

            coordinates.append(first_node_coords[0])

        # if the edge has more than two coordinates,
        # add all coordinates, except the last (that will be
        # taken care of by next node)
        else:

            for i in range(0, (len(edge_geometry_coords) - 1)):

                coordinates.append(edge_geometry_coords[i])



        # if it's the last edge, add the final coordinate of the 
        # edge -- to return to start 

        print("\nedge_num", edge_num)
        print("total edges", len(edge_visit_order))
        print("last edge index:", (len(edge_visit_order) - 1))

        if edge_num == (len(edge_visit_order) - 1): 

            print("last edge!!")

            coordinates.append(edge_geometry_coords[-1])

            # coordinates.append(edge_geometry_coords[-1])

        # increment edge num 
        edge_num += 1 

    # add last node of last edge (should = first node) to coords:

    route_feature_collection = {
                                "type": "FeatureCollection",
                                "features": [
                                    {
                                      "type": "Feature",
                                      "properties": { "route_length_km" : route_length/1000},
                                      "geometry": {
                                        "type": "LineString",
                                        "coordinates": coordinates
                                    }
                                }]
                            }
     
    return json.dumps(route_feature_collection)
    # return None


def make_euler_circuit(start_node, updated_graph_instance): 
    """ Given a graph instance (with updated num traversal) 
    attributes in edges_dict, return a list contain the sequence in which
    the graph's nodes should be visited.

    Choose the start node randomly in server file.

    """

    current_edges_on_graph_list = make_edges_list(updated_graph_instance.edges_dict)

    current_node = start_node 

    node_visit_order = [current_node]
    edge_visit_order = []

    # print("\n\n\ncurrent_edges_on_graph_list:", current_edges_on_graph_list)

    while len(current_edges_on_graph_list) > 0:

        # print("current_edges_on_graph_list:", current_edges_on_graph_list)
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

    # add node visit order and edge_visit order to graph instance

    updated_graph_instance.node_visit_order  = node_visit_order

    updated_graph_instance.edge_visit_order = edge_visit_order
        
    updated_graph_instance.node_geojson = make_node_geojson(updated_graph_instance)

    updated_graph_instance.edge_geojson = make_edge_geojson(updated_graph_instance)

    updated_graph_instance.route_geojson = make_route_geojson(updated_graph_instance)


    print("\n\n\n\n\nROUTE COLLECTION",updated_graph_instance.route_geojson)

    print("check done")

    return updated_graph_instance


if __name__ == '__main__':

    # import doctest
    # doctest.testmod()

    import time

    start = time.time()

    # 3. get graph with updated traversals count 
    # bbox = [NORTH, SOUTH , EAST, WEST] # min lng 

    bbox_geom_str = str({"type":"FeatureCollection",
                         "features":[{"id":"2a01221a7db21efadd487199ba4d89d9",
                         "type":"Feature","properties":{},"geometry":
                         {"coordinates":[[[-122.40017025263401,37.76001428340129],[-122.40238039286139,37.75982767848936],[-122.4020048835992,37.756841935919326],[-122.39958016664835,37.75696068934555],[-122.40017025263401,37.76001428340129]]],
                         "type":"Polygon"}}]})

    bbox = get_bbox_from_geojson(bbox_geom_str)

    # updated_graph_inst = get_eulerian_graph_edges(bbox, "osm")

    # # 2. get start node 
    # start_node = choice(list(updated_graph_inst.nodes_dict.keys()))

    # # # 3. calculate euler circuit 

    # euler_circuit_output = make_euler_circuit(start_node, updated_graph_inst)

    # print("\n\nEuler circuit order:")

    # print("node visit order:", euler_circuit_output.node_visit_order)
    # print("edge visit order:", euler_circuit_output.edge_visit_order)

    # print("edges geojson")
    # print("\n\n\n")
    # print(euler_circuit_output.edge_geojson)

    # print("nodes geojson")
    # print("\n\n\n")
    # print(euler_circuit_output.node_geojson)

    # print("\n\nProcess time:", time.time() - start, "seconds")



