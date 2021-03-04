
import time

start = time.time()

# from networkx import shortest_path
from osmnx import graph_from_bbox

print("\n\nProcess time:", time.time() - start, "seconds")