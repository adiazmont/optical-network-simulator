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


def db_to_abs(db_value):
    """
    :param db_value: list or float
    :return: Convert dB to absolute value
    """
    absolute_value = 10**(db_value/float(10))
    return absolute_value


def inspect_osnr_per_span(topology='linear', osnr_type='osnr'):
    """
    :param topology: type of topology defined in class Scripts - string
    :param osnr_type: type of OSNR to compute (OSNR or gOSNR) - string
    :return: plot the corresponding figure to the parameter to inspect, considering all the
                spans for each transmission.
    """
    channel_list = [list(range(1, 9)), list(range(1, 17)), list(range(1, 33)), list(range(1, 65))]
    channel_index = range(len(channel_list))
    inspect_values = {x: None for x in channel_index}
    spans_length = {x: None for x in channel_index}
    for index, channels in zip(channel_index, channel_list):
        my_network = UnitTest(topo='linear', link_length=500, span_length=100, channels=channels)
        # uncomment to get the centre channel
        # i = int(len(channels) / 2)
        # below use index-[0] for first wavelength
        # and index-[-1] for last wavelength
        cut = channels[-1]  # channel under test
        if topology == 'linear':
            tmp_osnr_values = []
            tmp_spans_length = []
            for span in my_network.spans:
                power = my_network.net.inspect_power_and_noise(
                    my_network.l1, span, cut)['signal_power']
                noise = my_network.net.inspect_power_and_noise(
                    my_network.l1, span, cut)['signal_ase_noise']
                if osnr_type == 'gosnr':
                    noise = my_network.net.inspect_power_and_noise(
                        my_network.l1, span, cut)['total_noise']

                osnr = power - noise
                tmp_osnr_values.append(osnr)
                tmp_spans_length.append(span.length / 1000.0)
            inspect_values[index] = tmp_osnr_values
            spans_length[index] = tmp_spans_length
    graphics = Graphic()
    graphics.plot_osnr(inspect_values, spans_length, osnr_type)


def inspect_osnr_per_distance(topology='linear', osnr_type='osnr'):
    """
    :param topology: type of topology defined in class UnitTest - string
    :param osnr_type: type of OSNR to compute (OSNR or gOSNR) - string
    :return: plot the corresponding figure to the parameter to inspect, considering only
                the last span for each transmission.
    """
    channel_list = [list(range(1, 9)), list(range(1, 17)), list(range(1, 33)), list(range(1, 65))]
    channel_index = range(len(channel_list))
    inspect_values = {x: None for x in channel_index}
    distances = [100, 200, 500, 1000, 2000, 3000]
    for index, channels in zip(channel_index, channel_list):
        tmp_osnr_values = []
        for distance in distances:
            my_network = UnitTest(topo='linear', link_length=distance, span_length=100, channels=channels)
            # uncomment to get the centre channel
            # i = int(len(channels) / 2)
            # below use index-[0] for first wavelength
            # and index-[-1] for last wavelength
            cut = channels[0]  # channel under test
            if topology == 'linear':
                power = my_network.net.inspect_power_and_noise(
                    my_network.l1, my_network.spans[-1], cut)['signal_power']
                noise = my_network.net.inspect_power_and_noise(
                    my_network.l1, my_network.spans[-1], cut)['signal_ase_noise']
                if osnr_type == 'gosnr':
                    noise = my_network.net.inspect_power_and_noise(
                        my_network.l1, my_network.spans[-1], cut)['total_noise']
                osnr = power - noise
                tmp_osnr_values.append(osnr)
            del my_network
        inspect_values[index] = tmp_osnr_values

    graphics = Graphic()
    graphics.plot_osnr_per_distance(inspect_values, distances, osnr_type)


def inspect_transmission_per_span(topology='linear', param=None):
    """
    :param topology: type of topology defined in class UnitTest
    :param param: parameter to inspect: 'signal_power', 'signal_ase_noise' or 'signal_nli_noise'
    :return: plot the corresponding figure to the parameter to inspect, considering all the
                spans for each transmission.
    """
    channel_list = [list(range(1, 9)), list(range(1, 17)), list(range(1, 33)), list(range(1, 65))]
    channel_index = range(len(channel_list))
    inspect_values = {x: None for x in channel_index}
    spans_length = {x: None for x in channel_index}
    for index, channels in zip(channel_index, channel_list):
        my_network = UnitTest(topo='linear', link_length=500, span_length=100, channels=channels)
        # uncomment to get the centre channel
        # i = int(len(channels) / 2)
        # below use index-[0] for first wavelength
        # and index-[-1] for last wavelength
        cut = channels[-1]  # channel under test
        if topology == 'linear':
            tmp_values = []
            tmp_spans_length = []
            for span in my_network.spans:
                tmp_values.append(my_network.net.inspect_power_and_noise(
                    my_network.l1, span, cut)[param])
                tmp_spans_length.append(span.length/1000.0)
            inspect_values[index] = tmp_values
            spans_length[index] = tmp_spans_length
    graphics = Graphic()
    if param == 'signal_power':
        graphics.plot_dict_power_levels(inspect_values, spans_length)
    if param == 'signal_ase_noise' or param == 'signal_nli_noise':
        graphics.plot_dict_noise_levels(inspect_values, spans_length)


def inspect_transmission_per_distance(topology='linear', param=None):
    """
    :param topology: type of topology defined in class UnitTest
    :param param: parameter to inspect: 'signal_power', 'signal_ase_noise' or 'signal_nli_noise'
    :return: plot the corresponding figure to the parameter to inspect, considering only
                the last span for each transmission.
    """
    channel_list = [list(range(1, 9)), list(range(1, 17)), list(range(1, 33)), list(range(1, 65))]
    channel_index = range(len(channel_list))
    inspect_values = {x: None for x in channel_index}
    distances = [100, 200, 500, 1000, 2000, 3000]
    for index, channels in zip(channel_index, channel_list):
        tmp_values = []
        for distance in distances:
            my_network = UnitTest(topo='linear', link_length=distance, span_length=100, channels=channels)
            # uncomment to get the centre channel
            # i = int(len(channels) / 2)
            # below use index-[0] for first wavelength
            # and index-[-1] for last wavelength
            cut = channels[0]  # channel under test
            if topology == 'linear':
                tmp_values.append(my_network.net.inspect_power_and_noise(
                    my_network.l1, my_network.spans[-1], cut)[param])
            del my_network
        inspect_values[index] = tmp_values
    graphics = Graphic()
    if param == 'signal_power':
        graphics.plot_dict_power_levels_distance(inspect_values, distances)
    if param == 'signal_ase_noise' or param == 'signal_nli_noise':
        graphics.plot_dict_noise_levels_distance(inspect_values, distances)


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
            self.n1 = Node(1, amplifier=Amplifier(target_gain=9), node_type='tx')  # Tx node
            nodes.append(self.n1)
            self.n2 = Node(2, amplifier=Amplifier(target_gain=9), node_type='inline')  # in-line node
            nodes.append(self.n2)
            self.n3 = Node(3, node_type='inline')  # in-line node
            nodes.append(self.n3)
            self.n4 = Node(4, amplifier=Amplifier(target_gain=18), node_type='inline')  # in-line node
            nodes.append(self.n4)
            self.n5 = Node(5, amplifier=Amplifier(target_gain=18), node_type='inline')  # in-line node
            nodes.append(self.n5)
            self.n6 = Node(6, amplifier=Amplifier(target_gain=9), node_type='inline')  # in-line node
            nodes.append(self.n6)
            self.n7 = Node(7, node_type='inline')  # in-line node
            nodes.append(self.n7)
            self.n8 = Node(8, node_type='rx')  # Rx node
            nodes.append(self.n8)

            # Add nodes to the network object
            for node in nodes:
                self.net.add_node(node)

            links = []
            # Create links of the network
            self.l1 = Link(self.n1, self.n2)
            links.append(self.l1)
            self.l2 = Link(self.n2, self.n3)
            links.append(self.l2)
            self.l3 = Link(self.n3, self.n4)
            links.append(self.l3)
            self.l4 = Link(self.n3, self.n5)
            links.append(self.l4)
            self.l5 = Link(self.n5, self.n6)
            links.append(self.l5)
            self.l6 = Link(self.n6, self.n7)
            links.append(self.l6)
            self.l7 = Link(self.n4, self.n7)
            links.append(self.l7)
            self.l8 = Link(self.n7, self.n8)
            links.append(self.l8)

            # Add links to the network object
            for link in links:
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
                                      Amplifier(target_gain=9, wavelength_dependent_gain_id='wdg1'))
            self.net.add_span_to_link(self.l2, self.span_link2,
                                      Amplifier(target_gain=14, wavelength_dependent_gain_id='wdg2'))
            self.net.add_span_to_link(self.l5, self.span_link5,
                                      Amplifier(target_gain=9, wavelength_dependent_gain_id='wdg2'))
            self.net.add_span_to_link(self.l6, self.span_link6,
                                      Amplifier(target_gain=5, wavelength_dependent_gain_id='wdg1'))
            self.net.add_span_to_link(self.l7, self.span_link7,
                                      Amplifier(target_gain=5, wavelength_dependent_gain_id='wdg2'))

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
            self.n1 = Node(1, amplifier=Amplifier(target_gain=9), node_type='tx')  # Tx node
            nodes.append(self.n1)
            self.n2 = Node(2, amplifier=Amplifier(target_gain=9), node_type='rx')  # in-line node
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


inspect_osnr_per_distance(osnr_type='gosnr')
# inspect_osnr_per_span(osnr_type='gosnr')
# inspect_transmission_per_span(param='signal_nli_noise')
# inspect_transmission_per_distance(param='signal_nli_noise')
# my_network = UnitTest(topo='linear', link_length=500, span_length=100, channels=list(range(1, 9)))
# my_network.inspect_power(cut=1)
# graphics = Graphic()
# graphics.inspect_srs_before_edfa()
