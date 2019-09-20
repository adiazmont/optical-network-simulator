from transmission_system import TransmissionSystem
import numpy as np


def abs_to_db(absolute_value):
    """
    :param absolute_value: list or float
    :return: Convert absolute value to dB
    """
    db_value = 10 * np.log10(absolute_value)
    return db_value


class Network(object):

    # Generate the abstract topology
    def __init__(self):
        self.network = {}
        self.nodes = []
        self.links = {}
        self.transmission_system = TransmissionSystem()

    def add_node(self, new_node):
        if new_node in self.nodes:
            raise ValueError("network.addNode \'%s\' already in network!" % new_node)

        self.nodes.append(new_node)
        self.network[new_node] = []

    def add_link(self, new_link):
        self.links[new_link] = []
        src_node = new_link.src_node
        dst_node = new_link.dst_node
        self.network[src_node] .append((dst_node, new_link))

    def add_span_to_link(self, link, span, amplifier=None):
        link.add_span(span, amplifier)
        self.links[link].append((span, amplifier))

    def build(self):
        self.transmission_system.init_interfaces(self.links)

    def transmit(self, src_node, dst_node, signals, route='auto'):
        """
        :param src_node: source Node() object
        :param dst_node: destination Node() object
        :param signals: signals to transmit sequentially - list[Signal(),]
        :param route: path from src to node - list[tuple(Node(), Link())]
        :return:
        """
        if route == 'auto':
            path = self.find_path(src_node, dst_node)
        else:
            path = route

        self.transmission_system.propagate(path, signals)

    def monitor(self, target_link, target_span, target_signal_index, links):
        """

        :param target_link:
        :param target_span:
        :param target_signal_index:
        :param links:
        :return: OSNR in linear form
        """
        osnr_stage_i = 0
        for link in links:
            for span, _amplifier in link.spans:
                input_power = self.transmission_system.input_power[link][span][target_signal_index]
                ase_noise = \
                    self.transmission_system.amplified_spontaneous_emission_noise[link][span][target_signal_index]
                nonlinear_noise = self.transmission_system.nonlinear_interference_noise[link][span][target_signal_index]
                print("Noise and power at span %s: %s - %s - %s" % (str(span.span_id), str(ase_noise),
                                                                    str(nonlinear_noise), str(input_power)))
                if osnr_stage_i == 0:
                    osnr_stage_i = input_power / (ase_noise * nonlinear_noise)
                else:
                    osnr_stage_i = 1 / (1 / osnr_stage_i + ((ase_noise * nonlinear_noise) / input_power))
                print("OSNR at span %s: %s" % (str(span.span_id), str(osnr_stage_i)))
                if span.span_id == target_span.span_id:
                    break
            if link.link_id == target_link.link_id:
                break

        final_osnr = osnr_stage_i
        print("Final OSNR: %s" % str(final_osnr))
        return 0

    def inspect_power_and_noise(self, link, span, signal_index):
        """
        :param link: Link() object
        :param span: Span() object
        :param signal_index: int
        :return: dictionary with power and noise(s) level in dB at given interface
        """
        _struct = {
            'signal_power': abs_to_db(self.transmission_system.get_active_channel_power(link, span, signal_index)),
            'signal_ase_noise': abs_to_db(
                self.transmission_system.get_active_channel_ase_noise(link, span, signal_index)),
            'signal_nli_noise': abs_to_db(
                self.transmission_system.get_active_channel_nli_noise(link, span, signal_index)),
            'total_noise': abs_to_db(
                self.transmission_system.get_active_channel_ase_noise(link, span, signal_index) +
                self.transmission_system.get_active_channel_nli_noise(link, span, signal_index))}
        return _struct

    # Dijkstra algorithm for finding shortest path
    def find_path(self, src_node, dst_node):
        """
        :param src_node: source Node() object
        :param dst_node: destination Node() object
        :return:
        """
        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight, Link())
        shortest_paths = {src_node: (None, 0, None)}
        current_node = src_node
        visited = set()
        while current_node != dst_node:
            visited.add(current_node)
            destinations = self.network[current_node]
            weight_to_current_node = shortest_paths[current_node][1]
            for node_to_link_relation in destinations:
                next_node = node_to_link_relation[0]
                link_to_next_node = node_to_link_relation[1]
                length_of_link = link_to_next_node.length()
                weight = length_of_link + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight, link_to_next_node)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "network.find_path: Route Not Possible"
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path
        path = []
        link_to_next_node = None
        while current_node is not None:
            path.append((current_node, link_to_next_node))
            next_node = shortest_paths[current_node][0]
            link_to_next_node = shortest_paths[current_node][2]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        return path

    def topology(self):
        """
        This function requires fixing.
        :return: dummy representation of the built network
        """
        for link in self.links:
            src_node = link.src_node
            dst_node = link.dst_node
            link_string_representation = ""
            roadm = "ROADM"
            edfa = "EDFA-"
            for span_obj in sorted(self.links[link]):
                span = span_obj[0]
                span_length = span.length

                amplifier = span_obj[1]
                if amplifier is not None:
                    link_string_representation += (" ---" + str(span_length) + "km---" +
                                                   edfa + str(amplifier.target_gain) + "dB")
                else:
                    link_string_representation += " ---" + str(span_length) + "km---"
            str_src_node = roadm + str(src_node.label)
            str_dst_node = roadm + str(dst_node.label)
            print(str_src_node + link_string_representation + "> " + str_dst_node)
