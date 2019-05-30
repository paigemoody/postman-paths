from osmnx import graph_from_bbox, graph_to_gdfs

import networkx as nx

# sample bbox constraints
# NORTH = 37.7599 # max lat 
# SOUTH = 37.7569 # min lat
# EAST = -122.3997 # max lng
# WEST = -122.4023 # min lng 


class OSMGraph:
    """Unidirected graph created from OSM"""

    graph_type = "undirected"
    # source = "OSM"

    def __init__(self, bbox, source):
        """Create a Graph."""

        self.source = source

        self.bbox = bbox

        north, south, east, west = bbox

        self.ox_graph = graph_from_bbox(north, south, east, west, network_type='walk')

        # set self.nodes_df and self.edges_df
        self.get_dataframes()

        # set self.nodes list
        self.get_nodes_list()

        #  set self.edges list 
        self.get_unique_edges_list()

        # set self.edges_dict 
        self.make_edges_dict()

        # print("\n\nCLASS -- edges_dict:", self.edges_dict)

        # set self.nodes_dict
        self.make_nodes_dict()

        # print("\n\nCLASS -- nodes_dict:", self.nodes_dict)

        # instantiate an attribute for node visit order and 
        # edge visit order -- will be updated once calculated 
        self.node_visit_order = []

        self.edge_visit_order = []

    def get_dataframes(self):

        self.nodes_df, self.edges_df = graph_to_gdfs(self.ox_graph)

    def get_nodes_list(self):

        ox_graph = (self.ox_graph)

        self.nodes = list(ox_graph.nodes)

    def get_unique_edges_list(self):
        """From uni-directional ox graph, make list of unique edges"""

        # make list of edges without default weight parameter
        all_edges = [] 

        ox_graph = self.ox_graph

        edge_count = 0

        for edge in list(ox_graph.edges):
            edge_count += 1 

            all_edges.append(edge[0:2])

        # [ edge[0:2] for edge in list(( self.ox_graph ).edges)]

        print("edges from nx: ", len(all_edges))

        unique_edges = []

        for edge in all_edges:

            # testing what happens when edges that have the 
            # same start and end node are ignored

            if edge[0] == edge[1]:
                print(f"\n\n\n{edge} has matching nodes")

            else:
                rev_edge = edge[::-1]

                # make sure that both versions of the edge are not 
                # already accounted for 

                if edge not in unique_edges:

                    if rev_edge not in unique_edges:

                        unique_edges.append(edge)

            print("unique_edges:", len(unique_edges))

            self.edges = unique_edges


    def make_edges_dict(self):
        """Given graph instance make dict of edges and edge attribuets"""

        edges_dict = {}

        # if the graph instance was made from OSM data, set dataframe variable
        # if self.source == "OSM":

        edges_df = self.edges_df

        for edge in self.edges:

            edge_attrs = {}

            # if self.source == "OSM": 
            
            start_node, end_node = edge

            edge_df_row = edges_df.loc[(edges_df['u'] == start_node) & (edges_df['v'] == end_node)]

            edge_length = edge_df_row['length'].values[0]

            # print("\n\n\nedge_length:", edge_length)

            edge_hwy_type = edge_df_row['highway'].values[0]

            # handle edges that don't have a name - 
            # check for nan by looking for names with class 'float'
            edge_name = edge_df_row['name'].values[0]

            if type(edge_name) is float: 

                edge_name = "None"


            edge_osmid = edge_df_row['osmid'].values[0]
            edge_geometry = edge_df_row['geometry'].values[0]

            # length is in meters 
            edge_attrs['length'] = edge_length
            edge_attrs['hwy_type'] = edge_hwy_type
            edge_attrs['name'] = edge_name
            edge_attrs['osmid'] = edge_osmid
            edge_attrs['geometry'] = edge_geometry

            # elif self.source == "DIY": 
            #     # default edge length for DIY graphs to 1
            #     # useful for testing
            #     edge_attrs['length'] = 1

            edge_attrs['num_traversals'] = 1

            # the values of the edges dict for the edge is a dict of attributes
            edges_dict[edge] = edge_attrs

        self.edges_dict = edges_dict

    def make_nodes_dict(self):

        nodes_dict = {}

        # if the graph instance was made from OSM data, set dataframe variable
        # if self.source == "OSM":

        nodes_df = self.nodes_df

        for node in self.nodes:

            node_attrs = {} 

            # if self.source == "OSM": 

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


            # checking claculation of odd nodes 
            is_odd_mine = False
            # if there are an odd number of edges that contain the node
            # mark node as odd 
            # print("\n\nnode:", node)
            # print("\n\nconnected_edges:", connected_edges)

            if (len(connected_edges) != 0) and (len(connected_edges) % 2 != 0):
                print(node, ":",len(connected_edges) )
                is_odd_mine = True

            # # use nx's odd node calcu
            # is_odd_nx = False

            # graph = self.ox_graph
            # deg = graph.degree[node]

            # if deg % 2 != 0:
            #     is_odd_nx = True

            node_attrs['connected_edges'] = connected_edges
            # node_attrs['is_odd_mine'] = is_odd_mine

            node_attrs['is_odd'] = is_odd_mine

            # if deg != len(connected_edges):
            #     print("\n\n\nnode:",node)
            #     print("is_odd_mine",is_odd_mine)
            #     print("len(connected_edges):",len(connected_edges))

            #     print("\nis_odd_nx",is_odd_nx)
            #     print("deg:",deg)

            nodes_dict[node] = node_attrs

        self.nodes_dict = nodes_dict

    def __repr__(self):
        """Provide helpful representation of graph when printed."""

        return f"<bbox={self.bbox}\nsource={self.source}\ntotal nodes={len(self.nodes)}\ntotal edges={len(self.edges)}>"

if __name__ == '__main__':

    from graph_constructor_2 import get_bbox_from_geojson

    bbox = get_bbox_from_geojson('test_bbox_input.geojson')

    source = "OSM"

    example_graph_instance = OSMGraph(bbox, source)

    print("example_graph_instance:\n", example_graph_instance)




