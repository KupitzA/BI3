import math
import random
from random import gauss
from generic_network import GenericNetwork


class Layout:
    def __init__(self, file_path):
        """
        :param file_path: path to a white-space-separated file that contains node interactions
        """
        # create a network from the given file
        self.network = GenericNetwork()
        self.network.read_from_tsv(file_path)
        # friction coefficient
        self.alpha = 0.03
        # random force interval
        self.interval = 0.3
        # initial square to distribute nodes
        self.size = 50

    def init_positions(self):
        """
        Initialise or reset the node positions, forces and charge.
        """
        #random.seed()
        for node in self.network.nodes.values():
            node.pos_x = random.randrange(self.size)
            node.pos_y = random.randrange(self.size)

    def calculate_forces(self):
        """
        Calculate the force on each node during the current iteration.
        """
        pairwiseForce = {}
        for nodeid, node in self.network.nodes.items():
            pairwiseForce[nodeid] = {}
            for node2id, node2 in self.network.nodes.items():
                if node2id not in pairwiseForce:
                    coulomb = - node.degree() * node2.degree() * math.hypot(node.pos_x-node2.pos_x, node.pos_y-node2.pos_y)
                    coulomb_x = float(coulomb) / (node.pos_x-node2.pos_x) if node.pos_x != node2.pos_x \
                        else float(coulomb) / 0.1
                    coulomb_y = float(coulomb) / (node.pos_y - node2.pos_y) if node.pos_y != node2.pos_y \
                        else float(coulomb) / 0.1
                    if node.has_edge_to(node2):
                        harmonic_x = - float(1/2) * (2*(node.pos_x-node2.pos_x) + pow(node.pos_y-node2.pos_y , 2))
                        harmonic_y = - float(1 / 2) * (2 * (node.pos_y - node2.pos_y) + pow(node.pos_x - node2.pos_x, 2))
                        coulomb_x += harmonic_x
                        coulomb_y += harmonic_y
                    pairwiseForce[nodeid][node2id] = (coulomb_x, coulomb_y)
                elif node2id in pairwiseForce and node2 != node:
                    pairwiseForce[nodeid][node2id] = pairwiseForce[node2id][nodeid]
        for nodeid in self.network.nodes.keys():
            for node2id in node.neighbour_nodes:
                if node2id != nodeid:
                    node.force_x += pairwiseForce[nodeid][node2id][0]
                    node.force_y += pairwiseForce[nodeid][node2id][1]

    def add_random_force(self, temperature):
        """
        Add a random force within [- temperature * interval, temperature * interval] to each node.
        (There is nothing to do here for you.)
        :param temperature: temperature in the current iteration
        """
        for node in self.network.nodes.values():
            node.force_x += gauss(0.0, self.interval * temperature)
            node.force_y += gauss(0.0, self.interval * temperature)

    def displace_nodes(self):
        """
        Change the position of each node according to the force applied to it and reset the force on each node.
        """
        for node in self.network.nodes.values():
            node.pos_x += self.alpha * node.force_x
            node.pos_y += self.alpha * node.force_y
            node.force_x = 0
            node.force_y = 0

    def calculate_energy(self):
        """
        Calculate the total energy of the network in the current iteration.
        :return: total energy
        """
        totalE = 0
        for node in self.network.nodes.values():
            for node2 in self.network.nodes.values():
                if node2.identifier > node.identifier:
                    totalE += float(node.degree() * node2.degree()) / math.hypot(node.pos_x-node2.pos_x, node.pos_y-node2.pos_y)
                    if node.has_edge_to(node2):
                        pow1 = pow(node.pos_x-node2.pos_x, 2)
                        pow2 = pow(node.pos_y-node2.pos_y, 2)
                        totalE += float(1/2) * (pow1 + pow2)
        return totalE

    def layout(self, iterations):
        """
        Executes the force directed layout algorithm. (There is nothing to do here for you.)
        :param iterations: number of iterations to perform
        :return: list of total energies
        """
        # initialise or reset the positions and forces
        self.init_positions()
        energies = []

        for _ in range(iterations):
            self.calculate_forces()
            self.displace_nodes()
            energies.append(self.calculate_energy())

        return energies

    def simulated_annealing_layout(self, iterations):
        """
        Executes the force directed layout algorithm with simulated annealing.
        :param iterations: number of iterations to perform
        :return: list of total energies
        """
        self.init_positions()
        energies = []

        for i in range(iterations):
            # TODO: DECREASE THE TEMPERATURE IN EACH ITERATION. YOU CAN BE CREATIVE.
            temperature = iterations-i
            # there is nothing to do here for you
            self.calculate_forces()
            self.add_random_force(temperature)
            self.displace_nodes()
            energies.append(self.calculate_energy())

        return energies
