import numpy as np # seems to slow down a bit
import osmnx as ox # really slows down file run?
import networkx as nx

# sample bbox constraints
NORTH = 37.7599 # max lat 
SOUTH = 37.7569 # min lat
EAST = -122.3997 # max lng
WEST = -122.4023 # min lng 

class OSMGraph:
    """Unidirected graph created from OSM"""

    graph_type = "undirected"
    source = "OSM"

    def __init__(self, north, south, east, west):
        """Create a Graph."""

        ox_graph = ox.graph_from_bbox(north, south, east, west, 
                 network_type='walk')

        all_edges = [ edge[0:2] for edge in list(( ox_graph ).edges)]

        unique_edges = []

        for edge in all_edges:
            if edge not in unique_edges and edge[::-1] not in unique_edges:
                unique_edges.append(edge)

        self.ox_graph = ox_graph

        self.nodes_df, self.edges_df = ox.graph_to_gdfs(ox_graph)

        self.nodes = list(ox_graph.nodes)

        self.edges = unique_edges

class DIYGraph:
    """Graph made from list of edges"""

    graph_type = "undirected"
    source = "DIY"

    def __init__(self, list_of_edges):

        self.nodes_df = None

        all_nodes = set()

        # make a list of nodes based on nodes 
        # contained within all edge
        for edge in list_of_edges:

            first_node, second_node = edge

            all_nodes.add(first_node)
            all_nodes.add(second_node)

        self.nodes = list(all_nodes)

        self.edges = list_of_edges


def make_edges_dict(graph_instance):
    """Given graph instance make dict of edges and edge attribuets"""

    edges_dict = {}

    # if the graph instance was made from OSM data, set dataframe variable
    if graph_instance.source == "OSM":

        edges_df = graph_instance.edges_df

    for edge in graph_instance.edges:

        edge_attrs = {}

        if graph_instance.source == "OSM": 
        
            start_node, end_node = edge

            edge_df_row = edges_df.loc[(edges_df['u'] == start_node) & (edges_df['v'] == end_node)]

            edge_length = edge_df_row['length'].values[0]
            edge_hwy_type = edge_df_row['highway'].values[0]
            edge_name = edge_df_row['name'].values[0]
            edge_osmid = edge_df_row['osmid'].values[0]
            edge_geometry = edge_df_row['geometry'].values[0]

            # # highway type
            # # length
            # # name 
            # # osmid

            # length is in meters 
            edge_attrs['length'] = edge_length
            edge_attrs['hwy_type'] = edge_hwy_type
            edge_attrs['name'] = edge_name
            edge_attrs['osmid'] = edge_osmid
            edge_attrs['geometry'] = edge_geometry

        elif graph_instance.source == "DIY": 
            # default edge length for DIY graphs to 1
            # useful for testing
            edge_attrs['length'] = 1

        edge_attrs['num_traversals'] = None

        edges_dict[edge] = edge_attrs

    return edges_dict


def make_nodes_dict(graph_instance):

    nodes_dict = {}

    # if the graph instance was made from OSM data, set dataframe variable
    if graph_instance.source == "OSM":

        nodes_df = graph_instance.nodes_df

    for node in graph_instance.nodes:

        node_attrs = {} 

        if graph_instance.source == "OSM": 

            node_df_row = nodes_df.loc[(nodes_df['osmid'] == node)]

            node_x = node_df_row['x'].values[0]
            node_y = node_df_row['y'].values[0]
            node_geometry = node_df_row['geometry'].values[0]

            node_attrs['x'] = node_x
            node_attrs['y'] = node_y
            node_attrs['geometry'] = node_geometry

        connected_edges = []

        for edge in graph_instance.edges:
            if node in edge:
                connected_edges.append(edge)

        is_odd = False
        # if there are an odd number of edges that contain the node
        # mark node as odd 
        if len(connected_edges) % 2 != 0:
            is_odd = True

        node_attrs['connected_edges'] = connected_edges
        node_attrs['is_odd'] = is_odd



        nodes_dict[node] = node_attrs

    return nodes_dict


# OG_graph = OSMGraph(NORTH, SOUTH, EAST, WEST)

# ABCD_graph = DIYGraph([('A','B'), ('B', 'C'), ('C', 'D'), ('D','A'), ('A', 'C')])

# for node in make_nodes_dict(OG_graph):
#     print()
#     print("node:", node)
#     print(make_nodes_dict(OG_graph)[node])

# for node in make_nodes_dict(ABCD_graph):
#     print()
#     print("node:", node)
#     print(make_nodes_dict(ABCD_graph)[node])


# try getting a route from using class instance
# print("get shortest_path")
# print(nx.shortest_path(OG_graph.ox_graph, 65313455, 65320188, weight='length'))

