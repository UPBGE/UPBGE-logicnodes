from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket


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
        socket = self.get_output('changed')
        if socket is None:
            curr = self.get_input(self.current_value)
            if not self.initialize:
                self.initialize = True
                self.old = self.new = curr
                return self.set_output('changed', False)
            elif self.old != curr:
                self.new = curr
                return self.set_output('changed', True)
        return socket

    def get_previous_value(self):
        return self.old

    def get_current_value(self):
        return self.new

    def reset(self):
        super().reset()
        self.old = self.new

    def evaluate(self):
        self._set_ready()
