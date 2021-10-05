
import json

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

        Description:
        --------------
        num_entangled_qubits : int
            Number of entangled qubits in the node.

        qubit_pos : int
            Qubit position of the unentangled qubit.

        entangled_qubits : dict
            Dictionary mapping for entangled nodes.

            The identifier is represented as follows:
                "srcNode:srcNodeQubitPos": "targetNode:targetNodeQubitPos"

            For Example:
                If A is the source node (with 2 Qubits) and B is the target node
                (with 4 Qubits). Suppose, the 2nd qubit in A is entangled with
                4th qubit in B then it is represented as follows:

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

    # def _increment_qubit_pos(self):
    #     """
    #     Increments the qubit pos.
    #     """

    #     self.qubit_pos += 1

    def entangle_qubits(self, target, src_qubit_pos=None, target_qubit_pos=None):
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

        Returns:
        --------
        True when successfully entangled, otherwise returns False.

        """

        if self.get_num_entangled_qubits() < self.get_num_qubits() and target.get_num_entangled_qubits() < target.get_num_qubits():

            if src_qubit_pos is None or target_qubit_pos is None:
                # src_qubit_pos = self.qubit_pos
                # target_qubit_pos = target.qubit_pos

                src_qubit_pos = self.get_num_entangled_qubits()
                target_qubit_pos = target.get_num_entangled_qubits()

            src_id = self.name + ":" + str(src_qubit_pos)
            target_id = target.get_node_name() + ":" + str(target_qubit_pos)

            self.increment_entangled_qubits()
            target.increment_entangled_qubits()

            self.entangled_qubits[src_id] = target_id
            target.entangled_qubits[target_id] = src_id

            # self._increment_qubit_pos()
            # target._increment_qubit_pos()

        else:
            return False

        return True

    def increment_entangled_qubits(self):
        """
        Increment the entangled qubits.
        """

        self.num_entangled_qubits += 1

    def get_num_entangled_qubits(self):
        """
        Returns the number of entangled qubits.
        """

        return self.num_entangled_qubits

    def get_entangled_qubits(self):

        return self.entangled_qubits

    def print_info(self):
        """
        Prints the general information about the Node.
        """

        print('Node:', self.name)
        print('Number of qubits:', self.num_qubits)
        print('Entangled Qubits:\n', json.dumps(self.entangled_qubits, indent=4), sep='')
        print('Number of Entangled Qubits:', self.get_num_entangled_qubits())

