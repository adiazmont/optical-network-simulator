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


class Cost239:

    def __init__(self):

        # Create a Network object
        self.net = Network()

        cities = ['Amsterdam', 'Berlin', 'Brussels', 'Copenhagen', 'London',
                  'Luxembourg', 'Milan', 'Paris', 'Prague', 'Vienna', 'Zurich']
        nodes = []
        # Create the 11 nodes of the Cost239 network
        amsterdam = Node(1)
        nodes.append(amsterdam)
        berlin = Node(2)
        nodes.append(berlin)
        brussels = Node(3)
        nodes.append(brussels)
        copenhagen = Node(4)
        nodes.append(copenhagen)
        london = Node(5)
        nodes.append(london)
        luxembourg = Node(6)
        nodes.append(luxembourg)
        milan = Node(7)
        nodes.append(milan)
        paris = Node(8)
        nodes.append(paris)
        prague = Node(9)
        nodes.append(prague)
        vienna = Node(10)
        nodes.append(vienna)
        zurich = Node(11)
        nodes.append(zurich)

        for node in nodes:
            self.net.add_node(node)

        links = []
        # Create the 26 links of the Cost239 network
        l_amsterdam_london = Link(amsterdam, london)
        links.append(l_amsterdam_london)

        l_amsterdam_brussels = Link(amsterdam, brussels)
        links.append(l_amsterdam_brussels)

        l_amsterdam_luxembourg = Link(amsterdam, luxembourg)
        links.append(l_amsterdam_luxembourg)

        l_amsterdam_berlin = Link(amsterdam, berlin)
        links.append(l_amsterdam_berlin)

        l_amsterdam_copenhagen = Link(amsterdam, copenhagen)
        links.append(l_amsterdam_copenhagen)

        l_berlin_copenhagen = Link(berlin, copenhagen)
        links.append(l_berlin_copenhagen)

        l_berlin_paris = Link(berlin, paris)
        links.append(l_berlin_paris)

        l_berlin_prague = Link(berlin, prague)
        links.append(l_berlin_prague)

        l_berlin_vienna = Link(berlin, vienna)
        links.append(l_berlin_vienna)

        l_brussels_london = Link(brussels, london)
        links.append(l_brussels_london)

        l_brussels_paris = Link(brussels, paris)
        links.append(l_brussels_paris)

        l_brussels_milan = Link(brussels, paris)
        links.append(l_brussels_milan)

        l_brussels_luxembourg = Link(brussels, luxembourg)
        links.append(l_brussels_luxembourg)

        l_brussels_prague = Link(brussels, prague)
        links.append(l_brussels_prague)

        l_copenhagen_london = Link(copenhagen, london)
        links.append(l_copenhagen_london)

        l_copenhagen_prague = Link(copenhagen, prague)
        links.append(l_copenhagen_prague)

        l_london_paris = Link(london, paris)
        links.append(l_london_paris)

        l_luxembourg_paris = Link(luxembourg, paris)
        links.append(l_luxembourg_paris)

        l_luxembourg_zurich = Link(luxembourg, zurich)
        links.append(l_luxembourg_zurich)

        l_milan_paris = Link(milan, paris)
        links.append(l_milan_paris)

        l_milan_zurich = Link(milan, zurich)
        links.append(l_milan_zurich)

        l_milan_vienna = Link(milan, vienna)
        links.append(l_milan_vienna)

        l_paris_zurich = Link(paris, zurich)
        links.append(l_paris_zurich)

        l_prague_zurich = Link(prague, zurich)
        links.append(l_prague_zurich)

        l_prague_vienna = Link(prague, vienna)
        links.append(l_prague_vienna)

        l_vienna_zurich = Link(vienna, zurich)
        links.append(l_vienna_zurich)


tt = Cost239()

"""
        amsterdam_london - 390
        amsterdam_brussels - 200
        amsterdam_luxembourg - 310
        amsterdam_berlin - 600
        amsterdam_copenhagen - 750
        berlin_copenhagen - 400
        berlin_paris - 730
        berlin_prague - 320
        berlin_vienna - 710
        brussels_london - 340
        brussels_paris - 270
        brussels_milan - 850
        brussels_luxembourg - NaN
        brussels_prague - 730
        copenhagen_london - 1000
        copenhagen_prague - 760
        london_paris - 410
        luxembourg_paris - 370
        luxembourg_zurich - 440
        milan_paris - 810
        milan_zurich - NaN
        milan_vienna - 720
        paris_zurich - 590
        prague_zurich - 600
        prague_vienna - 350
        vienna_zurich - 720
"""