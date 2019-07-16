
# Node types
Tx = 'tx'
Inline = 'inline'
Rx = 'rx'

class Node(object):

    def __init__(self, label, wss_no=1, wss_attenuation=9, amplifier=None, node_type='tx'):
        """label: node name
           wss_no: number of switches
           wss_attenuation: wave selective switch attenuation (dB)
           amplifier: amplifier if any
           node_type: tx | inline | rx"""
        self.node_id = id(self)
        self.label = label
        self.node_type = node_type
        self.wss_no = wss_no
        self.wss_attenuation = wss_attenuation
        self.amplifier = amplifier

    def attenuation(self):
        """return node attenuation in dB"""
        return self.wss_no * self.wss_attenuation
