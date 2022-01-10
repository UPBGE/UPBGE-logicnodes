from bge import render
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSetResolution(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.x_res = None
        self.y_res = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        x_res = self.get_input(self.x_res)
        y_res = self.get_input(self.y_res)
        if is_waiting(x_res, y_res):
            return
        self._set_ready()
        render.setWindowSize(x_res, y_res)
        self.done = True
