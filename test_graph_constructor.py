import unittest
from classes import OSMGraph
from graph_constructor_2 import *

NORTH = 37.7599 # max lat 
SOUTH = 37.7569 # min lat
EAST = -122.3997 # max lng
WEST = -122.4023 # min lng 
SOURCE = "OSM"

TEST_GRAPH = OSMGraph(NORTH, SOUTH, EAST, WEST, SOURCE)

class TestGetOddNodes(unittest.TestCase):

  def test_get_odd_nodes(self):
    """Given nodes dictionary, return a list of all
    nodes where is_odd = True""" 
    
    input_nodes_dict = { 
        'A': {'is_odd': False},
        'B': {'is_odd': True},
        'C': {'is_odd': True},
        'D': {'is_odd': False},
        'E': {'is_odd': False}
      }

    expected_output = ['B', 'C']

    self.assertEqual(get_odd_nodes(input_nodes_dict), expected_output)

class TestGetLIstOfAllPairs(unittest.TestCase):

  def test_get_list_of_all_pairs_lists(self):
    """Return the correct list of lists of pairs"""

    input_list = ['A','B','C','D']

    expected_output = [
              [ ('A','B'), ('C','D') ], 
              [ ('A','C'), ('B','D') ], 
              [ ('A','D'), ('B','C') ] ]


    self.assertEqual(get_list_of_all_pairs_lists(input_list), expected_output)


# REQUIRES GRAPH INSTANCE
class TestGetShortestRouteTwoNodes(unittest.TestCase):

  def test_get_shortest_route_two_nodes(self):
    """Correct shortest route returned""" 

    input_start = 65294615
    input_end = 65320193
    input_graph_instance = TEST_GRAPH

    expected_output = [65294615, 65320191, 65320193]

    self.assertEqual(get_shortest_route_two_nodes(input_start, input_end, input_graph_instance), expected_output)


class TestGetRouteEdgesFromRoute(unittest.TestCase):

  def test_get_route_edges_from_route(self):
    """Correct edges returned from list of edges""" 

    input_route = ['A', 'B', 'C', 'D','E']
    
    expected_output = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')]
    
    self.assertEqual(get_route_edges_from_route(input_route), expected_output)


class TestGetRouteLength(unittest.TestCase):

  def test_get_route_length(self):
    """Correct route length returned"""

    input_route_edges = [('A', 'B'), ('B', 'E')]
  
    input_edges_dict = { 
      ('A','B') : {'length' : 10},
      ('A','D') : {'length' : 8},
      ('B','C') : {'length' : 8},
      ('B','E') : {'length' : 6},
      ('C','E') : {'length' : 5},
      ('C','D') : {'length' : 10},
    }
    
    expected_output = 16

    self.assertEqual(get_route_length(input_route_edges, input_edges_dict), expected_output)


# REQUIRES GRAPH INSTANCE TO TEST
class TestGetDictPairingsListsLengths(unittest.TestCase):

  def test_get_dict_pairings_lists_lengths(self):
    """Return a dictionary of the length 
    of each pairing.
    """
    input_list_of_possible_pairs_lists = [[(65294615, 65320193), (65313455, 65320188)], [(65294615, 65313455), (65320193, 65320188)], [(65294615, 65320188), (65320193, 65313455)]]
    
    input_graph_instance = TEST_GRAPH
    expected_output = {((65294615, 65320193), (65313455, 65320188)): 506.546, ((65294615, 65313455), (65320193, 65320188)): 506.546, ((65294615, 65320188), (65320193, 65313455)): 330.56899999999996}

    self.assertEqual(get_dict_pairings_lists_lengths(input_list_of_possible_pairs_lists, input_graph_instance), 
                    expected_output)


class TestGetTwiceTraversalEdges(unittest.TestCase):

  def test_get_twice_traversals_edges(self):
    """Return correct list of edges to traverse twice""" 

    input_dict = {(('A', 'B'), ('B', 'C')): 18, 
                  (('A', 'C'), ('B', 'C')): 26 }

    expected_output = [('A', 'B'), ('B', 'C')]
    
    self.assertEqual(get_twice_traversals_edges(input_dict), expected_output)
    
# REQUIRES GRAPH INSTANCE
class TestUpdateTwiceTraversalEdges(unittest.TestCase):

  def test_update_twice_traversal_edges(self):
    """Return correct edges dict for graph instance"""

    input_twice_traversals_edges = [(65294615, 65320188), (65320193, 65313455)]
    input_graph_instance = TEST_GRAPH

    actual_output =  update_twice_traversal_edges(input_twice_traversals_edges, TEST_GRAPH)

    actual_output_edges_dict = actual_output.edges_dict

    # assert that all the edges included in the twice traversal 
    # pairs have two traversals
    # eg. to go from *15 -> *88 you need to pass through node *13
    self.assertTrue(actual_output_edges_dict[(65294613, 65294615)]['num_traversals'] == 2)
    self.assertTrue(actual_output_edges_dict[(65294613, 65320188)]['num_traversals'] == 2)
    self.assertTrue(actual_output_edges_dict[(65320193, 65313458)]['num_traversals'] == 2)
    self.assertTrue(actual_output_edges_dict[(65313455, 65313458) ]['num_traversals'] == 2)

if __name__ == '__main__':
    # Run all tests when called like a script 
    unittest.main()