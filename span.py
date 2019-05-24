
class Span():
    "A span of optical fibre"

    def __init__(self, length=50, fibre_attenuation=0.22):
        """length: length in km
           fibre_attenuation: fraction (output power/input power?)"""
        self.span_id = id(self)
        self.length = length
        self.fibre_attenuation = fibre_attenuation
