from transmissionSystem import TransmissionSystem
import random

# Class for network generation
class Network(object):

    # Generate the abstract topology
    def __init__(self, spectrum_band='C', bandwidth=12.5*(10E9), grid=0.4*(10E-9)):
        self.network = {}
        self.nodes = []
        self.links = {}
        self.transmission = TransmissionSystem(spectrum_band, bandwidth, grid)

    def addNode(self, new_node):
        if new_node in self.nodes:
            raise ValueError("network.addNode \'%s\' already in network!" %new_node)

        self.nodes.append(new_node)
        self.network[new_node] = []

    def addLink(self, new_link):
        self.links[new_link] = []
        src_node = new_link.src_node
        dst_node = new_link.dst_node
        self.network[src_node] .append((dst_node, new_link))

    def addSpanToLink(self, link, span, amplifier=None):
        link.addSpan(span, amplifier)
        self.links[link].append((span, amplifier))

    def transmit(self, src_node, dst_node, route='auto', spectrum_band='C',
                 channel_no=1, channels='auto', launch_power=-2, bandwidth=12.5*(10E9), grid=0.4*(10E-9)):
        if route=='auto':
            path = self.findPath(src_node, dst_node)
        else:
            path = route

        if channels=='auto':
            wavelength_channels = self.getWavelengthChannels(channel_no)
        else:
            wavelength_channels = channels

       # transmission = TransmissionSystem(spectrum_band, bandwidth, grid)
        if self.transmission.run(path, wavelength_channels, launch_power):
            print("network.transmit: Transmission successful!")
        else:
            print("network.transmit: Error in transmission.")

    def monitor(self, link, span, channel):
        return self.transmission.monitor(link, span, channel)

    def getWavelengthChannels(self, channel_no):
        return random.sample(range(1, 91),  channel_no)

    # Dijkstra algorithm for finding shortest path
    def findPath(self, src_node, dst_node, path=[]):
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
                return "Route Not Possible"
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
        for link in sorted(self.links):
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
            str_src_node = roadm + str(src_node.label )
            str_dst_node = roadm + str(dst_node.label)
            print(str_src_node + link_string_representation + "> " + str_dst_node)
