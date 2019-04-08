

class Link():
    
    def __init__(self, src_node, dst_node):
        if src_node == dst_node:
            raise ValueError("link.__init__ src_node must be different from dst_node!")
        self.link_id = id(self)
        self.src_node = src_node
        self.dst_node = dst_node
        self.spans = []
        
    def addSpan(self, span, amplifier):
        self.spans.append((span, amplifier))
        
    def getLinkLength(self):
        length = 0
        for span in self.spans:
            length += span[0].length
        return length
        
    def getSpans(self):
        return self.spans
