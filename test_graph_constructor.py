import unittest

import numpy as np # seems to slow down a bit
import osmnx as ox # really slows down file run?
import networkx as nx

from graph_constructor import make_nodes_dict

NORTH = 37.7599 # max lat 
SOUTH = 37.7569 # min lat
EAST = -122.3997 # max lng
WEST = -122.4023 # min lng 

# make a real graph for tests that need that 
CONSTRUCTED_GRAPH = ox.graph_from_bbox(NORTH, SOUTH, EAST, WEST, network_type='walk')

# make simple square graph, multidirectional 
# so that all directions of edges will be accounted 
# for when building dictionary
SQUARE_GRAPH = nx.MultiDiGraph()
SQUARE_GRAPH.add_edges_from([
                      ('A', 'B'), ('B', 'A'), 
                      ('B', 'C'), ('C', 'B'), 
                      ('C', 'D'), ('D', 'C'),
                      ('D', 'A'), ('A', 'D')
                      ])


class TestMakeNodesDict(unittest.TestCase):
    """Experimenting with unittests for dummy function"""

    def test_correct_nodes_dict_returned(self):
        """
        Confirm that nodes dict has atleast 
        one node.
        """

        expected_output = {
                          'A': {('A', 'B'), ('A', 'D')}, 
                          'B': {('B', 'C'), ('B', 'A')}, 
                          'C': {('C', 'B'), ('C', 'D')}, 
                          'D': {('D', 'C'), ('D', 'A')}
                          }

        self.assertEqual( make_nodes_dict(SQUARE_GRAPH) , expected_output)

    def test_all_nodes_in_dict(self):
        """
        Confirm all nodes in graph appear
        as keys in output dict.
        """

        expected_keys_set = set(list(SQUARE_GRAPH.nodes))

        self.assertEqual( set(make_nodes_dict(SQUARE_GRAPH).keys()) , expected_keys_set)

if __name__ == '__main__':
    # Run all tests when called like a script 
    unittest.main()