
from node import Node
from network import Network
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import math

network = Network()

network.build_network(5, 8)
network.assign_qubits()
network.entangle_qubits_in_network()

sample_network = network.get_network()
nodes = network.get_nodes()

# network.print_network()

# for node in nodes:
#     node.print_info()

# network.get_path()

updated_network = network.get_entangled_network()
# print(updated_network)

if network.is_connected_network(updated_network):
    sd_pairs = network.generate_random_sd_pairs(2)

    print(sd_pairs)

    print(network.get_path(sd_pairs[0][0], sd_pairs[0][1]))

    # G = nx.from_numpy_matrix(np.array(sample_network))
    G = nx.from_numpy_matrix(np.array(updated_network))

    nx.draw(G, with_labels = True, node_size = 1000)

    plt.show()
else:
    print('Disconnected graph')