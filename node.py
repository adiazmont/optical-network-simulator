
class Node():
    
    def __init__(self, label, wss_no=1, wss_attenuation=9, amplifier=None, type=0):
        self.node_id = id(self)
        self.label = label
        self.type = type
        self.wss_no = wss_no
        self.wss_attenuation = wss_attenuation
        self.amplifier = amplifier
        
    def getNodeType(self):
        return self.type

    def getAmplifier(self):
        return self.amplifier

    def getNodeAttenuation(self):
        return self.wss_no * self.wss_attenuation
            
    
