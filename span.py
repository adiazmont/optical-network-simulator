
class Span():

    def __init__(self, length=50, fibre_attenuation=0.22):
        self.span_id = id(self)
        self.length = length
        self.fibre_attenuation = fibre_attenuation
        
    def getSpanId(self):
        return self.span_id

    def getFibreSpanLength(self):
        return self.length
        
    def getFibreAttenuation(self):
        return self.fibre_attenuation
