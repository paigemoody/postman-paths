import numpy as np # seems to slow down a bit
# import osmnx as ox # really slows down file run?
from osmnx import graph_from_bbox
from osmnx import graph_to_gdfs
import networkx as nx

# sample bbox constraints
NORTH = 37.7599 # max lat 
SOUTH = 37.7569 # min lat
EAST = -122.3997 # max lng
WEST = -122.4023 # min lng 


class OSMGraph:
    """Unidirected graph created from OSM"""

    graph_type = "undirected"
    # source = "OSM"

    def __init__(self, north, south, east, west, source):
        """Create a Graph."""

        self.source = source

        self.ox_graph = graph_from_bbox(north, south, east, west, network_type='walk')

        # self.nodes_df, self.edges_df = graph_to_gdfs(ox_graph)

        # set self.nodes_df and self.edges_df
        self.get_dataframes()

        # set self.nodes list
        self.get_nodes_list()

        #  set self.edges list 
        self.get_unique_edges_list()

        # set self.edges_dict 
        self.make_edges_dict()

        # set self.nodes_dict
        self.make_nodes_dict()

    def get_dataframes(self):

        self.nodes_df, self.edges_df = graph_to_gdfs(self.ox_graph)

    def get_nodes_list(self):

        ox_graph = (self.ox_graph)

        self.nodes = list(ox_graph.nodes)

    def get_unique_edges_list(self):
        """From uni-directional ox graph, make list of unique edges"""

        # make list of edges without default weight parameter
        all_edges = [ edge[0:2] for edge in list(( self.ox_graph ).edges)]

        unique_edges = []

        for edge in all_edges:
            if edge not in unique_edges and edge[::-1] not in unique_edges:
                unique_edges.append(edge)

        self.edges = unique_edges


    def make_edges_dict(self):
        """Given graph instance make dict of edges and edge attribuets"""

        edges_dict = {}

        # if the graph instance was made from OSM data, set dataframe variable
        if self.source == "OSM":

            edges_df = self.edges_df

        for edge in self.edges:

            edge_attrs = {}

            if self.source == "OSM": 
            
                start_node, end_node = edge

                edge_df_row = edges_df.loc[(edges_df['u'] == start_node) & (edges_df['v'] == end_node)]

                edge_length = edge_df_row['length'].values[0]
                edge_hwy_type = edge_df_row['highway'].values[0]
                edge_name = edge_df_row['name'].values[0]
                edge_osmid = edge_df_row['osmid'].values[0]
                edge_geometry = edge_df_row['geometry'].values[0]

                # length is in meters 
                edge_attrs['length'] = edge_length
                edge_attrs['hwy_type'] = edge_hwy_type
                edge_attrs['name'] = edge_name
                edge_attrs['osmid'] = edge_osmid
                edge_attrs['geometry'] = edge_geometry

            elif self.source == "DIY": 
                # default edge length for DIY graphs to 1
                # useful for testing
                edge_attrs['length'] = 1

            edge_attrs['num_traversals'] = 1

            edges_dict[edge] = edge_attrs

        self.edges_dict = edges_dict

    def make_nodes_dict(self):

        nodes_dict = {}

        # if the graph instance was made from OSM data, set dataframe variable
        if self.source == "OSM":

            nodes_df = self.nodes_df

        for node in self.nodes:

            node_attrs = {} 

            if self.source == "OSM": 

                node_df_row = nodes_df.loc[(nodes_df['osmid'] == node)]

                node_x = node_df_row['x'].values[0]
                node_y = node_df_row['y'].values[0]
                node_geometry = node_df_row['geometry'].values[0]

                node_attrs['x'] = node_x
                node_attrs['y'] = node_y
                node_attrs['geometry'] = node_geometry

            connected_edges = []

            for edge in self.edges:
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

        self.nodes_dict = nodes_dict

# class DIYGraph:
#     """Graph made from list of edges"""

#     graph_type = "undirected"
#     source = "DIY"

#     def __init__(self, list_of_edges):

#         self.nodes_df = None

#         all_nodes = set()

#         # make a list of nodes based on nodes 
#         # contained within all edge
#         for edge in list_of_edges:

#             first_node, second_node = edge

#             all_nodes.add(first_node)
#             all_nodes.add(second_node)

#         self.nodes = list(all_nodes)

#         self.edges = list_of_edges

# OG_graph = OSMGraph(NORTH, SOUTH, EAST, WEST, "OSM")

# print(OG_graph.edges_dict)

# ABCD_graph = DIYGraph([('A','B'), ('B', 'C'), ('C', 'D'), ('D','A'), ('A', 'C')])

# for node in make_nodes_dict(OG_graph):
#     print()
#     print("node:", node)
#     print(make_nodes_dict(OG_graph)[node])

# for node in make_nodes_dict(ABCD_graph):
#     print()
#     print("node:", node)
#     print(make_nodes_dict(ABCD_graph)[node])

