
from node import Node
import random
import math

class Network:

    def __init__(self):

        self.nodes = []
        self.network = []
        self.paths = []

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

    def build_network(self, min_nodes=4, max_nodes=8, min_links=-1):
        """
        Randomly generates the network.
        """

        # print('Min Links:', min_links)

        num_nodes = random.randint(min_nodes, max_nodes)

        if min_links == -1:
            min_links = math.ceil(0.5 * num_nodes)

        # Initialize the network with no links.
        for i in range(num_nodes):

            node = []

            for j in range(num_nodes):
                node.append(-1)

            self.network.append(node)

        # Randomly assign links between nodes.
        for i in range(num_nodes):

            zero_count = 0
            assigned = []

            for j in range(num_nodes):

                if i == j:
                    self.network[i][j] = 0

                    zero_count += 1

                elif self.network[i][j] == -1:

                    link = random.randint(0, 1)

                    self.network[i][j] = link
                    self.network[j][i] = link

                    if link == 0:
                        zero_count += 1


            # print('Zero Count:', zero_count)
            if zero_count > min_links:

                one_count = zero_count - min_links + 1

                while one_count > 0:

                    node_id = random.randint(0, num_nodes - 1)

                    if node_id not in assigned:

                        assigned.append(node_id)
                        self.network[i][node_id] = 1
                        self.network[node_id][i] = 1

                        one_count -= 1

        # self.print_network(self.network)

        return self.network

    def assign_qubits(self, min_qubits=5, max_qubits=8):
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

    def get_entangled_network(self):

        node_count = len(self.nodes)

        new_network = []

        for i in range(node_count):

            row = []

            for j in range(node_count):

                row.append(0)

            new_network.append(row)


        for i in range(node_count):

            entangled_qubits = self.nodes[i].get_entangled_qubits()

            for k, v in entangled_qubits.items():

                if v is None:
                    continue

                linked_node = int(v.split(':')[0])

                new_network[i][linked_node] += 1

        return new_network

    def pair_exists(self, pair, pair_list):
        """
        Checks if the pair exists.
        """

        # for p in pair_list:

        #     if pair[0] == p[1] and pair[1] == p[0]:
        #         return True

        #     if pair[0] == p[0] and pair[1] == p[1]:
        #         return True

        return False

    def get_random_sd_pair(self):
        """
        Generates a single random SD pair.
        """

        source = -1
        dest = -1

        while source == dest or source == dest + 1 or source == dest - 1:
            source = random.randint(0, len(self.nodes) - 1)

            dest = random.randint(0, len(self.nodes) - 1)

        pair = (source, dest)

        return pair

    def generate_random_sd_pairs(self, num_pairs, new_network):
        """
        Generates the random Source-Destination pairs.
        """

        # Initialize the sd pairs list.
        sd_pairs = []

        if 2 * num_pairs < len(self.nodes):

            for _ in range(num_pairs):

                # Get a random pair.
                pair = self.get_random_sd_pair()

                x = 0

                while not self.pair_exists(pair, sd_pairs):

                    if pair not in sd_pairs and len(self.get_paths(pair[0], pair[1], new_network)) > 0:
                        break

                    # Generate new pair when the pair already exists.
                    pair = self.get_random_sd_pair()

                    if x > 10:
                        # Break the loop after 5 retries
                        break

                    x += 1

                sd_pairs.append(pair)


        else:
            print('No such SD pairs')

        return sd_pairs

    def is_connected_network(self, network):

        for i in range(len(network)):

            all_zeroes = False

            for j in range(len(network)):

                if network[i][j] != 0:
                    break

                if j == len(network) - 1 and network[i][j] == 0:
                    all_zeroes = True

            if all_zeroes:
                return False

        return True

    def get_adjacent_nodes(self, node_name, network):

        nds = network[node_name]
        adjacent_nodes = []

        for node, value in enumerate(nds):

            if value > 0:
                adjacent_nodes.append(node)

        adjacent_nodes.reverse()

        return adjacent_nodes

    def update_network(self, path, new_network):
        """
        Removes the entangled link in the network on the path.
        """

        for i, node in enumerate(path):

            u = path[i]
            v = path[i + 1]

            new_network[u][v] -= 1
            new_network[v][u] -= 1

            if i == len(path) - 2:
                break

        return new_network


    # def get_path(self, source, dest):
    #     """
    #     Returns the path from source to destination.
    #     """

    #     new_network = self.get_entangled_network()

    #     # visited = [node for node in range(len(self.nodes))]
    #     visited = []

    #     stack = []

    #     stack.append(source)

    #     paths = []
    #     path = []

    #     while len(stack) > 0:

    #         top = stack[-1]
    #         # stack.pop()

    #         if top not in visited:
    #             path.append(top)
    #             # print(top, end=', ')
    #             visited.append(top)

    #         if top == dest:
    #             paths.append(path)
    #             break
    #             # path = []


    #         adjacent_nodes = self.get_adjacent_nodes(top, new_network)
    #         # print('\n\n', top, ' :', self.get_adjacent_nodes(top, new_network))

    #         visited_count = 0

    #         for node in adjacent_nodes:

    #             if node in visited:
    #                 visited_count += 1

    #             if node not in visited:
    #                 stack.append(node)
    #                 break

    #         if visited_count == len(adjacent_nodes):
    #             stack.pop()

    #     print(paths)
    #     print(new_network)

    def find_paths(self, u, d, new_network, visited, path):
        """
        Finds the path from u to d in the network and appends to the paths list.
        """

        # Mark the current node as visited.
        visited[u] = True

        # Append the current node to path list.
        path.append(u)

        # If current node is the destination then append to the paths list.
        if u == d:

            self.paths.append(list(path))

        else:

            for i in self.get_adjacent_nodes(u, new_network):

                if visited[i] == False:

                    self.find_paths(i, d, new_network, visited, path)

        # Pop current node from the path.
        path.pop()

        # Mark the current node as unvisited.
        visited[u] = False


    def get_paths(self, s, d, new_network):
        """
        Returns all path from source to destination.
        """

        # Mark all nodes as unvisited
        visited = [False] * (len(self.nodes))

        # Initialize the path array.
        path = []

        self.paths = []

        # Recursively find paths.
        self.find_paths(s, d, new_network, visited, path)

        return self.paths


    def print_network(self, nwk = None):
        """
        Prints the adjacency matrix of the network.
        """

        num_nodes = 0

        if nwk is None:
            num_nodes = self.get_num_nodes()
        else:
            num_nodes = len(nwk)


        for i in range(num_nodes):

            for j in range(num_nodes):

                if nwk is None:

                    print(self.network[i][j], end='\t')

                else:
                    print(nwk[i][j], end='\t')

            print('')
