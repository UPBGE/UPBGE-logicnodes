from bge import logic
from uplogic.nodes import GEActionNode
from uplogic.nodes import GEOutSocket
from uplogic.nodes import STATUS_WAITING
from uplogic.nodes import is_waiting
from uplogic.nodes import not_met


class GESetMouseCursorVisibility(GEActionNode):
    def __init__(self):
        super()
        self.condition = None
        self.visibility_status = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return STATUS_WAITING
        visibility_status = self.get_socket_value(self.visibility_status)
        if is_waiting(visibility_status):
            return STATUS_WAITING
        logic.mouse.visible = visibility_status
        return True

    def evaluate(self):
        self._set_ready()
