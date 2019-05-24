

from collections import namedtuple

Span = namedtuple('Span', 'span amplifier')

class Link():

    def __init__(self, src_node, dst_node):
        if src_node == dst_node:
            raise ValueError("link.__init__ src_node must be different from dst_node!")
        self.link_id = id(self)
        self.src_node = src_node
        self.dst_node = dst_node
        self.spans = []

    def addSpan(self, span, amplifier):
        self.spans.append(Span(span, amplifier))

    def length(self):
        return sum(span.span.length for span in self.spans)
