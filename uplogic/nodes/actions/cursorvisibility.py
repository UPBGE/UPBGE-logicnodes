from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting
from uplogic.utils import not_met


class ULSetCursorVisibility(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.visibility_status = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_input(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        visibility_status = self.get_input(self.visibility_status)
        if is_waiting(visibility_status):
            return
        logic.mouse.visible = visibility_status
        self.done = True
