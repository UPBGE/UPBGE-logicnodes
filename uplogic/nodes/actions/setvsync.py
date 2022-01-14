from bge import render
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSetVSync(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.vsync_mode = None
        self.done = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        vsync_mode = self.get_input(self.vsync_mode)
        if is_waiting(vsync_mode):
            return
        self._set_ready()
        render.setVsync(vsync_mode)
        self.done = True
