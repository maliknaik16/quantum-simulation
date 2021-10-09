
from network import Network
from utils import select_path, copy_graph, get_labels
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import math
import random
import traceback

def sequential_multipath_scheduling(D, network, graph):

    queue = []

    # Final demands.
    demands = {}

    for sd in D:
        demands[sd] = []
        queue.append(sd)

    while len(queue) > 0:

        sd_pair = queue[0]
        queue.pop(0)

        s = sd_pair[0]
        d = sd_pair[1]

        paths = network.get_paths(s, d, graph)

        if len(paths) > 0:

            path = select_path(paths)

            graph = network.update_network(path, graph)

            demands[sd_pair].append(list(path))

            queue.append(sd_pair)

    k = 0

    num_paths = []

    for k, v in demands.items():
        num_paths.append(len(v))

    return min(num_paths)

def run_sequential_multipath(save_figure = False):

    results = {
        "num_nodes": [],
        "num_sd_pairs": [],
        "min_num_qubits_assigned": [],
        "max_num_qubits_assigned": [],
        "min_num_entangled_qubits": [],
        "max_num_entangled_qubits": [],
        "k": []
    }

    x = 10
    increment = 10

    while x < 60:
    # for x in range(10, 20, 10):

        exception = False

        print('Num nodes:', x)

        try:
            # Initialize the network.
            network = Network()

            network.build_network(x, x)
            network.assign_qubits(9, x)
            network.entangle_qubits_in_network()

            # Get nodes.
            nodes = network.get_nodes()

            # Get number of nodes.
            num_nodes = len(nodes)

            min_num_qubits_assigned = 10
            max_num_qubits_assigned = -1
            min_num_entangled_qubits = 10
            max_num_entangled_qubits = -1

            for node in nodes:

                num_qubits = node.get_num_qubits()
                num_qubits_entangled = node.get_num_entangled_qubits()

                if num_qubits > max_num_qubits_assigned:
                    max_num_qubits_assigned = num_qubits

                if num_qubits < min_num_qubits_assigned:
                    min_num_qubits_assigned = num_qubits

                if num_qubits_entangled > max_num_entangled_qubits:
                    max_num_entangled_qubits = num_qubits_entangled

                if num_qubits_entangled < min_num_entangled_qubits:
                    min_num_entangled_qubits = num_qubits_entangled


            updated_network = network.get_entangled_network()

            updated_network_copy = copy_graph(updated_network)

            # Randomly generate the demands.
            # D = network.generate_random_sd_pairs(random.randint(2, 4))
            D = network.generate_random_sd_pairs(1, updated_network_copy)

            num_sd_pairs = len(D)

            k = sequential_multipath_scheduling(D, network, updated_network_copy)

            if save_figure:
                labels = get_labels(nodes)

                G = nx.from_numpy_matrix(np.array(updated_network))

                nx.draw(G, node_color='#f3f3f3ff', edgecolors='#3d85c6', font_size=12, labels=labels, edge_color='#cc0000', with_labels=True, style='--', node_size=2000)

                plt.savefig("visualization/sequential_multipath/%d.png" % (x, ))
                # plt.show()

            results["num_nodes"].append(num_nodes)
            results["num_sd_pairs"].append(num_sd_pairs)
            results["min_num_qubits_assigned"].append(min_num_qubits_assigned)
            results["max_num_qubits_assigned"].append(max_num_qubits_assigned)
            results["min_num_entangled_qubits"].append(min_num_entangled_qubits)
            results["max_num_entangled_qubits"].append(max_num_entangled_qubits)
            results["k"].append(k)

            print(results)
        except:
            exception = True

            print(traceback.format_exc())

        if not exception:
            x += increment

    # print(results)
    # df = pd.DataFrame(results)
    # df.to_csv("results/sequential_multipath/test_1.csv", index=False)

