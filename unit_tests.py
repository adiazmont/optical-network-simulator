from network import Network
from node import Node
from link import Link
from span import Span
from amplifier import Amplifier
from optical_signal import OpticalSignal
import numpy as np


def abs_to_db(absolute_value):
    """
    :param absolute_value: list or float
    :return: Convert absolute value to dB
    """
    db_value = 10*np.log10(absolute_value)
    return db_value


def db_to_abs(db_value):
    """
    :param db_value: list or float
    :return: Convert dB to absolute value
    """
    absolute_value = 10**(db_value/float(10))
    return absolute_value


class UnitTest:

    def __init__(self, topo='cian', link_length=1, span_length=1, channels=None):
        """
        :param topo: topology to be used
        :param link_length: only used when topo='linear
        :param span_length: only used when topo='linear
        :param channels: only used when topo='linear
        """

        # Create a Network object
        self.net = Network()

        if topo == 'cian':
            nodes = []
            # Create the nodes of the network
            self.n1 = Node(1, amplifier=Amplifier(target_gain=9))  # Tx node
            nodes.append(self.n1)
            self.n2 = Node(2, amplifier=Amplifier(target_gain=9))  # in-line node
            nodes.append(self.n2)
            self.n3 = Node(3)  # in-line node
            nodes.append(self.n3)
            self.n4 = Node(4, amplifier=Amplifier(target_gain=18))  # in-line node
            nodes.append(self.n4)
            self.n5 = Node(5, amplifier=Amplifier(target_gain=18))  # in-line node
            nodes.append(self.n5)
            self.n6 = Node(6, amplifier=Amplifier(target_gain=9))  # in-line node
            nodes.append(self.n6)
            self.n7 = Node(7)  # in-line node
            nodes.append(self.n7)
            self.n8 = Node(8)  # Rx node
            nodes.append(self.n8)

            # Add nodes to the network object
            for node in nodes:
                self.net.add_node(node)

            self.links = []
            # Create links of the network
            self.l1 = Link(self.n1, self.n2)
            self.links.append(self.l1)
            self.l2 = Link(self.n2, self.n3)
            self.links.append(self.l2)
            self.l3 = Link(self.n3, self.n4)
            self.links.append(self.l3)
            self.l4 = Link(self.n3, self.n5)
            self.links.append(self.l4)
            self.l5 = Link(self.n5, self.n6)
            self.links.append(self.l5)
            self.l6 = Link(self.n6, self.n7)
            self.links.append(self.l6)
            self.l7 = Link(self.n4, self.n7)
            self.links.append(self.l7)
            self.l8 = Link(self.n7, self.n8)
            self.links.append(self.l8)

            # Add links to the network object
            for link in self.links:
                self.net.add_link(link)

            # Create spans of the links
            fibre_attenuation = 0.22
            self.span_link1 = Span(length=45, fibre_attenuation=fibre_attenuation)
            self.span_link2 = Span(length=70, fibre_attenuation=fibre_attenuation)
            self.span_link5 = Span(length=45, fibre_attenuation=fibre_attenuation)
            self.span_link6 = Span(length=20, fibre_attenuation=fibre_attenuation)
            self.span_link7 = Span(length=25, fibre_attenuation=fibre_attenuation)

            # Add spans to the links
            self.net.add_span_to_link(self.l1, self.span_link1,
                                      Amplifier(target_gain=9.9, wavelength_dependent_gain_id='wdg1'))
            self.net.add_span_to_link(self.l2, self.span_link2,
                                      Amplifier(target_gain=15.4, wavelength_dependent_gain_id='wdg2'))
            self.net.add_span_to_link(self.l5, self.span_link5,
                                      Amplifier(target_gain=9.9, wavelength_dependent_gain_id='wdg2'))
            self.net.add_span_to_link(self.l6, self.span_link6,
                                      Amplifier(target_gain=4.4, wavelength_dependent_gain_id='wdg1'))
            self.net.add_span_to_link(self.l7, self.span_link7,
                                      Amplifier(target_gain=5.5, wavelength_dependent_gain_id='wdg2'))

            # Build network
            self.net.build()

            # Create a route to use for transmission
            route = [(self.n1, self.l1), (self.n2, self.l2), (self.n3, self.l4), (self.n5, self.l5),
                     (self.n6, self.l6), (self.n7, self.l8), (self.n8, None)]
            # OpticalSignal index starts from 1
            # Create OpticalSignal instances to sequencially add to transmission
            signals = [OpticalSignal(81), OpticalSignal(82), OpticalSignal(83), OpticalSignal(84), OpticalSignal(85)]
            # Invoke network function for transmission
            self.net.transmit(self.n1, self.n8, signals, route)

        if topo == 'linear':
            nodes = []
            self.n1 = Node(1, amplifier=Amplifier(target_gain=9))  # Tx node
            nodes.append(self.n1)
            self.n2 = Node(2, amplifier=Amplifier(target_gain=9))  # in-line node
            nodes.append(self.n2)

            for node in nodes:
                self.net.add_node(node)

            links = []
            self.l1 = Link(self.n1, self.n2)
            links.append(self.l1)

            for link in links:
                self.net.add_link(link)

            number_of_spans = link_length / span_length
            fibre_attenuation = 0.22
            self.spans = []
            while number_of_spans > 0:
                span = Span(length=span_length, fibre_attenuation=fibre_attenuation)
                self.net.add_span_to_link(self.l1, span,
                                          Amplifier(target_gain=span_length*fibre_attenuation,
                                                    wavelength_dependent_gain_id='wdg1'))
                self.spans.append(span)
                number_of_spans -= 1
            self.net.build()

            route = [(self.n1, self.l1), (self.n2, None)]
            # OpticalSignal index starts from 1
            signals = []
            for channel in channels:
                signals.append(OpticalSignal(channel))
            self.net.transmit(self.n1, self.n2, signals, route)


# my_network = UnitTest(topo='linear', link_length=500, span_length=100, channels=list(range(1, 9)))
my_network = UnitTest()
# osnr = my_network.net.monitor(my_network.l1, my_network.span_link1, 83, my_network.links)
# osnr = my_network.net.monitor(my_network.l2, my_network.span_link2, 83, my_network.links)
# osnr = my_network.net.monitor(my_network.l5, my_network.span_link5, 83, my_network.links)
osnr = my_network.net.monitor(my_network.l6, my_network.span_link6, 83, my_network.links)
# osnr = my_network.net.monitor(my_network.l6, my_network.span_link6, 81, my_network.links)
# osnr = my_network.net.monitor(my_network.l7, my_network.span_link7, 83, my_network.links)
