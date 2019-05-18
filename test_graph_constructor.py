import unittest

import numpy as np # seems to slow down a bit
import osmnx as ox # really slows down file run?
import networkx as nx

from graph_constructor import make_nodes_dict
from graph_constructor import get_odd_nodes
from graph_constructor import get_list_of_all_pairs_lists
from graph_constructor import get_shortest_path_route_two_nodes
from graph_constructor import get_route_edges_from_shortest_path
from graph_constructor import get_total_length_shortest_path
from graph_constructor import get_dict_length_pairings_lists
from graph_constructor import get_optimal_pairing_list_dict
from graph_constructor import get_all_double_back_edges
from graph_constructor import make_traversal_dict_with_added_edges

NORTH = 37.7599 # max lat 
SOUTH = 37.7569 # min lat
EAST = -122.3997 # max lng
WEST = -122.4023 # min lng 
# make a real graph for tests that need that 
CONSTRUCTED_GRAPH = ox.graph_from_bbox(NORTH, SOUTH, EAST, WEST, network_type='walk')

# make simple square graph, multidirectional 
# so that all directions of edges will be accounted 
# for when building dictionary
SQUARE_EULER_GRAPH = nx.MultiDiGraph()
SQUARE_EULER_GRAPH.add_edges_from([
                      ('A', 'B'), ('B', 'A'), 
                      ('B', 'C'), ('C', 'B'), 
                      ('C', 'D'), ('D', 'C'),
                      ('D', 'A'), ('A', 'D')
                      ])

SQUARE_NON_EULER_GRAPH = nx.MultiDiGraph()
SQUARE_NON_EULER_GRAPH.add_edges_from([
                      ('A', 'B'), ('B', 'A'), 
                      ('B', 'C'), ('C', 'B'), 
                      ('C', 'D'), ('D', 'C'),
                      ('D', 'A'), ('A', 'D'),
                      ('C', 'A'), ('A', 'C')
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

        self.assertEqual( make_nodes_dict(SQUARE_EULER_GRAPH) , expected_output)

    def test_all_nodes_in_dict(self):
        """
        Confirm all nodes in graph appear
        as keys in output dict.
        """

        expected_keys_set = set(list(SQUARE_EULER_GRAPH.nodes))

        self.assertEqual( set(make_nodes_dict(SQUARE_EULER_GRAPH).keys()) , expected_keys_set)

class TestGetOddNodes(unittest.TestCase):

    def test_no_odd_nodes_in_euler_graph(self):
        """
        Confirm that an euler graph
        has zero odd nodes
        """
        self.assertEqual(get_odd_nodes(SQUARE_EULER_GRAPH),
                         [])

    def test_odd_nodes_non_euler_graph(self):
        """
        Confirm two odd nodes in square, non
        euler graph.
        """

        self.assertEqual(set(get_odd_nodes(SQUARE_NON_EULER_GRAPH)), 
                        set(['A', 'C'])
                        )

class TestListOfPairsLists(unittest.TestCase):

    def test_all_pairing_opts_returned(self):
        """
        Confirm all possible lists of pairs
        are returned. 
        """

        input_list_of_nodes = ['A','B','C','D']

        expected_output = [
                  [ ('A','B'), ('C','D') ], 
                  [ ('A','C'), ('B','D') ], 
                  [ ('A','D'), ('B','C') ] ]

        self.assertEqual( get_list_of_all_pairs_lists(input_list_of_nodes), 
                          expected_output
                         ) 

class TestGetShortestPathRoute(unittest.TestCase):

    def test_node_order(self):
        """
        Confirm correct node order
        between two points on CONSTRUCTED_GRAPH
        """
        expected_output = [65294615, 65320191, 65320193]

        self.assertEqual(get_shortest_path_route_two_nodes(65294615, 65320193, CONSTRUCTED_GRAPH),
                        expected_output)

class TestGetRouteEdges(unittest.TestCase):

    def test_simplest_route(self):
        """
        Confirm output for two node route
        """

        route = ['A', 'B']
        self.assertEqual(get_route_edges_from_shortest_path(route), 
                        [('A', 'B')])
    
    def test_odd_route(self):
        """
        Confirm output for odd number of nodes route
        """
        route = ['A', 'B', 'C']

        self.assertEqual(get_route_edges_from_shortest_path(route), 
                        [('A', 'B'), ('B', 'C')])


    def test_even_route(self):
        """ 
        Confirm output for odd number of nodes route
        """

        route = ['A', 'B', 'C','D']

        self.assertEqual(get_route_edges_from_shortest_path(route), 
                        [('A', 'B'), ('B', 'C'), ('C', 'D')])

class TestGetTotalLenShortestPath(unittest.TestCase):

    def test_get_total_length_shortest_path(self):
        """
        Confirm output length for input list of edges
        """

        input_edges_list = [(65294615, 65294613), (65294613, 65320188)]

        expeted_output = 228.606

        actual_output = get_total_length_shortest_path(input_edges_list, CONSTRUCTED_GRAPH)
        
        self.assertEqual(actual_output, expeted_output)

class TestGetDictLenthPairings(unittest.TestCase):

    def test_get_dict_length_pairings_lists(self): 

        input_pairings_list = [
            [(65294615, 65320193), (65313455, 65320188)], 
            [(65294615, 65313455), (65320193, 65320188)], 
            [(65294615, 65320188), (65320193, 65313455)]
            ]

        expected_output = {
            ((65294615, 65320193), (65313455, 65320188)): 506.546, 
            ((65294615, 65313455), (65320193, 65320188)): 506.546, 
            ((65294615, 65320188), (65320193, 65313455)): 330.56899999999996
            }
        actual_output = get_dict_length_pairings_lists(input_pairings_list, CONSTRUCTED_GRAPH)


        self.assertEqual(actual_output, expected_output)

class TestGestOptimalPairingListDict(unittest.TestCase):

    def test_get_optimal_pairing_list_dict(self):
        """
        Test output of get_optimal_pairing_list_dict
        """ 

        input_pairings_list_dict = {
            (('A','B'), ('C','D')): 5, 
            (('A','C'), ('B','D')): 10, 
            (('A','D'), ('B','C') ): 30
            }

        expected_output = {'optimal_pairing': (('A','B'), ('C','D')),
                           'optimal_added_distance': 5}

        actual_output = get_optimal_pairing_list_dict(input_pairings_list_dict)

        self.assertEqual(actual_output, expected_output)

class TestGetAllDoubleBackEdges(unittest.TestCase):

    def test_get_all_double_back_edges(self):
        """
        Confirm output contains all edges in optimal pairing
        """ 
        
        input_optimal_pairing_list_dict = {'optimal_pairing': ((65294615, 65320188), (65320193, 65313455)), 
                                           'optimal_added_distance': 330.56899999999996}

        expected_output = [(65294615, 65294613), 
                           (65294613, 65320188), 
                           (65320193, 65313458), 
                           (65313458, 65313455)]


        actual_output = get_all_double_back_edges(input_optimal_pairing_list_dict, CONSTRUCTED_GRAPH)
    
        self.assertEqual(actual_output, expected_output)

class TestMakeTraversalDictWithAddedEdges(unittest.TestCase):

    def test_twice_traversal_list(self):

        input_twice_traversal_list = [(65294615, 65294613), 
                           (65294613, 65320188), 
                           (65320193, 65313458), 
                           (65313458, 65313455)]

        expected_output = {(65294613, 65294615): 2, 
                           (65294613, 65320188): 2, 
                           (65294615, 65320191): 1, 
                           (65294615, 65294616): 1, 
                           (65294616, 65320193): 1, 
                           (65320191, 65320193): 1, 
                           (65320191, 65320188): 1, 
                           (65320191, 65313455): 1, 
                           (65320193, 65313458): 2, 
                           (65313453, 65313455): 1, 
                           (65313453, 3074358133): 1, 
                           (65313455, 65313458): 2, 
                           (3074358133, 65320188): 1}

        actual_output = make_traversal_dict_with_added_edges(input_twice_traversal_list, CONSTRUCTED_GRAPH)

        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    # Run all tests when called like a script 
    unittest.main()