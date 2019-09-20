

from collections import namedtuple

SpanTuple = namedtuple('Span', 'span amplifier')


class Link:

    def __init__(self, src_node, dst_node, bidirection=False):
        """
        :param src_node: Node() object
        :param dst_node: Node() object
        """
        if src_node == dst_node:
            raise ValueError("link.__init__ src_node must be different from dst_node!")
        self.link_id = id(self)
        self.src_node = src_node
        self.dst_node = dst_node
        self.bidirection = bidirection
        self.spans = []

    def add_span(self, span, amplifier):
        """
        :param span: Span() object
        :param amplifier: Amplifier() object
        :return: appends a SpanTuple to the spans attribute
        """
        self.spans.append(SpanTuple(span, amplifier))

    def length(self):
        """
        :return: link legth adding up span lengths in spans attribute
        """
        return sum(span.span.length for span in self.spans)
