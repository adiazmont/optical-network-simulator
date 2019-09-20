

class Node(object):

    def __init__(self, label, wss_no=1, wss_attenuation=9, amplifier=None):
        """label: node name
           wss_no: number of switches
           wss_attenuation: wave selective switch attenuation (dB)
           amplifier: amplifier if any"""
        self.node_id = id(self)
        self.label = label
        self.wss_no = wss_no
        self.wss_attenuation = wss_attenuation
        self.amplifier = amplifier

    def attenuation(self):
        """return node attenuation in dB"""
        return self.wss_no * self.wss_attenuation
