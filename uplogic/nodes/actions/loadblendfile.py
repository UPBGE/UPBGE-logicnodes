from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket


class ULLoadBlendFile(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.file_name = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self._set_ready()
        condition = self.get_input(self.condition)
        file_name = self.get_input(self.file_name)
        if condition:
            logic.startGame(file_name)
        self.done = True
