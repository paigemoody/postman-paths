import unittest
from circuit_constructor import *


class TestMakeEdgesList(unittest.TestCase):

    def make_edges_list(self):
        """Confirm 'num_traversals:2' edges added twice"""

        self.assertEqual(
                        make_edges_list(
                            { ('A','B') : {'num_traversals': 1},
                            ('A','D') : {'num_traversals': 1},
                            ('B','C') : {'num_traversals': 1},
                            ('B','E') : {'num_traversals': 2},
                            ('C','E') : {'num_traversals': 2},
                            ('C','D') : {'num_traversals': 1}}),
                        [
                            ('A', 'B'), 
                            ('A', 'D'), 
                            ('B', 'C'), 
                            ('B', 'E'), ('B', 'E'), 
                            ('C', 'E'), ('C', 'E'), 
                            ('C', 'D')]
                        )


class TestGetBridges(unittest.TestCase): 

    def test_get_bridges(self):
        """Confirm bridge list matches expected."""

        input_edges_list = [
                      ('A', 'B'),
                      ('C', 'D'),
                      ('D', 'A'),
                      ('C', 'A'),
                      ]

        expected_output = [('A', 'B')]

        self.assertEqual(get_bridges(input_edges_list), expected_output)


class TestGetConnEdges(unittest.TestCase):

    def test_get_all_conn_edges_remaining_in_graph(self):
        """Confirm output connected edges"""
        
        input_current_node = 'A'

        input_remaining_edges = [
                                ('A', 'B'), ('A', 'B'),
                                ('D', 'C'), ('A', 'D')
                                ]

        input_nodes_dict = { 
                            'A': {'connected_edges': 
                                    [('A', 'B'), ('A', 'D')]
                                    }, 
                            'B': {'connected_edges': 
                                    [('B', 'C'), ('B', 'A')]
                                    }
                            }


        actual_output = set(get_all_conn_edges_remaining_in_graph(
                        input_current_node, 
                        input_remaining_edges, 
                        input_nodes_dict))

        self.assertTrue(
                        (('A', 'D') in actual_output) 
                        and 
                        (('A', 'B') in actual_output)
                        )

class TestChooseEdgeToTraverse(unittest.TestCase):

    def test_choose_edge_to_traverse(self):
        """Confirm correct next edge chosen"""

        current_node = 'A'
        possible_next_edges = [('A','B'), ('A', 'D')]
        current_bridges = [('A','B'), ('B', 'C')]

        expected_output = ('A', 'D')
        
        actual_output = choose_edge_to_traverse(current_node,possible_next_edges,current_bridges)
        
        self.assertEqual(actual_output, expected_output)


class TestMakeEulerCircuit(unittest.TestCase):
    """NOTE this test takes in a graph from OSM that is likely to change."""
     
    def test_make_euler_circuit_edges(self):
        """Confirm that start and end node are the same"""

        NORTH = 37.7599 # max lat 
        SOUTH = 37.7569 # min lat
        EAST = -122.3997 # max lng
        WEST = -122.4023 # min lng  
        SOURCE = "OSM"

        start_node = 65294616

        bbox = [NORTH, SOUTH , EAST, WEST] # min lng 
        updated_graph_inst = get_eulerian_graph_edges(bbox, SOURCE)

        actual_output_dict = make_euler_circuit(start_node, updated_graph_inst)
        node_visit_order = make_euler_circuit(start_node, updated_graph_inst)["node_visit_order"]
        
        self.assertTrue((node_visit_order[0] == node_visit_order[-1]))


if __name__ == '__main__':
    # Run all tests when called like a script 
    unittest.main()