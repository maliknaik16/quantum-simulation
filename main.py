
from node import Node
from network import Network
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import math

network = Network()

network.build_network(3, 5)
network.assign_qubits()
network.entangle_qubits_in_network()

sample_network = network.get_network()
nodes = network.get_nodes()

network.print_network()

for node in nodes:
    node.print_info()

G = nx.from_numpy_matrix(np.array(sample_network))

nx.draw(G, with_labels = True, node_size = 1000)

plt.show()

