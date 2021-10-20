from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import is_waiting


class ULOnValueChanged(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.old = None
        self.new = None
        self.current_value = None
        self.initialize = False
        self.OUT = ULOutSocket(self, self.get_changed)
        self.OLD = ULOutSocket(
            self,
            self.get_previous_value
        )
        self.NEW = ULOutSocket(self, self.get_current_value)

    def get_changed(self):
        return self.old != self.new

    def get_previous_value(self):
        return self.old

    def get_current_value(self):
        return self.new

    def reset(self):
        super().reset()
        self.old = self.new

    def evaluate(self):
        curr = self.get_socket_value(self.current_value)
        self._set_ready()
        if not self.initialize:
            self.initialize = False
            self.old = self.new = curr
        elif self.old != curr:
            self.new = curr
