

class REXUS():
    """Class for communicating with REXUS"""
    def __init__(self):
        self.message = None
        self.response = None
        
    def communicate(self, message):
        self.message = message
        self.response = 'Foo'
    