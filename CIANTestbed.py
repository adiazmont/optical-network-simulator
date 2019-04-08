from network import Network
from node import Node
from link import Link
from span import Span
from amplifier import Amplifier
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
        n1 = Node(1, amplifier=Amplifier(target_gain=9), type=0)# Tx node
        nodes.append(n1)
        edfa_gains.append(9)
        n2 = Node(2, amplifier=Amplifier(target_gain=9), type=1) # in-line node
        nodes.append(n2)
        edfa_gains.append(9)
        n3 = Node(3, type=1) # in-line node
        nodes.append(n3)
        n4 = Node(4, amplifier=Amplifier(target_gain=18), type=1) # in-line node
        nodes.append(n4)
        n5 = Node(5, amplifier=Amplifier(target_gain=18), type=1) # in-line node
        nodes.append(n5)
        edfa_gains.append(18)
        n6 = Node(6, amplifier=Amplifier(target_gain=9), type=1) # in-line node
        nodes.append(n6)
        edfa_gains.append(9)
        n7 = Node(7, type=1) # in-line node
        nodes.append(n7)
        n8 = Node(8, type=2) # Rx node
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
        self.net.addSpanToLink(l1, span_link1, Amplifier(target_gain=fibre_attenuation*span_link1.getFibreSpanLength(), wavelengthDependentGainId=0))
        edfa_gains.append(fibre_attenuation*span_link1.getFibreSpanLength())
        self.net.addSpanToLink(l2, span_link2, Amplifier(target_gain=fibre_attenuation*span_link2.getFibreSpanLength(), wavelengthDependentGainId=1))
        edfa_gains.append(fibre_attenuation*span_link2.getFibreSpanLength())
        self.net.addSpanToLink(l5, span_link5, Amplifier(target_gain=fibre_attenuation*span_link5.getFibreSpanLength(), wavelengthDependentGainId=1))
        edfa_gains.append(fibre_attenuation*span_link5.getFibreSpanLength())
        self.net.addSpanToLink(l6, span_link6, Amplifier(target_gain=fibre_attenuation*span_link6.getFibreSpanLength(), wavelengthDependentGainId=0))
        edfa_gains.append(fibre_attenuation*span_link6.getFibreSpanLength())
        self.net.addSpanToLink(l7, span_link7, Amplifier(target_gain=fibre_attenuation*span_link7.getFibreSpanLength(), wavelengthDependentGainId=1))
        edfa_gains.append(fibre_attenuation*span_link7.getFibreSpanLength())
        
        # Dynamic part
        route = [(n1, l1), (n2, l2), (n3, l4), (n5, l5), (n6, l6), (n7, l8), (n8, None)]
        
#        link_load_30 = 27 + 1
        link_load_70 = 63 + 1
        
        channels = random.sample(range(1, 91),  link_load_70)
        channel_to_analyze = channels[-1] - 1
        launch_power = -20
        self.net.transmit(n1, n8, route, channels=channels, launch_power=launch_power)
        
        channel = round(1529.2+channel_to_analyze*0.4, 2)
        osnr_level = self.net.monitor(l6, span_link6, channel_to_analyze)
        wss_no = 5
        edfa_no = 8
        total_link_length = 45 + 70 + 45 + 20
        awl = self.check_bins(channels)
        average_edfa_gain = np.mean(edfa_gains)
        wss_no_x_attenuation = wss_no * 9
        #edfa_no * average_edfa_gain
        training_parameters = [channel, wss_no, edfa_no, total_link_length, launch_power, average_edfa_gain, wss_no_x_attenuation]
        [training_parameters.append(x) for x in edfa_gains]
        [training_parameters.append(x) for x in awl.values()]
        training_parameters.append(osnr_level)
        
        self.training_parameters = tuple(training_parameters)
        
        
    def check_bins(self, channels):
        bin1 = []
        bin2 = []
        bin3 = []
        bin4 = []
        bin5 = []
        bin6 = []
        bin7 = []
        bin8 = []
        bin9 = []
        bin10 = []
        bins = {}

        for channel in channels:
            if channel <= 9:
                bin1.append(channel)
            elif channel <= 18:
                bin2.append(channel)
            elif channel <= 27:
                bin3.append(channel)
            elif channel <= 36:
                 bin4.append(channel)
            elif channel <= 45:
                bin5.append(channel)
            elif channel <= 54:
                bin6.append(channel)
            elif channel <= 63:
                bin7.append(channel)
            elif channel <= 72:
                bin8.append(channel)
            elif channel <= 81:
                bin9.append(channel)
            elif channel <= 90:
                bin10.append(channel)

        bins[1] = len(bin1)
        bins[2] = len(bin2)
        bins[3] = len(bin3)
        bins[4] = len(bin4)
        bins[5] = len(bin5)
        bins[6] = len(bin6)
        bins[7] = len(bin7)
        bins[8] = len(bin8)
        bins[9] = len(bin9)
        bins[10] = len(bin10)

        return bins

tt = CIANTestbed()
