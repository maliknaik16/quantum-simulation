
def select_path(paths):

    path = paths[0]

    min_len = len(path)

    for i in range(len(paths)):

        if len(paths[i]) < min_len:
            path = paths[i]
            min_len = len(path)

    return path

def copy_graph(matrix):

    graph = []

    v = len(matrix)

    for i in range(v):

        row = []

        for j in range(v):
            row.append(matrix[i][j])

        graph.append(row)

    return graph

def get_labels(nodes):

    labels = {}

    nums = {
        '0': '₀',
        '1': '₁',
        '2': '₂',
        '3': '₃',
        '4': '₄',
        '5': '₅',
        '6': '₆',
        '7': '₇',
        '8': '₈',
        '9': '₉'
    }

    for i, node in enumerate(nodes):
        labels[i] = str(i) + ' ' + nums[str(node.get_num_qubits())] + ',' + nums[str(node.get_num_entangled_qubits())]

    return labels
