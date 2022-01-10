from uplogic.nodes import ULConditionNode
from uplogic.nodes import ULOutSocket
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_waiting


class ULValueChangedTo(ULConditionNode):
    def __init__(self):
        ULConditionNode.__init__(self)
        self.monitored_value = None
        self.trigger_value = None
        self.changed = None
        self.old = None
        self.OUT = ULOutSocket(self, self.get_changed)

    def get_changed(self):
        socket = self.get_output('changed')
        if socket is None:
            monitored_value = self.get_input(self.monitored_value)
            trigger_value = self.get_input(self.trigger_value)
            if is_waiting(monitored_value, trigger_value):
                return STATUS_WAITING
            return self.set_output(
                'changed',
                (
                    monitored_value == trigger_value and
                    self.changed
                )
            )
        return socket

    def evaluate(self):
        monitored_value = self.get_input(self.monitored_value)
        self.changed = monitored_value != self.old
        self.old = monitored_value
        self._set_ready()
