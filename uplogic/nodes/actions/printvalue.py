from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import not_met


class ULPrintValue(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        value = self.get_input(self.value)
        self._set_ready()
        print(value)
        self.done = True
