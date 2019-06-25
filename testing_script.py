from network import Network
from node import Node
from link import Link
from span import Span
from amplifier import Amplifier

class TestingScript():

    def main(self):

        # Create a Network object
        optiman = Network()

        # Create the nodes of the network
        n1 = Node(1, amplifier=Amplifier(target_gain=9), node_type='tx')
        n2 = Node(2, wss_no=2,amplifier=Amplifier(target_gain=18), node_type='inline')
        n3 = Node(3, node_type='rx')

        # Add the nodes to the network
        optiman.addNode(n1)
        optiman.addNode(n2)
        optiman.addNode(n3)

        # Create links of the network
        l1 = Link(n1, n2)
        l2 = Link(n2, n3)

        # Add links to the network
        optiman.addLink(l1)
        optiman.addLink(l2)

        # Create spans of the links
        s100 = Span(length=100)
        s80 = Span(length=80)
        s50 = Span()

        # Add spans to the links
        optiman.addSpanToLink(l1, s100, Amplifier(target_gain=22, wavelengthDependentGainId='wdg1'))
        optiman.addSpanToLink(l1, s80, Amplifier(target_gain=17.6, noise_figure=5.5,
                                                 wavelengthDependentGainId='wdg2'))
        optiman.addSpanToLink(l2, s50, Amplifier(target_gain=11, wavelengthDependentGainId='wdg1'))

        channels=[5, 6, 7]
        optiman.transmit(n1, n3, channels=channels, launch_power=-10)

        for channel in channels:
            print("OSNR at channel %s is %s dB." % (channel, optiman.monitor(l2, s50, channel - 1)))

        # Display network topology
#        print(optiman.network)

if __name__ == '__main__':
    TestingScript().main()
