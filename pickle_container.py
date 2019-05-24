

class PickleContainer():

    def __init__(self):
        self.container = []

    def addToContainer(self, _tuple):
        self.container.append(_tuple)

    def getContainer(self):
        return self.container
