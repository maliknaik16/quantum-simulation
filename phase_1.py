
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

nodes = []

class Node:

    def __init__(self, name, num_qubits):
        """
        The entangled qubits are represented as follows:

        Parameters:
        -----------
        name : string
            Name of the node. Example: A, B, C, etc.

        num_qubits : int
            Number of qubits in the node.

        entangled_qubits: dict
            Dictionary mapping entangled nodes.

            The identifier is represented as follows:
                "srcNode:srcNodeQubitPos": "targetNode:targetNodeQubitPos"

            For Example:
                If A is the source node and B is the target node. Suppose,
                the 2nd qubit in A is entangled with 4th qubit in B then it is
                represented as follows:

                In "A":
                    {
                        "A:0": None,
                        "A:1": "B:3"
                    }

                In "B":
                    {
                        "B:0": None,
                        "B:1": None,
                        "B:0": None,
                        "B:3": "A:1",
                    }

        """

        self.name = name
        self.num_qubits = num_qubits
        self.num_entangled_qubits = 0
        self.qubit_pos = 0
        self.entangled_qubits = {}

        for i in range(self.num_qubits):
            self.entangled_qubits[str(self.name) + ":" + str(i)] = None

    def get_node_name(self):
        """
        Returns the node name.
        """

        return self.name

    def get_num_qubits(self):
        """
        Returns the number of qubits.
        """

        return self.num_qubits

    def _increment_qubit_pos(self):
        """
        Increments the qubit pos.
        """

        self.qubit_pos += 1

    def entangle_qubits(self, target, src_qubit_pos, target_qubit_pos):
        """
        Entangles qubits in source and target.

        Parameters:
        -----------
        target: Node
            Target Node object.
        src_qubit_pos: int
            Qubit position in the current node.
        target_qubit_pos : int
            Qubit position in the target node.

        """

        if src_qubit_pos is None or target_qubit_pos is None:
            src_qubit_pos = self.qubit_pos
            target_qubit_pos = target.qubit_pos

        src_id = self.name + ":" + str(src_qubit_pos)
        target_id = target.get_node_name() + ":" + str(target_qubit_pos)

        self.num_entangled_qubits += 1
        self.entangled_qubits[src_id] = target_id
        target.entangled_qubits[target_id] = src_id

        self._increment_qubit_pos()
        target._increment_qubit_pos()


    def get_num_entangled_qubits(self):
        """
        Returns the number of entangled qubits.
        """

        # num_entangled_qubits = 0

        # for _, v in self.entangled_qubits.items():

        #     if v is not None:
        #         num_entangled_qubits += 1

        # return num_entangled_qubits

        return self.num_entangled_qubits

    def print_info(self):
        print('Node:', self.name)
        print('Number of qubits:', self.num_qubits)
        print('Entangled Qubits:', self.entangled_qubits)
        print('Number of Entangled Qubits:', self.get_num_entangled_qubits())


def print_graph_matrix(graph):
    """
    Prints the adjacency matrix of the network/graph.
    """

    num_nodes = len(graph)

    for i in range(num_nodes):
        for j in range(num_nodes):
            print(graph[i][j], end='\t')

        print('')

def build_graph():
    """
    Randomly generates the graph.
    """

    num_nodes = random.randint(4, 8)

    graph = []

    # Initialize the graph with no links.
    for i in range(num_nodes):

        node = []

        for j in range(num_nodes):
            node.append(-1)

        graph.append(node)

    # Randomly assign links between nodes.
    for i in range(num_nodes):

        for j in range(num_nodes):

            if i == j:
                graph[i][j] = 0
            elif graph[i][j] == -1:

                link = random.randint(0, 1)

                graph[i][j] = link
                graph[j][i] = link

    return graph

def get_node_neighbor_numbers(graph, node_number):
    """
    Returns the index/number of the neighbor nodes.
    """

    neighbor_nodes_number = []
    node_map = graph[node_number]

    print(node_map)
    for node, link in enumerate(node_map):

        if link == 1:
            neighbor_nodes_number.append(node)

    return neighbor_nodes_number

def get_node_neighbors(graph, node_number):
    """
    Returns the instances of the neighbor nodes.
    """

    neighbors = []

    node_numbers = get_node_neighbor_numbers()

    for node in node_number:
        neighbors.append(nodes[node])

    return neighbors

def assign_qubits(graph):
    """
    Randomly assign qubits to the nodes.
    """

    global nodes

    num_nodes = len(graph)

    for i in range(num_nodes):
        nodes.append(Node(str(i), random.randint(2, 8)))

def entangle_qubits_in_network(graph):
    """
    Randomly entangle qubits with neighboring nodes.
    """

    global nodes

    for i, node in enumerate(nodes):

        num_qubits = node.get_num_entangled_qubits()
        neighbors = get_node_neighbors(graph, i)

# alice = Node('A', 4)
# bob = Node('B', 3)

# alice.entangle_qubits(bob, 3, 1)
# alice.print_info()

# bob.print_info()

# sample_network = [
#     [0, 1, 1, 1],
#     [1, 0, 0, 1],
#     [1, 0, 0, 1],
#     [1, 1, 1, 0]
# ]

sample_network = build_graph()

assign_qubits(sample_network)

entangle_qubits_in_network(sample_network)

# print_graph_matrix(sample_network)

# print(get_node_neighbor_numbers(sample_network, 2))

# for node in nodes:
#     node.print_info()

G = nx.from_numpy_matrix(np.array(sample_network))

nx.draw(G, with_labels = True, node_size = 1000)

plt.show()

