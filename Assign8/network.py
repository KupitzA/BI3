from Node import Node

class CorrelationNetwork:
    def __init__(self, correlation_matrix, threshold):
        """
        Constructs a co-expression network from a correlation matrix by adding edges between nodes with absolute
        correlation bigger than the given threshold.
        :param correlation_matrix: a CorrelationMatrix (see correlation.py)
        :param threshold: a float between 0 and 1
        """
        self.cor = correlation_matrix
        self.nodes = {}
        for entry, cor in correlation_matrix.items():
            node1 = Node(entry[0])
            node2 = Node(entry[1])
            self.appendNode(node1)
            self.appendNode(node2)
            if abs(cor) > threshold:
                node1.addLinkTo(node2)
                node2.addLinkTo(node1)

    def appendNode(self, node):
        """
        Appends node to network
        """
        if node.id not in self.nodes:
            self.nodes[node.id] = node

    def to_sif(self, file_path):
        """
        Write the network into a simple interaction file (SIF).
        Column 0: label of the source node
        Column 1: interaction type
        Columns 2+: label of target node(s)
        :param file_path: path to the output file
        """
        with open(file_path, 'w') as f:
            values = [value for (key, value) in sorted(self.nodes.items())]
            keys = sorted(self.nodes.keys())
            written = []
            s = ''
            for position, value in enumerate(keys):
                for node2id in values[position].nodelist:
                    if node2id not in written: #and node2id != value:
                        s = str(value) + '\t'
                        s += str(round(self.cor[(value, node2id.id)], 2)) + '\t'
                        s += str(node2id) + '\n'
                    written.append(node2id)
                f.write(s)
