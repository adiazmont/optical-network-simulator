from network import Network
from node import Node
from link import Link
from span import Span
from amplifier import Amplifier
from optical_signal import OpticalSignal
from graphics import Graphic
import numpy as np


def abs_to_db(absolute_value):
    """
    :param absolute_value: list or float
    :return: Convert absolute value to dB
    """
    db_value = 10*np.log10(absolute_value)
    return db_value


class CIANTestbed:

    def __init__(self):

        # Create a Network object
        self.net = Network()

        nodes = []
        # Create the nodes of the network
        n1 = Node(1, amplifier=Amplifier(target_gain=9))
        nodes.append(n1)
        n2 = Node(2, amplifier=Amplifier(target_gain=9))
        nodes.append(n2)
        n3 = Node(3)
        nodes.append(n3)
        n4 = Node(4, amplifier=Amplifier(target_gain=18))
        nodes.append(n4)
        n5 = Node(5, amplifier=Amplifier(target_gain=18))
        nodes.append(n5)
        n6 = Node(6, amplifier=Amplifier(target_gain=9))
        nodes.append(n6)
        n7 = Node(7)
        nodes.append(n7)
        n8 = Node(8)
        nodes.append(n8)

        for node in nodes:
            self.net.add_node(node)

        links = []
        # Create links of the network
        l1 = Link(n1, n2)
        links.append(l1)
        l2 = Link(n2, n3)
        links.append(l2)
        l3 = Link(n3, n4)
        links.append(l3)
        l4 = Link(n3, n5)
        links.append(l4)
        l5 = Link(n5, n6)
        links.append(l5)
        l6 = Link(n6, n7)
        links.append(l6)
        l7 = Link(n4, n7)
        links.append(l7)
        l8 = Link(n7, n8)
        links.append(l8)

        for link in links:
            self.net.add_link(link)

        # Create spans of the links
        fibre_attenuation = 0.2
        span_link1 = Span(length=45, fibre_attenuation=fibre_attenuation)
        span_link2 = Span(length=70, fibre_attenuation=fibre_attenuation)
        span_link5 = Span(length=45, fibre_attenuation=fibre_attenuation)
        span_link6 = Span(length=20, fibre_attenuation=fibre_attenuation)
        span_link7 = Span(length=25, fibre_attenuation=fibre_attenuation)

        # Add spans to the links
        self.net.add_span_to_link(l1, span_link1, Amplifier(target_gain=9, wavelength_dependent_gain_id='wdg1'))
        self.net.add_span_to_link(l2, span_link2, Amplifier(target_gain=14, wavelength_dependent_gain_id='wdg1'))
        self.net.add_span_to_link(l5, span_link5, Amplifier(target_gain=9, wavelength_dependent_gain_id='wdg1'))
        self.net.add_span_to_link(l6, span_link6, Amplifier(target_gain=4, wavelength_dependent_gain_id='wdg1'))
        self.net.add_span_to_link(l7, span_link7, Amplifier(target_gain=5, wavelength_dependent_gain_id='wdg1'))

        self.net.build()

        route = [(n1, l1), (n2, l2), (n3, l4), (n5, l5), (n6, l6), (n7, l8), (n8, None)]
        # OpticalSignal index starts from 1
        signals = [OpticalSignal(83), OpticalSignal(81), OpticalSignal(82), OpticalSignal(84), OpticalSignal(85)]
        self.net.transmit(n1, n8, signals, route)

        channel = 1529.2 + 83 * 0.4
        osnr_values = []
        spans_length = []
        osnr_values.append(abs_to_db((10**(-2.0/10.0)*0.8-(10**(-39.0/10.0)*4))/(10**(-39.0/10.0))))
        # print(abs_to_db((10**(-2.0/10.0)*0.8-(10**(-39.0/10.0)*4))/(10**(-39.0/10.0))))
        spans_length.append(0)
        osnr = self.net.monitor(l1, span_link1, 83, links)
        # print("OSNR of channel %s (nm) is %s dB at span %s." % (
        #     str(channel), str(osnr), span_link1.span_id))
        osnr_values.append(osnr)
        spans_length.append(span_link1.length)
        osnr = self.net.monitor(l2, span_link2, 83, links)
        # print("OSNR of channel %s (nm) is %s dB at span %s." % (
        #     str(channel), str(osnr), span_link2.span_id))
        osnr_values.append(osnr)
        spans_length.append(span_link2.length)
        osnr = self.net.monitor(l5, span_link5, 83, links)
        # print("OSNR of channel %s (nm) is %s dB at span %s." % (
        #     str(channel), str(osnr), span_link5.span_id))
        osnr_values.append(osnr)
        spans_length.append(span_link5.length)
        osnr = self.net.monitor(l6, span_link6, 83, links)
        # print("OSNR of channel %s (nm) is %s dB at span %s." % (
        #     str(channel), str(osnr), span_link6.span_id))
        osnr_values.append(osnr)
        spans_length.append(span_link6.length)

        graphics = Graphic()
        graphics.plot_osnr_increment(osnr_values, spans_length)


tt = CIANTestbed()
