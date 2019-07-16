from network import Network
from node import Node
from link import Link
from span import Span
from amplifier import Amplifier
from transmissionSystem import TransmissionSystem
from graphics import Graphic
import random
import numpy as np

class CIANTestbed():

    def __init__(self):

        # Create a Network object
        self.net = Network()

        nodes = []
        edfa_gains = []
        self.training_parameters = ()
        # Create the nodes of the network
        n1 = Node(1, amplifier=Amplifier(target_gain=9), node_type='tx')# Tx node
        nodes.append(n1)
        edfa_gains.append(9)
        n2 = Node(2, amplifier=Amplifier(target_gain=9), node_type='inline') # in-line node
        nodes.append(n2)
        edfa_gains.append(9)
        n3 = Node(3, node_type='inline') # in-line node
        nodes.append(n3)
        n4 = Node(4, amplifier=Amplifier(target_gain=18), node_type='inline') # in-line node
        nodes.append(n4)
        n5 = Node(5, amplifier=Amplifier(target_gain=18), node_type='inline') # in-line node
        nodes.append(n5)
        edfa_gains.append(18)
        n6 = Node(6, amplifier=Amplifier(target_gain=9), node_type='inline') # in-line node
        nodes.append(n6)
        edfa_gains.append(9)
        n7 = Node(7, node_type='inline') # in-line node
        nodes.append(n7)
        n8 = Node(8, node_type='rx') # Rx node
        nodes.append(n8)

        for node in nodes:
            self.net.addNode(node)

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
            self.net.addLink(link)

        # Create spans of the links
        fibre_attenuation = 0.2
        span_link1 = Span(length=45, fibre_attenuation=fibre_attenuation)
        span_link2 = Span(length=70, fibre_attenuation=fibre_attenuation)
        span_link5 = Span(length=45, fibre_attenuation=fibre_attenuation)
        span_link6 = Span(length=20, fibre_attenuation=fibre_attenuation)
        span_link7 = Span(length=25, fibre_attenuation=fibre_attenuation)

        # Add spans to the links
        self.net.addSpanToLink(l1, span_link1, Amplifier(target_gain=fibre_attenuation*span_link1.length, wavelengthDependentGainId='wdg1'))
        edfa_gains.append(fibre_attenuation*span_link1.length)
        self.net.addSpanToLink(l2, span_link2, Amplifier(target_gain=fibre_attenuation*span_link2.length, wavelengthDependentGainId='wdg2'))
        edfa_gains.append(fibre_attenuation*span_link2.length)
        self.net.addSpanToLink(l5, span_link5, Amplifier(target_gain=fibre_attenuation*span_link5.length, wavelengthDependentGainId='wdg2'))
        edfa_gains.append(fibre_attenuation*span_link5.length)
        self.net.addSpanToLink(l6, span_link6, Amplifier(target_gain=fibre_attenuation*span_link6.length, wavelengthDependentGainId='wdg1'))
        edfa_gains.append(fibre_attenuation*span_link6.length)
        self.net.addSpanToLink(l7, span_link7, Amplifier(target_gain=fibre_attenuation*span_link7.length, wavelengthDependentGainId='wdg2'))
        edfa_gains.append(fibre_attenuation*span_link7.length)

        route = [(n1, l1), (n2, l2), (n3, l4), (n5, l5), (n6, l6), (n7, l8), (n8, None)]
        channels = [81, 82, 83, 84, 85]
        transmission_system = TransmissionSystem(spectrum_band='C', bandwidth=12e9, grid=0.4e-9, launch_power=-40)
        self.net.transmit(transmission_system, n1, n8, route, channels=channels)

        channel = 1529.2 + 82 * 0.4
        osnr_values = []
        spans_length = []
        print("OSNR of channel %s (nm) is %s dB at span %s." % (str(channel), str(self.net.monitor(0, 0, 82)), 0))
        osnr_values.append(self.net.monitor(0, 0, 82))
        spans_length.append(0)
        print("OSNR of channel %s (nm) is %s dB at span %s." % (
        str(channel), str(self.net.monitor(l1, span_link1, 82)), span_link1.span_id))
        osnr_values.append(self.net.monitor(l1, span_link1, 82))
        spans_length.append(span_link1.length)
        print("OSNR of channel %s (nm) is %s dB at span %s." % (
        str(channel), str(self.net.monitor(l2, span_link2, 82)), span_link2.span_id))
        osnr_values.append(self.net.monitor(l2, span_link2, 82))
        spans_length.append(span_link2.length)
        print("OSNR of channel %s (nm) is %s dB at span %s." % (
        str(channel), str(self.net.monitor(l5, span_link5, 82)), span_link5.span_id))
        osnr_values.append(self.net.monitor(l5, span_link5, 82))
        spans_length.append(span_link5.length)
        print("OSNR of channel %s (nm) is %s dB at span %s." % (
        str(channel), str(self.net.monitor(l6, span_link6, 82)), span_link6.span_id))
        osnr_values.append(self.net.monitor(l6, span_link6, 82))
        spans_length.append(span_link7.length)

        graphics = Graphic()
        graphics.plot_osnr_increment(osnr_values, spans_length)
        # Display network topology
        self.net.topology()


tt = CIANTestbed()
