import itertools

input_list_1 = ['A','B','C','D']
expected_result_1 =  [
                  [ ('A','B'), ('C','D') ], 
                  [ ('A','C'), ('B','D') ], 
                  [ ('A','D'), ('B','C') ]
                 ]


input_list_2 = ['A','B','C','D','E', 'F']

expected_result_2 = [

    [('A', 'B'), ('C', 'D'), ('E', 'F')],

    [('A', 'B'), ('C', 'E'), ('D', 'F')],

    [('A', 'B'), ('C', 'F'), ('D', 'E')],

    [('A', 'C'), ('B', 'D'), ('E', 'F')],

    [('A', 'C'), ('B', 'E'), ('D', 'F')],

    [('A', 'C'), ('B', 'F'), ('D', 'E')],

    [('A', 'D'), ('B', 'C'), ('E', 'F')],

    [('A', 'D'), ('B', 'E'), ('C', 'F')],

    [('A', 'D'), ('B', 'F'), ('C', 'E')],

    [('A', 'E'), ('B', 'C'), ('D', 'F')],

    [('A', 'E'), ('B', 'D'), ('C', 'F')],

    [('A', 'E'), ('B', 'F'), ('C', 'D')],

    [('A', 'F'), ('B', 'C'), ('D', 'E')],

    [('A', 'F'), ('B', 'D'), ('C', 'E')],

    [('A', 'F'), ('B', 'E'), ('C', 'D')]
]


def all_pairs(lst):


    if len(lst) == 0:
        yield []
        return
    
    if len(lst) % 2 == 1:
        # Handle odd length list
        for i in range(len(lst)):
            for result in all_pairs(lst[:i] + lst[i+1:]):
                yield result
    
    else:
        a = lst[0]
        for i in range(1,len(lst)):
            pair = (a,lst[i])
            for rest in all_pairs(lst[1:i]+lst[i+1:]):
                yield [pair] + rest


def all_pairs_new(input_list):



    return []

# tests 
def test_all_pairs():
    

    assert list(all_pairs(input_list_2)) == expected_result_2



def test_new_all_pairs():

    assert list(test_new_all_pairs(input_list_2)) == expected_result_2