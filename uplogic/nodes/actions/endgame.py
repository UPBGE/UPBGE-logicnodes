from bge import logic
from uplogic.nodes import GEActionNode
from uplogic.nodes import not_met


class GEEndGame(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None

    def evaluate(self):
        self._set_ready()
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        logic.endGame()
