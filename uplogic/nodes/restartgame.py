from bge import logic
from uplogic.nodes import GEActionNode
from uplogic.nodes import GEOutSocket


class GERestartGame(GEActionNode):

    def __init__(self):
        super()
        self.condition = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self._set_ready()
        condition = self.get_socket_value(self.condition)
        if condition:
            logic.restartGame()
        self.done = True
