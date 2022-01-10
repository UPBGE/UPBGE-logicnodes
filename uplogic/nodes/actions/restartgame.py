from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket


class ULRestartGame(ULActionNode):

    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self._set_ready()
        condition = self.get_input(self.condition)
        if condition:
            logic.restartGame()
        self.done = True
