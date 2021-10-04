from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import not_met


class ULEndGame(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None

    def evaluate(self):
        self._set_ready()
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        logic.endGame()
