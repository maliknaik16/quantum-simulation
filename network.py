
from node import Node
import random
import math

class Network:

    def __init__(self):

        self.nodes = []
        self.network = []

    def get_network(self):
        """
        Returns the network.
        """

        return self.network

    def get_nodes(self):
        """
        Returns the nodes.
        """

        return self.nodes

    def get_num_nodes(self):
        """
        Returns the number of nodes in the network.
        """

        return len(self.get_nodes())

    def get_neighbors_count(self, node_name):
        """
        Returns the number of neighbors.
        """

        return len(self.get_neighbor_names(node_name))

    def get_neighbor_names(self, node_name):
        """
        Returns the names of the neighbor nodes.
        """

        # Initialize the neighbor nodes list.
        neighbor_nodes = []

        # Get the link information for the node.
        node_map = self.network[node_name]

        for node, link in enumerate(node_map):

            # Append the node if there is a link.
            if link == 1:
                neighbor_nodes.append(node)

        return neighbor_nodes

    def get_node_neighbors(self, node_name):
        """
        Returns the instances of the neighbor nodes.
        """

        # Initialize the neighbors list.
        neighbors = []

        # Get the neighbor node names.
        node_names = self.get_neighbor_names(node_name)

        for node in node_names:
            neighbors.append(self.nodes[node])

        return neighbors

    def build_network(self, min_nodes=4, max_nodes=8):
        """
        Randomly generates the network.
        """

        num_nodes = random.randint(min_nodes, max_nodes)

        # Initialize the network with no links.
        for i in range(num_nodes):

            node = []

            for j in range(num_nodes):
                node.append(-1)

            self.network.append(node)

        # Randomly assign links between nodes.
        for i in range(num_nodes):

            for j in range(num_nodes):

                if i == j:
                    self.network[i][j] = 0
                elif self.network[i][j] == -1:

                    link = random.randint(0, 1)

                    self.network[i][j] = link
                    self.network[j][i] = link

        return self.network

    def assign_qubits(self, min_qubits=2, max_qubits=6):
        """
        Randomly assign qubits to the nodes.
        """

        # Get the number of nodes in the network.
        num_nodes = len(self.network)

        for i in range(num_nodes):
            self.nodes.append(Node(str(i), random.randint(min_qubits, max_qubits)))

    def entangle_qubits_in_network(self):
        """
        Randomly entangle qubits with neighboring nodes.
        """

        visited = []

        for node in self.nodes:

            # Get the node name.
            node_name = int(node.get_node_name())

            # Get number of qubits.
            num_qubits = node.get_num_qubits()

            # Get the neighbors of the current node.
            neighbors = self.get_node_neighbors(node_name)

            # Get the number of neighbors of the current node.
            neighbors_count = len(neighbors)

            # Set the number of qubits each neighbor can entangle.
            num_qubits_neighbors_can_entangle = int(math.floor(num_qubits / neighbors_count)) if neighbors_count > 0 else num_qubits

            visited.append(node_name)

            for neighbor in neighbors:

                # Neighbor node index.
                neighbor_node_name = int(neighbor.get_node_name())

                if neighbor_node_name in visited:
                    continue

                # Get number of qubits in the target node.
                target_num_qubits = neighbor.get_num_qubits()

                # Get the neighbors of the target node.
                target_neighbors_count = self.get_neighbors_count(neighbor_node_name)

                # Number of qubits that can be entangled with the target node.
                target_neighbor_ratio = int(math.floor(target_num_qubits / target_neighbors_count))

                for k in range(target_neighbor_ratio):

                    if num_qubits_neighbors_can_entangle == 0 and num_qubits > 0:
                        _ = node.entangle_qubits(neighbor)

                    elif k < num_qubits_neighbors_can_entangle:
                        _ = node.entangle_qubits(neighbor)

    def print_network(self):
        """
        Prints the adjacency matrix of the network.
        """

        num_nodes = self.get_num_nodes()

        for i in range(num_nodes):

            for j in range(num_nodes):
                print(self.network[i][j], end='\t')

            print('')
