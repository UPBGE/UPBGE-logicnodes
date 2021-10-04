from bge import logic
from uplogic.nodes import ULActionNode
from uplogic.nodes import ULOutSocket
from uplogic.nodes import STATUS_WAITING
from uplogic.nodes import is_waiting
from uplogic.nodes import not_met


class ULSetCursorVisibility(ULActionNode):
    def __init__(self):
        ULActionNode.__init__(self)
        self.condition = None
        self.visibility_status = None
        self.OUT = ULOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = STATUS_WAITING
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        visibility_status = self.get_socket_value(self.visibility_status)
        if is_waiting(visibility_status):
            return
        logic.mouse.visible = visibility_status
        self.done = True
