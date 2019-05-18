import unittest


from circuit_constructor import get_bridges
from circuit_constructor import get_all_conn_edges_remaining_in_graph
from circuit_constructor import choose_edge_to_traverse
from circuit_constructor import get_list_of_edges_by_traversal_count

class TestGetBridges(unittest.TestCase): 

    def test_get_bridges(self):
        """
        Confirm bridge list matches expected.
        """

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
        """
        Confirm output connected edges
        """
        input_current_node = 'A'

        input_remaining_edges = [
                                ('A', 'B'), ('A', 'B'),
                                ('D', 'C'), ('D', 'A')
                                ]

        input_nodes_dict = {
                          'A': {('A', 'B'), ('A', 'D')}, 
                          'B': {('B', 'C'), ('B', 'A')}, 
                          'C': {('C', 'B'), ('C', 'D')}, 
                          'D': {('D', 'C'), ('D', 'A')}
                          }

        expected_output = set([
                            ('A', 'B'), 
                            ('D', 'A'),
                           ])

        actual_output = set(get_all_conn_edges_remaining_in_graph(
                        input_current_node, 
                        input_remaining_edges, 
                        input_nodes_dict))

        self.assertEqual(actual_output, expected_output)

class TestChooseEdgeToTraverse(unittest.TestCase):

    def test_choose_edge_to_traverse(self):
        """
        Confirm correct next edge chosen
        """

        input_current_node = 'A'
        input_possible_next_edges = [('A', 'B'), ('D', 'A')]
        input_current_bridges = [('A', 'D'), ('D', 'C')]

        expected_output = ('A', 'B')

        actual_output = choose_edge_to_traverse(input_current_node, 
                        input_possible_next_edges, 
                        input_current_bridges)

        self.assertEqual(actual_output, expected_output)


class TestGetListEdgesByTraversalCount(unittest.TestCase):

    def test_get_list_of_edges_by_traversal_count(self):
        """
        Confirm corred edge list returned
        """

        input_edge_traversals_dict_eulerian = {

            ('A','B') : 2,
            ('B','C') : 2,
            ('C','D') : 1,
            ('D','A') : 1,
            ('A','C') : 1
        }

        expected_output = set([('A','B'),('A','B'), 
                                ('B','C'), ('B','C'),
                                ('C','D'),
                                ('D','A'),
                                ('A','C') 
                                ])

        actual_output = set(get_list_of_edges_by_traversal_count(input_edge_traversals_dict_eulerian))

        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    # Run all tests when called like a script 
    unittest.main()