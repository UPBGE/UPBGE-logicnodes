import bge

class PYOnInit():

    initialized: bool = False

    def evaluate(self):
        if self.initialized:
            return False
        self.initialized = True
        return True
