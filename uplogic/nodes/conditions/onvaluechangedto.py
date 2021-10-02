from uplogic.nodes import GEConditionNode
from uplogic.nodes import GEOutSocket
from uplogic.nodes import STATUS_WAITING
from uplogic.nodes import is_waiting


class GEValueChangedTo(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.monitored_value = None
        self.trigger_value = None
        self.changed = None
        self.old = None
        self.OUT = GEOutSocket(self, self.get_changed)

    def get_changed(self):
        monitored_value = self.get_socket_value(self.monitored_value)
        trigger_value = self.get_socket_value(self.trigger_value)
        if is_waiting(monitored_value, trigger_value):
            return STATUS_WAITING
        return (
            monitored_value == trigger_value and
            self.changed
        )

    def evaluate(self):
        monitored_value = self.get_socket_value(self.monitored_value)
        self.changed = monitored_value != self.old
        self.old = monitored_value
        self._set_ready()
